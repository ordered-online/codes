# ordered online codes service

This django based micro service provides an API to obtain codes for user authentication.
The service creates disposable codes on demand. Each code has its own unique string.
Any code, but also other values can be rendered to a qr code.

## Technology Stack

- Python 3
- Django

## Quickstart

```
$ python3 -m pip install -r requirements.txt
```

Run the server in development mode.

```
$ cd codes
$ python3 manage.py migrate
$ python3 manage.py runserver 127.0.0.1:8003
```
