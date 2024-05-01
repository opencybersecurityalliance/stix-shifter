import json
from json import JSONEncoder

# 
# one-time
#    monkey-patch the json dumper
#    this makes external calls to `import json` never know the difference
#    the object will just auto-serialize
# 

# check to make sure this only runs once
if not hasattr(JSONEncoder, "original_default"):
    from collections import OrderedDict
    builtin_jsonable  = (dict, list, tuple, set, frozenset, str, int, float, bool, type(None))
    builtin_list_like = (list, tuple, set, frozenset)
    
    json.override_table = OrderedDict() # this allows for adding serializers to classes you didnt define yourself
    json.fallback_table = OrderedDict() # this allows for adding generic methods like using str(obj) or obj.__dict__
    
    def object_to_jsonable(obj):
        # 
        # first check the override_table
        # 
        for each_checker in reversed(json.override_table.keys()):
            type_matches = isinstance(each_checker, type) and isinstance(obj, each_checker)
            callable_check_matches = not isinstance(each_checker, type) and callable(each_checker) and each_checker(obj)
            if type_matches or callable_check_matches:
                custom_converter_function = json.override_table[each_checker]
                output = custom_converter_function(obj)
                return handle_recursion(output)
        
        # shortcut for builtins since they're the most common (optimization)
        if type(obj) in builtin_jsonable:
            return handle_recursion(obj)
        
        # 
        # then check the __json__ method
        # 
        if hasattr(obj.__class__, "__json__"):
            json_method = getattr(obj.__class__, "__json__")
            if callable(json_method):
                output = json_method(obj)
                return handle_recursion(output)
        
        # 
        # then check the fallback_table
        # 
        for each_checker in reversed(json.fallback_table.keys()):
            type_matches = isinstance(each_checker, type) and isinstance(obj, each_checker)
            callable_check_matches = not isinstance(each_checker, type) and callable(each_checker) and each_checker(obj)
            if type_matches or callable_check_matches:
                custom_converter_function = json.fallback_table[each_checker]
                output = custom_converter_function(obj)
                return handle_recursion(output)
        
        return handle_recursion(obj)
    
    # for some reason recursion is not normally performed on builtin objects, so this forces it to occur
    def handle_recursion(jsonable_value):
        if isinstance(jsonable_value, dict):
            return {
                object_to_jsonable(each_key) : object_to_jsonable(each_value)
                    for each_key, each_value in jsonable_value.items()
            }
        elif isinstance(jsonable_value, builtin_list_like):
            return [
                object_to_jsonable(each) for each in jsonable_value
            ]
        else:
            return jsonable_value
    
    JSONEncoder.original_default = original_default = JSONEncoder.default
    JSONEncoder.original_encode  = original_encode  = JSONEncoder.encode
    
    class PatchedJsonEncoder(json.JSONEncoder):
        # transform objects known to JSONEncoder here
        def encode(self, obj, *args, **kwargs):
            obj = object_to_jsonable(obj)
            return original_encode(self, obj, *args, **kwargs)

        # handle objects not known to JSONEncoder here
        def default(self, obj, *args, **kwargs):
            obj = object_to_jsonable(obj)
            if type(obj) in builtin_jsonable:
                return obj
            return original_default(self, obj, *args, **kwargs)
    
    # apply the patch
    JSONEncoder.default = PatchedJsonEncoder.default
    JSONEncoder.encode = PatchedJsonEncoder.encode # needs to be overridden because of https://stackoverflow.com/questions/16405969/how-to-change-json-encoding-behaviour-for-serializable-python-object/16406798#16406798
    
    original_dump = json.dump
    json.dump = lambda obj, *args, **kwargs: original_dump((object_to_jsonable(obj) if isinstance(obj, builtin_jsonable) else obj), *args, cls=PatchedJsonEncoder, **kwargs)

def fix_it(): pass # to support the old interface 