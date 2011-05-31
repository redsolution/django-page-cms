# --- django-page-cms urls ----

urlpatterns += patterns('',
    (r'^pages/', include('pages.urls')),
{% if cms_settings.frontpage_handler.module == 'pages.redsolution_setup' %}
    url(r'^$', 'pages.views.details', name='pages-root'),
{% endif %}
)

from pages.models import Page
pages_dict = {
    'queryset': Page.objects.exclude(status=Page.DRAFT),
    'date_field': 'last_modification_date',
}
try:
    sitemaps
except NameError:
    sitemps = {}

sitemaps['pages'] = GenericSitemap(pages_dict)
