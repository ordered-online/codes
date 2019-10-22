# ordered online codes service

This django based micro service provides an API to obtain codes for user authentication.
The service creates disposable codes on demand. Each code has its own unique numeral value.
Note that codes can be predicted, since they are generated in a sequential way.
It is therefore important to make sure, that authentication cannot be inferred by third parties.

## Technology Stack

- Python 3
- Django

## Quickstart

Make sure, that Python 3 is installed. Install all requirements with the following command:
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

Example response if unsuccessful:
```json
{
  "success": false
}
```

### `/code/new/`
Create a new code.
Method: GET

Example with `curl:
```
$ curl -i -X GET http://127.0.0.1:8000/code/new/

{
    "value": "1af50d6cab08281f2f3dba71f3cbc7691713c75d"
}
```

### `/code/<value>/render/`
Render the given code value to a base64 encoded image.
Parameters: None
Method: GET

Example with `curl`:
```
$ curl -i -X GET http://127.0.0.1:8000/code/1af50d6cab08281f2f3dba71f3cbc7691713c75d/render/

{
    "base64": "PD94b...C9zdmc+Cg=="
}
```

