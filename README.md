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
