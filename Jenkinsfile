pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-token')
        DOCKER_USER = 'siddhartha9'
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
                    echo "🚀 Building Docker image..."
                    sh "docker build -t ${DOCKER_USER}/${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Test Container') {
            steps {
                script {
                    echo "🧪 Running test container on a random port..."
                    sh '''
                    docker run --rm -d -p 6146:5051 --name test_container ${DOCKER_USER}/${IMAGE_NAME}:latest
                    sleep 5
                    docker stop test_container
                    '''
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-token', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        echo "📦 Logging into Docker Hub..."
                        sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${DOCKER_USER}/${IMAGE_NAME}:latest
                        '''
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo "🚢 Deploying latest container..."

                    // Stop old container if running
                    sh '''
                    docker stop ${IMAGE_NAME} || true
                    docker rm ${IMAGE_NAME} || true
                    '''

                    // Find a free port dynamically (start from 5052)
                    def BASE_PORT = 5052
                    def FREE_PORT = sh(
                        script: "for p in $(seq ${BASE_PORT} 5100); do ! lsof -Pi :$p -sTCP:LISTEN -t >/dev/null && echo $p && break; done",
                        returnStdout: true
                    ).trim()

                    if (FREE_PORT == "") {
                        error("❌ No free port found between 5052 and 5100!")
                    }

                    echo "✅ Using available port: ${FREE_PORT}"

                    sh "docker run -d -p ${FREE_PORT}:5051 --name ${IMAGE_NAME} ${DOCKER_USER}/${IMAGE_NAME}:latest"
                }
            }
        }
    }

    post {
        success {
            echo "✅ Deployment completed successfully!"
        }
        failure {
            echo "❌ Deployment failed. Please check the Jenkins logs for errors."
        }
    }
}
