# --- django-page-cms urls ----

urlpatterns += patterns('',
    (r'^pages/', include('pages.urls')),
{% if cms_settings.frontpage_handler.module == 'pages.redsolution_setup' %}
    url(r'^$', 'pages.views.details', name='pages-root'),
{% endif %}
)
