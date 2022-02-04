pipeline {
    agent any
    environment {
        PATH="$PATH:/usr/local/bin"
        APP_STACK_NAME="Weather-App"
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
        #        1- cloudformation ile container çalışacak ec2, bu adıma uyarla ve ec2 yaml yaz.
        #        2- ec2 yaml yazıldıktan sonra k8s cluster yaratılır.
        #        3- k8s cluster yaratıldıktan sonra k8s cluster yapısının yapıldığı ec2'ye ulaşılır.
        #        4- ec2'ye ulaşıldıktan sonra k8s cluster yapısının yapıldığı ec2'ye ulaşılır.
        #     }
        # }
        stage('Building images and pushing to dockerhub') {
            steps {
                docker build -t devenes/weather-app:latest
                sh "docker push devenes/weather-app"                
            }
        }
            # stage('Deploying kubernetes files') {
            #     steps {
            #         sh "ansible/deploy.yaml \
            #         -i ansible/inventory/dynamic-inventory-master_aws_ec2.yaml"
            #     }
            # }
    }
}