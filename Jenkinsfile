pipeline {
  agent any

  environment {
    DOCKERHUB_CREDENTIALS = credentials('jenkinss')  
    DOCKER_IMAGE = "siddhartha9/fitness-tracker"
    KUBECONFIG_CREDENTIALS = credentials('kubeconfig') 
  }

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
          sh 'docker build -t $DOCKER_IMAGE:latest .'
        }
      }
    }

    stage('Push to DockerHub') {
      steps {
        script {
          // Secure Docker login using Jenkins credentials
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
          writeFile file: 'kubeconfig', text: "${KUBECONFIG_CREDENTIALS}"
          withEnv(["KUBECONFIG=${WORKSPACE}/kubeconfig"]) {
            sh '''
              kubectl set image deployment/fitness-tracker-deployment fitness-tracker=$DOCKER_IMAGE:latest --record || \
              kubectl apply -f k8s-deployment.yaml
              kubectl rollout status deployment/fitness-tracker-deployment
            '''
          }
        }
      }
    }

    stage('Verify Deployment') {
      steps {
        sh '''
          kubectl get pods -l app=fitness-tracker
          kubectl get svc fitness-tracker-service
        '''
      }
    }
  }

  post {
    success {
      echo "? Deployment successful!"
    }
    failure {
      echo "? Deployment failed. Check logs."
    }
  }
}

