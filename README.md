# Weather API

<p align="left"> <a href="https://aws.amazon.com" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/amazonwebservices/amazonwebservices-original-wordmark.svg" alt="aws" width="40" height="40"/> </a> <a href="https://www.docker.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> </a> <a href="https://expressjs.com" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/express/express-original-wordmark.svg" alt="express" width="40" height="40"/> </a> <a href="https://git-scm.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a> <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" alt="javascript" width="40" height="40"/> </a> <a href="https://www.jenkins.io" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/jenkins/jenkins-icon.svg" alt="jenkins" width="40" height="40"/> </a> <a href="https://www.nginx.com" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/nginx/nginx-original.svg" alt="nginx" width="40" height="40"/> </a> <a href="https://nodejs.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/nodejs/nodejs-original-wordmark.svg" alt="nodejs" width="40" height="40"/> </a> </p>


![pipeline](/readme/pipeline.png)

You can use the following commands if you want to run the application locally:

`npm install`

`npm run start`

You can see the real-time weather of **Barcelona** in the browser at:

`http://localhost:3456/temperature?city=barcelona`

--------------------------------------------------------------------------------
## Application Containerization with Docker

To containerize the application you need to build a Docker image first. We defined the dependencies, requirements, and instructions in the `Dockerfile`:

```bash
FROM node:16-alpine
# Create app directory
WORKDIR /usr/src/app
# Install app dependencies
COPY package*.json ./
RUN npm install
# Copy app files 
COPY . .
# Define the port that the app will listen on
EXPOSE 3456
# Define the command that will be executed when the container is run
CMD [ "node", "index.js" ]
```

To build the Docker image you need to use the `docker build` command: 

`docker build -t devenes/weather-app:20 .`

After you have built the Docker image, run the containerized application using the `docker run` command: 

`docker run -p 3456:3456 devenes/weather-app:20`

After you have run the Docker image as a container, you can access the app using the following URL on your local machine:
`http://localhost:3456/`

`http://localhost:3456/temperature?city=barcelona`

To upload the Docker image to Docker Hub, we used the `docker push` command:

`docker push devenes/weather-app:20`

