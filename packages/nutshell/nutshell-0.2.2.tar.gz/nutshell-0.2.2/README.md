# Nushell API

This is a work-in-progress attempt at a pythonic API for Nutshell.

## Installation

```bash 
pip install nutshell
```

Nutshell access credentials should be stored in a .env file in the root directory or as environment variables. The
following variables are required:

```bash
NUTSHELL_KEY=your_api_key
NUTSHELL_USERNAME=your_username
```

## Usage

Pydantic dataclasses for supported API methods are available in the methods module.

```python
import asyncio

from rich import print

from nutshell.methods import FindActivityTypes
from nutshell.nutshell_api import NutshellAPI

single_call = FindActivityTypes()

nut = NutshellAPI(single_call)
call_response = asyncio.run(nut.call_api())

for call in call_response:
    print(call)
```

___
Results are returned as a list of tuples. The first element is the method instance, the second is the response.

```python
(
    FindActivityTypes(
        api_method='findActivityTypes',
        order_by='name',
        order_direction='ASC',
        limit=50,
        page=1,
        params={
            'orderBy': 'name',
            'orderDirection': 'ASC',
            'limit': 50,
            'page': 1
        }
    ),
    FindActivityTypesResult(
        result=[
            ActivityTypes(
                stub=True,
                id=1,
                rev='1',
                entity_type='Activity_Types',
                name='Phone Call / Meeting'
            ),
            ActivityTypes(
                stub=True,
                id=3,
                rev='3',
                entity_type='Activity_Types',
                name='Email/Log'
            ),
        ]
    )
)
```

All responses have a `result` attribute that contains the data returned by the API. The data is returned as a list of
Pydantic models based on the API method invoked.