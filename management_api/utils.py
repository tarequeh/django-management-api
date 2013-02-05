from StringIO import StringIO

from django.conf import settings
from django.core.management import call_command, get_commands

from management_api import logger


def get_command_list():
    commands = []

    commands_app_mapping = get_commands()

    exposed_commands = getattr(settings, 'MANAGEMENT_API_EXPOSED_COMMANDS', settings.INSTALLED_APPS)

    for command_name, app_name in commands_app_mapping.items():
        if command_name in exposed_commands:
            commands.append(command_name)

    return commands


def execute_command(command, *args, **kwargs):
    command_result = StringIO()

    kwargs.update({
        'interactive': False,
        'stdout': command_result
    })

    result = None

    try:
        call_command(command, *args, **kwargs)
        command_result.seek(0)
        result = command_result.read()
    except Exception, e:
        logger.error(
            'Command: %s, args: %s, kwargs: %s. Error: %s',
            command,
            ', '.join(args),
            str(kwargs),
            str(e)
        )
    except SystemExit as e:
        logger.error(
            'Command: %s, args: %s, kwargs: %s. Error: %s',
            command,
            ', '.join(args),
            str(kwargs),
            str(e)
        )

    return result
