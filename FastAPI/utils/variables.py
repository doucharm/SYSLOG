import os

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
status_block=os.environ.get('STATUS_BLOCK',False) #je-li uzivatel dostává skutečné kódy 