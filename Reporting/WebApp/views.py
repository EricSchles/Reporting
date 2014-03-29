import csv
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django import forms
from models import Website, Ad

class UploadFileForm(forms.Form):
  title = forms.CharField(max_length=50)
  file = forms.FileField()
  
def handle_uploaded_file(f, w):
  print("in huf")
  skipped = False
  results = []
  for row in csv.reader(f, delimiter=','):
    #Skip the header
    #TODO: Be cleaner/smarter
    if not skipped:
      print("Skipping")
      skipped = True
    else:
      print(row)
      #a = Ad(row, w.name)
      a = Ad(name=row[0],
        age=row[1],
        ethnicity=row[2],
        phone_number=row[3],
        location=row[4],
        ad=row[5],
        date=row[6],
        website=w)
      results.append(a)
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
      #request.ads = results
      print(results)
      return render_to_response('confirm.html', {'ads': results})
  else:
    form = UploadFileForm()
  return render_to_response('upload.html', {'form': form})
  
def confirm(request, results):
  return render_to_response('confirm.html', {'ads' : results})
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  