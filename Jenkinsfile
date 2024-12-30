pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask-app'
        DOCKER_TAG = 'latest'
        PATH = "/usr/local/bin:$PATH"
    }
    
    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/amiroudiallo-dev/webstack-portfolio.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Upgrade Pip') {
            steps {
                sh './venv/bin/python3 -m pip install --upgrade pip'
            }
        }

        stage('Test Application') {
            steps {
                sh './venv/bin/python3 -m unittest discover -s tests'
                sh './venv/bin/python app.py &'
                sh 'curl http://127.0.0.1:9440/status'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE:$DOCKER_TAG .'
            }
        }

        stage('Run Application in Docker') {
            steps {
                sh '''
                    docker stop flask-app || true
                    docker rm flask-app || true
                    docker run -d -p 9440:9440 --name flask-app $DOCKER_IMAGE:$DOCKER_TAG
                    sleep 5
                    curl http://127.0.0.1:9440/status
                '''
            }
        }

        stage('Clean up Docker') {
            steps {
                sh 'docker stop flask-app || true'
                sh 'docker rm flask-app || true'
            }
        }
    }
}
