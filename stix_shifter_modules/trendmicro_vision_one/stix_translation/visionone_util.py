def remove_enclosed_quote(in_str):
    if len(in_str) > 2 and in_str[0] == "'" and in_str[-1] == "'":
        return in_str[1:len(in_str) - 1]
    else:
        return in_str
