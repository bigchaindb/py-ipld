from copy import deepcopy
from multihash import digest

from cbor import dumps, loads, Tag


# NOTE: jbenet plans to register tag 258:
#       https://www.iana.org/assignments/cbor-tags/cbor-tags.xhtml
LINK_TAG = 258
LINK_SYMBOL = '/'


def marshal(json_data):
    cp_json_data = deepcopy(json_data)

    def transform(di):
        for k, v in di.items():
            if isinstance(v, dict):
                di[k] = transform(v)

        if LINK_SYMBOL in di.keys():
            # TODO: Support: https://github.com/jbenet/js-multiaddr
            link = di[LINK_SYMBOL]
            di.pop(LINK_SYMBOL, None)
            if di:
                raise KeyError('Links must not have siblings')
            return Tag(LINK_TAG, link)
        return di

    # TODO: Currently, all keys are being sorted. It is yet to be
    #       determined if this is compatible with other implementations.
    return dumps(transform(cp_json_data), sort_keys=True)


def unmarshal(cbor_data):
    json_data = loads(cbor_data)

    def transform(di):
        # NOTE: https://github.com/ipfs/js-ipld/blob/master/src/cbor.js#L81
        #       Am I right in assuming that this is not supported in IPLD
        #       anymore, as links cannot have properties themselves?
        for k, v in di.items():
            # NOTE: Dear Python-experts: Is this safe?
            if isinstance(v, Tag):
                di[k] = {
                    LINK_SYMBOL: v.value
                }
            elif isinstance(v, dict):
                di[k] = transform(v)
        return di
    return transform(json_data)


def multihash(data):
    # NOTE: This is just a utility function to make the usage of this
    #       library more convenient.
    # NOTE: Not sure why all IPLD implementations use sha2-256...
    return digest(data, 'sha2_256').encode('base58').decode('utf-8')
