from cbor import Tag, dumps

from ipld.cbor import marshal, LINK_TAG


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


def test_link_is_string():
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
