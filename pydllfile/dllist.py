import os

from pyheapfile.heap import Node, to_bytes, from_bytes

LINK_SIZE = 8

## todo

## refactor heapfile handling
## - calc of offset to write to in heapfile
## - check boundery
## - from_buffer/to_buffer methods

## end-of todo


class Element(object):
    """double linked list element"""

    def __init__(self, fd, pos=None, data=None, prev=0, succ=0, link_size=LINK_SIZE):
        # link_size == 8
        # ==>
        # 2**(8*8) == 18446744073709551616 bytes
        self.fd = fd
        self.link_size = link_size
        self.pos = pos
        self.prev = prev
        self.succ = succ
        self.data = data

    def elem_meta_size(self):
        return self.link_size * 2

    def len_total(self):
        elem_len = self.elem_meta_size()
        if self.data != None:
            elem_len += len(self.data)
        return elem_len

    def _read(self, pos, rlen=None):
        """read into and return a new element object"""
        elem = self.__class__(self.fd, pos, link_size=self.link_size)
        return elem.read(rlen)

    def read(self, rlen=None):
        """read the element"""
        self.fd.seek(self.pos, os.SEEK_SET)
        self.prev = from_bytes(self.fd.read(self.link_size))
        self.succ = from_bytes(self.fd.read(self.link_size))
        if rlen != None and rlen > 0:
            self.data = self.fd.read(rlen)
        else:
            self.data = None
        return self

    def write(self):
        self.fd.seek(self.pos, os.SEEK_SET)
        self.fd.write(to_bytes(self.prev, self.link_size))
        self.fd.write(to_bytes(self.succ, self.link_size))
        self.write_content()

    # following the high level API to use directly
    # to update the content of an element
    # all other tasks should be done via DoubleLinkedListFile
    # see also write_elem there

    def write_content(self):
        self.fd.seek(self.pos + self.elem_meta_size(), os.SEEK_SET)
        if self.data != None and len(self.data) > 0:
            self.fd.write(self.data)

    # end-of high level API to use directly

    def insert_pos(self, elem_pos):
        elem = self._read(elem_pos)
        return self.insert(elem)

    def insert(self, elem):
        """insert the element before other in the list,
        this does not aquire space from the underlying heap"""
        self.prev = elem.prev
        self.succ = elem.pos
        elem.prev = self.pos
        elem.write()
        self.write()
        return self

    def insert_after_pos(self, elem_pos):
        elem = self._read(elem_pos)
        return self.insert_after(elem)

    def insert_after(self, elem):
        """insert the element after other in the list,
        this does not aquire space from the underlying heap"""
        self.prev = elem.pos
        self.succ = elem.succ
        elem.succ = self.pos
        if elem.succ != 0:
            succ = self._read(self.succ)
            succ.prev = self.pos
            succ.write()
        elem.write()
        self.write()
        return self

    def remove(self):
        """removes the element from the list,
        this does not free the underlying heap"""
        if self.prev != 0:
            prev = self._read(self.prev)
            prev.succ = self.succ
            prev.write()
        if self.succ != 0:
            succ = self._read(self.succ)
            succ.prev = self.prev
            succ.write()


class DoubleLinkedListFile(object):
    """manages the elements within a heap file"""

    def __init__(self, heap_fd, link_size=LINK_SIZE):
        self.fd = heap_fd
        self.link_size = link_size

    def read_from_node(self, pos):
        if pos == 0:
            raise Exception("invalid position. must be > 0")
        node = self.fd.read_node(pos)
        elem = Element(self.fd, pos + Node.node_size(), link_size=self.link_size)
        data_len = node.used - elem.elem_meta_size()
        elem.read(data_len)
        return node, elem

    def read_elem(self, pos):
        if pos == 0:
            raise Exception("invalid position. must be > 0")
        node_pos = pos - Node.node_size()
        return self.read_from_node(node_pos)

    def write_elem(self, node, elem, update_elem_all=True):
        elem_len = elem.len_total()
        if elem_len > node.aloc:
            raise Exception("block too long")
        if node.used != elem_len:
            node.used = elem_len
            self.fd.write_node(node)
        if update_elem_all == True:
            elem.write()
        else:
            elem.write_content()
        return node, elem

    def remove_elem(self, node, elem, merge_free=True):
        elem.remove()
        self.fd.free(node, merge_free=merge_free)

    def insert_elem(
        self, elem_data, other_elem=None, before=True, equal_size_match=False
    ):
        elem = Element(self.fd, data=elem_data, link_size=self.link_size)
        node = self.fd.alloc(elem.len_total(), equal_size_match=equal_size_match)

        if node == None or node.id == 0:
            raise Exception("invalid position. must be > 0")

        node.used = elem.len_total()
        self.fd.write_node(node)
        elem.pos = node.id + node.node_size()
        if other_elem != None:
            if before == True:
                elem.insert(other_elem)
            else:
                elem.insert_after(other_elem)
        else:
            elem.prev = 0
            elem.succ = 0
            elem.write()
        return node, elem, other_elem
