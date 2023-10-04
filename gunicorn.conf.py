from multiprocessing import cpu_count

from app.config import PORT


bind = f'0.0.0.0:{PORT}'
workers = cpu_count() * 2 + 1
accesslog = "gunicorn.access.log"
errorlog = "gunicorn.error.log"
capture_output = True
loglevel = 'warning'
