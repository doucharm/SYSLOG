import os
"""
Module to retrieve environment variables and configure settings for the application.

- allow_vpn: Whether VPN usage is allowed for access. Defaults to False.

- database_ip: The location of the database. Defaults to "http://localhost:31120/gql".

- origins: List of allowed CORS origins limiting access to the endpoint. Defaults to ["http://localhost:3000", "http://localhost:3001"].

- log_server: The address of the log server. Defaults to 'localhost'.

- log_port: The port number for the log server. Defaults to '514'.

- token_life_limit: The duration of a JWT token's validity in seconds. Defaults to 3600 seconds (1 hour).

- status_block: Whether users receive real codes for status. Defaults to True.
"""
#Tady se importuje promenne prostredi
allow_vpn=os.environ.get('ALLOW_VPN',False) #je-li je povolen použítí VPN na přístup
database_ip=os.environ.get('DATABASE_IP',"http://localhost:31120/gql") #lokace  databáze
origins = [ #CORS omezuje přístup do endpoint pouze z zdroje uvedeno
    "http://localhost:3000",
    "http://localhost:3002",
]
log_server=os.environ.get('LOG_SERVER','localhost')
log_port=os.environ.get('LOG_PORT','514')# lokace log serveru
token_life_limit=os.environ.get('TOKEN_LIFE_LIMIT',3600) # jak dlouho trva jeden JWT
status_block=os.environ.get('STATUS_BLOCK',True) #je-li uzivatel dostává skutečné kódy 