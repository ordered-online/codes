import base64
import io

import pyqrcode
from django.http import JsonResponse, HttpResponse

from .models import Code


def new_code(request):
    """
    Create a new code and return it as a JSONResponse.

    Allowed methods: GET
    """
    if request.method != "GET":
        return JsonResponse({"success": False})
    code = Code.objects.create()
    return JsonResponse({
        "success": True,
        "code": {
            "value": code.value,
            "timestamp": code.timestamp,
        },
    })


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
    return JsonResponse({
        "success": True,
        "base64": encoding.decode("ascii"),
    })
