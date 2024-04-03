import sys

if sys.version_info.major == 3 and sys.version_info.minor >= 10:
    from collections.abc import MutableMapping
else:
    from collections import MutableMapping
import collections


def parse_list(inputlist):
    output = []
    for inputdict in inputlist:
        output.append(flatten(inputdict))
    return output


def flatten(inputdict, parent_key='', sep='.'):
    items = []
    # print(items)

    for k, v in inputdict.items():

        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.abc.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            if isinstance(v, list):
                total = int()
                for idx, vv in enumerate(v):
                    new_key_1 = new_key + sep + str(idx)
                    if isinstance(vv, str):
                        items.append((new_key_1, vv))
                    else:
                        items.extend(flatten(vv, new_key_1, sep=sep).items())
                    total += 1
                items.append((f"total.{new_key}", total))
            # else:
            items.append((new_key, v))
    # print(items)
    return dict(items)
