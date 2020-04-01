from django.http import HttpResponse


def index(request):
  return HttpResponse("This is the main page. We can add some buttons or something.")
