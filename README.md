# django-management-api

A django dependent package that exposes API to allow you to run any management
commands via API

## Usage

# Retrieve list of commands

Add the following URL path to your project

```python
url(r'^management_api/', include('management_api.urls')),
```
Then access your list of management commands via:

```
/management_api/v1/commands/?format=json
```
