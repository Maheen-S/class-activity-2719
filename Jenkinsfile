pipeline {
    environment {
        imagename = "maheens6/class-activity-image"
        dockerImage = ''
        containerName = 'class-activity-container'
        dockerHubCredentials = 'DOCKER_USERNAME'
    }

    agent any

    stages {
        stage('Clone Git') {
            steps {
                git([url: 'git@github.com:Maheen-S/class-activity-2719.git', branch: 'main'])
            }
        }

        stage('Building image') {
            steps {
                script {
                    dockerImage = docker.build "${imagename}:latest"
                }
            }
        }

        stage('Running image') {
            steps {
                script {
                    if (isUnix()) {
                        sh "docker run -d --name ${containerName} ${imagename}:latest"
                    } else {
                        bat "docker run -d --name ${containerName} ${imagename}:latest"
                    }
                }
            }
        }

        stage('Stop, Remove Container') {
            steps {
                script {
                    if (isUnix()) {
                        sh "docker stop ${containerName} || true"
                        sh "docker rm ${containerName} || true"
                    } else {
                        bat "docker stop ${containerName} || exit 0"
                        bat "docker rm ${containerName} || exit 0"
                    }
                }
            }
        }

        stage('Deploy Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: dockerHubCredentials, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        if (isUnix()) {
                            sh "docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD"
                            sh "docker push ${imagename}:latest"
                        } else {
                            bat "docker login -u %DOCKER_USERNAME% -p %DOCKER_PASSWORD%"
                            bat "docker push ${imagename}:latest"
                        }
                    }
                }
            }
        }
    }
}
