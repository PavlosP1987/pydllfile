
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# pydllfile - double linked list in heap file storage

`pydllfile` is a file persistent double linked list


# memory / file layout

## general node layout

| name | size / value | description |
| --- | --- | --- | 
| magik | 4 byte 0x_2_bad_dead | header magic number byte sequence for node structure |
| prev | x bytes | previous element |
| succ | x bytes | next ele,ment |
| data | x bytes | data area |



## limitation

- 



# Platform

Tested on Python3, and Linux.


# development status

alpha state.
the API or logical call flow might change without prior notice.

read [`CHANGELOG`](https://github.com/kr-g/pyheapfile/blob/main/CHANGELOG.MD)
for latest, or upcoming news.


# installation
    
available on pypi. install with:

    python3 -m pip install pydllfile
    
