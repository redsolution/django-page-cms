from redsolutioncms.make import BaseMake
from redsolutioncms.models import CMSSettings
from pages.redsolution_setup.models import PagesSettings
from os.path import dirname, join
import shutil

class Make(BaseMake):

    def premake(self):
        super(Make, self).premake()

        cms_settings = CMSSettings.objects.get_settings()
        pages_settings = PagesSettings.objects.get_settings()

        # Integration with django-seo
        if 'redsolutioncms.django-seo' in cms_settings.installed_packages:
            try:
                from seo.redsolution_setup.models import SeoSettings
            except ImportError:
                pass
            else:
                seo_settings = SeoSettings.objects.get_settings()
                seo_settings.models.get_or_create(model='pages.models.Page')
        # Integration with django-tinymce-attachments
        if 'redsolutioncms.django-tinymce-attachment' in cms_settings.installed_packages:
            try:
                from attachment.redsolution_setup.models import AttachmentSettings
            except ImportError:
                pass
            else:
                attachment_settings = AttachmentSettings.objects.get_settings()
                attachment_settings.models.get_or_create(model='pages.models.Page')
                attachment_settings.links.get_or_create(model='pages.models.Page')

        # Integration with django-model-url
        if 'redsolutioncms.django-model-url' in cms_settings.installed_packages:
            try:
                from modelurl.redsolution_setup.models import ModelUrlSettings
            except ImportError:
                pass
            else:
                model_url_settings = ModelUrlSettings.objects.get_settings()
                model_url_settings.models.get_or_create(model='pages.models.Page')
                model_url_settings.views.get_or_create(view='pages.views.details', object='current_page')

        # Integration with django-trustedhtml
        if 'redsolutioncms.django-trusted-html' in cms_settings.installed_packages:
            pages_settings.validation_backend = 'trustedhtml'
            pages_settings.save()

        # Integration with django-server-config
        if 'redsolutioncms.django-server-config' in cms_settings.installed_packages:
            try:
                from config.redsolution_setup.models import ConfigSettings
            except ImportError:
                pass
            else:
                config_settings = ConfigSettings.objects.get_settings()
                config_settings.appmedia.get_or_create(appname='pages',
                    source='pages', target='pages')


    def make(self):
        super(Make, self).make()
        cms_settings = CMSSettings.objects.get_settings()
        pages_settings = PagesSettings.objects.get_settings()

        cms_settings.render_to('settings.py', 'pages/redsolutioncms/settings.pyt', {
            'pages_settings': pages_settings,
        })
        cms_settings.render_to('urls.py', 'pages/redsolutioncms/urls.pyt', {
            'pages_settings': pages_settings,
        })

        # render base and default templates
        cms_settings.render_to(['..', 'templates', 'pages', 'base.html'],
            'pages/redsolutioncms/base.html', {}, 'w')
        cms_settings.render_to(['..', 'templates', 'pages', 'index.html'],
            'pages/redsolutioncms/index.html', {
            'pages_settings': pages_settings,
        }, 'w')
        # render additional templates
        for template in pages_settings.templates.all():
            cms_settings.render_to(['..', 'templates', 'pages', '%s' % template.filename],
                'pages/redsolutioncms/additional_template.html', {
                'pages_settings': pages_settings,
                'template': template,
            }, 'w')
        # copy initial data fixture
        cms_settings.copy_file(
            join(cms_settings.project_dir, 'fixtures', 'initial_data.json'),
            join(dirname(__file__), 'fixtures', 'project_data', 'initial_data.json'),
            mode='a',
        )

    def postmake(self):
        super(Make, self).postmake()
        cms_settings = CMSSettings.objects.get_settings()
        pages_media_dir = join(dirname(dirname(__file__)), 'media')
        project_media_dir = join(cms_settings.project_dir, 'media')

#       WARNING! Silently delete media dirs
        try:
            shutil.rmtree(join(project_media_dir, 'pages'))
#            no such directory
        except OSError:
            pass

        if 'redsolutioncms.django-server-config' not in cms_settings.installed_packages:

#           copy files to media directory
            shutil.copytree(
                join(pages_media_dir, 'pages'),
                join(project_media_dir, 'pages'),
            )
        else:
            from config.redsolution_setup.models import ConfigSettings
            config_settings = ConfigSettings.objects.get_settings()
            config_settings.appmedia.create(
                appname='pages', source='pages', target='pages',
            )

        if 'redsolutioncms.django-menu-proxy' in cms_settings.installed_packages:
            cms_settings.render_to('settings.py', 'pages/redsolutioncms/settings_menu.pyt')

make = Make()

