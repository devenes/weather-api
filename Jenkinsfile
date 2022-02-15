pipeline {
  agent any
  stages {
    stage("Stop Running Container") {
      steps {
        sh "docker stop weather-app"
      }
    }
    stage("Delete Container") {
      steps {
        sh "docker rm weather-app"
      }
    }
    stage("Delete Image") {
      steps {
        sh "echo y | docker image prune -a"        
      }
    }
    stage("Pull Image") {
      steps {
        sh """
          docker pull devenes/weather-app:$version
        """
      }
    }
    stage("Run Container") {
      steps {
        sh """
          docker run --name weather-app -d -p 3456:3456 devenes/weather-app:$version
        """
      }
    }    
  }
}
