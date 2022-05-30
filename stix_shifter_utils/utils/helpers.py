import json

class StixObjectIdEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, StixObjectId):
            return obj.object_id
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class StixObjectId(object):
    object_id:str = None
    def __init__(self, object_id):
        self.object_id = object_id

    def __str__(self):
        return self.object_id
    
    def __repr__(self):
        return self.__str__()

    def __eq__(self, another):
        return hasattr(another, 'object_id') and self.object_id == another.object_id

    def __hash__(self):
        return hash(self.object_id)

    def __add__(self, other):
        return str(self.object_id) + other

    def __radd__(self, other):
        return other + str(self.object_id)

    def split(self, sep=None):
        return self.object_id.split(sep=sep)

    def update(self, object_id):
        self.object_id = object_id


def dict_merge(dct, merge_dct, add_keys=True):
    """ 
    https://gist.github.com/angstwad/bf22d1822c38a92ec0a9?permalink_comment_id=2622319#gistcomment-2622319
    
    Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.

    This version will return a copy of the dictionary and leave the original
    arguments untouched.

    The optional argument ``add_keys``, determines whether keys which are
    present in ``merge_dict`` but not ``dct`` should be included in the
    new dict.

    Args:
        dct (dict) onto which the merge is executed
        merge_dct (dict): dct merged into dct
        add_keys (bool): whether to add new keys

    Returns:
        dict: updated dict
    """
    try:
        if isinstance(dct, dict): 
            dct = dct.copy()
            if not add_keys:
                merge_dct = {
                    k: merge_dct[k]
                    for k in set(dct).intersection(set(merge_dct))
                }

            for k, v in merge_dct.items():
                if (k in dct and isinstance(dct[k], dict) and isinstance(merge_dct[k], dict)):
                    dct[k] = dict_merge(dct[k], merge_dct[k], add_keys=add_keys)
                else:
                    dct[k] = merge_dct[k]

        elif isinstance(dct, list): 
            return dct + list(set(merge_dct) - set(dct))

    except Exception as e:
        pass

    return dct

def find(element, dd, default=None):
    try:
        keys = element.split('.')
        rv = dd
        for key in keys:
            rv = rv[key]
        return rv
    except Exception:
        return default
