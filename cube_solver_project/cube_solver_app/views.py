from django.shortcuts import render
from django.http import HttpResponse

from . import solver
from . import tester


def index(request):
    return render(request, "cube_solver_app/index.html")


def solve(request):
    layout = request.GET["layout"]

    error, result = tester.test(layout)

    if error:
        return HttpResponse(result)
    else:
        result = solver.solve(layout)
        return HttpResponse(result)
