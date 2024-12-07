from django.http import HttpResponse


def index(request):
    return HttpResponse("Books Homepage!!!")