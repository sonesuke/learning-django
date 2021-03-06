# mypy: disallow_untyped_defs = False

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .service import ProjectService


@require_http_methods(["PUT", "DELETE"])
def project(request):

    if request.method == "PUT":
        ret = ProjectService.create()
        return HttpResponse(ret)

    if request.method == "DELETE":
        ProjectService.delete_all()
        return HttpResponse("delete all")
