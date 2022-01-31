FROM node:12-alpine

RUN npm install

EXPOSE 3456
ENTRYPOINT [ "node", "index.js" ]