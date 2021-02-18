
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# pydllfile - double linked list in heap file storage

`pydllfile` is a file persistent double linked list


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

- xpos (default) == 8 bytes ==> 2^(8*8) 
== 18.446.744.073.709.551.616 bytes total file size (default)

| [binary prefix](https://en.wikipedia.org/wiki/Binary_prefix) | size | unit |
| --- | --- | --- |
| 2^20 | 17592186044416 | MB |
| 2^30 | 17179869184 | GB |
| 2^40 | 16777216 | TB |
| 2^50 | 16384 | PB |
| 2^60 | 16 | EB |

- 


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
    
