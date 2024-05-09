# SYSLOG
Monitor GQL endpoint requests using FastAPI and Prometheus to scrape metrics, record and process used JWT to ensure only safe request are processed by database

How to use:
   This project is a seperate aplication to the actual database and it purpose is to stand before the user and the server, providing necessary filtering for incoming request and processing metadata coming back from the server to the client also know as a reverse proxy 
   Front-end aplication will make all requests to the address of fastapi:8010
   Server endpoint will be positioned in DATABASE_IP
   

To install and run on Docker enviroment: <br/>
   -Have a database running on $DATABASE_IP (default localhost:31120) and is using network bridge $BRIDGE_NAME (alias might be needed incase of naming) <br/>
   Have CORS enable request from localhost:8010<br/>
   -run these command on shell
   ```
docker compose up
docker network connect $BRIDGE_NAME FastAPI
   ```


   
