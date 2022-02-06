pipeline {
  environment {
    registry = "devenes/weather-app"
    registryCredential = 'dockerHub'
    dockerImage = ''
    dockerfile = 'Dockerfile'
    dockerfilePath = '.'    
   }
   agent any  
   stages {
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
    stage('Deploy Image') {
      steps{
         script {
            docker.withRegistry( '', registryCredential ) {
            dockerImage.push()
          }
        }
      }
    }
    stage('Run Image') {
      steps{
        script {
          docker.withRegistry( '', registryCredential ) {
            dockerImage.run()
          }
        }
      }
    }
  }
}
// Language: Groovy