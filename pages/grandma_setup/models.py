# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from grandma.models import BaseSettings, GrandmaSettings, BaseSettingsManager


class ConfigSettingsManager(models.Manager):
    def get_settings(self):
        if self.get_query_set().count():
            return self.get_query_set()[0]
        else:
            # TODO: initialization
            new_settings = PagesSettings.objects.create()
            return new_settings

class PageSettingsManager(BaseSettingsManager):
    def get_settings(self):
        if self.get_query_set().count():
            return self.get_query_set()[0]
        else:
            pages_settings = self.get_query_set().create()
            if pages_settings.seo_was_installed():
                try:
                    from seo.grandma_setup.models import SeoSettings
                except ImportError:
                    pass
                else:
                    seo_settings = SeoSettings.objects.get_settings()
                    seo_settings.models.get_or_create(model='pages.models.Page')
            return pages_settings

class PagesSettings(BaseSettings):
    '''
        PAGE_LANGUAGES = (
            ('ru', gettext_noop('Russian')),
            ('en', gettext_noop('English')),
        )
        DEFAULT_PAGE_TEMPLATE = 'pages/index.html'
        PAGE_TEMPLATES = (
           ('pages/frontpage.html', u'Main page'),
        )
    '''
    objects = PageSettingsManager()

    def seo_was_installed(self):
        grandma_settings = GrandmaSettings.objects.get_settings()
        return grandma_settings.package_was_installed('grandma.django-seo')

    def menu_proxy_was_installed(self):
        grandma_settings = GrandmaSettings.objects.get_settings()
        return grandma_settings.package_was_installed('grandma.django-menu-proxy')

    def trusted_html_was_installed(self):
        grandma_settings = GrandmaSettings.objects.get_settings()
        return grandma_settings.package_was_installed('grandma.django-trusted-html')


class PageLanguage(BaseSettings):
    '''Page CMS language'''
    settings = models.ForeignKey(PagesSettings)
    code = models.CharField(verbose_name=_('Language code'), max_length=5)
    verbose_name = models.CharField(verbose_name=_('Language name'), max_length=30)
    default = models.BooleanField(verbose_name=_('Default language'), default=False)


class PageTemplate(BaseSettings):
    '''Page CMS template
        User can add as many templates as needed
    '''
    settings = models.ForeignKey(PagesSettings)
    filename = models.CharField(
        verbose_name=_('Template file name'),
        help_text=_('How file will be stored in templates directory'),
        max_length=50,
    )
    verbose_name = models.CharField(
        verbose_name=_('Template name'),
        help_text=_('How template appear in admin interface'),
        max_length=50,
    )
    default = models.BooleanField(verbose_name=_('Default template'), default=False)
