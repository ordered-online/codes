import base64
import io
import json

import pyqrcode
from django.forms import model_to_dict
from django.http import JsonResponse

from .models import Code


class SuccessResponse(JsonResponse):
    def __init__(self, response=None):
        if response is None:
            super().__init__({
                "success": True,
            })
        else:
            super().__init__({
                "success": True,
                "response": response
            })


class AbstractFailureResponse(JsonResponse):
    reason = None

    def __init__(self):
        super().__init__({
            "success": False,
            "reason": self.reason
        })


class IncorrectAccessMethod(AbstractFailureResponse):
    reason = "incorrect_access_method"


class ErroneousValue(AbstractFailureResponse):
    reason = "erroneous_value"


def new_code(request):
    """
    Create a new code and return it as a JSONResponse.

    Allowed methods: GET
    """
    if request.method != "GET":
        return IncorrectAccessMethod

    code = Code.objects.create()

    return SuccessResponse(model_to_dict(code))


def render_to_qr_code(request):
    """
    Render the given value into an svg qr code.

    Allowed methods: POST
    """
    if request.method != "POST":
        return JsonResponse({"success": False})

    data = json.loads(request.body)
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
