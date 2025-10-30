pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = 'siddhartha9'
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
                    sh "docker build -t ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Test Container') {
            steps {
                script {
                    echo "🧪 Running test container on a random port..."
                    sh '''
                        docker run --rm -d -p 6146:5051 --name test_container ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest
                        sleep 5
                        docker stop test_container
                    '''
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dokcerhub-token', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        echo "📦 Logging into Docker Hub..."
                        sh '''
                            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                            docker push ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest
                        '''
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo "🚢 Deploying latest container..."
                    sh '''
                        docker stop ${IMAGE_NAME} || true
                        docker rm ${IMAGE_NAME} || true

                        PORT=5052
                        if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
                            echo "⚠️ Port $PORT already in use. Switching to port 5055..."
                            PORT=5055
                        fi

                        docker run -d -p $PORT:5051 --name ${IMAGE_NAME} ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest
                        echo "✅ App deployed successfully on port $PORT"
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "🎉 Pipeline executed successfully! Fitness Tracker app is up and running."
        }
        failure {
            echo "❌ Deployment failed. Please check the Jenkins logs for errors."
        }
    }
}
