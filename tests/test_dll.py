import unittest

from pyheapfile.heap import HeapFile, Node
from pydllfile.dllist import DoubleLinkedListFile, Element

fnam = "mytest.hpf"


class HeapTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_default(self):
        hpf = HeapFile(fnam).create()
        hpf.close()

        hpf = HeapFile(fnam).open()

        node0 = hpf.alloc(0x50, data="not empty first node".encode())
        self.assertNotEqual(node0, None)

        dlf = DoubleLinkedListFile(hpf)
        nd1, el1, _ = dlf.insert_elem("two".encode())
        nd2, el2, el1 = dlf.insert_elem("zero".encode(), other_elem=el1, before=True)
        nd0, el0, el2 = dlf.insert_elem("one".encode(), other_elem=el2, before=False)

        print("el0", el0.pos, el0.prev, el0.succ)
        print("el1", el1.pos, el1.prev, el1.succ)
        print("el2", el2.pos, el2.prev, el2.succ)

        self.assertEqual(el2.prev, el1.succ)
        self.assertEqual(el2.succ, el0.pos)

        self.assertEqual(el2.prev, 0)
        self.assertEqual(el1.succ, 0)

        pos = el2.pos

        test_data = ["zero", "one", "two"]
        idx = 0

        while pos != 0:
            nod, elm = dlf.read_elem(pos)
            self.assertEqual(elm.data.decode(), test_data[idx])
            pos = elm.succ
            idx += 1

        dlf.remove_elem(nd0, el0)

        test_data = ["zero", "two"]
        idx = 0

        while pos != 0:
            nod, elm = dlf.read_elem(pos)
            self.assertEqual(elm.data.decode(), test_data[idx])
            pos = elm.succ
            idx += 1

        hpf.close()
