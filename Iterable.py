
def opponents(iterable, obj):
    """takes iterable for 2 elements and if the obj == anyone, the function returns the other one"""
    if obj == iterable[0]:
        return iterable[1]
    elif obj == iterable[1]:
        return iterable[0]
    return obj

def flat_list(lst, type_to_flat=(list, set)):
    result = []
    for i in lst:
        if isinstance(i, type_to_flat):
            result.extend(flat_list(list(i)))
        else:
            result.append(i)
    return result
def split_list(lst, num=2):
    result = []
    for i in range(0, len(lst), num):
        result.append(lst[i:i+num])
    return result

def search_iterable(iterable, search_for, ignore_case=True):
    if ignore_case:
        return [o for o in iterable if search_for.lower() in str(o).lower()]
    else:
        return [o for o in iterable if search_for in str(o)]
def indexes(iterable, obj):
    return [i for i in range(len(iterable)) if iterable[i] == obj]
def get_key(dic, value, first_value_only=True):
    keys = []
    for k in dic:
        if dic[k] == value:
            if first_value_only:
                return k
            else:
                keys.append(k)
    if keys:
        return keys
def multy_key(dic):
    result = {}
    values = set(dic.values())
    for i in values:
        keys = [o for o in dic if dic[o] == i]
        result[str(keys)] = i
    return result
def swap_dict(dic):
    """k: v ➡ v: k"""
    result = {}
    for k, v in dic.items():
        if isinstance(v, (list, tuple, set, dict)):
            v = str(v)
        result[v] = k
    return result
def return_dict_in_lines(dec, sep=': '):
    """Return a dict formatted as 'key: value' lines."""
    return '\n'.join([f"{i}{sep}{dec[i]}" for i in dec])
