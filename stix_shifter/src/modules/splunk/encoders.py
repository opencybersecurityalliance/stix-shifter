import re

def simple(value):
    if isinstance(value, str):
        return "\"{}\"".format(value)
    else:
        return value

def like(field, value):
    encoded_value = re.escape(value).replace("\\%", ".*").replace("_", ".")

    return "match({}, \"^{}$\")".format(field, encoded_value)

def set(field, value):
    values = [str(simple(v)) for v in value.values]

    return "{} IN ({})".format(field, ', '.join(values))

def matches(field, value):
    encoded_value = value.replace("\\", "\\\\") # Splunk needs backslashes encoded in searches

    return "match({}, \"{}\")".format(field, encoded_value)
