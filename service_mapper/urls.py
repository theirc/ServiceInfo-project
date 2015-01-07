import os

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.views.generic import RedirectView
from django.views.static import serve

import api.urls

# FIXME: Developers, remove this once we have any real translated strings.
# There has to be one string or none of the tools produce any output, which
# is confusing.
# Translators: You do NOT need to translate this:
foo = _("THIS IS A TEST")

FRONTEND_DIR = os.path.join(settings.PROJECT_ROOT, 'frontend')

# Reminder: the `static` function is a no-op if DEBUG is False, as in production.
urlpatterns = [
    # Django admin
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        # Redirect / to /index.html if running locally.
        # NB: We only get this far on a / URL with runserver if we add --nostatic to runserver,
        # e.g. "python manage.py runserver --nostatic"
        # Otherwise, the static file handler wraps the whole WSGI app and returns a
        # "Directory indexing not allowed" error on a / URL before the rest of Django can
        # even see it.  (Blechh.)
        url(r'^$', RedirectView.as_view(url=settings.STATIC_URL + 'index.html'), name='index-html-redirect'),
        # The few files we want to serve statically when running locally
        url(r'^(?P<path>(index.html|bundle\.js))$', serve, kwargs={'document_root': settings.STATIC_ROOT}),
        url(r'^(?P<path>(admin|styles|locales|rest_framework|debug_toolbar)/.*)$', serve, kwargs={'document_root': settings.STATIC_ROOT}),
    ]
