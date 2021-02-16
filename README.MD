
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# pydllfile - double linked list in heap file storage

`pydllfile` is a file persistent double linked list


# memory / file layout

## general node layout

| name | size / value | description |
| --- | --- | --- | 
| prev | xpos bytes | previous element |
| succ | xpos bytes | next element |
| data | x bytes | data area |


## limitation

- xpos default == 8 bytes ==> 2**(8*8) == 18446744073709551616 bytes total file size
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
    
