import copy

from cbor import Tag, dumps


LINK_TAG = 258
LINK_SYMBOL = '/'


def marshal(original):
    cp_original = copy.deepcopy(original)

    def transform(di):
        for k, v in di.items():
            if isinstance(v, dict):
                di[k] = transform(v)

        if LINK_SYMBOL in di.keys():
            link = di[LINK_SYMBOL]
            di.pop(LINK_SYMBOL, None)
            if len(di.keys()) > 1:
                raise KeyError('Links must not have siblings')
            return Tag(LINK_TAG, link)
        return di

    # TODO: Currently, all keys are being sorted. It is yet to be
    #       determined if this is compatible with other implementations.
    return dumps(transform(cp_original), sort_keys=True)


def unmarshal(cbor_buffer, opts):
    pass
