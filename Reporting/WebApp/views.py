from django.shortcuts import render_to_response
from django.http import HttpResponse
from django import forms

class UploadFileForm(forms.Form):
  title = forms.CharField(max_length=50)
  file = forms.FileField()

def upload(request):
  if request.method == 'POST':
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
      handle_uploaded_file(request.FILES['file'])
      return HttpResponseRedirect('/success/url/')
  else:
    form = UploadFileForm()
  return render_to_response('upload.html', {'form': form})
  