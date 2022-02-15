pipeline {
  agent any
  stages {
    stage("Stop Running Container") {
      steps {
        sh "docker stop weather-app"
      }
    }
    stage("Delete Running Container") {
      steps {
        sh "docker rm weather-app"
      }
    }
    stage("Delete Image") {
      steps {
        sh "echo y | docker image prune -a"        
      }
    }
    stage("pull") {
      steps {
        sh """
          docker pull devenes/weather-app:$version
        """
      }
    }
    stage("run") {
      steps {
        sh """
          docker run --name weather-app -d -p 3456:3456 devenes/weather-app:$version
        """
      }
    }
  }
}
