from grandma.make import BaseMake
from grandma.models import GrandmaSettings
from pages.grandma_setup.models import PagesSettings
from os.path import dirname, join
import shutil

class Make(BaseMake):

    def premake(self):
        super(Make, self).premake()

        cms_settings = GrandmaSettings.objects.get_settings()
        pages_settings = PagesSettings.objects.get_settings()

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
        if 'grandma.django-tinymce-attachment' in cms_settings.installed_packages:
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
        if 'grandma.django-trusted-html' in cms_settings.installed_packages:
            pages_settings.validation_backend = 'trustedhtml'
            pages_settings.save()


    def make(self):
        super(Make, self).make()
        cms_settings = GrandmaSettings.objects.get_settings()
        pages_settings = PagesSettings.objects.get_settings()

        cms_settings.render_to('settings.py', 'pages/grandma/settings.py', {
            'pages_settings': pages_settings,
        })
        cms_settings.render_to('urls.py', 'pages/grandma/urls.py', {
            'pages_settings': pages_settings,
        })

        # render base and default templates
        cms_settings.render_to(['..', 'templates', 'pages', 'base.html'],
            'pages/grandma/base.html', {}, 'w')
        cms_settings.render_to(['..', 'templates', 'pages', 'index.html'],
            'pages/grandma/index.html', {
            'pages_settings': pages_settings,
        }, 'w')
        # render additional templates
        for template in pages_settings.templates.all():
            cms_settings.render_to(['..', 'templates', 'pages', '%s' % template.filename],
                'pages/grandma/additional_template.html', {
                'pages_settings': pages_settings,
                'template': template,
            }, 'w')

    def postmake(self):
        super(Make, self).postmake()
        cms_settings = GrandmaSettings.objects.get_settings()
        pages_media_dir = join(dirname(dirname(__file__)), 'media')
        project_media_dir = join(cms_settings.project_dir, 'media')

#       WARNING! Silently delete media dirs
        try:
            shutil.rmtree(join(project_media_dir, 'pages'))
#            no such directory
        except OSError:
            pass

        if 'grandma.django-server-config' not in cms_settings.installed_packages:

#           copy files to media directory
            shutil.copytree(
                join(pages_media_dir, 'pages'),
                join(project_media_dir, 'pages'),
            )

        if 'grandma.django-menu-proxy' in cms_settings.installed_packages:
            cms_settings.render_to('settings.py', 'pages/grandma/settings_menu.py')
