# PartialJson

[![Partialjson](https://github.com/iw4p/partialjson/raw/main/images/partialjson.png
)](https://pypi.org/project/partialjson/)

This library is meant to parse any kind of JSON response coming from various LLMs.
This includes
- Partial JSONs
- JSONs with markdown
- JSONs with \n between elements.

## Parse Partial and incomplete JSON in python

![](https://github.com/iw4p/partialjson/raw/main/images/partialjson.gif)

### Parse Partial and incomplete JSON in python with just 3 lines of python code.

[![PyPI version](https://img.shields.io/pypi/v/partialjson.svg)](https://pypi.org/project/partialjson)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/partialjson.svg)](#Installation)
[![Downloads](https://pepy.tech/badge/partialjson)](https://pepy.tech/project/partialjson)


## Example
```python
from partialjson.json_parser import JSONParser
parser = JSONParser()

incomplete_json = '{"name": "John", "age": 30, "is_student": false, "courses": ["Math", "Science"'
print(parser.parse(incomplete_json))
# {'name': 'John', 'age': 30, 'is_student': False, 'courses': ['Math', 'Science']}


llm_json = '{\n  "response": "Here are the top gainers in the last 24 hours:",\n  "coins": [\n    "GLEECUSDT",\n    "PACUSDT",\n    "PLUUSDT",\n    "DADDYUSDT",\n    "LMWRUSDT",\n    "COMAIUSDT",\n    "CDTBTC",\n    "CSWAPUSDT",\n    "WQUILETH"\n  ],\n  "tweets": [],\n  "casts": [],\n  "nfts": [],\n  "news": []\n}'
print(parser.parse(llm_json))
# {"response": "Here are the top gainers in the last 24 hours:", "coins": ["GLEECUSDT", "PACUSDT", "PLUUSDT", "DADDYUSDT", "LMWRUSDT", "COMAIUSDT", "CDTBTC", "CSWAPUSDT", "WQUILETH"], "tweets": [], "casts": [], "nfts": [], "news": []}

another_json = ''```json{\n  "response": "Here are the top gainers in the last 24 hours:",\n  "coins": [\n    "GLEECUSDT",\n    "PACUSDT",\n    "PLUUSDT",\n    "DADDYUSDT",\n    "LMWRUSDT",\n    "COMAIUSDT",\n    "CDTBTC",\n    "CSWAPUSDT",\n    "WQUILETH"\n  ],\n  "tweets": [],\n  "casts": [],\n  "nfts": [],\n  "news": []\n}\n''
# {"response": "Here are the top gainers in the last 24 hours:", "coins": ["GLEECUSDT", "PACUSDT", "PLUUSDT", "DADDYUSDT", "LMWRUSDT", "COMAIUSDT", "CDTBTC", "CSWAPUSDT", "WQUILETH"], "tweets": [], "casts": [], "nfts": [], "news": []}
```

### Installation

```sh
$ pip install partialjson
```
Also can be found on [pypi](https://pypi.org/project/partialjson/)

### How can I use it?
  - Install the package by pip package manager.
  - After installing, you can use it and call the library.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=iw4p/partialjson&type=Date)](https://star-history.com/#iw4p/partialjson&Date)

### Issues
Feel free to submit issues and enhancement requests or contact me via [vida.page/nima](https://vida.page/nima).

### Contributing
Please refer to each project's style and contribution guidelines for submitting patches and additions. In general, we follow the "fork-and-pull" Git workflow.

 1. **Fork** the repo on GitHub
 2. **Clone** the project to your own machine
 3. **Update the Version** inside __init__.py
 4. **Commit** changes to your own branch
 5. **Push** your work back up to your fork
 6. Submit a **Pull request** so that we can review your changes