"""
Separate Celery settings file

"""
from __future__ import absolute_import, unicode_literals
from config_passwords import django_set
import os

if not os.name == "nt":
    import django
    from celery import Celery
    from kombu import Exchange

    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    # Setup django project
    django.setup()
    app = Celery('core',
                 broker=django_set['broker'],
                 backend=django_set['backend'])

    # Using a string here means the worker doesn't have to serialize
    # the configuration object to child processes.
    # - namespace='CELERY' means all celery-related configuration keys
    #   should have a `CELERY_` prefix.
    # app.config_from_object('django.conf:settings', namespace='CELERY')

    app.conf.timezone = 'UTC'
    app.conf.enable_utc = True
    # Load task modules from all registered Django app configs.
    app.autodiscover_tasks()
    # One for internal:
    default_exchange = Exchange('default', type='direct')
    # One for tests only
    tests_exchange = Exchange('tests_run', type='direct', durable=False)

    app.conf.update(
        accept_content=['json', 'pickle', 'application/x-python', 'application/json', 'application/x-python-serialize'],
        task_serializer='pickle',
        result_serializer='json',
        # Do not set! Or logic will not wait of task OK: # task_ignore_result=True,

        # http://docs.celeryproject.org/en/latest/userguide/configuration.html#result-backend
        # http://docs.celeryproject.org/en/latest/userguide/configuration.html#database-url-examples
        # https://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html#keeping-results
        # 1406, "Data too long for column 'result' at row 1" - it's not so important to keep it in DB
        result_backend=django_set['result_backend'],

        # http://docs.celeryproject.org/en/latest/userguide/configuration.html#beat-scheduler
        beat_scheduler='django_celery_beat.schedulers:DatabaseScheduler',

        # http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-default-queue
        task_default_queue='default',
        task_default_exchange='tests_run',
        task_default_routing_key='default',
        task_default_exchange_type='direct',

        # http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-create-missing-queues
        # task_create_missing_queues=True,  # By Default

        # http://docs.celeryproject.org/en/latest/userguide/configuration.html#worker-prefetch-multiplier
        worker_prefetch_multiplier=0,

        # http://docs.celeryproject.org/en/latest/userguide/configuration.html#events
        # worker_send_task_events=True,  # -E at worker service
        # http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-send-sent-event
        # task_send_sent_event=True,
        worker_pool_restarts=True,

        # Maybe this should be disabled to allow workers to get ALL tasks in queue.
        # http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_acks_late
        # http://docs.celeryproject.org/en/master/faq.html#faq-acks-late-vs-retry
        # task_acks_late = False,  # By Default

        # http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-track-started
        # task_track_started=True,

        # http://docs.celeryproject.org/en/latest/userguide/configuration.html#broker-pool-limit
        broker_pool_limit=None,

        # http://docs.celeryproject.org/en/latest/userguide/configuration.html#broker-connection-timeout
        broker_connection_timeout=2,
        broker_connection_retry=True,
        broker_connection_max_retries=0,

        # https://github.com/celery/celery/issues/5340
        # http://docs.celeryproject.org/en/latest/userguide/routing.html#routing-options-rabbitmq-priorities
        # task_queue_max_priority  = 10,
        # task_default_priority = 5,

        # Dev IDEA:
        # http://docs.celeryproject.org/en/latest/userguide/configuration.html#worker-direct
        worker_direct=True,
    )

    # app.control.add_consumer(
    #     queue='routines',
    #     exchange='default',
    #     exchange_type='direct',
    #     routing_key='routines.*',
    #     destination=['w_routines@test.tet-ad.com'])
    #
    # # New:
    # app.control.add_consumer(
    #     queue='alpha',
    #     exchange='default',
    #     exchange_type='direct',
    #     routing_key='alpha.*',
    #     destination=['alpha@test.tet-ad.com'])
    #
    # app.control.add_consumer(
    #     queue='bravo',
    #     exchange='default',
    #     exchange_type='direct',
    #     routing_key='bravo.*',
    #     destination=['bravo@test.tet-ad.com'])

    app.control.cancel_consumer(
        'default',
        destination=[
            'alpha@tentacle',
            'bravo@tentacle',
        ])
