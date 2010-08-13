# django-page-cms urls 

urlpatterns += patterns('',
    (r'^pages', include('pages.urls')),
    {% if pages_settings.handle_frontpage %}
    url(r'^$', 'pages.views.details', name='site-root'),
    {% endif %}
    {% if 'grandma.django-tinymce-attachment' in cms_settings.installed_packages %}
    url(r'^tinymce/', include('tinymce.urls')),
    {% endif %}
)
