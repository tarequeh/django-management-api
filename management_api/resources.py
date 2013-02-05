from django.conf import settings
from django.conf.urls.defaults import url
from django.core.management import find_management_module, find_commands, call_command

from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.bundle import Bundle
from tastypie.exceptions import BadRequest, NotFound
from tastypie.resources import Resource
from tastypie.utils import trailing_slash, dict_strip_unicode_keys


class CommandsResource(Resource):
    class Meta:
        resource_name = "commands"
        always_return_data = True
        allowed_methods = ['get', 'post']
        authorization = Authorization()

    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_detail'),
                name="api_dispatch_detail"
                ),
            ]

    def get_detail(self, request, **kwargs):
        """
        When you get the tracker, it will set an identification cookie and send you prize
        details
        """
        bundle = Bundle()

        exposed_apps = getattr(settings, 'MANAGEMENT_API_EXPOSED_APPS', settings.INSTALLED_APPS)

        # Find and load the management module for each installed app.
        for app_name in exposed_apps:
            try:
                path = find_management_module(app_name)
                bundle.data.update(dict([
                    (name, app_name) for name in find_commands(path)
                ]))
            except ImportError:
                pass  # No management module - ignore this app

        return self.create_response(request, bundle)
