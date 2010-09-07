from redsolutioncms.admin import CMSBaseAdmin
from django.contrib import admin
from models import PagesSettings, PageTemplate

class TemplateInline(admin.TabularInline):
    model = PageTemplate

class PagesSettingsAdmin(CMSBaseAdmin):
    model = PagesSettings
    inlines = [TemplateInline]
    exclude = ['validation_backend', ]
