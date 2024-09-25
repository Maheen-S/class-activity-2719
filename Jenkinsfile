pipeline {
    agent any
    environment {
        DOCKER_USERNAME = credentials('DOCKER_USERNAME')
        DOCKER_PASSWORD = credentials('DOCKER_PASSWORD')
    }
    stages {
        stage('Checkout dev branch') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            git config --global user.name "Jenkins"
                            git config --global user.email "jenkins@example.com"
                            git checkout dev
                        '''
                    } else {
                        bat '''
                            git config --global user.name "Jenkins"
                            git config --global user.email "jenkins@example.com"
                            git checkout dev
                        '''
                    }
                }
            }
        }
        stage('Merge dev into stage') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            git checkout stage || git checkout -b stage origin/stage
                            git merge dev --no-ff
                            git push origin stage
                        '''
                    } else {
                        bat '''
                            git checkout stage || git checkout -b stage origin/stage
                            git merge dev --no-ff
                            git push origin stage
                        '''
                    }
                }
            }
        }
        stage('Run PyTests on Staging') {
            agent {
                docker {
                    image 'python:3.10'
                    args '-u root'  // For Unix-based environments
                }
            }
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            python -m pip install --upgrade pip
                            if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
                            python -m pytest -v --disable-warnings
                        '''
                    } else {
                        bat '''
                            python -m pip install --upgrade pip
                            if exist requirements.txt pip install -r requirements.txt
                            python -m pytest -v --disable-warnings
                        '''
                    }
                }
            }
        }
        stage('Merge stage into main') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            git checkout main || git checkout -b main origin/main
                            git merge stage --no-ff
                            git push origin main
                        '''
                    } else {
                        bat '''
                            git checkout main || git checkout -b main origin/main
                            git merge stage --no-ff
                            git push origin main
                        '''
                    }
                }
            }
        }
        stage('Build and Push Docker Image') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            docker build -t dockerimg .
                            echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                            docker tag dockerimg $DOCKER_USERNAME/dockerimg:latest
                            docker push $DOCKER_USERNAME/dockerimg:latest
                        '''
                    } else {
                        bat '''
                            docker build -t dockerimg .
                            echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                            docker tag dockerimg %DOCKER_USERNAME%/dockerimg:latest
                            docker push %DOCKER_USERNAME%/dockerimg:latest
                        '''
                    }
                }
            }
        }
        stage('Run Docker Container') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            docker run -d -p 8080:80 $DOCKER_USERNAME/dockerimg:latest
                        '''
                    } else {
                        bat '''
                            docker run -d -p 8080:80 %DOCKER_USERNAME%/dockerimg:latest
                        '''
                    }
                }
            }
        }
    }
}
