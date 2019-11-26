# Broker settings.
broker_url = 'amqp://guest:guest@localhost:5672//'

accept_content = ['json']  # (set, list, or tuple) of types (pickle, yaml, etc) mb MIME ('application/json')
# result_accept_content = None  # same as prev
# enable_utc = True  # default
timezone = 'Europe/Moscow'  # default UTC TODO: consider moscow, europe

# task_annotations = {'*': {'rate_limit': '10/s'}}  # можно менять разное всякое
# task_compression = None  # gzip, bzip2, etc
# task_serializer = 'json'  # pickle, yaml, msgpack, etc

# Using the database to store task state and results.
result_backend = 'db+sqlite:///results.sqlite'

task_annotations = {'tasks.add': {'rate_limit': '10/s'}}

# ---------------------------------- TASK SETTINGS ----------------------------------------
# task_always_eager = True  # provision_debug для синхронного выполнения
# task_eager_propagates = True  # все ошиьки локальных тасков будут вылетать
# task_remote_tracebacks = True  # если перерасываем ошибку, то прикрепить traceback worker
# task_ignore_result = True  # чтобы глобально забивать на результат
task_store_errors_even_if_ignored = True  # хранить ошибки в любом случае
task_track_started = True  # репортить, что таска начала выполняться
task_time_limit = 24 * 60 * 60  # лимит на время, после него воркер убивается
task_soft_time_limit = task_time_limit - 60 * 5  # будет брошен exception SoftTimeLimitExceeded
# task_acks_late  # признавать задачу выполненной поле выполнения
# task_reject_on_worker_lost  # TODO: WTF?
# task_default_rate_limit  TODO: WTF?
# worker_disable_rate_limits  TODO: WTF?

# ---------------------------------- RESULT BACKEND ----------------------------------------
# result_backend = 'database'  # TODO: think abount it
# result_backend_transport_options = {}  TODO: WTF?
result_serializer = 'json'
result_compression = None
result_expires = None  # не удалять результат из базы
# result_expires    TODO: WTF?
# result_chord_join_timeout  TODO: WTF?


# -------------------------------- DB_BACKEND ----------------------------------------------
# result_backend = 'db+postgresql://scott:tiger@localhost/mydatabase'
database_short_lived_sessions = True  # уменьшает производительность, зато не будет ошибок с долгими сессиями

# -------------------------------- BROKER SETTINGS ----------------------------------------------
broker_failover_strategy = "round-robin"
# broker_heartbeat = 10  # TODO: доделать
# broker_heartbeat_checkrate = 2.0
# TODO: others

# -------------------------------- WORKER ----------------------------------------------
imports = ('myapp.tasks',)  # Что бы нам такое заимпортить при старте
# worker_concurrency = None  # сколько процов использует один воркер
worker_prefetch_multiplier = 1  # по дефолту 4, но они так-то могут херово распределяться
worker_lost_wait = 60  # сколько воркеру дается на завершение после ошибки
# worker_disable_rate_limits  # TODO: WTF?
worker_state_db = 'worker_state'  # сохраненное состояние воркера (имя файла)

# -------------------------------- EVENT ----------------------------------------------
worker_send_task_events = True  # отслеживание для flower
task_send_sent_event = True
event_queue_ttl = 60
event_queue_expires = 600
# event_exchange
# event_queue_prefix
event_serializer = 'json'

# -------------------------------- REMOTE CONTROL ----------------------------------------------
control_queue_ttl = 60 * 60  # если команду в течение часа не выполнили, значит не повезло
control_queue_expires = 300
worker_hijack_root_logger = True  # заменяем логер, все хендлеры слетают
worker_log_color = True
worker_pool_restarts = True  # разрешить удаленно pool_restart

# -------------------------------- CELERY BEAT ----------------------------------------------

# TODO: вот это вот все
