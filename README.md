# CI
## jekins 

### helm_repo
링크 (https://github.com/vkfkdto004/helm_repo) 에서 확인 가능.

### jenkins logic
jenkins를 이용하여 github에 올라온 파일을 webhook으로 인식. <br>
docker를 이용하여 이미지를 build 하고, dockerhub에 push 할 것 <br>
이 빌드된 이미지는 argoCD 에서 처리하여 CD 자동화 진행. <br>

* 여기서 docker는 jenkins에서 실행하는 것이 아닌 pod 형식으로 배포해서 사용할 예정이다. (해당 yaml파일은 현 레포지토리에 업로드)
* alpine linux 기반으로 되어 있어 가볍고, ping 명령어가 가능하여 jenkins와 통신 가능 확인.
<br>
<br>

```
kubectl get all -n ci
NAME            READY   STATUS    RESTARTS      AGE
pod/jenkins-0   2/2     Running   2 (89m ago)   171m

NAME                    TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)          AGE
service/jenkins         LoadBalancer   ##.###.##.##   ###.###.##.##   8080:32749/TCP   171m
service/jenkins-agent   ClusterIP      ##.###.##.##   <none>          50000/TCP        171m

NAME                       READY   AGE
statefulset.apps/jenkins   1/1     171m

(metallb-system을 구성해놓아 service를 LoadBalancer로 해놓아도 정상 접근 가능)
```

2026.01.02 - helm을 이용하여 jenkins 배포 / github-webhook 구성하여 정상 동작 테스트 확인. / 간단한 nginx 이미지를 빌드하고 dockerhub에 push 진행. <br>
```
테스트 후 Jenkins 디테일한 동작 구조 파악 (대략적 전체 구조는 helm_repo에 설명되어있음)

- jenkins pod는 stateful로 구성되어 있고, 일종의 jenkins Contoller라고 보면됨.
  - jenkins controller의 역할로써, github webhook 수신, Jenkins 파일 파싱, 어떤 agent를 띄울지 결정, 파이프라인 상태 관리 등을 함.
  - 여기서 한가지 알아야 할점은 빌드는 직접 하지 않는다는 것.

- github에서 push event가 일어나면, controller가 빌드 진행해야겠다고 판단
- jenkins kubernetes 플러그인이 동작해 동일 네임스페이스(ci) 안에서 임시 Pod 생성 (이 임시 Pod가 agent pod)
- agent pod 안에서는 아래와 같은 일이 동작함.
  - jenkins controller와 JNLP로 연결
  - git repo clone
  - Jenkinsfile 실행 ( build / test / deploy 등 Jenkinsfile에 맞게 pipeline 스크립트가 실행됨 )
  - 작업이 완료되면 Pod가 졸료되고, Jenkins controller는 상태 보존.
```

<<<<<<< HEAD
=======
2026.01.03~04 - values.yaml을 수정하여 jenkins agent에 sidecar를 실행해서 docker-build를 하려고 했는데 실패. jenkinsfile에 kaniko pod를 추가로 실행시킬 수 있게 하여 image build 부터 push 까지 할 수 있도록 구성 완료 <br>
```
Jenkinsfile을 보면 도커허브에 업로드하기 위해 인증정보가 있어야 하는데 이 정보를 k8s에서 마운트해서 사용 + 도커허브 인증정보에 대한 k8s secret이 있어야함.

kubectl create secret docker-registry dockerhubconfig \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username=DOCKERHUB_USERNAME \
  --docker-password=DOCKERHUB_TOKEN \
  --docker-email=user@example.com \
  -n ci

위에 맞게 secret을 생성 후에 Jenkinsfile을 push 하면 자동으로 webhook이 실행되며 도커허브에 이미자가 업로드됨.
```
>>>>>>> fbd761a (jenkinsfile upload 2026.01.03-04)
