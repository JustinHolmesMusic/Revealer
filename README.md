## How to run
Create virtual env:
```
$ python -m venv venv
```

Activate it:
```
source venv/bin/activate
```

Install dependencies:
```
$ pip install -r requirements.txt
```

Install precommit hook
```
$ pre-commit install
```


## Ape tests
```
$ ape plugins install solidity
$ ape test
```
