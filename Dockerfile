FROM node:12 as build

WORKDIR /app
COPY package.json index.js ./
RUN npm install

FROM node:12-alpine

COPY --from=build /app /
EXPOSE 3456
ENTRYPOINT [ "node", "index.js" ]