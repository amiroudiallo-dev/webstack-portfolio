pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask-app'
        DOCKER_TAG = 'latest'
        APP_PORT = '9440'
        PATH = "/usr/local/bin:${env.PATH}"
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning the repository...'
                git 'https://github.com/amiroudiallo-dev/webstack-portfolio.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                sh '''
                    python3 -m venv venv
                    ./venv/bin/pip install -r requirements.txt || exit 1
                '''
            }
        }

        stage('Upgrade Pip') {
            steps {
                echo 'Upgrading pip...'
                sh './venv/bin/python3 -m pip install --upgrade pip'
            }
        }

        stage('Test Application') {
            steps {
                echo 'Running tests...'
                sh './venv/bin/python3 -m unittest discover -s tests'
                echo 'Starting the application for status check...'
                sh './venv/bin/python app.py &'
                sleep 15
                sh 'curl --retry 5 --retry-delay 5 http://127.0.0.1:$APP_PORT/status'
                sh 'pkill -f "python app.py" || true'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t $DOCKER_IMAGE:$DOCKER_TAG .'
            }
        }

        stage('Push Docker Image') {
            agent {
                none
            }
            steps {
                echo 'Pushing Docker image...'
                withCredentials([usernamePassword(credentialsId: 'c291fae5-f7d3-4082-aebb-dcc6e6824678', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker tag $DOCKER_IMAGE:$DOCKER_TAG $DOCKER_USER/$DOCKER_IMAGE:$DOCKER_TAG
                        docker push $DOCKER_USER/$DOCKER_IMAGE:$DOCKER_TAG
                    '''
                }
            }
        }

        stage('Run Application in Docker') {
            steps {
                echo 'Running application in Docker...'
                sh '''
                    docker stop flask-app || echo "Failed to stop container"
                    docker rm -f flask-app || echo "Failed to remove container"
                    docker run -d -p $APP_PORT:$APP_PORT --name flask-app $DOCKER_IMAGE:$DOCKER_TAG
                    sleep 5
                    curl http://127.0.0.1:$APP_PORT/status
                '''
            }
        }

        stage('Clean Docker Resources') {
            steps {
                echo 'Cleaning Docker resources...'
                sh '''
                    docker stop flask-app || echo "Failed to stop container"
                    docker rm -f flask-app || echo "Failed to remove container"
                    docker rmi -f $DOCKER_IMAGE:$DOCKER_TAG || true
                '''
            }
        }
    }

    post {
        failure {
            emailext (
                subject: "Build Failed: ${env.JOB_NAME} [${env.BUILD_NUMBER}]",
                body: "Check the Jenkins logs for details: ${env.BUILD_URL}",
                to: 'amiroudiallo.yw@gmail.com'
            )
        }
        success {
            echo 'Pipeline executed successfully!'
        }
    }
}