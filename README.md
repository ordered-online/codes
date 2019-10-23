# ordered online codes service

This django based micro service provides an API to obtain codes for user authentication.
The service creates disposable codes on demand. Each code has its own unique string.
Any code, but also other values can be rendered to a qr code.

## Technology Stack

- Python 3
- Django

## Quickstart

Make sure, that Python 3 is installed. Install all requirements with the following command:
On macOS, please run:

```
export CFLAGS="-I$(brew --prefix openssl)/include $CFLAGS"
export LDFLAGS="-L$(brew --prefix openssl)/lib $LDFLAGS"
```
(This is necessary to build the `psycopg2` library.)

```
$ python3 -m pip install -r requirements.txt
```

Run the server.
```
$ cd codes
$ python3 manage.py migrate
$ python3 manage.py runserver
```

## API Endpoints

Following API Endpoints are supported:

### Create a new unique code with `/code/new/`
Create a new code.
Method: GET

Example with `curl:
```
$ curl -i -X GET http://127.0.0.1:8000/code/new/

{
    "success": true,
    "response": {
        "value": "dbb63047336a703641f7d34e964db0057e45e702"
    }
}
```

Failure Responses:
- [IncorrectAccessMethod](#IncorrectAccessMethod) if the service was accessed with any other method than specified.


### Render a payload value to a qr code with `/code/render/qr/`
Render the given payload value to a base64 encoded image.
Method: POST

|Parameter|Restriction|Mandatory|
|-|-|-|
|value|Should be a value, which can be rendered to a qr code.|yes|

Example with `curl`:
```
$ curl -i -X POST -H 'Content-Type: application/json' -d '{"value": "https://philippmatth.es"}' http://127.0.0.1:8000/code/render/qr/

{
    "success": true,
    "response": {
        "base64": "..."
    }
}
```

Failure Responses:
- [IncorrectAccessMethod](#IncorrectAccessMethod) if the service was accessed with any other method than specified.
- [ErroneousValue](#ErroneousValue) if the passed value could not be rendered to a qr code.

## Failure Responses

Following failure responses are supported:

### ErroneousValue

```
{ 
   "success":false,
   "reason":"erroneous_value"
}
```

### IncorrectAccessMethod

```
{ 
   "success":false,
   "reason":"incorrect_access_method"
}
```
