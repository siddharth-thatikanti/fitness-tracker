stage('Deploy') {
    steps {
        script {
            echo "🚢 Deploying latest container..."
            sh '''
            docker stop fitness-tracker-app || true
            docker rm fitness-tracker-app || true

            for PORT in $(seq 5052 5100); do
                if ! lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null; then
                    echo "✅ Using available port: $PORT"
                    docker run -d -p $PORT:5051 --name fitness-tracker-app siddhartha9/fitness-tracker-app:latest
                    echo "🌐 App running on http://localhost:$PORT"
                    exit 0
                fi
            done

            echo "❌ No available ports found between 5052 and 5100!"
            exit 1
            '''
        }
    }
}
