.. image:: https://img.shields.io/pypi/v/py-ipld.svg
    :target: https://pypi.python.org/pypi/py-ipld
.. image:: https://img.shields.io/travis/bigchaindb/py-ipld.svg
    :target: https://travis-ci.org/bigchaindb/py-ipld
.. image:: https://img.shields.io/codecov/c/github/bigchaindb/py-ipld/master.svg
    :target: https://codecov.io/github/bigchaindb/py-ipld?branch=master


py-ipld
=======
| Python implementation of the `IPLD specification <https://github.com/ipfs/specs/tree/master/ipld>`_.


Status
------
This is a Work-in-Progress. For TODOs, see: `#1 <https://github.com/bigchaindb/py-ipld/issues/1>`_


Installation
------------

.. code-block:: bash

    $ pip install ipld  # (not yet)


Usage
-----
In the Python REPL:

.. code-block:: python
    
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

That's it. No readthedocs, no private methods :boom:.


Tests
-----
*Only relevant, if you want to help developing.*

.. code-block:: bash

    $ pip install --process-dependency-links -e .[dev]
    $ py.test -v


Acknowledgements
----------------
Thanks to the `contributors <https://github.com/bigchaindb/bigchaindb/graphs/contributors>`_
over at BigchainDB for letting me take their setup structure.
