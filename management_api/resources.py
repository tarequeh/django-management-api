from django.conf import settings
from django.core.management import get_commands, load_command_class
from django.core.management.base import BaseCommand

from tastypie.authorization import Authorization
from tastypie.bundle import Bundle
from tastypie.exceptions import NotFound, ImmediateHttpResponse
from tastypie.resources import Resource
from tastypie.utils import dict_strip_unicode_keys

from management_api.utils import get_command_list, execute_command


class CommandsResource(Resource):
    class Meta:
        resource_name = 'commands'
        always_return_data = True
        allowed_methods = ['get', 'post']
        authorization = Authorization()

    def __init__(self, *args, **kwargs):
        authorization_class_name = getattr(settings, 'MANAGEMENT_API_AUTHORIZATION_CLASS', None)

        if authorization_class_name is not None:
            AuthorizationClass = __import__(authorization_class_name)
            self._meta.authorization = AuthorizationClass()

        super(CommandsResource, self).__init__(*args, **kwargs)

    def get_list(self, request, **kwargs):
        """
        The GET request handler traverses the django applications and retrieves all available
        commands
        """
        bundle = Bundle()

        commands = get_command_list()

        bundle.data.update({
            'commands': commands
        })

        return self.create_response(request, bundle)

    def get_detail(self, request, **kwargs):
        """
        The GET request handler traverses the django applications and retrieves all available
        commands
        """
        bundle = Bundle()

        command = kwargs.get('pk', None)

        if command is None:
            raise NotFound('Management comamnd is required')

        available_commands = get_command_list()

        if command not in available_commands:
            raise NotFound('Management comamnd is not available over API')

        try:
            app_name = get_commands()[command]
        except KeyError:
            raise ImmediateHttpResponse('Error getting management command details')

        if isinstance(app_name, BaseCommand):
            # If the command is already loaded, use it directly.
            klass = app_name
        else:
            klass = load_command_class(app_name, command)

        description = klass.usage(command)
        description = description.replace('\n', '')
        options = {}

        for option in klass.option_list:
            option_name = ', '.join(option._long_opts)
            options[option_name] = option.help

        bundle.data.update({
            'description': description,
            'options': options
        })

        return self.create_response(request, bundle)

    def post_list(self, request, **kwargs):
        """
        The POST handler accepts a command name and parameters in a list and executes the
        command
        """
        deserialized = self.deserialize(
            request,
            request.raw_post_data,
            format=request.META.get('CONTENT_TYPE', 'application/json')
        )

        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        request_data = dict_strip_unicode_keys(deserialized)

        command = request_data.get('command', None)

        if command is None:
            raise NotFound('Management comamnd is required')

        available_commands = get_command_list()

        if command not in available_commands:
            raise NotFound('Management comamnd is not available over API')

        command_args = request_data.get('args', [])

        result = execute_command(command, *command_args)

        if result is None:
            raise ImmediateHttpResponse('Error retrieving details for command')

        bundle = Bundle()
        bundle.data.update({
            'result': result
        })

        return self.create_response(request, bundle)
