"""
Decorator and helpers for tasks, like:
- send emails on start/finish
- fix errors
- parse outputs, etc

"""

import functools

from django.template import loader
from django.conf import settings
from celery.exceptions import SoftTimeLimitExceeded
from billiard.exceptions import WorkerLostError

from core.mail_send import Mails

# Python logger
import logging

log = logging.getLogger("core.corelogger")
curr_hostname = getattr(settings, 'CURR_HOSTNAME', None)


def exception(function):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur
    """

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        # Messages for fails
        MSG_T_SOFT = '<=Soft Time Limit=> Task soft time limit exceeded. {}.{}'
        MSG_FAIL = '<=TestExecTasks=> Task fail "{}.{}" ! Error output: {}'

        # TODO: Remove debug looging

        try:
            return function(*args, **kwargs)
        except SoftTimeLimitExceeded:
            log.error("Task SoftTimeLimitExceeded: %s", (function, args, kwargs))
            TMail.t_lim(function, *args, **kwargs)
            raise SoftTimeLimitExceeded(MSG_T_SOFT.format(function.__module__, function.__name__))
        except WorkerLostError as e:
            log.error("Task WorkerLostError: %s", (function, e, args, kwargs))
            TMail.t_fail(function, e, *args, **kwargs)
            raise Exception(MSG_FAIL.format(function.__module__, function.__name__, e))
        except Exception as e:
            log.error("Task Exception: %s", (function, e, args, kwargs))
            TMail.t_fail(function, e, *args, **kwargs)
            raise Exception(MSG_FAIL.format(function.__module__, function.__name__, e))

    return wrapper


class TMail:

    @staticmethod
    def t_lim(function, *args, **kwargs):
        txt = '{} : {} Task time exceeded!'.format(curr_hostname, function.__name__)
        log.error("<=Task Time Limit=> %s", txt)
        task_limit = loader.get_template('root/email/task_service/task_details.html')
        # Try to get user email if present:
        user_email = kwargs.get('user_email', None)

        task_details = dict(task_args=args,
                            task_kwargs=kwargs,
                            task=function.__name__,
                            module=function.__module__)

        mail_details = dict(SUBJECT=txt, TASK_DETAILS=task_details)
        mail_html = task_limit.render(mail_details)
        Mails.short(mail_html=mail_html, subject=txt, send_to=user_email)

    @staticmethod
    def t_fail(function, err, *args, **kwargs):
        log.error("<=Task helpers=> %s", '({}) : ({}) Task failed!'.format(curr_hostname, function.__name__))
        task_limit = loader.get_template('root/email/task_service/task_details.html')

        # Try to get user email if present:
        user_email = kwargs.get('user_email', None)

        subj_txt = '{} - Task Failed - {}'.format(curr_hostname, function.__name__)

        task_details = dict(task_args=args,
                            task_kwargs=kwargs,
                            task=function.__name__,
                            module=function.__module__,
                            err=err)

        mail_details = dict(SUBJECT=subj_txt, TASK_DETAILS=task_details)
        mail_html = task_limit.render(mail_details)
        Mails.short(mail_html=mail_html, subject=subj_txt, send_to=user_email)
