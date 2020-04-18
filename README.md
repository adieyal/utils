# utils
## qsdict

Takes a list of dicts or objects and convert it into nested dicts.

```python
lst = [
    {"shape": "circle", "colour": "blue", "count": 5},
    {"shape": "circle", "colour": "pink", "count":15},
    {"shape": "square", "colour": "yellow", "count": 29},
    {"shape": "square", "colour": "blue", "count": 10}
]

qsdict(lst, "shape", "colour", "count")

# returns

{
    "circle": {
        "blue": 5,
        "pink": 15
    },
    "square": {
        "yellow": 29,
        "blue": 10
    }
}

qsdict(lst, "colour", "shape", "count")

# returns

{
    "blue": {
        "circle": 5,
        "square": 10
    },
    "pink": {
        "circle": 15
    },
    "yellow": {
        "square": 29
    }
}
```

Can also accept callables

```python

qsdict(lst, lambda x: x["colour"][0:2], "shape", "count")

{
    "bl": {
        "circle": 5,
        "square": 10
    },
    "pi": {
        "circle": 15
    },
    "ye": {
        "square": 29
    }
}
```

Access an arbitary number of arguments

```python
lst = [
    {"shape": "circle", "colour": "blue", "country": "France", "count": 5},
    {"shape": "circle", "colour": "pink", "country": "Germany", "count":15},
    {"shape": "square", "colour": "yellow", "country": "France", "count": 29},
    {"shape": "square", "colour": "blue", "country": "China", "count": 10}
]

qsdict(lst, lambda x: x["colour"][0:2], "shape", "country","count")

# Returns
{
    "bl": {
        "circle": {
            "France": 5
        },
        "square": {
            "China": 10
        }
    },
    "pi": {
        "circle": {
            "Germany": 15
        }
    },
    "ye": {
        "square": {
            "France": 29
        }
    }
}
```

Pass a tuple as the last argument if you prefer the leave node to be a list

```python
qsdict(lst, lambda x: x["colour"][0:2], "shape", ("country","count"))

{
    "bl": {
        "circle": [
            "France",
            5
        ],
        "square": [
            "China",
            10
        ]
    },
    "pi": {
        "circle": [
            "Germany",
            15
        ]
    },
    "ye": {
        "square": [
            "France",
            29
        ]
    }
}
```

## mergedict

Merges two nested dictionaries. Note that the first dictionary is updated.

```python
d1 = {
    "blue": {
        "circle": {
            "France": 5
        },
        "square": {
            "China": 10
        }
    },
    "pink": {
        "circle": {
            "Germany": 15
        }
    },
    "yellow": {
        "square": {
            "France": 29
        }
    }
}

d2 = {
    "blue": {
        "brightness": 4,
    },
    "pink": {
        "brightness": 4,
    },
    "yellow": {
        "brightness": 4,
    }
}

mergedict(d1, d2)

print(d1)

{
    "blue": {
        "circle": {
            "France": 5
        },
        "square": {
            "China": 10
        },
        "brightness": 4
    },
    "pink": {
        "circle": {
            "Germany": 15
        },
        "brightness": 4
    },
    "yellow": {
        "square": {
            "France": 29
        },
        "brightness": 4
    }
}
```

If you don't want to clobber the first dictionary, provide an empty dictionary
```
d0 = {}
mergedict(d0, d1)
mergedict(d0, d2)
```

This can be repeated an arbitary number of times to create a complicated data structure while avoiding nested loops and unwieldy code. This code is courtsey of this Stack Overflow [thread](https://stackoverflow.com/questions/7204805/how-to-merge-dictionaries-of-dictionaries).

## regex.optimise

Simple regex list optimiser. Takes in a list of words and helps the regex engine along by recursively adding parentheses in the correct places e.g a list of the following names JEFF, JAMES, JEREMY, JUSTIN, JASON, JEFFREY will become `J(A(MES|SON)|E(F(F(REY))|REMY)|USTIN)`. Use when you want to check for the existence of a token in a string. e.g.

```python
import re
import regex
names = ['JEFF', 'JAMES', 'JEREMY', 'JUSTIN', 'JASON', 'JEFFREY']

re_names = re.compile("(" + regex.optimise(names) + ")")
if re_names.search("some text JAMES some text"):
    print("search string contains 'JAMES'")
```

It does not provide much value when `len(names)` is small, but shows dramatic improvement as the length of tokens increases
