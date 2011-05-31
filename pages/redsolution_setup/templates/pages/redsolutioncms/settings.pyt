# ---- django-page-cms ----

INSTALLED_APPS += [
    'pages',
]

MIDDLEWARE_CLASSES += [
    'django.middleware.locale.LocaleMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS += [
    'pages.context_processors.media',
    'pages.context_processors.pages_navigation',
]
DEFAULT_PAGE_TEMPLATE = 'pages/index.html'

# Hardcoded settings, they should  be customizable 
PAGE_TAGGING = False
PAGE_PERMISSION = False
PAGE_HIDE_ROOT_SLUG = True
PAGE_LANGUAGES = (
    ('ru', gettext_noop('Russian')),
    ('en', gettext_noop('English')),
)

# Customizable settings

{% if 'redsolutioncms.django-tinymce' in cms_settings.installed_packages %}
PAGE_TINYMCE = True
{% else %}
PAGE_TINYMCE = False
{% endif %}

PAGE_TEMPLATES = (
{% for template in pages_settings.templates.all %}
   ('pages/{{ template.filename }}', u'{{ template.verbose_name }}'),
{% endfor %}
)

{% if pages_settings.validate %}
{% if pages_settings.validation_backend == 'html5lib' %}
INSTALLED_APPS += [
    'html5lib',
]
PAGE_SANITIZE_USER_INPUT = True
{% endif %}
{% else %}
PAGE_SANITIZE_USER_INPUT = False
{% endif %}

{% if 'redsolutioncms.django-server-config' in cms_settings.installed_packages %}
try:
    CONFIG_APP_MEDIA
except NameError:
    CONFIG_APP_MEDIA = {}

CONFIG_APP_MEDIA['pages'] = [('pages', 'pages',)]
{% endif %}

{% if pages_settings.disable_page_cache %}
PAGE_DISABLE_CACHE = True
{% else %}
PAGE_DISABLE_CACHE = False
{% endif %}
