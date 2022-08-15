# Contributing
## Running tests
```bash
python3 manage.py test
```

With coverage
```bash
pip3 install coverage
coverage run --source=noxcrux_api --omit="*/migrations/*,*/tests/*,*/__init__.py" ./manage.py test && coverage html
python3 -m http.server --directory htmlcov
```
