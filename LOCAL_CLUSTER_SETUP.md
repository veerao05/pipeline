# Local Kubernetes Cluster Setup for CI/CD Pipeline

This guide explains how to set up and deploy your application to a local Kubernetes cluster.

## Prerequisites

### 1. Install Docker Desktop (Recommended)
- Download and install Docker Desktop for macOS
- Enable Kubernetes in Docker Desktop:
  - Open Docker Desktop → Settings → Kubernetes
  - Check "Enable Kubernetes"
  - Click "Apply & Restart"

### 2. Alternative: Install Minikube
```bash
# Install minikube
brew install minikube

# Start minikube cluster
minikube start --driver=docker

# Enable ingress addon
minikube addons enable ingress
```

### 3. Install kubectl (if not already installed)
```bash
# Install kubectl
brew install kubectl

# Verify installation
kubectl version --client
```

## Local Cluster Configuration

### 1. Verify Cluster is Running
```bash
# Check cluster info
kubectl cluster-info

# Check nodes
kubectl get nodes

# Check if you can connect
kubectl get pods --all-namespaces
```

### 2. Get Cluster Details for GitLab CI/CD

#### For Docker Desktop Kubernetes:
```bash
# Get cluster server URL
kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}'
# Usually: https://kubernetes.docker.internal:6443
```

#### For Minikube:
```bash
# Get cluster server URL
minikube ip
kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}'
```

### 3. Create Service Account and Token for GitLab CI/CD

```bash
# Create service account
kubectl create serviceaccount gitlab-deploy

# Create cluster role binding
kubectl create clusterrolebinding gitlab-deploy-binding \
    --clusterrole=cluster-admin \
    --serviceaccount=default:gitlab-deploy

# For Kubernetes 1.24+, create token manually
kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: gitlab-deploy-token
  annotations:
    kubernetes.io/service-account.name: gitlab-deploy
type: kubernetes.io/service-account-token
EOF

# Get the token
kubectl get secret gitlab-deploy-token -o jsonpath='{.data.token}' | base64 --decode
```

Save this token - you'll need it for GitLab CI/CD variables.

## GitLab CI/CD Variables Setup

Go to your GitLab project → Settings → CI/CD → Variables and add:

| Variable Name | Value | Description |
|---------------|-------|-------------|
| `LOCAL_KUBE_TOKEN` | [token from above] | Service account token |
| `LOCAL_CLUSTER_SERVER` | https://kubernetes.docker.internal:6443 | Cluster API server URL |

## Local Testing Commands

### 1. Build and Test Locally
```bash
# Build Docker image locally
docker build -t math-app:local .

# Run locally for testing
docker run --rm math-app:local
```

### 2. Deploy to Local Cluster Manually
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get deployments -n pipeline-local
kubectl get pods -n pipeline-local

# Check logs
kubectl logs -n pipeline-local -l app=math-app

# Port forward to access locally
kubectl port-forward -n pipeline-local svc/math-app-service 8080:80
```

### 3. Clean Up Local Deployment
```bash
# Delete deployment
kubectl delete -f k8s/

# Delete namespace
kubectl delete namespace pipeline-local
```

## Troubleshooting

### Common Issues:

1. **Connection Refused**
   - Ensure Kubernetes is enabled in Docker Desktop
   - Check if kubectl can connect: `kubectl get nodes`

2. **Image Pull Errors**
   - Ensure Docker registry credentials are set up
   - For local testing, use `imagePullPolicy: Never` and build image locally

3. **Permission Denied**
   - Verify service account has proper cluster role bindings
   - Check token is valid and not expired

4. **Pod Stuck in Pending**
   - Check resource requirements in deployment.yaml
   - Verify node has sufficient resources: `kubectl describe nodes`

### Useful Debug Commands:
```bash
# Check cluster events
kubectl get events --sort-by=.metadata.creationTimestamp

# Describe problematic pod
kubectl describe pod <pod-name> -n pipeline-local

# Check service account
kubectl get serviceaccounts
kubectl describe serviceaccount gitlab-deploy

# Check cluster resources
kubectl top nodes
kubectl top pods --all-namespaces
```

## Security Notes for Local Development

- The local cluster uses `insecure-skip-tls-verify: true` for simplicity
- In production, always use proper TLS certificates
- Rotate service account tokens regularly
- Use least privilege access principles for service accounts

## Next Steps

1. Set up the GitLab CI/CD variables as described above
2. Push code to trigger the CI pipeline
3. Manually trigger the CD pipeline from GitLab UI
4. Monitor deployment in your local cluster using kubectl commands