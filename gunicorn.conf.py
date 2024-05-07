from multiprocessing import cpu_count

from src.config import PORT

bind = "0.0.0.0:" + str(PORT)
workers = (cpu_count() * 2) + 1
capture_output = True
loglevel = "warning"
