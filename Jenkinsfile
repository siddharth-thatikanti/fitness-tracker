pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'siddhartha9'
        IMAGE_NAME = 'fitness-tracker'
    }

    stages {
        stage('Checkout') {
    steps {
        git branch: 'main', url: 'https://github.com/siddharth-thatikanti/fitness-tracker.git'
       }
    }
}

        

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKERHUB_USER}/${IMAGE_NAME}:latest")
                }
            }
        }

        stage('Test') {
            steps {
                sh 'echo "Running syntax tests for Flask app..."'
                sh 'python3 -m py_compile app.py'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([string(credentialsId: 'uufj jbjd gobn gbet', variable: 'DOCKERHUB_PASS')]) {
                    sh 'echo $DOCKERHUB_PASS | docker login -u $DOCKERHUB_USER --password-stdin'
                    sh 'docker push $DOCKERHUB_USER/$IMAGE_NAME:latest'
                }
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker run -d -p 5051:5051 $DOCKERHUB_USER/$IMAGE_NAME:latest'
            }
        }
    }

    post {
        success {
            echo "? Fitness Tracker App deployed successfully!"
        }
        failure {
            echo "? Deployment failed. Check logs."
        }
    }




