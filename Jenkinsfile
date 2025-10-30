pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'siddhartha9'
        IMAGE_NAME = 'fitness-tracker-app'
    }

    stages {
        stage('Checkout') {
            steps {
                echo "📦 Checking out code from GitHub..."
                git branch: 'main', url: 'https://github.com/siddharth-thatikanti/fitness-tracker.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "🚀 Building Docker image..."
                    sh "docker build -t ${DOCKERHUB_USER}/${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Test Container') {
            steps {
                script {
                    echo "🧪 Running test container on a random port..."
                    sh '''
                    docker run --rm -d -p 6146:5051 --name test_container ${DOCKERHUB_USER}/${IMAGE_NAME}:latest
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
                        echo "📤 Pushing image to Docker Hub..."
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

                    // Stop and remove any old container if running
                    sh '''
                    docker stop fitness-tracker-app || true
                    docker rm fitness-tracker-app || true
                    '''

                    // Find a free port and deploy
                    sh '''
                    for PORT in $(seq 5052 5100); do
                        if ! lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null; then
                            echo "✅ Using available port: $PORT"
                            docker run -d -p $PORT:5051 --name fitness-tracker-app ${DOCKERHUB_USER}/${IMAGE_NAME}:latest
                            echo "🌐 Application deployed successfully at: http://$(hostname -I | awk '{print $1}'):$PORT"
                            echo "📜 Displaying latest 50 container logs:"
                            docker logs --tail 50 fitness-tracker-app
                            exit 0
                        fi
                    done

                    echo "❌ No available ports found between 5052 and 5100!"
                    exit 1
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed. Please check Jenkins logs."
        }
    }
}
