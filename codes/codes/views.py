import base64
import io

import pyqrcode
from django.forms import model_to_dict
from django.http import JsonResponse

from .models import Code


def new_code(request):
    """
    Create a new code and return it as a JSONResponse.

    Allowed methods: GET
    """
    if request.method != "GET":
        return JsonResponse({"success": False})
    code = Code.objects.create()
    return JsonResponse(model_to_dict(code))


def render_code(request, value):
    """
    Render the given value into an svg qr code.

    Allowed methods: GET
    """
    if request.method != "GET":
        return JsonResponse({"success": False})
    stream = io.BytesIO()
    pyqrcode.create(value).svg(stream)
    encoding = base64.b64encode(stream.getvalue())
    return JsonResponse({"base64": encoding.decode("ascii")})
