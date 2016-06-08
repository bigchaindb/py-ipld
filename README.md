# py-ipld

[![codecov](https://codecov.io/gh/bigchaindb/py-ipld/branch/master/graph/badge.svg)](https://codecov.io/gh/bigchaindb/py-ipld)
[![Build Status](https://travis-ci.org/bigchaindb/py-ipld.svg?branch=master)](https://travis-ci.org/bigchaindb/py-ipld)

> Python implementation of the [IPLD specification](https://github.com/ipfs/specs/tree/master/ipld).


## Status

This is a Work-in-Progress. For TODOs, see: #1


## Installation

```
$ pip install py-ipld (not yet)
```


## Usage

In the Python REPL:

```python
>>> from ipld import marshal, multihash, unmarshal
>>>
>>> file = {
... 'name': 'hello.txt',
... 'size': 11
... }
>>>
>>> marshalled = marshal(file)
>>>
>>> multihash(marshalled)
'QmQtX5JVbRa25LmQ1LHFChkXWW5GaWrp7JpymN4oPuBSmL'
>>>
>>> unmarshal(marshal(file)) == file
True
```

That's it. No readthedocs, no private methods :boom:.


## Tests

*Only relevant, if you want to help developing.*

```
$ pip install --process-dependency-links -e .[dev]
$ python -m pytest -v -s
```


## Acknowledgements

Thanks to the [contributors](https://github.com/bigchaindb/bigchaindb/graphs/contributors) over at BigchainDB for letting me take
their setup structure.
