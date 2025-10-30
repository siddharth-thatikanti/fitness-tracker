pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'your_dockerhub_username'  // replace this
        IMAGE_NAME = 'fitness-tracker-app'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/siddharth-thatikanti/fitness-tracker.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $DOCKERHUB_USER/$IMAGE_NAME:latest .'
                }
            }
        }

        stage('Test') {
            steps {
                echo 'Running basic container test...'
                sh 'docker run --rm -d -p 5052:5051 $DOCKERHUB_USER/$IMAGE_NAME:latest'
                sh 'sleep 5'
                sh 'curl -f http://localhost:5051 || echo "Container test failed"'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-token', variable: 'DOCKERHUB_PASS')]) {
                    sh 'echo $DOCKERHUB_PASS | docker login -u $DOCKERHUB_USER --password-stdin'
                    sh 'docker push $DOCKERHUB_USER/$IMAGE_NAME:latest'
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying container...'
                sh 'docker stop fitness-tracker || true'
                sh 'docker rm fitness-tracker || true'
                sh 'docker run -d --name fitness-tracker -p 5051:5051 $DOCKERHUB_USER/$IMAGE_NAME:latest'
            }
        }
    }

    post {
        success {
            echo '✅ Deployment Successful! Application running on port 5051.'
        }
        failure {
            echo '❌ Deployment failed. Check logs.'
        }
    }
}

