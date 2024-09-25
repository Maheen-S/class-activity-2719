pipeline {
    environment {
        DOCKER_USERNAME = credentials('DOCKER_USERNAME')
        DOCKER_PASSWORD = credentials('DOCKER_PASSWORD')
    }
    stages {
        stage('Clone Git') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/dev']], userRemoteConfigs: [[url: 'https://your-repo-url.git']]])
            }
        }
        stage('Git Setup') {
            steps {
                sh '''
                    git config --global user.name "Jenkins"
                    git config --global user.email "jenkins@example.com"
                '''
            }
        }
        stage('Merge dev into stage') {
            steps {
                script {
                    sh '''
                        git checkout stage
                        git merge dev --no-ff
                        git push origin stage
                    '''
                }
            }
        }
        stage('Run PyTests on Staging') {
            agent {
                docker {
                    image 'python:3.10'
                }
            }
            steps {
                sh '''
                    python -m pip install --upgrade pip
                    if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
                    python -m pytest -v --disable-warnings
                '''
            }
        }
        stage('Merge stage into main') {
            steps {
                script {
                    sh '''
                        git checkout main
                        git merge origin/stage --no-ff
                        git push origin main
                    '''
                }
            }
        }
        stage('Build and Push Docker Image') {
            steps {
                script {
                    sh '''
                        docker build -t dockerimg .
                        echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                        docker tag dockerimg $DOCKER_USERNAME/dockerimg:latest
                        docker push $DOCKER_USERNAME/dockerimg:latest
                    '''
                }
            }
        }
        stage('Run Docker Container') {
            steps {
                sh '''
                    docker run -d -p 8080:80 $DOCKER_USERNAME/dockerimg:latest
                '''
            }
        }
    }
}
