# Kubernetes Deployment Guide

Deploy Waifu Animation Chat to SolidRusT HQ Kubernetes cluster.

## Prerequisites

1. **Access to SolidRusT K8s cluster**
   ```bash
   kubectl get nodes  # Should show cluster nodes
   ```

2. **Docker access to Gitea registry**
   ```bash
   docker login poseidon.hq.solidrust.net:30008
   ```

3. **SolidRusT API Key** from https://console.solidrust.ai

4. **kubeseal** (for secrets)
   ```bash
   # macOS
   brew install kubeseal
   
   # Linux
   wget https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/kubeseal-linux-amd64
   sudo install -m 755 kubeseal-linux-amd64 /usr/local/bin/kubeseal
   ```

## Quick Start

### 1. Build and Push Images

```bash
# Build backend
docker build -f k8s/Dockerfile.backend -t poseidon.hq.solidrust.net:30008/waifu-animation/backend:latest .
docker push poseidon.hq.solidrust.net:30008/waifu-animation/backend:latest

# Build frontend
docker build -f k8s/Dockerfile.frontend -t poseidon.hq.solidrust.net:30008/waifu-animation/frontend:latest .
docker push poseidon.hq.solidrust.net:30008/waifu-animation/frontend:latest
```

### 2. Create Namespace

```bash
kubectl create namespace waifu-animation
```

### 3. Create Sealed Secret

```bash
# Create temporary secret file
kubectl create secret generic waifu-secrets \
  --from-literal=llm-api-key=srt_prod_YOUR_ACTUAL_KEY_HERE \
  --namespace=waifu-animation \
  --dry-run=client -o yaml > /tmp/secret.yaml

# Seal it
kubeseal -f /tmp/secret.yaml -w k8s/overlays/production/sealed-secret.yaml

# Clean up plain secret
rm /tmp/secret.yaml
```

### 4. Deploy to Cluster

```bash
# Apply with kustomize
kubectl apply -k k8s/overlays/production/

# Watch rollout
kubectl rollout status deployment/waifu-backend -n waifu-animation
kubectl rollout status deployment/waifu-frontend -n waifu-animation
```

### 5. Verify Deployment

```bash
# Check pods
kubectl get pods -n waifu-animation

# Check logs
kubectl logs -l component=backend -n waifu-animation --tail=50
kubectl logs -l component=frontend -n waifu-animation --tail=50

# Test backend health
kubectl port-forward svc/waifu-backend 8000:8000 -n waifu-animation
curl http://localhost:8000/api/system-info
```

### 6. Access Application

Depending on your ingress setup:

**Option A: Port Forward (development)**
```bash
kubectl port-forward svc/waifu-frontend 3000:80 -n waifu-animation
# Access at http://localhost:3000
```

