# Sysenv

Sysenv is a lightweight tool whose role is to load environment variables for configuration purposes.  
It has the advantage of offering some rather practical features to improve configuration management.  

## Table of content
- [Sysenv](#sysenv)
  - [Table of content](#table-of-content)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Usage](#usage)
    - [Basics](#basics)
    - [Advanced](#advanced)
      - [Custom configuration class](#custom-configuration-class)
  - [Variables syntax](#variables-syntax)

## Features

- Environment variables loader in app (not for the system);
- Typing of environment variables;
- Supports interpolation.

## Requirements

- python >= 3.8

## Usage

### Basics

Sysenv is really easy to use, as the following example shows.  
We consider the following environment file :

```bash
# .env
MY_APP_FTPS_HOST=hostname
MY_APP_FTPS_USER=username
MY_APP_FTPS_PORT=int:22

MY_APP_STORAGE_DIR=pathlib.Path:storage
MY_APP_STUFF_STORAGE=pathlib.Path:{{MY_APP_STORAGE_DIR}}/stuffs
```

We can observe that the syntax of the values is a bit special. Sysenv supports `variable typing` and `interpolation` (see [Variables syntax](#variables-syntax)).  
**Important:** Sysenv has no environment variable file loader. It is not its role to do this type of processing. So you are free to use the tool of your choice, like `python-dotenv` for example.

```python
# __main__.py

import dotenv
import sysenv

# In this example, we are using python-dotenv to load environment variables.
dotenv.load_dotenv()
env: sysenv.Sysenv = sysenv.Sysenv(prefix='MY_APP_')

# Now, we can access to our env vars!
print(env.FTPS_HOST)
'''
>>> 'hostname' 
'''

print(env.STUFF_STORAGE)
''' 
>>> PosixPath('storage/stuffs') 
'''
```

We can notice that the prefix `MY_APP_` has been substitued.

### Advanced

#### Custom configuration class

We can use Sysenv with a custom config class like the following example.

```python
# config/config.py

import sysenv

class Config(sysenv.Sysenv):
    def __init__(self, prefix: str = 'MY_APP_') -> None:
        super().__init__(prefix)

        self.another_var: str = 'Hey!'

    @property
    def ftp_uri(self) -> str:
        return f'ftp://{self.FTPS_HOST}:{self.FTPS_PORT}'

```

We can also instanciate the Config class in the `__init__.py` file for facilities...

```python
# config/__init__.py

from config.config import Config

conf: Config = Config()
```

Then, considering the same env vars as above :

```python
# __main__.py

from config import conf

print(conf.as_dict)
'''
>>> {'FTPS_HOST': 'hostname',
     'FTPS_USER': 'username',
     'FTPS_PORT': 22,
     'STORAGE_DIR': PosixPath('storage'),
     'STUFF_STORAGE': PosixPath('storage/stuffs'),
     'another_var': 'Hey!'}
'''

print(conf.ftp_uri)
''' 
>>> ftp://hostname:22 
'''
```

## Variables syntax

...