from cbor import dumps, Tag

from ipld import LINK_TAG, marshal, multihash, unmarshal


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
        'l1': Tag(LINK_TAG, 'takemedowntotheparadisecity'),
    }, sort_keys=True)

    expected = {
        'hello': 'world',
        'num': 1,
        'l1': {
            '/': 'takemedowntotheparadisecity',
        },
    }

    assert unmarshal(src) == expected


def test_transform_cbor_with_nested_link_to_dict():
    src = dumps({
        'num': 1,
        'hello': 'world',
        'l1': Tag(LINK_TAG, 'takemedowntotheparadisecity'),
        'secret': {
            'l1': Tag(LINK_TAG, 'Ihhh ein Sekret!')
        },
    }, sort_keys=True)

    expected = {
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

    assert unmarshal(src) == expected


def test_multihashing_cbor():
    src = dumps({
        'name': 'hello.txt',
        'size': 11
    }, sort_keys=True)

    assert multihash(src) == 'QmQtX5JVbRa25LmQ1LHFChkXWW5GaWrp7JpymN4oPuBSmL'
