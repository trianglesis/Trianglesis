from __future__ import absolute_import, unicode_literals
import os

# Can lock celery with log write permissions.
from core.corelogger import test_logger
log = test_logger()

if not os.name == "nt":
    # This will make sure the app is always imported when
    # Django starts so that shared_task will use this app.
    from .core_celery import app as celery_app
    __all__ = ['celery_app']
