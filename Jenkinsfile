pipeline {
    environment {
        imagename = "maheens6/class-activity-image"
        dockerImage = ''
        containerName = 'class-activity-container'
        dockerHubCredentials = 'DOCKER_USERNAME'
    }
  
    agent any

    stages {
        stage('Cloning Git') {
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
                    sh "docker run -d --name ${containerName} ${imagename}:latest"
                }
            }
        }
 
        stage('Stop and Remove Container') {
            steps {
                script {
                    sh "docker stop ${containerName} || true"
                    sh "docker rm ${containerName} || true"
                }
            }
        }
 
        stage('Deploy Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: dockerHubCredentials, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh "docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD"

                        sh "docker push ${imagename}:latest"
                    }
                }
            }
        }
    }
}