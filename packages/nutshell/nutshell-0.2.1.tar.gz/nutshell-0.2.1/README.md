# Nushell API

This is a work in progress pythonic API for Nutshell.

## Installation

```bash 
pip install nutshell
```

Nutshell access credentials should be stored in a .env file in the root directory.

## Usage

Pydantic dataclasses are available in the nutshell.methods module.

```python
from nutshell.methods impoort

GetUser

user = GetUser(user_id=1)
```

Once instantiated, these methods can be collected into an interable and passed to the
NutshellCalls class in the api_call module.

```python
from nutshell.api_call import NutshellCalls

calls = NutshellCalls([user])
results = calls.call_api()
```