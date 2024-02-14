import logging
import logging.handlers
import http.client
import datetime
logging.basicConfig(
    level=logging.DEBUG, 
    format='\t%(levelname)s:\t%(message)s')
#format zprávy do log souboru
formatter = logging.Formatter(
    fmt='\t%(levelname)s:\t%(message)s')
from .variables import log_port,log_server
syslog = logging.handlers.SysLogHandler()
syslog.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(syslog)
#detailní log podle odpovědního kódu
def request_log(bearer_token:str='N/A',ip_address:str='N/A',status_code:int = 404 ):
    if status_code>299:
        message = http.client.responses[status_code]
        time=datetime.datetime.now()
        print("Request from IP %s with authentication token %s return with code %i : %s at %s" %( ip_address,bearer_token,status_code,message,str(time)))
        #logger.debug("Request from IP %s with authentication token %s return with code %i : %s at %s",
                  # ip_address,bearer_token,status_code,message,str(time))