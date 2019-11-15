import base64
import io
import json
from json import JSONDecodeError

import pyqrcode
from django.forms import model_to_dict
from django.http import JsonResponse

from .models import Code


class SuccessResponse(JsonResponse):
    status_code = 200

    def __init__(self, response=None):
        if response is None:
            super().__init__({})
        else:
            super().__init__(response)


class AbstractFailureResponse(JsonResponse):
    reason = None

    def __init__(self):
        super().__init__({
            "reason": self.reason
        })


class IncorrectAccessMethod(AbstractFailureResponse):
    reason = "incorrect_access_method"
    status_code = 405


class ErroneousValue(AbstractFailureResponse):
    reason = "erroneous_value"
    status_code = 400


class MalformedJson(AbstractFailureResponse):
    reason = "malformed_json"
    status_code = 400


def new_code(request):
    """
    Create a new code and return it as a JSONResponse.

    Allowed methods: GET
    """
    if request.method != "GET":
        return IncorrectAccessMethod()

    code = Code.objects.create()

    return SuccessResponse(model_to_dict(code))


def render_to_qr_code(request):
    """
    Render the given value into an svg qr code.

    Allowed methods: POST
    """
    if request.method != "POST":
        return IncorrectAccessMethod()

    try:
        data = json.loads(request.body)
    except JSONDecodeError:
        return MalformedJson()

    value = data.get("value")
    if not value:
        return ErroneousValue()

    stream = io.BytesIO()
    try:
        pyqrcode.create(value).svg(stream)
    except ValueError:
        return ErroneousValue()

    encoding = base64.b64encode(stream.getvalue())
    return SuccessResponse({"base64": encoding.decode("ascii")})
