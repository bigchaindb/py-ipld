import pytest

from cbor import dumps, Tag
from ipld import LINK_TAG, marshal, multihash, unmarshal
from multiaddr import Multiaddr, exceptions


def test_transform_dict_to_cbor():
    src = {
        'hello': 'world',
        'num': 1,
    }

    expected = {
        'num': 1,
        'hello': 'world',
    }

    assert marshal(src) == dumps(expected, sort_keys=True)


def test_transform_dict_with_link_to_cbor():
    src = {
        'hello': 'world',
        'num': 1,
        'l1': {
            '/': 'takemedowntotheparadisecity',
        },
    }

    expected = {
        'num': 1,
        'hello': 'world',
        'l1': Tag(LINK_TAG, 'takemedowntotheparadisecity'),
    }

    assert marshal(src) == dumps(expected, sort_keys=True)


def test_transform_dict_with_nested_link_to_cbor():
    src = {
        'hello': 'world',
        'num': 1,
        'l1': {
            '/': 'takemedowntotheparadisecity',
        },
        'secret': {
            'l1': {
                '/': 'Ihhh ein Sekret!',
            },
        },
    }

    expected = {
        'num': 1,
        'hello': 'world',
        'l1': Tag(LINK_TAG, 'takemedowntotheparadisecity'),
        'secret': {
            'l1': Tag(LINK_TAG, 'Ihhh ein Sekret!')
        },
    }

    assert marshal(src) == dumps(expected, sort_keys=True)


def test_transformation_doesnt_mutate_input():
    src = {
        'l1': {
            '/': 'takemedowntotheparadisecity',
        },
    }

    expected = {
        'l1': {
            '/': 'takemedowntotheparadisecity',
        },
    }

    marshal(src)

    assert src == expected


def test_transform_raise_key_error():
    src = {
        'l1': {
            '/': 'takemedowntotheparadisecity',
            'badlinksibling': 'icauseakeyerror',
            'badlinksibling2': 'icauseakeyerror'
        },
    }

    with pytest.raises(KeyError):
        marshal(src)


def test_transform_cbor_to_dict():
    src = dumps({
        'hello': 'world',
        'num': 1,
    }, sort_keys=True)

    expected = {
        'num': 1,
        'hello': 'world',
    }

    assert unmarshal(src) == expected


def test_transform_cbor_with_link_to_dict():
    src = dumps({
        'num': 1,
        'hello': 'world',
        'l1': Tag(LINK_TAG, '/p2p/QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4')
    }, sort_keys=True)

    expected = {
        'hello': 'world',
        'num': 1,
        'l1': {
            '/': '/p2p/QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4'
        },
    }

    assert unmarshal(src) == expected

def test_transform_cbor_with_faulty_link_to_dict():
    src = dumps({
        'num': 1,
        'hello': 'world',
        'l1': Tag(LINK_TAG, 'takemedowntotheparadisecity')
    }, sort_keys=True)

    with pytest.raises(exceptions.StringParseError):
        unmarshal(src)

def test_transform_cbor_with_nested_link_to_dict():
    src = dumps({
        'num': 1,
        'hello': 'world',
        'l1': Tag(LINK_TAG, '/p2p/QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4'),
        'secret': {
            'l1': Tag(LINK_TAG, '/p2p/QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4')
        },
    }, sort_keys=True)

    expected = {
        'hello': 'world',
        'num': 1,
        'l1': {
            '/': '/p2p/QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4',
        },
        'secret': {
            'l1': {
                '/': '/p2p/QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4',
            },
        },
    }

    assert unmarshal(src) == expected


def test_transform_dict_to_cbor_with_multiaddr():
    addr1 = Multiaddr('/ip4/127.0.0.1/udp/1234')
    addr2 = Multiaddr('/ipfs/Qmafmh1Cw3H1bwdYpaaj5AbCW4LkYyUWaM7Nykpn5NZoYL')

    src = {
        'data': 'hello world',
        'size': 11,
        'l1': {
            '/': str(addr1),
        },
        'l2': {
            '/': str(addr2),
        }
    }

    expected = {
        'data': 'hello world',
        'size': 11,
        'l1': Tag(LINK_TAG, addr1.to_bytes()),
        'l2': Tag(LINK_TAG, addr2.to_bytes()),
    }

    assert marshal(src) == dumps(expected, sort_keys=True)


def test_transform_cbor_to_dict_with_multiaddr():
    addr1 = Multiaddr('/ip4/127.0.0.1/udp/1234')
    addr2 = Multiaddr('/ipfs/Qmafmh1Cw3H1bwdYpaaj5AbCW4LkYyUWaM7Nykpn5NZoYL')

    src = dumps({
        'data': 'hello world',
        'size': 11,
        'l1': Tag(LINK_TAG, addr1.to_bytes()),
        'l2': Tag(LINK_TAG, addr2.to_bytes()),
    }, sort_keys=True)

    expected = {
        'data': 'hello world',
        'size': 11,
        'l1': {
            '/': str(addr1),
        },
        'l2': {
            '/': str(addr2),
        }
    }

    assert unmarshal(src) == expected


def test_multihashing_cbor():
    src = dumps({
        'name': 'hello.txt',
        'size': 11
    }, sort_keys=True)

    assert multihash(src) == 'QmQtX5JVbRa25LmQ1LHFChkXWW5GaWrp7JpymN4oPuBSmL'
