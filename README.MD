
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# pydllfile - double linked list in heap file storage

`pydllfile` implements a file persistent 
[`double linked list`](https://en.wikipedia.org/wiki/Doubly_linked_list)


# What's new ?

Check
[`CHANGELOG`](https://github.com/kr-g/pydllfile/blob/main/CHANGELOG.MD)
for latest ongoing, or upcoming news


# memory / file layout

a double linked element node resides inside a heap node as data part. 
see also [`pyheapfile`](https://github.com/kr-g/pyheapfile/) for layout.


## general node layout

| name | size / value | description |
| --- | --- | --- | 
| prev | xpos bytes | previous element |
| succ | xpos bytes | next element |
| data | x bytes | data area |


## limitation

- xpos (default) == 8 bytes ==> 2**(8*8) 
== 18.446.744.073.709.551.616 bytes total file size (default)

| [binary prefix](https://en.wikipedia.org/wiki/Binary_prefix) | size | unit |
| --- | --- | --- |
| 2**20 | 17.592.186.044.416 | MB |
| 2**30 | 17.179.869.184 | GB |
| 2**40 | 16.777.216 | TB |
| 2**50 | 16.384 | PB |
| 2**60 | 16 | EB |

- the default can be changed by creating `DoubleLinkedListFile` with a different `link_size`
- see other limits also here [`pyheapfile`](https://github.com/kr-g/pyheapfile/)
-

## remark on hexdump tool

hexdump tool raise error when configured not properly. use valid hex address for node and link.
the internal hexdump tool for dumping single elements nodes from the dllfile can be called with:


    usage: python3 -m pydllfile.hexdump [options]

    dump heapfile double linked elements

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show version info and exit
      -V, --verbose         show more info
      -f FILE_NAME, --file FILE_NAME
                            input file
      -n NODE_NO, --node NODE_NO
                            hex address of node. blanks in a quoted string are ignored. address of 0x0 will read the 2nd heap node since a dll element node can not be
                            stored in first heap node. (default: 000000)
      -l LINK_NO, --link LINK_NO
                            hex address of dll element node. blanks in a quoted string are ignored. (default: 000000)
      -aw ADDESS_WIDTH, --addess_width ADDESS_WIDTH
                            hex address width. (default: 6)
      -ls LINK_SIZE, --link_size LINK_SIZE
                            link size. (default: 8)
      -r REL_NO, --relative REL_NO
                            relative position of dll element node. can be combined with -n or -l option. when negative it reads backwards starting from the -n/-l node.
                            keep in mind that -n is an address and -r is a position. (default: 0)
      -w WIDTH, --width WIDTH
                            with of data output (default: 16)
      -g GROUP, --group GROUP
                            group bytes in data output (default: 1)
      -ho, --header_only    prints only header, no data.



# Platform

Tested on Python3, and Linux.


# development status

alpha state.
the API or logical call flow might change without prior notice.

read [`CHANGELOG`](https://github.com/kr-g/pydllfile/blob/main/CHANGELOG.MD)
for latest, or upcoming news.


# installation
    
available on pypi. install with:

    python3 -m pip install pydllfile
    
