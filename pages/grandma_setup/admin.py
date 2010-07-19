from grandma.admin import GrandmaBaseAdmin
from django.contrib import admin
from models import PagesSettings, PageLanguage, PageTemplate


class TemplateInline(admin.TabularInline):
    model = PageTemplate

class LanguageInline(admin.TabularInline):
    model = PageLanguage

class PagesSettingsAdmin(GrandmaBaseAdmin):
    model = PagesSettings
    inlines = [TemplateInline, LanguageInline]
