def simple(value):
    if isinstance(value, str):
        return "\"{}\"".format(value)
    else:
        return value

def like(field, value):
    return "like({}, \"{}\")".format(field, value)

def set(field, value):
    values = [str(simple(v)) for v in value.values]

    return "{} IN ({})".format(field, ', '.join(values))

def matches(field, value):
    return "match({}, \"{}\")".format(field, value)

def subset(field, value):
    return "cidrmatch(\"{}\", {})".format(value, field)
