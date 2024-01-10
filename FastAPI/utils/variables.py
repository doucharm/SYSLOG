import os
allow_vpn=os.environ.get('ALLOW_VPN',False)
database_ip=os.environ.get('DATABASE_IP',"http://localhost:31120/gql")
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
]
log_server=os.environ.get('LOG_SERVER','localhost')
log_port=os.environ.get('LOG_PORT','514')
token_life_limit=os.environ.get('TOKEN_LIFE_LIMIT',3600)
status_block=os.environ.get('STATUS_BLOCK',True)