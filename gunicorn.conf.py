from multiprocessing import cpu_count

from src.config.enviroment import env

bind = f"{env.HOST}:{env.PORT}"
workers = (cpu_count() * 2) + 1
capture_output = True
loglevel = "warning"
