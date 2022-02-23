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