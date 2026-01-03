pipeline {
  agent { 
    kubernetes {
      label 'kaniko-agent'
      defaultContainer 'kaniko'
      yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    jenkins: kaniko
spec:
  containers:
  - name: kaniko
    resources:
      requests:
        memory: "1Gi"
        cpu: "500m"
      limits:
        memory: "2Gi"
        cpu: "1"
    image: gcr.io/kaniko-project/executor:debug
    imagePullPolicy: IfNotPresent
    command: ["sleep"]
    args: ["infinity"]
    volumeMounts:
    - name: dockerconfig
      mountPath: /kaniko/.docker
    env:
    - name: HOME
      value: "/home/jenkins/agent"
  restartPolicy: Never
  volumes:
  - name: dockerconfig
    projected:
      sources:
      - secret:
          name: dockerhubconfig
          items:
          - key: .dockerconfigjson
            path: config.json
"""
    }
  }

  environment {
    REGISTRY   = "docker.io"
    PROJECT    = "kimwooseop/ci_build"
    IMG_TAG = "v1"
  }

  stages {
    stage('Git Checkout') {
      steps {
        echo 'Github Repogitory Jenkinsfile & Sourcecode Checkout'
        checkout scm
      }
    }

    stage('Docker Image Build & Push') {
      steps {
        container(name: 'kaniko', shell: '/busybox/sh') {
          script {
            def dest = "${env.REGISTRY}/${env.PROJECT}:${env.IMG_TAG}"
            sh """
              echo "Image Building ${dest}"
              /kaniko/executor \
                --dockerfile=./Dockerfile \
                --context=dir://./ \
                --destination=${dest} \
                --verbosity=debug \
                --cleanup
            """
          }
        }
      }
    }
  }

  post { 
    always { 
      script {
        def dest = "${env.REGISTRY}/${env.PROJECT}:${env.IMG_TAG}"
        echo "Finished build of ${dest}"
      }
    }
  }
}