import logging
import logging.handlers
import http.client
import datetime
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
def request_log(bearer_token:str='N/A',ip_address:str='N/A',status_code:int = 404 ):
    if status_code>299:
        message = http.client.responses[status_code]
        time=datetime.datetime.now()
        print("Request from IP %s with authentication token %s return with code %i : %s at %s",
                    ip_address,bearer_token,status_code,message,str(time))