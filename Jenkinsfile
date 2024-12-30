pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask-app'
        DOCKER_TAG = 'latest'
        APP_PORT = '9440'
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
                sh 'curl http://127.0.0.1:$APP_PORT/status'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE:$DOCKER_TAG .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'amiroudiallodev', passwordVariable: '#Wendpuire.dia45#')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker tag $DOCKER_IMAGE:$DOCKER_TAG amiroudiallodev/$DOCKER_IMAGE:$DOCKER_TAG'
                    sh 'docker push amiroudiallodev/$DOCKER_IMAGE:$DOCKER_TAG'
                }
            }
        }

        stage('Run Application in Docker') {
            steps {
                sh '''
                    docker stop flask-app || true
                    docker rm flask-app || true
                    docker run -d -p $APP_PORT:$APP_PORT --name flask-app $DOCKER_IMAGE:$DOCKER_TAG
                    sleep 5
                    curl http://127.0.0.1:$APP_PORT/status
                '''
            }
        }

        stage('Clean Docker Resources') {
            steps {
                sh '''
                    docker stop flask-app || true
                    docker rm flask-app || true
                    docker image prune -f
                    docker container prune -f
                '''
            }
        }
    }

    post {
        failure {
            mail to: 'amiroudiallo.yw@example.com',
                subject: "Build Failed: ${env.JOB_NAME} [${env.BUILD_NUMBER}]",
                body: "Check the Jenkins logs for details: ${env.BUILD_URL}"
        }
    }
}
