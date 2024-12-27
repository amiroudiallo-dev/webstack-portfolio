pipeline {
    agent any

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

        stage('Test Application') {
            steps {
                sh './venv/bin/python app.py &'
                sh 'curl http://127.0.0.1:9440/status'
            }
        }
    }
}
