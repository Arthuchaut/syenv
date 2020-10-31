# Sysenv

Sysenv is a lightweight tool whose role is to load environment variables for configuration purposes.  
It has the advantage of offering some rather practical features to improve configuration management.  

## Table of content
- [Features](#features)
- [Usage](#usage)
- [Variables syntax](#variables-syntax)

## Features

- Environment variables loader in app (not for the system);
- Typing of environment variables;
- Supports interpolation.

## Usage

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
print(env.STUFF_STORAGE)
# >>> 'hostname'
# >>> PosixPath('storage/stuffs')
```

We can notice that the prefix `MY_APP_` has been substitued.

## Variables syntax

...