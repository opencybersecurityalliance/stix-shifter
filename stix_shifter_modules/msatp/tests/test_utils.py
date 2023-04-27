def all_keys_in_object(keys_to_check, obj):
    """checks that all the keys in keys_to_check are present in the object (in no certain order)

    parameters
    ----------
    keys_to_check : set
        a set of the properties that the object must have
    obj : dict
        the object to check against
    """
    return all(key in obj for key in keys_to_check)


def resolve_refs(objects, obj, ref, ref_type, error_msg):
    """
    resolves an array of references, checks that each is not none and optionaly its type and returns a list of
    the referenced objects

    parameters
    ----------
    objects : dict
        the objects dictionary
    obj : dict
        the current object
    ref : str
        the name of the reference property. for example: host_ref
    ref_type : str
        the type of the objects being referenced or None if they are not uniform
    error_msg : str
        the error to show if assertions fail
    """
    assert ref in obj
    ref_arr = obj[ref]
    assert type(ref_arr) is list
    arr = []
    for ref_idx in ref_arr:
        assert ref_idx in objects
        ref_obj = objects[ref_idx]
        assert ref_obj is not None, error_msg
        assert 'type' in ref_obj, error_msg
        if ref_type is not None:
            assert ref_obj['type'] == ref_type
        arr.append(ref_obj)
    return arr


def resolve_ref(objects, obj, ref, ref_type, error_msg):
    """
    resolves an object from a reference, checks that it is not none and its type and returns the referenced object

    parameters
    ----------
    objects : dict
        the objects dictionary
    obj : dict
        the current object
    ref : str
        the name of the reference property. for example: host_ref
    ref_type : str
        the type of the object being referenced
    error_msg : str
        the error to show if assertions fail
    """
    assert ref in obj, f"property {ref} not found in object {obj.get('type')}"
    ref_idx = obj[ref]
    assert ref_idx in objects, f"index {ref_idx} from reference {ref} not found in objects"
    ref_obj = objects[ref_idx]
    assert ref_obj is not None, error_msg
    assert 'type' in ref_obj, "referenced object is missing the type property"
    assert ref_obj['type'] == ref_type, f"type of referenced object is not as expected. expected {ref_obj} found {ref_obj['type']}"
    return ref_obj


def hashes_are_correct(file_obj, hashes):
    assert file_obj['hashes']['MD5'] == hashes["MD5"]
    assert file_obj['hashes']['SHA-1'] == hashes["SHA1"]
    assert file_obj['hashes']['SHA-256'] == hashes["SHA256"]