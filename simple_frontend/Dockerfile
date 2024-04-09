FROM node:lts-alpine

WORKDIR /app

COPY package*.json ./
COPY public /app/public  
COPY src /app/src 

RUN npm install
EXPOSE ${PORT}
CMD [ "npm", "start" ]
