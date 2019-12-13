import multiprocessing
# /tmp should be mounted as tempfs
# dependencies: inotify, greenlet, gevent, eventlet, setproctitle, aiohttp, gthread

worker_class = 'eventlet'
workers = min(multiprocessing.cpu_count() * 2 + 1, 5)
threads = workers
worker_connections = 100  # recommended was 1000

# connection and reloading
keepalive = 5
graceful_timeout = 30  # time for worker to stop
max_requests_jitter = 15  # to not restart simultaneously
max_requests = 500  # and worker restarts (help against memory leaks), mb bad for models

pidfile = "/var/run/gunicorn.pid"
bind = ['0.0.0.0:8000', 'unix:///var/run//gunicorn.sock']  # where to bind
proxy_allow_ips = ['127.0.0.1', 'nginx', 'caddy', 'traefik']  # allowed ips to proxy from
pythonpath = ['.', '..']
reuse_port = True
preload_app = True  # for heavy app it's ok, but disables reload

# cool hooks
# def on_exit(server): pass  # cool exit hook!

# limit_request_fields = 100  # disables ddos, cuts headers larger
# limit_request_field_size = 8190
# limit_request_line = 4096
