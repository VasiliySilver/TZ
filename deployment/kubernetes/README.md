# Kubernetes Deployment

Развёртывание Book Management API в Kubernetes с использованием Kustomize.

## 📁 Структура

```
kubernetes/
├── base/                           # Базовые манифесты
│   ├── namespace.yaml              # Namespace: tz
│   ├── configmap.yaml              # ConfigMap с настройками
│   ├── secrets.yaml                # Secrets (пароли)
│   ├── postgres-statefulset.yaml   # PostgreSQL StatefulSet + PVC
│   ├── rabbitmq-statefulset.yaml   # RabbitMQ StatefulSet + PVC
│   ├── api-deployment.yaml         # API Deployment + Service
│   ├── consumer-deployment.yaml    # Consumer Deployment
│   └── kustomization.yaml          # Kustomize base
└── overlays/
    ├── local/                      # Для minikube
    │   ├── api-service-nodeport.yaml
    │   ├── api-deployment-patch.yaml
    │   └── kustomization.yaml
    └── prod/                       # Для production
        ├── api-deployment-patch.yaml
        ├── api-ingress.yaml
        └── kustomization.yaml
```

## 🚀 Quick Start (Minikube)

### 1. Подготовка

```bash
# Запустить minikube
minikube start --cpus=4 --memory=4096

# Включить ingress (опционально)
minikube addons enable ingress

# Проверить
kubectl get nodes
```

### 2. Собрать Docker образы для minikube

```bash
# Переключиться на Docker daemon minikube
eval $(minikube docker-env)

# Собрать образы
cd /path/to/TZ
docker build -t vasiliysilver/tz-api:dev -f deployment/docker/Dockerfile.api .
docker build -t vasiliysilver/tz-consumer:dev -f deployment/docker/Dockerfile.consumer .

# Проверить
docker images | grep tz
```

### 3. Deploy через Makefile

```bash
# Из корня проекта
make k8s-local

# Или вручную
kubectl apply -k deployment/kubernetes/overlays/local
```

### 4. Проверить статус

```bash
# Через Makefile
make k8s-status

# Или вручную
kubectl get pods -n tz -w
kubectl get svc -n tz
kubectl get pvc -n tz
```

Ожидаемый результат:
```
NAME                           READY   STATUS    RESTARTS   AGE
postgres-0                     1/1     Running   0          2m
rabbitmq-0                     1/1     Running   0          2m
tz-api-xxxxxxxxxx-xxxxx        1/1     Running   0          1m
tz-consumer-xxxxxxxxxx-xxxxx   1/1     Running   0          1m
```

### 5. Получить доступ к API

```bash
# Через NodePort
minikube service tz-api-service -n tz

# Или через port-forward
kubectl port-forward -n tz svc/tz-api-service 8000:8000

# Открыть в браузере
open http://localhost:8000/docs
```

### 6. Доступ к RabbitMQ Management UI

```bash
# Через NodePort (30672)
minikube service rabbitmq-management -n tz

# Или через port-forward
kubectl port-forward -n tz svc/rabbitmq-service 15672:15672

# Открыть
open http://localhost:15672
# Login: guest / guest
```

### 7. Логи

```bash
# Через Makefile
make k8s-logs

# Или конкретного пода
kubectl logs -n tz -f deployment/tz-api
kubectl logs -n tz -f deployment/tz-consumer
kubectl logs -n tz -f statefulset/postgres
kubectl logs -n tz -f statefulset/rabbitmq
```

### 8. Тестирование API

```bash
# Получить URL
export API_URL=$(minikube service tz-api-service -n tz --url)

# Создать книгу
curl -X POST "$API_URL/api/v1/books/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Kubernetes in Action",
    "authors": ["123e4567-e89b-12d3-a456-426614174000"],
    "publication_year": 2023,
    "pages": 500,
    "genre": "Technical"
  }'

# Получить все книги
curl "$API_URL/api/v1/books/"
```

### 9. Удалить

```bash
# Через Makefile
make k8s-delete

# Или вручную
kubectl delete -k deployment/kubernetes/overlays/local

# Полная очистка (включая PVC)
kubectl delete namespace tz
```

## 🏭 Production Deployment

### 1. Подготовка

```bash
# Убедиться что kubectl настроен на prod кластер
kubectl config current-context

# Создать namespace
kubectl create namespace tz
```

### 2. Обновить secrets

```bash
# Сгенерировать сильные пароли
export POSTGRES_PASSWORD=$(openssl rand -base64 32)
export RABBITMQ_PASSWORD=$(openssl rand -base64 32)

# Создать secret
kubectl create secret generic tz-secrets \
  --from-literal=POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
  --from-literal=RABBITMQ_PASSWORD=$RABBITMQ_PASSWORD \
  -n tz
```

### 3. Собрать и загрузить образы

```bash
# Собрать
docker build -t vasiliysilver/tz-api:latest -f deployment/docker/Dockerfile.api .
docker build -t vasiliysilver/tz-consumer:latest -f deployment/docker/Dockerfile.consumer .

# Загрузить в registry
docker push vasiliysilver/tz-api:latest
docker push vasiliysilver/tz-consumer:latest
```

