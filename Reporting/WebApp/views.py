from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from models import Website, Ad

class UploadFileForm(forms.Form):
  title = forms.CharField(max_length=50)
  file = forms.FileField()
  
def handle_uploaded_file(f, w):
  skipped = False
  results = []
  for chunk in f.chunks():
    #Skip the header
    #TODO: Be cleaner/smarter
    if not skipped:
      skipped = True
      continue
    s = chunk.split(',')
    a = Ad(s[0].strip(), s[1].strip(), s[2].strip(), s[3].strip(), s[4].strip(), s[5].strip(), s[6].strip(), w)
    results.push(a)
  return results

def upload(request):
  if request.method == 'POST':
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
      f = request.FILES['file']
      w = None
      try:
        w = Website.objects.get(name=f.name)
      except Website.DoesNotExist:
        w = Website(name=f.name)
        w.save()
      results = handle_uploaded_file(f, w)
      return HttpResponseRedirect('/upload/confirm/', {'ads': results})
  else:
    form = UploadFileForm()
  return render_to_response('upload.html', {'form': form})
  
def confirm(request):
  print(request)
  return render_to_response('confirm.html')
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  