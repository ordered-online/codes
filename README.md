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

### `/code/new/`
Create a new code.
Parameters: None
Method: GET

Example response if unsuccessful:
```json
{
  "success": false
}
```

Example response if successful:
```json
{
  "success": true,
  "code": {
    "value": "da5d9d7cd737768933d29c346ad305c2d9743b6a", 
    "timestamp": "2019-10-19T10:28:58.838Z"
  }
}
```

### `/code/<value>/render/`
Render the given code value to a base64 encoded image.
Parameters: None
Method: GET

Example response if unsuccessful:
```json
{
  "success": false
}
```

Example response if successful:
```json
{
  "success": true,
  "base64": "PD94b...Zz4K"
}
```

