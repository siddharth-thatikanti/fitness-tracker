pipeline {
  agent any

  environment {
    // Jenkins credentials IDs
    DOCKERHUB_CREDENTIALS = credentials('jenkinss')  // DockerHub credentials ID in Jenkins
    KUBECONFIG_CREDENTIALS = credentials('kubeconfig') // Kubernetes config credential
    DOCKER_IMAGE = "siddhartha9/fitness-tracker"
  }

  stages {

    /* -------------------------------------------------------
       Stage 1: Checkout source code from GitHub (main branch)
    ---------------------------------------------------------*/
    stage('Checkout Code') {
      steps {
        echo '🔁 Checking out Fitness Tracker code from GitHub...'
        git branch: 'main',
            url: 'https://github.com/siddharth-thatikanti/fitness-tracker.git'
      }
    }

    /* -------------------------------------------------------
       Stage 2: Build Docker Image
    ---------------------------------------------------------*/
    stage('Build Docker Image') {
      steps {
        script {
          echo '🐳 Building Docker image...'
          sh 'docker build -t $DOCKER_IMAGE:latest .'
        }
      }
    }

    /* -------------------------------------------------------
       Stage 3: Push Docker Image to DockerHub
    ---------------------------------------------------------*/
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

    /* -------------------------------------------------------
       Stage 4: Deploy to Kubernetes
    ---------------------------------------------------------*/
stage('Deploy to Kubernetes') {
  steps {
    script {
      echo '☸️ Deploying Fitness Tracker to Kubernetes...'
      
      // Correct way to use a secret file
      withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG_FILE')]) {
        sh '''
          export KUBECONFIG=$KUBECONFIG_FILE
          
          # Try to update image, or apply if not exists
          kubectl set image deployment/fitness-tracker-deployment fitness-tracker=$DOCKER_IMAGE:latest || \
          kubectl apply -f k8s-deployment.yaml
          
          kubectl rollout status deployment/fitness-tracker-deployment
        '''
      }
    }
  }
}

    /* -------------------------------------------------------
       Stage 5: Verify Deployment
    ---------------------------------------------------------*/
    stage('Verify Deployment') {
      steps {
        echo '🔍 Verifying deployment...'
        sh '''
          kubectl get pods -l app=fitness-tracker
          kubectl get svc fitness-tracker-service
        '''
      }
    }
  }

  /* -------------------------------------------------------
     Post Actions: Notifications
  ---------------------------------------------------------*/
  post {
    success {
      echo "✅ Deployment successful! Your Fitness Tracker app is live."
    }
    failure {
      echo "❌ Deployment failed. Please check Jenkins logs for details."
    }
  }
}

