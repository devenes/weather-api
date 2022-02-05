pipeline {
  environment {
    registry = "devenes/weather-app"
    registryCredential = 'dockerhub'
    dockerImage = ''
    dockerfile = 'Dockerfile'
    dockerfilePath = '.'    
   }
   agent any
  
    stages {
        stage('Build') {
            steps {
            sh 'docker build -t $registry/$dockerImage:$BUILD_NUMBER .'
            }
        }
        stage('Test') {
            steps {
            sh 'docker run -it --rm $registry/$dockerImage:$BUILD_NUMBER'
            }
        }
        stage('Deploy') {
            steps {
            sh 'docker push $registry/$dockerImage:$BUILD_NUMBER'
            }
        }
        stage('Delete old containers') {
            steps {
            sh 'docker stop $(docker ps -a -q)'
            sh 'docker rm $(docker ps -a -q)'
            }
        }        
        stage('Delete image') {
            steps {
                sh 'docker rmi $(docker images -q)'
            }
        }
        stage('Delete old images') {
            steps {
                sh 'docker rmi -f $(docker images -q --filter "dangling=true")'
            }
        }
        stage('Delete old directories') {
            steps {
                sh 'rm -rf /usr/src/app/node_modules'
                sh 'rm -rf /usr/src/app/package-lock.json'
            }
        }
        stage('Delete old best-cloud-academy-api') {
            steps {
                sh 'rm -rf /usr/src/app/best-cloud-academy-api'
            }
        }
        stage('Clone and build image') {
            steps {
                sh 'git clone https://github.com/devenes/best-cloud-academy-api.git' 
                sh 'cd best-cloud-academy-api && docker build -t devenes/weather-app:latest .'
            }
        }
        stage('Pull image') {
            steps {
                sh 'docker pull devenes/weather-app:latest'    
            }    
        }
        stage('Start container') {
            steps {
                sh 'docker run --name best-cloud -d -p 3456:3456 devenes/weather-app:latest'
            }
        }
    }             
}
// Language: Groovy