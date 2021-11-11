#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from askvce.settings import *


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'askvce.settings')
    os.environ.setdefault('DJANGO_SUPERUSER_USER_NAME',
                          DJANGO_SUPERUSER_USER_NAME)
    os.environ.setdefault('DJANGO_SUPERUSER_PASSWORD',
                          DJANGO_SUPERUSER_PASSWORD)
    os.environ.setdefault('DJANGO_SUPERUSER_EMAIL', DJANGO_SUPERUSER_EMAIL)
    os.environ.setdefault('DJANGO_SUPERUSER_FIRST_NAME',
                          DJANGO_SUPERUSER_FIRST_NAME)
    os.environ.setdefault('DJANGO_SUPERUSER_LAST_NAME',
                          DJANGO_SUPERUSER_LAST_NAME)
    os.environ.setdefault('DJANGO_SUPERUSER_DOB', DJANGO_SUPERUSER_DOB)
    os.environ.setdefault('DJANGO_SUPERUSER_GRAD_YEAR',
                          DJANGO_SUPERUSER_GRAD_YEAR)
    os.environ.setdefault('DJANGO_SUPERUSER_HTNO', DJANGO_SUPERUSER_HTNO)
    os.environ.setdefault('DJANGO_SUPERUSER_PHONE',
                          DJANGO_SUPERUSER_PHONE)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
