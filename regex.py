"""
Wrapper code for python re module. This module catches overflow exceptions as well as adding additional regex functions
"""

from __future__ import with_statement
from itertools import groupby
from random import randint
import string
import time
import re
from operator import truth

def optimise(it):
    """
    Simple regex list optimiser. Takes in a list of words and helps the regex
    engine along by recursively adding parentheses in the correct places
    e.g a list of the following names JEFF, JAMES, JEREMY, JUSTIN, JASON, JEFFREY will become J(A(MES|SON)|E(F(F(REY))|REMY)|USTIN)

    This could be improved even more for example see (http://search.cpan.org/~dankogai/Regexp-Optimizer-0.15/lib/Regexp/List.pm)
    Builds an optimised regular expression from an iterator containing tokens. It does this by aggregating prefixes so as
    to reduce the number of options that the state machine must try when trying to match a list of words. Any token containing
    regular expression syntax is left unoptimised and appended to the end of the regular expression.
    """

    nonAlphaNum = re.compile("[^a-zA-Z0-9-\s]") 
    isRegex = lambda x: truth(nonAlphaNum.search(x))
    lst = [el for el in it]
    exclude = [x for x in lst if isRegex(x)]
    lst = [x for x in lst if not isRegex(x)]
    lst.sort()
    opt = _optimise(lst)
    if len(exclude) > 0:
        opt = "%s|%s" % (opt, "|".join(exclude))
    return opt

def _getLongestPrefix(lst):
    l = min(map(len, lst))
    first = lst[0]
    for i in range(l, -1, -1):
        flag = True
        for el in lst:
            if not el.startswith(first[0:i]):
                flag = False
                break
        if flag:
            return first[0:i]
    return ""

def _optimise(lst, root=True):
    """
    An internal method that creates an optimised regex
    """
    s = ""
    chunks = []

    l = [x for x in lst if len(x) > 0]
    gen = groupby(l, lambda x: x[0])
    for (key, ngen) in gen:
        sublist = [x for x in ngen]
        prefix = _getLongestPrefix(sublist)
        lp = len(prefix)
        if len(sublist) == 1:
            s = "%s" % sublist[0]
        else:
            s = "%s%s" % (prefix, _optimise(map(lambda x: x[lp:], sublist), False))
        chunks.append(s)
    res = "|".join(chunks)
    if (len(l) > 0) and ('' in lst):
        res = "(?:%s)?" % res
    elif (not root) and (len(chunks) > 1):
        res = "(?:%s)" % res
    return res

if __name__ == "__main__":
    names = ["JEFF", "JAMES", "JEREMY", "JUSTIN", "JASON", "JEFFREY"]
    optimised = optimise(names)
    print(optimised)

