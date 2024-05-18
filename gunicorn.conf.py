from multiprocessing import cpu_count

from src.config import env

bind = "0.0.0.0:" + str(env.PORT)
workers = (cpu_count() * 2) + 1
capture_output = True
loglevel = "warning"
