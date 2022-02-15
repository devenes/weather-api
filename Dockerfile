FROM node:16-alpine


# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./

# Install app dependencies
RUN npm install

#Copy app files
COPY . .

EXPOSE 3456
CMD [ "node", "index.js" ]