**Option B: HTTPRoute (production)**
- Ensure Gateway API is configured
- Update `httproute.yaml` with your gateway name and hostname
- Access at configured hostname (e.g., https://waifu.hq.solidrust.net)

## Configuration

### Update LLM Settings

Edit `k8s/overlays/production/configmap.yaml`:

```yaml
data:
  llm-provider: "openai"
  llm-api-url: "https://artemis.hq.solidrust.net/v1/chat/completions"
  llm-model: "vllm-primary"  # or gpt-4o-mini, claude-haiku
```

Apply changes:
```bash
kubectl apply -f k8s/overlays/production/configmap.yaml
kubectl rollout restart deployment/waifu-backend -n waifu-animation
```

### Update API Key

```bash
# Create new sealed secret (see step 3 above)
kubectl apply -f k8s/overlays/production/sealed-secret.yaml

# Restart backend to pick up new secret
kubectl rollout restart deployment/waifu-backend -n waifu-animation
```

### Scale Replicas

```bash
# Scale backend
kubectl scale deployment/waifu-backend --replicas=3 -n waifu-animation

# Scale frontend
kubectl scale deployment/waifu-frontend --replicas=3 -n waifu-animation
```

## Storage

### SQLite Persistence

The backend uses a PersistentVolumeClaim for SQLite database:

```bash
# Check PVC status
kubectl get pvc -n waifu-animation

# Backup database
kubectl exec -n waifu-animation deployment/waifu-backend -- \
  tar czf - /data/waifu_chat.db > waifu-backup-$(date +%Y%m%d).tar.gz

# Restore database
kubectl exec -i -n waifu-animation deployment/waifu-backend -- \
  tar xzf - -C / < waifu-backup-20260126.tar.gz
```

### Migrate to PostgreSQL (Future)

See issue #6 for PostgreSQL/Data Layer migration plan.

## Monitoring

### Resource Usage

```bash
# Pod resource usage
kubectl top pods -n waifu-animation

# Node placement
kubectl get pods -n waifu-animation -o wide
```

### Logs

```bash
# Stream backend logs
kubectl logs -f -l component=backend -n waifu-animation

# Stream frontend logs
kubectl logs -f -l component=frontend -n waifu-animation

# Last 100 lines
kubectl logs -l app=waifu-animation -n waifu-animation --tail=100
```

### Events

```bash
# Check for issues
kubectl get events -n waifu-animation --sort-by='.lastTimestamp'
```

## Troubleshooting

### Pods Not Starting

```bash
# Describe pod for events
kubectl describe pod <pod-name> -n waifu-animation

# Common issues:
# - Image pull errors: Check registry credentials
# - Resource limits: Check node capacity
# - Secret missing: Verify sealed-secret.yaml applied
```

### WebSocket Connection Errors

```bash
# Test WebSocket endpoint
kubectl port-forward svc/waifu-backend 8000:8000 -n waifu-animation
# Use browser console: new WebSocket('ws://localhost:8000/ws/test-client')

# Check session affinity
kubectl get svc waifu-backend -n waifu-animation -o yaml | grep -A5 sessionAffinity
```

### Backend Can't Connect to Artemis

```bash
# Check DNS resolution
kubectl exec -n waifu-animation deployment/waifu-backend -- \
  nslookup artemis.hq.solidrust.net

# Test connectivity
kubectl exec -n waifu-animation deployment/waifu-backend -- \
  curl -v https://artemis.hq.solidrust.net/v1/chat/completions

# Verify API key
kubectl get secret waifu-secrets -n waifu-animation -o jsonpath='{.data.llm-api-key}' | base64 -d
```

### Database Locked Errors

```bash
# SQLite doesn't support multiple writers
# Ensure only 1 backend replica if using SQLite:
kubectl scale deployment/waifu-backend --replicas=1 -n waifu-animation

# Or migrate to PostgreSQL (issue #6)
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Deploy to K8s

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Build and push images
      run: |
        docker build -f k8s/Dockerfile.backend -t poseidon.hq.solidrust.net:30008/waifu-animation/backend:${{ github.sha }} .
        docker build -f k8s/Dockerfile.frontend -t poseidon.hq.solidrust.net:30008/waifu-animation/frontend:${{ github.sha }} .
        docker push poseidon.hq.solidrust.net:30008/waifu-animation/backend:${{ github.sha }}
        docker push poseidon.hq.solidrust.net:30008/waifu-animation/frontend:${{ github.sha }}
    
    - name: Deploy to K8s
      run: |
        kubectl set image deployment/waifu-backend backend=poseidon.hq.solidrust.net:30008/waifu-animation/backend:${{ github.sha }} -n waifu-animation
        kubectl set image deployment/waifu-frontend frontend=poseidon.hq.solidrust.net:30008/waifu-animation/frontend:${{ github.sha }} -n waifu-animation
```

## Update Strategy

### Rolling Update (Zero Downtime)

```bash
# Build new images with version tag
docker build -f k8s/Dockerfile.backend -t poseidon.hq.solidrust.net:30008/waifu-animation/backend:v1.2.0 .
docker push poseidon.hq.solidrust.net:30008/waifu-animation/backend:v1.2.0

# Update deployment
kubectl set image deployment/waifu-backend \
  backend=poseidon.hq.solidrust.net:30008/waifu-animation/backend:v1.2.0 \
  -n waifu-animation

# Watch rollout
kubectl rollout status deployment/waifu-backend -n waifu-animation
```

### Rollback

```bash
# Rollback to previous version
kubectl rollout undo deployment/waifu-backend -n waifu-animation

# Rollback to specific revision
kubectl rollout history deployment/waifu-backend -n waifu-animation
kubectl rollout undo deployment/waifu-backend --to-revision=2 -n waifu-animation
```

## Cleanup

```bash
# Delete entire namespace (WARNING: deletes all data)
kubectl delete namespace waifu-animation

# Or delete individual resources
kubectl delete -k k8s/overlays/production/
```

## Related Documentation

- **Artemis Integration:** `docs/ARTEMIS_INTEGRATION.md`
- **Database Migration:** Issue #6
- **Gateway API:** https://gateway-api.sigs.k8s.io/
- **Sealed Secrets:** https://sealed-secrets.netlify.app/

## Support

- **Issues:** https://github.com/suparious/adult-waifu-animation/issues
- **K8s Cluster:** Contact SolidRusT infrastructure team

---

**Version:** 1.0  
**Last Updated:** 2026-01-26  
**Related Issues:** #5 (K8s Deployment), #1 (Artemis Integration)
