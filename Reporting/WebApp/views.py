import csv
import json
import urllib
from django.core import serializers
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django import forms
from models import Website, Ad

class UploadFileForm(forms.Form):
  file = forms.FileField()
  
def handle_uploaded_file(f, w):
  print("in huf")
  skipped = False
  results = []
  for row in csv.reader(f, delimiter=','):
    if not skipped:
      skipped = True
    else:
      #print(row)
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
      website = None
      tmpurl = request.POST['website']
      tmpname = ""
      if tmpurl == "NEWSITE":
        tmpurl = request.POST['newSiteUrl']
        tmpname = request.POST['newSiteName']
      try:
        website = Website.objects.get(url=tmpurl)
      except Website.DoesNotExist:
        website = Website(name=tmpname, url=tmpurl)
      results = handle_uploaded_file(f, website)
      return render_to_response('confirm.html', {'ads': results, "website": website, "serialized_ads": serializers.serialize("json", results)})
      #return render_to_response('confirm.html', {'ads': results, "website": website, "serialized_ads": json.dumps(results)})
  else:
    form = UploadFileForm()
  websites = [Website(name="site1", url="site1.com"), Website(name="site2", url="site2.org"), Website(name="site3", url="site3.edu")]
  return render_to_response('upload.html', {'form': form, 'websites': websites})
  
def confirm(request, results):
  return render_to_response('confirm.html', {'ads' : results})
  
def success(request):
  website = None
  tmpname = request.POST['website_name']
  tmpurl = request.POST['website_url']
  try:
    website = Website.objects.get(url=tmpurl)
  except Website.DoesNotExist:
    website = Website(name=tmpname, url=tmpurl)
    website.save()
  data = json.loads(request.POST['ads'])
  for ad in data:
    a = Ad(name=ad['fields']['name'],
        age=ad['fields']['age'],
        ethnicity=ad['fields']['ethnicity'],
        phone_number=ad['fields']['phone_number'],
        location=ad['fields']['location'],
        ad=ad['fields']['ad'],
        date=ad['fields']['date'],
        website=website)
    a.save()
  return HttpResponse("Success! <a href=\"/upload/\">Add More</a> <a href=\"/\">Home</a>")
  #return render_to_response('submitted.html', {'data' : data, "website" : ws})

# Show list of websites
def websites(request):
  websites = Website.objects.all()
  return render_to_response("websites.html", {'websites': websites})

# Show ads for a website
def website_ads(request, website_id):
  try:
    website = Website.objects.get(id=website_id)
  except Website.DoesNotExist:
    return HttpResponse("Website does not exist.")

  try:
    ads = Ad.objects.filter(website=website)
  except Ad.DoesNotExist:
    return HttpResponse("There are no ads for the website: Name: {0} URL: {1}.".format(website.name, website.url))

  return render_to_response("website_ads.html", {'ads': ads, 'website': website})
