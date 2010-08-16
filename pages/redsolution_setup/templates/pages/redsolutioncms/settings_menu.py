MENU_PROXY_RULES += [
    {
        'name': 'pages',
        'method': 'children',
        'proxy': 'menuproxy.proxies.MenuProxy',
        'model': 'pages.models.Page',
        'children_filter': {'status': 1, },
        'ancestors_exclude': {'status': 0, },
    }, ]