Check out the [Docker Hub Profile](https://hub.docker.com/repository/docker/devenes/weather-app) to see the Docker image and the other versions of the containerized application.

You can download the Docker image from the Docker Hub using the following command:

`docker pull devenes/weather-app`

To stop the container, use the `docker stop` command:

`docker stop <container_id>`

To remove the container, use the `docker rm` command:

`docker rm <container_id>`

To remove the image, use the `docker rmi` command:

`docker rmi <image_id>`

-----------------------------------------

## CI/CD with GitHub Actions

We used GitHub Actions to automate the build and deployment of our Docker image to Docker Hub. We used this configuration in our GitHub Actions workflow to trigger the build and deploy the image to Docker Hub every time we commit to the "release" branch.

The `on` and `push` sections are defined to run the trigger when a new commit is created in the "release" branch.

```bash
name: Docker Build And Push
on:
  push:
    branches:
      - "release"
```      
Wrote the stages to build Docker image and login to Docker Hub.
For logining to Docker Hub you need to define your Docker Hub credentials in the environment variables on GitHub settings which are called `DOCKER_HUB_USERNAME` and `DOCKER_HUB_PASSWORD`.
```bash
jobs:
  docker:
    steps:    
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1
      - name: Login to DockerHub
        uses: docker/login-action@v1
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
```          

One of the best practices is to name the Docker image tag with using the `run_number` variable in the GitHub workflow to avoid overwriting images and define new versions.

```bash
- name: Build and push
  uses: docker/build-push-action@v2
  with:
    push: true
    # use the latest tag from the release branch with run_number
    tags: devenes/weather-app:${{github.run_number}}
```  
-----------------------------------------
## CI/CD with Jenkins using Webhooks
An alternative way to build and push the Docker image automatically is to use Webhooks on GitHub to trigger the build and push when a new commit is added into the "release" branch. You need to add a Webhook configuration on your GitHub repository settings with writing the Jenkins Webhook URL in the `Payload URL` section. 

Your `Payload URL` will appear as:

`http://your-jenkins-server:8080/github-webhook/`

- You need to be sure that GitHub plugin is installed and enabled on your Jenkins server: https://plugins.jenkins.io/github/

Simply when you add a new commit on your GitHub repository, you can trigger the Jenkins pipeline by sending a GET request to the `Payload URL`. It means that every time you commit into a specific branch which you selected on Jenkins settings or into any other branch, the Jenkins pipeline will be triggered. By defining the stages on Jenkins pipeline, you can clone your repository automatically or build, push and pull the Docker image.

- Install the Docker Pipelines plugin on Jenkins which allows building, testing, and using Docker images from Jenkins Pipeline projects:
https://plugins.jenkins.io/docker-workflow/

First, we need to set our credentials on the Jenkins pipeline which we defined in the `Global Configuration` section in `Manage Jenkins`.
```bash
  environment {
    registry = "devenes/weather-app"
    registryCredential = 'dockerHub'
    dockerfile = 'Dockerfile'
   }
```
You can add your Git repository URL in the pipeline stages with Git method or you can set your own Git repository URL in the Jenkins pipeline settings. 

```bash
    stage('Cloning Git') {
      steps {
        git 'https://github.com/devenes/best-cloud-academy-api.git'
      }
    }
    stage('Building image') {
      steps{
        script {
          dockerImage = docker.build registry + ":$BUILD_NUMBER"
        }
      }
    }
```
In order to upload the Docker image to Docker Hub in Jenkins pipeline, you need to set your Docker Hub credentials as the environment variables on Jenkins settings, named `dockerHubUser` and `dockerHubPassword` under ID `dockerHub`.

```bash
    stage('Deploy Image') {      
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerHub', passwordVariable: 'dockerHubPassword', usernameVariable: 'dockerHubUser')]) {
          sh "docker login -u ${env.dockerHubUser} -p ${env.dockerHubPassword}"
          sh "docker push devenes/weather-app:20"
        }
      }
    }
```
In other way you can set your credential ID on Jenkins pipeline as the environment variable and use following methods to upload the Docker image to Docker Hub: 
```bash
    stage('Deploy Image') {
      steps{
         script {
            docker.withRegistry( '', registryCredential ) {
            dockerImage.push()
          }
        }
      }
    }
```
- You may face the following error when you try to push the Docker image to Docker Hub.
 `denied: requested access to the resource is denied` 
 The solution that I tried, you can follow to use the `docker login` command to login to Docker Hub and then use the `docker push` command to push the Docker image to Docker Hub manually. Or you can use the `docker logout` command to logout from Docker Hub. And build your Docker image again. After that, you can use the `docker login` command to login to Docker Hub again and then use the `docker push` command to push the Docker image to Docker Hub. You refresh the Docker Hub credentials on your machine and then you can push the Docker image to Docker Hub.

------------------------------------------------------
## Getting started with AWS CloudFormation 

The way we chose to implement Jenkins into the CI/CD pipeline is using AWS CloudFormation to create a Stack and deploy it to AWS. The reason we use CloudFormation is to automatically configure and install a server like Nginx and also tools like Git, Docker, and Jenkins. 

- Use the `jenkins-server.yml` template file to create a CloudFormation Stack on AWS. 

------------------------------------------------------
## Reverse Proxy with Nginx

After running Docker container, we need to configure the app to be available on the Internet. But we will not be configuring the app to be available on the Internet. We will be manupulating the Nginx configuration file to use a reverse proxy to forward requests to the port which is Nginx listening on.

In the first step, we need to create a new Nginx server and configure it. The earlier we configure the Nginx server, the faster the app will be available on the Internet. So the fastest way to configure the Nginx server is using CloudFormation Stack so that we can edit the Nginx configuration file in the CloudFormation template. The first port we defined is 3456 on the app and Dockerfile when we built and we need to forward to make the app available on the Internet via HTTP protocol by listening on port 80. 

We added the following commands to the CloudFormation template under the `UserData` section:

```bash
# install nginx
amazon-linux-extras install nginx1.12
# start nginx
systemctl start nginx
# configure reverse proxy in nginx.conf with adding the following line at the 48th line under server section
sed -i '48i proxy_pass http://localhost:3456/;' etc/nginx/nginx.conf
```  
- Note: Adding a new line to the Nginx configuration file is not the best way to configure the Nginx server. Replacing the entire Nginx configuration file or directory is the best way to configure the Nginx server.

Final view of Nginx configuration file:
```bash
server {
    # listen on port 80
    listen       80 default_server;
    listen       [::]:80 default_server;
    server_name  _;
    root         /usr/share/nginx/html;

    # Load configuration files for the default server block.
    include /etc/nginx/default.d/*.conf;

    location / {
    # The port which is our app working on    
    proxy_pass http://localhost:3456/;
    }
```          

- Also if you want to see the result of the app on the Internet quickly, you can add `Docker pull` and `Docker run` commands into the CloudFormation template under the `UserData` section. So you can quickly see the result of the application on the Internet, without waiting for the manual installation and configuration of the resources.

```bash
docker pull devenes/weather-app:20
docker run -d -p 3456:3456 --name weather-app devenes/weather-app:20  
```

At the end of the CloudFormation template, we need to add the following command under the `UserData` section for restarting the Nginx server to be able to see the result of the app on the Internet with reverse proxy on port 80:
```bash
systemctl restart nginx.service
```
------------------------------------------------------
## Output on the live server


![names](/readme/names.png)

![toronto](/readme/toronto.png)

![madrid](/readme/madrid.png)
