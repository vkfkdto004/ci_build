pipeline {
    agent any

    environment{
        WORK_PATH = "/docker_build"
        IMAGE_NAME = "kimwooseop/ci_build"
        IMAGE_TAG = "v1"
    }
    stages {
        stage('Git Clone') {
            steps {
                echo 'Cloning Github Build Code!'
                checkout scm
            }
        }
        stage('Docker Image Build') {
            steps {
                echo 'Docker Image Build by Docker-builder'
<<<<<<< Updated upstream
                container('docker-builder') { 
=======
                container('kubectl'){
>>>>>>> Stashed changes
                sh '''
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ${WORK_PATH}
                '''
                }
                }
            }
        }
        stage('Docker Login'){
            steps {
                container('docker-builder') {
                    withCredentials([usernamePassword(
                        credentialsId: 'dockerhub',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        sh '''
                            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        '''
                    }
            }
        }
        stage('Docker Push') {
            steps {
                echo 'Docker Push to my Dockerhub Repository'
                container('docker-builder') { 
                sh '''
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                '''
                }
            }
        }
    }
}   
