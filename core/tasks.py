"""
Celery tasks.
All celery tasks should be collected here.
- Task should execute only separate case or case_routine.
- Task should not execute any code itself.
- Task should have exception handler which output useful data or send mail.

Note:
    - Be careful with recursive import.
    - Do not import case routines which import tasks from here.
"""
from __future__ import absolute_import, unicode_literals

import logging

from core.core_celery import app

from core.task_helpers import exception

log = logging.getLogger("core.corelogger")


DAY_LIMIT = 172800
HOURS_2 = 7200
HOURS_1 = 3600
MIN_90 = 5400
MIN_40 = 2400
MIN_20 = 1200
MIN_10 = 600
MIN_1 = 60
SEC_10 = 10
SEC_1 = 1


class TaskRoutines:

    @staticmethod
    @app.task(queue='w_routines@tentacle.dq2', routing_key='routines.TaskRoutines.t_routine_add',
              soft_time_limit=MIN_40, task_time_limit=MIN_90)
    @exception
    def t_routine_add(t_tag, **kwargs):
        """
        Check if working
        :param t_tag:
        :param kwargs:
        :return:
        """
        log.debug("<=TaskRoutines=> t_tag: %s kwargs: %s", t_tag, kwargs)
        # return Other.Functions(**kwargs)

    @staticmethod
    @app.task(queue='w_routines@tentacle.dq2', routing_key='routines.TaskRoutines.t_routine_fail',
              soft_time_limit=MIN_40, task_time_limit=MIN_90)
    @exception
    def t_routine_fail(t_tag, **kwargs):
        """
        Check if working
        :param t_tag:
        :param kwargs:
        :return:
        """
        log.debug("<=TaskRoutines=> t_tag: %s kwargs: %s", t_tag, kwargs)
        raise Exception("I want to fail that task!")
