pipeline {
  agent any

  environment {
    // DockerHub credentials stored in Jenkins (ID: jenkinss)
    DOCKERHUB_CREDENTIALS = credentials('jenkinss')
    DOCKER_IMAGE = "siddhartha9/fitness-tracker"
  }

  stages {

    stage('Checkout Code') {
      steps {
        echo '🔁 Checking out Fitness Tracker code from GitHub...'
        git branch: 'main',
            url: 'https://github.com/siddharth-thatikanti/fitness-tracker.git'
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          echo '🐳 Building Docker image...'
          sh '''
            echo "Building Docker image..."
            docker build -t $DOCKER_IMAGE:latest .
          '''
        }
      }
    }

    stage('Push to DockerHub') {
      steps {
        script {
          echo '📦 Pushing image to DockerHub...'
          sh '''
            echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
            docker push $DOCKER_IMAGE:latest
            docker logout
          '''
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        script {
          echo '☸️ Deploying Fitness Tracker to Kubernetes...'

          // Use the kubeconfig stored as a Jenkins secret file
          withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG_FILE')]) {
            sh '''
              export KUBECONFIG=$KUBECONFIG_FILE
              
              echo "📥 Applying Kubernetes configurations..."
              kubectl get nodes

              # Update deployment with new image OR apply it if not exists
              kubectl set image deployment/fitness-tracker-deployment fitness-tracker=$DOCKER_IMAGE:latest --record || \
              kubectl apply -f k8s-deployment.yaml

              echo "🔄 Waiting for rollout to complete..."
              kubectl rollout status deployment/fitness-tracker-deployment
            '''
          }
        }
      }
    }

    stage('Verify Deployment') {
      steps {
        echo '🔍 Verifying Kubernetes deployment...'
        withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG_FILE')]) {
          sh '''
            export KUBECONFIG=$KUBECONFIG_FILE
            echo "Listing pods and service..."
            kubectl get pods -l app=fitness-tracker
            kubectl get svc fitness-tracker-service
          '''
        }
      }
    }
  }

  post {
    success {
      echo "✅ Deployment successful! The Fitness Tracker app is live on Kubernetes 🚀"
    }
    failure {
      echo "❌ Deployment failed. Please check Jenkins logs for details."
    }
  }
}
pipeline {
  agent any

  environment {
    DOCKERHUB_CREDENTIALS = credentials('jenkinss')  
    DOCKER_IMAGE = "siddhartha9/fitness-tracker"
  }

  stages {

    stage('Checkout Code') {
      steps {
        echo '🔁 Checking out Fitness Tracker code from GitHub...'
        git branch: 'main',
            url: 'https://github.com/siddharth-thatikanti/fitness-tracker.git'
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          echo '🐳 Building Docker image...'
          sh 'docker build -t $DOCKER_IMAGE:latest .'
        }
      }
    }

    stage('Push to DockerHub') {
      steps {
        script {
          echo '📦 Pushing image to DockerHub...'
          sh """
            echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
            docker push $DOCKER_IMAGE:latest
          """
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        script {
          echo '☸️ Deploying Fitness Tracker to Kubernetes...'

          // Corrected secret-file handling
          withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG_FILE')]) {
            sh '''
              export KUBECONFIG=$KUBECONFIG_FILE

              kubectl set image deployment/fitness-tracker-deployment fitness-tracker=$DOCKER_IMAGE:latest || \
              kubectl apply -f k8s-deployment.yaml

              kubectl rollout status deployment/fitness-tracker-deployment
            '''
          }
        }
      }
    }

    stage('Verify Deployment') {
      steps {
        echo '🔍 Verifying Kubernetes deployment...'
        sh '''
          kubectl get pods -l app=fitness-tracker
          kubectl get svc fitness-tracker-service
        '''
      }
    }
  }

  post {
    success {
      echo "✅ Deployment successful! The Fitness Tracker app is live."
    }
    failure {
      echo "❌ Deployment failed. Please check Jenkins logs for details."
    }
  }
}

