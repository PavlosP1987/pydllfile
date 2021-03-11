from pyheapfile.hexdump import hexdumps


def main():
    import os
    import argparse

    from pyheapfile.heap import HeapFile, Node
    from pydllfile import VERSION

    from pydllfile.dllist import DoubleLinkedListFile, LINK_SIZE

    parser = argparse.ArgumentParser(
        prog="hexdump",
        usage="python3 -m pydllfile.%(prog)s [options]",
        description="dump heapfile double linked elements",
    )
    parser.add_argument(
        "-v",
        "--version",
        dest="show_version",
        action="store_true",
        help="show version info and exit",
        default=False,
    )
    parser.add_argument(
        "-V",
        "--verbose",
        dest="verbose",
        action="store_true",
        help="show more info",
        default=False,
    )

    parser.add_argument(
        "-f",
        "--file",
        dest="file_name",
        action="store",
        help="input file",
        required=True,
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-n",
        "--node",
        type=str,
        dest="node_no",
        action="store",
        help="""hex address of node. blanks in a quoted string are ignored.
                address of 0x0 will read the 2nd heap node since a dll element node
                can not be stored in first heap node.
                (default: %(default)s)""",
        default=f"{0:06x}",
    )
    group.add_argument(
        "-l",
        "--link",
        type=str,
        dest="link_no",
        action="store",
        help="""hex address of dll element node. blanks in a quoted string are ignored.
                (default: %(default)s)""",
        default=f"{0:06x}",
    )
    parser.add_argument(
        "-aw",
        "--addess_width",
        type=int,
        dest="addess_width",
        action="store",
        help="hex address width. (default: %(default)s)",
        default=6,
    )
    parser.add_argument(
        "-ls",
        "--link_size",
        type=int,
        dest="link_size",
        action="store",
        help="link size. (default: %(default)s)",
        default=LINK_SIZE,
    )
    parser.add_argument(
        "-r",
        "--relative",
        type=int,
        dest="rel_no",
        action="store",
        help="""relative position of dll element node.
            can be combined with -n or -l option.
            when negative it reads backwards starting from the -n/-l node.
            keep in mind that -n is an address and -r is a position.
            (default: %(default)s)""",
        default="0",
    )
    parser.add_argument(
        "-w",
        "--width",
        type=int,
        dest="width",
        action="store",
        help="with of data output (default: %(default)s)",
        default=16,
    )
    parser.add_argument(
        "-g",
        "--group",
        type=int,
        dest="group",
        action="store",
        help="group bytes in data output (default: %(default)s)",
        default=1,
    )
    parser.add_argument(
        "-ho",
        "--header_only",
        dest="header_only",
        action="store_false",
        help="prints only header, no data.",
        default=True,
    )

    args = parser.parse_args()

    if args.show_version:
        print("Version:", VERSION)
        return

    fnam = os.path.expanduser(args.file_name)
    node_nr = int(args.node_no.replace(" ", ""), 16)
    link_nr = int(args.link_no.replace(" ", ""), 16)
    rel_no = args.rel_no
    link_size = args.link_size
    header_only = args.header_only
    width = args.width
    addess_width = args.addess_width
    group = args.group
    verbose = args.verbose

    hpf = HeapFile(fnam).open()
    dllfile = DoubleLinkedListFile(hpf, link_size=link_size)

    def calc_node(elem_pos):
        if elem_pos == 0:
            return 0
        return elem_pos - Node.node_size()

    if link_nr == 0:
        node = hpf.read_node(node_nr)
        if node_nr == 0:
            node = hpf.read_next(node)
    else:
        node = Node()
        node.id = calc_node(link_nr)

    node, elem = dllfile.read_from_node(node.id)

    rel_dir_fw = True if rel_no > 0 else False
    rel_no = abs(rel_no)

    while rel_no > 0:
        rel_no -= 1
        prev = calc_node(elem.prev)
        succ = calc_node(elem.succ)
        node_pos = succ if rel_dir_fw else prev
        if verbose:
            print("next", hex(node_pos), "prev", hex(prev), "succ", hex(succ))
        if node_pos > 0:
            node, elem = dllfile.read_from_node(node_pos)
        else:
            node = None
            break

    if node == None:
        print("out of border")
        return

    print("Node base", ":", hex(node.id), end=" : ")
    print("prev", "/", "succ", ":", hex(elem.prev), "/", hex(elem.succ), end=" : ")
    print(
        "Node",
        ":",
        hex(calc_node(elem.prev)),
        "/",
        hex(calc_node(elem.succ)),
    )

    if header_only:
        hexdumps(
            elem.data,
            start_adr=node.id + Node.node_size(),
            width=width,
            group=group,
            addess_width=addess_width,
        )

    hpf.close()


if __name__ == "__main__":
    main()
