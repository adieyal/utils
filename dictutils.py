from collections import OrderedDict

def qsdict(qs, *args):
    """
    Convert a query string to a nested dict
    :param qs: The query string from which the array will be created. qs can also be an object and args are all attributes on that object.
    :param args: A list of fields which will be nested one inside the other in the dict. The last arg will be the value in the innermost dict. If an arg is callable then it will be executed with q as a parameter. If the last parameter is a tuple then all the values inside that tuple will be added as leaves.
    :return:  A nested dict

    e.g.
    qs = Queryset([{fa:1, fb:2, fc:3}, {fa:3, fb:4, fc:5}]),
    using fc as the value

    {
        1 : {
            2 : 3
        },
        3 : {
            4 : 5
        }
    }
    """

    if len(args) < 2:
        raise ValueError("Need at least two fields to nest dicts")

    def v(q, key):
        if callable(key):
            return key(q)
        elif hasattr(q, key):
            return getattr(q, key)
        elif key in q:
            return q[key]
        else:
            return None

    d = {}
    for q in qs:
        nested_dicts = [d]
        for key in args[:-2]:
            current_dict = nested_dicts[-1]
            value = v(q, key)
            if not value in current_dict:
                current_dict[value] = OrderedDict()
            nested_dicts.append(current_dict[value])
        current_dict = nested_dicts[-1]
        if type(args[-1]) == tuple:
            current_dict[v(q, args[-2])] = [v(q, el) for el in args[-1]]
        else:
            current_dict[v(q, args[-2])] = v(q, args[-1])

    return d

def mergedict(a, b, path=None, concatenate_arrays=True, update=True):
    """
    Derived from: http://stackoverflow.com/questions/7204805/python-dictionaries-of-dictionaries-merge
    merges b into a

        concatenate_arrays - if True then arrays are concatenate, otherwise they are recursively traversed 
        update - if True then values in b clobber values in a
    """
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                mergedict(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            elif isinstance(a[key], list) and isinstance(b[key], list):
                if concatenate_arrays:
                    a[key].extend(b[key])
                else:
                    for idx, val in enumerate(b[key]):
                        a[key][idx] = mergedict(a[key][idx], b[key][idx], path + [str(key), str(idx)], update=update)
            elif update:
                a[key] = b[key]
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
