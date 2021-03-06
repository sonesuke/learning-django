# mypy: disallow_untyped_defs = False

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["PUT", "DELETE"])
def project(request):

    if request.method == "PUT":
        return HttpResponse("PUT")

    if request.method == "DELETE":
        return HttpResponse("delete all")
