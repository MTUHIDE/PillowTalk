from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
import requests

def index(request):
  template = 'index.html'
  context = {
  }
  return render(request, template, context)

def submit(request):
  url = 'https://a537e14d.ngrok.io/cgi-bin/alexa.sh'
  myObj = {'Message':request.POST['Message']}
  x = requests.post(url, data = myObj)
  template = 'index.html'
  context = {
   'success':x.text,
  }
  return render(request, template, context)
   