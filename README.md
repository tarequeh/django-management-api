# django-management-api

A django dependent package that exposes API to allow you to run any management
commands via API

## Security

You can specify the authorization class in settings

Commands to be exposed is determined from a whitelist. To add commands to the
whitelist, please specify them in the following variable in settings:

```python
MANAGEMENT_API_EXPOSED_COMMANDS = (
    'syncdb',
    'migrate'
)
```

## Usage

### Setup

Add the following URL path to your project

```python
url(r'^management_api/', include('management_api.urls')),
```

### Retrieve list of available commands

Access your list of management commands via:

```
/management_api/v1/commands/?format=json
```

### Get help for a specific command

```
/management_api/v1/commands/syncdb/?format=json
```

### Run a specific command

Make a POST request to:

```
/management_api/v1/commands/?format=json
```

With the following data:

```javascript
{
    command: 'migrate',
    args: [
        'tastypie',
        '--fake'
    ],

    kwargs: {}
}
```
