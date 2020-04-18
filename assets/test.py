import random
import re
import regex
from timeit import timeit

"""
Comparing the performance of an unoptimised regex vs and optimised one. To run this, copy this file into the same directory as regex.py
"""

alphabet = "abcdefghijklmnopqrstuvwxyz"

def gen_string(length=10):
    return "".join(random.choice(alphabet) for _ in range(length))

results = []
with open("timing2.csv", "w") as fp:
    for num in range(100, 10000, 100):
        tokens = [gen_string() for _ in range(num)]
        sorted_tokens = sorted(tokens)
        re1 = re.compile("(" + "|".join(tokens) + ")")
        re2 = re.compile("(" + regex.optimise(tokens) + ")")
        time1 = timeit("re1.search(random.choice(tokens))", setup="from __main__ import re1, tokens, random")
        time2 = timeit("re1.search(random.choice(sorted_tokens))", setup="from __main__ import re1, sorted_tokens, random")
        time3 = timeit("re2.search(random.choice(tokens))", setup="from __main__ import re2, tokens, random")

        
        print(num, time1, time2, time3, sep=",", file=fp)
        
