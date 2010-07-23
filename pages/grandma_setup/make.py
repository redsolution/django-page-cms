from grandma.make import BaseMake
from grandma.models import GrandmaSettings
from django.template.loader import render_to_string
from pages.grandma_setup.models import PagesSettings
import os
import shutil

class Make(BaseMake):
    def make(self):
        super(Make, self).make()
        grandma_settings = GrandmaSettings.objects.get_settings()
        grandma_settings.render_to('settings.py', 'pages/grandma/settings.py')
        grandma_settings.render_to('urls.py', 'pages/grandma/urls.py')
        pages_settings = PagesSettings.objects.get_settings()
        grandma_settings.render_to(os.path.join('..', 'templates', 'pages', 'base.html'),
            'pages/grandma/base.html', {
            'pages_settings': pages_settings,
        }, 'w')
        grandma_settings.render_to(os.path.join('..', 'templates', 'pages', 'index.html'),
            'pages/grandma/index.html', {
            'pages_settings': pages_settings,
        }, 'w')
        grandma_settings.render_to(os.path.join('..', 'templates', 'pages', 'frontpage.html'),
            'pages/grandma/frontpage.html', {
            'pages_settings': pages_settings,
        }, 'w')

    def postmake(self):
        super(Make, self).postmake()
        grandma_settings = GrandmaSettings.objects.get_settings()
        if not grandma_settings.package_was_installed('grandma.django-server-config'):
            feedback_dir = os.path.dirname(os.path.dirname(__file__))
#           try delete dir before copy. be carefull!!!
            try:
                shutil.rmtree(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(feedback_dir))), 'media/pages/'),)
#            no such directory
            except OSError:
                pass
#            copy media to cms media directory
            shutil.copytree(
                os.path.join(feedback_dir, 'media/pages/'),
                os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(feedback_dir))), 'media/pages/'),
                )
        if grandma_settings.package_was_installed('grandma.django-menu-proxy'):
            grandma_settings.render_to('settings.py', 'pages/grandma/settings_menu.py')
