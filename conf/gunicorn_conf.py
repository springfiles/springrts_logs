from multiprocessing import cpu_count

mode = 'wsgi'
working_dir = '/home/infolog/'
user = 'infolog'
group = 'infolog'
bind = 'unix:/run/gunicorn/infolog.socket'
workers = max(2, min(4, cpu_count()))
timeout = 60
reload = False
loglevel = 'debug'
capture_output = True
accesslog = '/home/infolog/springrts_logs.access.log'
errorlog = '/home/infolog/springrts_logs.error.log'
syslog = False
proc_name = 'springrts_logs'
