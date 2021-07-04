# PTON

This project tries to generate medieval towns' maps.

# Install

You can install the dependencies using a `virtualenv` :

```
virtualenv venv
source venv/bin/activate
make init
```

# Usage of the generator

You have several ways to use the city generator. In both cases, you can give an optional argument : the number of citizens for you dreamed medieval city. It is set to 5000 by default.

### From command line

You can launch the code with python 3 with an optional argument :

```
$ python3 main.py [(int) number of citizens]
```

### From the python script
If you use an IDE, you can just run the main.py file which will launch our main function.

# Contributing

### Coding style

Please follow the [Google Python Style Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md) and [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

We use [YAPF](https://github.com/google/yapf) to enforce the coding style.

To lint and format your code, you can use the following command:

```
make lint
make format
```

### pre-commit

Install [pre-commit](https://pre-commit.com) and the following hooks.

```
pre-commit install
pre-commit install --hook-type commit-msg
```
