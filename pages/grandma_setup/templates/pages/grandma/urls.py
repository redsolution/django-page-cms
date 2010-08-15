# Django-page-cms urls

urlpatterns += patterns('',
    {% if pages_settings.render_frontpage %}
    url(r'^$', 'pages.views.details', name='pages-root'),
    {% endif %}
    (r'^pages', include('pages.urls')),
)
