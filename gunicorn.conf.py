# gunicorn.conf.py — Gunicorn configuration for AWS EC2 (Amazon Linux 2023)
import multiprocessing

# Bind to unix socket — Nginx will proxy to this
bind = "unix:/home/ec2-user/app/gunicorn.sock"

# Number of worker processes: (2 x CPU cores) + 1
workers = multiprocessing.cpu_count() * 2 + 1

# Worker class
worker_class = "sync"

# Timeout in seconds
timeout = 120

# Logging to stdout/stderr (systemd captures these)
accesslog = "-"
errorlog = "-"
loglevel = "info"
