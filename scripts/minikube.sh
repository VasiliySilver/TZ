#!/bin/bash
set -e

echo "🚀 Setting up Minikube for TZ project..."

# Check if minikube is installed
if ! command -v minikube &> /dev/null; then
    echo "❌ Minikube is not installed. Please install it first:"
    echo "   https://minikube.sigs.k8s.io/docs/start/"
    exit 1
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install it first:"
    echo "   https://kubernetes.io/docs/tasks/tools/"
    exit 1
fi

# Start minikube if not running
if ! minikube status &> /dev/null; then
    echo "📦 Starting Minikube..."
    minikube start --cpus=4 --memory=4096 --driver=docker
else
    echo "✅ Minikube is already running"
fi

# Enable required addons
echo "🔌 Enabling addons..."
minikube addons enable ingress
minikube addons enable metrics-server

# Build Docker images in minikube's Docker daemon
echo "🐳 Building Docker images in Minikube..."
eval $(minikube docker-env)

cd ../../../  # Go to project root

echo "  Building API image..."
docker build -f deployment/docker/Dockerfile.api -t tz-api:latest .

echo "  Building Consumer image..."
docker build -f deployment/docker/// filepath: /home/user/Nextcloud/Projects/home/TZ/deployment/kubernetes/scripts/setup-minikube.sh
#!/bin/bash
set -e

echo "🚀 Setting up Minikube for TZ project..."

# Check if minikube is installed
if ! command -v minikube &> /dev/null; then
    echo "❌ Minikube is not installed. Please install it first:"
    echo "   https://minikube.sigs.k8s.io/docs/start/"
    exit 1
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install it first:"
    echo "   https://kubernetes.io/docs/tasks/tools/"
    exit 1
fi

# Start minikube if not running
if ! minikube status &> /dev/null; then
    echo "📦 Starting Minikube..."
    minikube start --cpus=4 --memory=4096 --driver=docker
else
    echo "✅ Minikube is already running"
fi

# Enable required addons
echo "🔌 Enabling addons..."
minikube addons enable ingress
minikube addons enable metrics-server

# Build Docker images in minikube's Docker daemon
echo "🐳 Building Docker images in Minikube..."
eval $(minikube docker-env)

cd ../../../  # Go to project root

echo "  Building API image..."
docker build -f deployment/docker/Dockerfile.api -t tz-api:latest .

echo "  Building Consumer image..."
docker build -f deployment/docker/