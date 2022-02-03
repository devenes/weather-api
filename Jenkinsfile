pipeline {
    agent any
    environment {
        PATH="$PATH:/usr/local/bin"
        APP_STACK_NAME="FlaskApp"
        CFN_KEYPAIR="ofd"
        CFN_TEMPLATE="kubernetes-cluster.yaml"
        AWS_REGION="us-east-1"
    }
    stages {
        # stage('Create k8s Cluster') {
        #     steps {
        #         echo "Creating k8s Cluster for the app"
        #         sh """
        #         aws cloudformation create-stack --region ${AWS_REGION} \
        #         --stack-name ${APP_STACK_NAME} --capabilities CAPABILITY_IAM \
        #         --template-body file://${CFN_TEMPLATE} --parameters ParameterKey=KeyPairName,ParameterValue=${CFN_KEYPAIR}
        #         """
        #         sh "sleep 500"
        #     }
        # }
        stage('Building images and pushing to dockerhub') {
            steps {
                sh "cd FlaskFiles/result_server && \
                docker build -t mirana/flask_result_server:latest ."
                sh "cd FlaskFiles/web_server && \
                docker build -t mirana/flask_web_server:latest ."
                sh "docker push mirana/flask_result_server"
                sh "docker push mirana/flask_web_server"
            }
        }
            # stage('Deploying kubernetes files') {
            #     steps {
            #         sh "ansible-playbook ansible/deploy.yaml \
            #         -i ansible/inventory/dynamic-inventory-master_aws_ec2.yaml"
            #     }
            # }
    }
}