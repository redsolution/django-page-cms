"""Default example views"""
from django.http import Http404, HttpResponsePermanentRedirect
from pages import settings
from pages.models import Page, PageAlias
from pages.http import auto_render, get_language_from_request
from pages.http import get_slug_and_relative_path
from pages.urlconf_registry import get_urlconf
from django.core.urlresolvers import resolve, reverse
from django.utils import translation


class Details(object):
    """
    This class based view get the root pages for navigation
    and the current page to display if there is any.

    All is rendered with the current page's template.
    """

    def __call__(self, request, path=None, lang=None, delegation=True,
            **kwargs):

        current_page = False
        lang = self.choose_language(lang, request)

        # if the path is not defined, we assume that the user
        # is using the view in a non usual way and fallback onto the
        # the full request path.
        if path is None:
            path = request.path

        pages_navigation = self.get_navigation(request, path, lang)

        context = {
            'path': path,
            'pages_navigation': pages_navigation,
            'lang': lang,
        }

        is_staff = self.is_user_staff(request)

        current_page = self.resolve_page(request, context, is_staff)

        # if no pages has been found, we will try to find it via an Alias
        if not current_page:
            redirection = self.resolve_alias(request, path, lang)
            if redirection:
                return redirection
        else:
            context['current_page'] = current_page

        # If unauthorized to see the pages, raise a 404, That can
        # happen with expired pages.
        if not is_staff and not current_page.visible:
            raise Http404

        redirection = self.resolve_redirection(request, context)
        if redirection:
            return redirection

        template_name = self.get_template(request, context)

        if request.is_ajax():
            template_name = "body_%s" % template_name

        self.extra_context(request, context)

        answer = self.delegate(request, context, delegation)
        if answer:
            return answer

        return template_name, context

    def resolve_page(self, request, context, is_staff):
        """Return the appropriate page according to the path."""
        path = context['path']
        lang = context['lang']
        pages_navigation = context['pages_navigation']
        if settings.PAGE_HIDE_ROOT_SLUG:
            if path == reverse('pages-root') and pages_navigation:
                return Page.objects.root()[0]
        if path:
            return Page.objects.from_path(path, lang,
                exclude_drafts=(not is_staff))
        elif pages_navigation:
            return Page.objects.root()[0]

    def resolve_alias(self, request, path, lang):
        alias = PageAlias.objects.from_path(request, path, lang)
        if alias:
            url = alias.page.get_url_path(lang)
            return HttpResponsePermanentRedirect(url)
        raise Http404

    def resolve_redirection(self, request, context):
        """Check for redirections."""
        current_page = context['current_page']
        lang = context['lang']
        if current_page.redirect_to_url:
            return HttpResponsePermanentRedirect(current_page.redirect_to_url)

        if current_page.redirect_to:
            return HttpResponsePermanentRedirect(
                current_page.redirect_to.get_url_path(lang))

    def get_navigation(self, request, path, lang):
        """Get the pages that are at the root level."""
        return Page.objects.navigation().order_by("tree_id")

    def choose_language(self, lang, request):
        """Deal with the multiple corner case of choosing the language."""

        # Can be an empty string or None
        if not lang:
            lang = get_language_from_request(request)

        # Raise a 404 if the language is not in not in the list
        if lang not in [key for (key, value) in settings.PAGE_LANGUAGES]:
            raise Http404

        # We're going to serve CMS pages in language lang;
        # make django gettext use that language too
        if lang and translation.check_for_language(lang):
            translation.activate(lang)

        return lang

    def get_template(self, request, context):
        """Just there in case you have special business logic."""
        return context['current_page'].get_template()

    def is_user_staff(self, request):
        """Return True if the user is staff."""
        return request.user.is_authenticated() and request.user.is_staff

    def extra_context(self, request, context):
        """Call the PAGE_EXTRA_CONTEXT function if there is one."""
        if settings.PAGE_EXTRA_CONTEXT:
            context.update(settings.PAGE_EXTRA_CONTEXT())

    def delegate(self, request, context, delegation=True):
        # if there is a delegation to another view,
        # call this view instead.
        current_page = context['current_page']
        if delegation and current_page.delegate_to:
            urlconf = get_urlconf(current_page.delegate_to)
            result = resolve('/', urlconf)
            if result:
                view, args, kwargs = result
                kwargs.update(context)
                return view(request, *args, **kwargs)


# This view instance use the auto_render decorator. It means
# that you can use the only_context extra parameter to get
# only the local variables of this view without rendering
# the template.

#   >>> from pages.views import details
#   >>> context = details(request, only_context=True)
details = auto_render(Details())
