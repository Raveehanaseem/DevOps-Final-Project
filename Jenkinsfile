pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKERHUB_USERNAME = 'd4rk3y3'
        IMAGE_NAME = 'webapp'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Code Fetch Stage') {
            steps {
                echo 'Fetching code from GitHub...'
                checkout scm
                echo 'Code fetched successfully!'
                sh 'ls -la'
            }
        }

        stage('Docker Image Creation Stage') {
            steps {
                echo 'Building Docker image...'
                sh """
                    docker build -t ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG} .
                    docker tag ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG} ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:latest
                """
            }
        }

        stage('Push to DockerHub') {
            steps {
                echo 'Pushing image to DockerHub...'
                sh """
                    echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin
                    docker push ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}
                    docker push ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:latest
                """
            }
        }

        stage('Kubernetes Deployment Stage') {
            steps {
                echo 'Deploying to Kubernetes...'
                sh """
                    kubectl apply -f deployment.yaml
                    kubectl apply -f service.yaml
                    kubectl rollout status deployment/webapp-deployment
                    kubectl get pods
                    kubectl get services
                """
            }
        }

        stage('Prometheus/Grafana Stage') {
            steps {
                echo 'Setting up monitoring...'
                sh """
                    kubectl apply -f monitoring/prometheus-config.yaml
                    kubectl apply -f monitoring/prometheus-deployment.yaml
                    kubectl apply -f monitoring/grafana-deployment.yaml
                    kubectl get pods
                """
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs above.'
        }
        always {
            sh 'docker logout'
        }
    }
}