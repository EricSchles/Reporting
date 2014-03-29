from django.contrib import admin
from WebApp.models import Website, Ad, Url

class WebsiteAdmin(admin.ModelAdmin):
  fields = ['name', 'url']
  list_filter = ['name', 'url']
  
class AdInline(admin.TabularInline):
  model = Ad
  
# Register your models here.
admin.site.register(Website, WebsiteAdmin)
#admin.site.register(Ad, AdInline)
admin.site.register(Ad)
admin.site.register(Url)
