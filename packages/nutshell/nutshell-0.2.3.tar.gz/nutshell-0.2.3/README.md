# Nushell API

This is a work-in-progress attempt at a pythonic API for Nutshell.

## Installation

```bash 
pip install nutshell
```

## Usage

Create desired API calls as Pydantic models, pass the models to the NutshellAPI class, and call the API.

```python
import asyncio
import os

from rich import print
from dotenv import load_dotenv
import nutshell as ns

load_dotenv()

single_call = ns.FindActivityTypes()

nut = ns.NutshellAPI(os.getenv("NUTSHELL_USERNAME"), password=os.getenv("NUTSHELL_KEY"))
nut.api_calls = [single_call]
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
        params={'orderBy': 'name', 'orderDirection': 'ASC', 'limit': 50, 'page': 1}
    ),
    FindActivityTypesResult(
        result=[
            ActivityTypes(stub=True, id=1, rev='1', entity_type='Activity_Types', name='Phone Call / Meeting'),
            ActivityTypes(stub=True, id=3, rev='3', entity_type='Activity_Types', name='Email/Log'),
        ]
    )
)
```

All responses have a `result` attribute that contains the data returned by the API. The data is returned as Pydantic
models based on the API method invoked.