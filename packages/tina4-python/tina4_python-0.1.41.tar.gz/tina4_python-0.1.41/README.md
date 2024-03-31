### Tina4Python - This is not a framework for Python

Tina4Python is a light-weight routing and twig based templating system based on the [Tina4](https://github.com/tina4stack/tina4-php) stack which allows you to write websites and API applications very quickly.
.
### System Requirements

- Install Poetry:
```bash
curl -sSL https://install.python-poetry.org | python3 - 
```

- Install Jurigged (Enables Hot Reloading):
```bash
pip install jurigged
```

### Quick Start

After installing poetry you can do the following:
```bash
poetry new project-name
cd project-name
poetry add tina4_python
```
Create an entry point for Tina4 called ```app.py``` and add the following to the file
```python
from tina4_python import *
```

### Overview
The basic tina4 project uses an autoloader methodology from the src folder
All the source folders you should need are created there and they are run from __init__.py

If you are developing on Tina4, make sure you copy the public folder from tina4_python into src

### Installation

#### Windows

1.) Install Poetry:
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

2.) Add the following path to the system PATH:
```
%APPDATA%\pypoetry\venv\Scripts
```

3.) Install Tina4Python and Jurigged:
```bash
poetry add tina4_python
poetry add jurigged
```

**or**

```bash
pip install tina4_python
pip install jurigged
```

### Usage

After defining templates and routes, run the Tina4Python server:

- **Normal Server**:
```bash
poetry run
```

- **Server with Hot Reloading**:
```bash
poetry run jurigged main.py
```

- **Server on a Specific Port**:
```bash
poetry run app.py 7777
```
  
- **Server with alternate language** (for example fr = French):
```bash
poetry run main.py fr
```

Add more translations by going [here](TRANSLATIONS.md)

### Templating


Tina4 uses [Twig](https://twig.symfony.com/) templating to provide a simple and efficient way to create web pages.

1.) **Twig Files**: Add your Twig files within the `src/templates` folder. For instance, you might create files like `index.twig`, `base.twig`, etc., containing your HTML structure with Twig templating syntax for dynamic content.

2.) **Using Twig**: In these Twig files, you can use Twig syntax to embed dynamic content, control structures, variables, and more. For example:

```twig
<!-- index.twig -->
<!DOCTYPE html>
<html>
<head>
    <title>Welcome</title>
</head>
<body>
    <h1>Hello, {{ name }}!</h1>
</body>
</html>
```

### Defining Routes


The routing in Tina4Python can be defined in the `__init__.py` file or any file used as an entry point to your application. Tina4Python provides decorators to define routes easily.

1.) **Creating Routes**: Define routes using decorators from Tina4Python to handle HTTP requests.

Example:
```python
from tina4_python.Router import get
from tina4_python.Response import Response
@get("/hello")
async def hello(request, response):
  return response("Hello, World!")
```

This code creates a route for a GET request to `/hello`, responding with "Hello, World!".

2.) **Route Parameters**: You can define route parameters by enclosing variables with curly braces { }. The parameters are passed to the function as arguments.

 Example:
```python
from tina4_python.Router import get
from tina4_python.Response import Response

@get("/hello/{name}")
async def greet(**params):
   name = params['request'].params['name']
   return params['response'](f"Hello, {name}!")
 ````

This code creates a route for a GET request to `/hello/{name}`, where `name` is a parameter in the URL. The function `greet` accepts this parameter and responds with a personalized greeting.

Example:
- Visiting `/hello/John` will respond with "Hello, John!"
- Visiting `/hello/Alice` will respond with "Hello, Alice!"

3.) POST routes now require jwt token or API key to validate requests with an Authorization header
```
Authorization: Bearer <token>
```
You can generate tokens using tina4_python.tina4_auth which takes in a payload parameter which is a dictionary:

```python
import tina4_python

tina4_python.tina4_auth.get_token({"data": {"something":"more"}})
```

OR 

For ease of use you can supply an `API_KEY` param to your .env with a secret of your choice to use:

```dotenv
API_KEY=somehash
```

### Features
| Completed                  | To Do                            |
|----------------------------|----------------------------------|
| Python pip package         | Implement JWT for token handling |
| Basic environment handling |                                  |
| Basic routing              | OpenAPI (Swagger)                |
| Enhanced routing           |                                  |
| CSS Support                |                                  |
| Image Support              |                                  |
| Localization               |                                  |
| Error Pages                |                                  |
| Template handling          |                                  |

### Building and Deployment

#### Using Python

1. Building the package:
 ```bash
 python3 -m pip install --upgrade build
 python3 -m build
 python3 -m pip install --upgrade twine
 python3 -m twine upload dist/*
 ```

#### Using Poetry

1. Building the package:
```bash
poetry build
```

1. Publishing the package:
```bash
poetry publish
```
