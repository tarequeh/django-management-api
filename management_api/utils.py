from StringIO import StringIO

from django.conf import settings
from django.core.management import get_commands, load_command_class, call_command
from django.core.management.base import BaseCommand, handle_default_options

from tastypie.exceptions import ImmediateHttpResponse

from management_api import logger


def get_command_list():
    commands = []

    commands_app_mapping = get_commands()

    exposed_commands = getattr(settings, 'MANAGEMENT_API_EXPOSED_COMMANDS', settings.INSTALLED_APPS)

    for command_name, app_name in commands_app_mapping.items():
        if command_name in exposed_commands:
            commands.append(command_name)

    return commands


def execute_command(command, *args):
    try:
        app_name = get_commands()[command]
    except KeyError:
        raise ImmediateHttpResponse('Error getting management command details')

    if isinstance(app_name, BaseCommand):
        # If the command is already loaded, use it directly.
        klass = app_name
    else:
        klass = load_command_class(app_name, command)

    command_args = list(args)

    parser = klass.create_parser(app_name, command)
    options, arguments = parser.parse_args(command_args)
    handle_default_options(options)

    options = options.__dict__

    command_result = StringIO()

    options.update({
        'interactive': False,
        'stdout': command_result
    })

    result = None

    try:
        klass.execute(*arguments, **options)
        command_result.seek(0)
        result = command_result.read()
    except Exception, e:
        logger.error(
            'Command: %s, args: %s, kwargs: %s. Error: %s',
            command,
            ', '.join(arguments),
            str(e)
        )
    except SystemExit as e:
        logger.error(
            'Command: %s, args: %s, kwargs: %s. Error: %s',
            command,
            ', '.join(arguments),
            str(e)
        )
        command_result.seek(0)
        result = command_result.read()

    return result
