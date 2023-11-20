import logging
import logging.handlers

logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s.%(msecs)03d\t%(levelname)s:\t%(message)s', 
    datefmt='%Y-%m-%dT%I:%M:%S')

formatter = logging.Formatter(
    fmt='%(asctime)s.%(msecs)03d\t%(levelname)s:\t%(message)s', 
    datefmt='%Y-%m-%dT%I:%M:%S')

syslog = logging.handlers.SysLogHandler(address=("localhost", 514))
syslog.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(syslog)
