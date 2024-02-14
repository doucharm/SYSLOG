FROM node:16.14.0-alpine 
WORKDIR /usr/src
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3452
CMD [ "node", "App.js" ]