### 4. Deploy

```bash
# Через Makefile
make k8s-prod

# Или вручную
kubectl apply -k deployment/kubernetes/overlays/prod
```

### 5. Настроить Ingress

```bash
# Установить NGINX Ingress Controller (если нет)
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml

# Обновить DNS записи
# api.tz.example.com -> <INGRESS_EXTERNAL_IP>

# Проверить
kubectl get ingress -n tz
```

### 6. Мониторинг

```bash
# Статус
kubectl get pods,svc,pvc,ingress -n tz

# Логи
kubectl logs -n tz -f -l app=tz-api
kubectl logs -n tz -f -l app=tz-consumer

# Events
kubectl get events -n tz --sort-by='.lastTimestamp'

# Resource usage
kubectl top pods -n tz
```

## 🔧 Конфигурация

### Ресурсы

**Local (minikube):**
- API: 1 replica, 256Mi/250m (requests)
- Consumer: 1 replica, 128Mi/100m
- PostgreSQL: 256Mi/250m
- RabbitMQ: 256Mi/250m

**Production:**
- API: 3 replicas, 512Mi/500m (requests), 1Gi/1000m (limits)
- Consumer: 2 replicas, 256Mi/250m (requests), 512Mi/500m (limits)
- PostgreSQL: 256Mi/250m (requests), 1Gi/1000m (limits)
- RabbitMQ: 256Mi/250m (requests), 512Mi/500m (limits)

### Storage

- PostgreSQL PVC: 5Gi
- RabbitMQ PVC: 2Gi
- StorageClass: default (зависит от кластера)

### Secrets

```bash
# Просмотр (base64 encoded)
kubectl get secret tz-secrets -n tz -o yaml

# Обновление
kubectl edit secret tz-secrets -n tz
```

## 🐛 Troubleshooting

### Pod не запускается

```bash
# Описание пода
kubectl describe pod <pod-name> -n tz

# Логи
kubectl logs <pod-name> -n tz

# Логи предыдущего контейнера (если crashed)
kubectl logs <pod-name> -n tz --previous
```

### Проблемы с Storage

```bash
# Проверить PVC
kubectl get pvc -n tz

# Описание PVC
kubectl describe pvc <pvc-name> -n tz

# Проверить StorageClass
kubectl get storageclass
```

### API недоступен

```bash
# Проверить service
kubectl get svc -n tz
kubectl describe svc tz-api-service -n tz

# Проверить endpoints
kubectl get endpoints -n tz

# Port-forward для отладки
kubectl port-forward -n tz svc/tz-api-service 8000:8000
curl http://localhost:8000
```

### База данных не готова

```bash
# Подключиться к postgres pod
kubectl exec -it -n tz postgres-0 -- psql -U postgres

# Проверить данные
\l
\c postgres
\dt
SELECT * FROM alembic_version;
```

### Consumer не обрабатывает события

```bash
# Проверить RabbitMQ
kubectl port-forward -n tz svc/rabbitmq-service 15672:15672
# Открыть http://localhost:15672

# Проверить exchanges и queues
# Должен быть exchange: book_events (topic)
# Queue должна быть bound с routing key: book.*

# Логи consumer
kubectl logs -n tz -f -l app=tz-consumer
```

## 📊 Scaling

### Manual Scaling

```bash
# Scale API
kubectl scale deployment tz-api -n tz --replicas=5

# Scale Consumer
kubectl scale deployment tz-consumer -n tz --replicas=3

# Проверить
kubectl get pods -n tz
```

### Horizontal Pod Autoscaler (HPA)

```bash
# Установить metrics-server (если нет)
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Создать HPA для API
kubectl autoscale deployment tz-api -n tz \
  --cpu-percent=70 \
  --min=2 \
  --max=10

# Проверить
kubectl get hpa -n tz
```

## 🔄 Updates & Rollback

### Rolling Update

```bash
# Обновить образ
kubectl set image deployment/tz-api -n tz \
  api=vasiliysilver/tz-api:v1.1.0

# Следить за обновлением
kubectl rollout status deployment/tz-api -n tz
```

### Rollback

```bash
# История
kubectl rollout history deployment/tz-api -n tz

# Откатить на предыдущую версию
kubectl rollout undo deployment/tz-api -n tz

# Откатить на конкретную версию
kubectl rollout undo deployment/tz-api -n tz --to-revision=2
```

## 🧹 Cleanup

```bash
# Удалить всё в namespace
kubectl delete namespace tz

# Или через Makefile
make k8s-delete

# Остановить minikube
minikube stop
minikube delete
```

## 📝 Полезные команды

```bash
# Shell в pod
kubectl exec -it -n tz <pod-name> -- /bin/sh

# Копировать файлы
kubectl cp -n tz <pod-name>:/path/to/file ./local-file

# Проверить ConfigMap
kubectl get configmap tz-config -n tz -o yaml

# Restart deployment (пересоздать поды)
kubectl rollout restart deployment/tz-api -n tz

# Проверить resource usage
kubectl top nodes
kubectl top pods -n tz
```