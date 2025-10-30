pipeline {
    agent any

    environment {
        // Change this to your actual Docker Hub username
        DOCKERHUB_USER = "siddhartha9"
        IMAGE_NAME = "fitness-tracker-app"
        IMAGE_TAG = "latest"
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
                    sh "docker build -t ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Test Container') {
            steps {
                script {
                    echo "🧪 Running test container on a random port..."
                    // Use a random port to avoid 'port already allocated' errors
                    def testPort = 6000 + new Random().nextInt(999)
                    sh "docker run --rm -d -p ${testPort}:5051 --name test_container ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                    sh "sleep 5"
                    sh "docker stop test_container || true"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dokcerhub-token', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        echo "📦 Logging into Docker Hub..."
                        sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                        sh "docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo "🚢 Deploying latest container..."
                    sh "docker stop fitness-tracker-app || true"
                    sh "docker rm fitness-tracker-app || true"
                    sh "docker run -d -p 5052:5051 --name fitness-tracker-app ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful!"
        }
        failure {
            echo "❌ Deployment failed. Please check the Jenkins logs for errors."
        }
    }
}
