from django.shortcuts import render
from django.http import HttpResponse

def upload(request):
  return HttpResponse("Hello, world. You're at where the file uploader will be")
  