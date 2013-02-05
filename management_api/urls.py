from django.conf.urls.defaults import patterns, include

from tastypie.api import Api

from management_api.resources import CommandsResource


v1_api = Api(api_name='v1')

v1_api.register(CommandsResource())


urlpatterns = patterns('',
    (r'^', include(v1_api.urls)),
)
