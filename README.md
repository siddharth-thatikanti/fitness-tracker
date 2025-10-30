# fitness-tracker
# Python CI/CD App 🚀
A simple Flask application demonstrating an automated CI/CD pipeline using Jenkins and Docker.

## 🔧 Tech Stack
- Python 3.10
- Flask
- Docker
- Jenkins
- GitHub

## 🧩 Features
- Flask-based REST API
- Health check endpoint
- Jenkinsfile for CI/CD automation
- Dockerfile for containerization

## 🧱 Run Locally
```bash
docker build -t python-cicd-app .
docker run -d -p 5000:5000 python-cicd-app
