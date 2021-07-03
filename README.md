# PTON

This project tries to generate medieval towns' maps.

## Install

You can install the dependencies using a `virtualenv` :

```
virtualenv venv
source venv/bin/activate
make init
```

## Contributing

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
