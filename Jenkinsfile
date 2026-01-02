pipeline {
    agent any

    environment{
        REMOTE_BUILDER_POD = "kubectl exec -it -n default docker-builder"
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
                sh '''
                    ${REMOTE_BUILDER_POD} -- \
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ${WORK_PATH}
                '''
            }
        }
        stage('Docker Push') {
            steps {
                echo 'Docker Push to my Dockerhub Repository'
                sh '''
                    ${REMOTE_BUILDER_POD} -- \
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }
    }
}
