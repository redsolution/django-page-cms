# Django-page-cms urls

urlpatterns += patterns('',
    (r'^pages', include('pages.urls')),
    {% if pages_settings.handle_frontpage %}
    url(r'^$', 'pages.views.details', name='site-root'),
    {% endif %}
)
