import os

allow_vpn=os.environ.get('ALLOW_VPN',False)
database_ip=os.environ.get('DATABASE_IP',"http://localhost:31120/gql") 
log_server=os.environ.get('LOG_SERVER','syslog-ng')
log_port=os.environ.get('LOG_PORT','514')
token_life_limit=os.environ.get('TOKEN_LIFE_LIMIT',3600) 
status_block=os.environ.get('STATUS_BLOCK',False) 