# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from grandma.models import BaseSettings, GrandmaSettings, BaseSettingsManager

TEMPLATE_TYPES = (
    (0, _('One column')),
    (1, _('Two columns')),
)

class PageSettingsManager(BaseSettingsManager):
    def get_settings(self):
        if self.get_query_set().count():
            return self.get_query_set()[0]
        else:
            pages_settings = self.get_query_set().create()
            cms_settings = GrandmaSettings.objects.get_settings()
            
            # Integration with django-seo
            if 'grandma.django-seo' in cms_settings.installed_packages:
                try:
                    from seo.grandma_setup.models import SeoSettings
                except ImportError:
                    pass
                else:
                    seo_settings = SeoSettings.objects.get_settings()
                    seo_settings.models.get_or_create(model='pages.models.Page')
            # Integration with django-tinymce-attachments
            if 'grandma.django-tinymce-attachments' in cms_settings.installed_packages:
                try:
                    from attachments.grandma_setup.models import AttachmentSettings
                except ImportError:
                    pass
                else:
                    attachment_settings = AttachmentSettings.objects.get_settings()
                    attachment_settings.models.get_or_create(model='pages.models.Page')
                    attachment_settings.links.get_or_create(model='pages.models.Page')

            # Integration with django-model-url
            if 'grandma.django-model-url' in cms_settings.installed_packages:
                try:
                    from modelurl.grandma_setup.models import ModelUrlSettings
                except ImportError:
                    pass
                else:
                    model_url_settings = ModelUrlSettings.objects.get_settings()
                    model_url_settings.models.get_or_create(model='pages.models.Page')
                    model_url_settings.views.get_or_create(view='pages.views.details', object='current_page')

            # Integration with django-trustedhtml
            if 'grandma.trustedhtml' in cms_settings.installed_packages:
                pages_settings.validation_backend = 'trustedhtml'
                pages_settings.save() 
            
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
    
    default_template_type = models.IntegerField(verbose_name=_('Default template type'),
        choices=TEMPLATE_TYPES, default=0)
    validate = models.BooleanField(verbose_name=_('Validate html user input'), default=False)
    validation_backend = models.CharField(verbose_name=_('Validation service'), max_length=100, default='html5lib')
    render_frontpage = models.BooleanField(verbose_name=_('Render frontpage view'), default=False)
    
    # For future
#    use_tagging = models.BooleanField(verbose_name=_('Use pages tagging'), default=False)


class PageTemplate(BaseSettings):
    '''Page CMS template
        User can add as many templates as needed
    '''
    settings = models.ForeignKey(PagesSettings, related_name='templates')

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
    type = models.IntegerField(verbose_name=_('Template type'),
        choices=TEMPLATE_TYPES, default=0)
