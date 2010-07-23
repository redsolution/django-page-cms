# django-page-cms
INSTALLED_APPS += [
    'tagging',
    'pages',
    ]

TEMPLATE_CONTEXT_PROCESSORS += ('pages.context_processors.media',)

MIDDLEWARE_CLASSES += (
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    )

CACHE_BACKEND = "locmem:///?max_entries=5000"

DEFAULT_PAGE_TEMPLATE = 'pages/index.html'

PAGE_TEMPLATES = (
   ('pages/frontpage.html', u'Main page'),
)
