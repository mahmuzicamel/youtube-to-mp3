# YouTube to MP3 Helm Chart

This Helm chart deploys the YouTube to MP3 converter service on a Kubernetes cluster.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.2.0+
- Docker image `youtube-to-mp3` available in your cluster

## Installation

### 1. Package the chart (optional)
```bash
helm package helm-chart/youtube-to-mp3/
```

### 2. Install the chart
```bash
# Install with default values
helm install youtube-to-mp3 helm-chart/youtube-to-mp3/

# Install with custom values
helm install youtube-to-mp3 helm-chart/youtube-to-mp3/ -f custom-values.yaml

# Install with specific values
helm install youtube-to-mp3 helm-chart/youtube-to-mp3/ \
  --set image.repository=your-registry/youtube-to-mp3 \
  --set image.tag=v1.0.0 \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host=youtube-converter.example.com
```

### 3. Upgrade the chart
```bash
helm upgrade youtube-to-mp3 helm-chart/youtube-to-mp3/
```

### 4. Uninstall the chart
```bash
helm uninstall youtube-to-mp3
```

## Configuration

The following table lists the configurable parameters and their default values:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of replicas | `1` |
| `image.repository` | Image repository | `youtube-to-mp3` |
| `image.tag` | Image tag | `latest` |
| `image.pullPolicy` | Image pull policy | `IfNotPresent` |
| `service.type` | Service type | `ClusterIP` |
| `service.port` | Service port | `80` |
| `service.targetPort` | Container target port | `8000` |
| `ingress.enabled` | Enable ingress | `false` |
| `ingress.hosts` | Ingress hosts | `[{host: youtube-to-mp3.local, paths: [{path: /, pathType: Prefix}]}]` |
| `resources.limits.cpu` | CPU limit | `1000m` |
| `resources.limits.memory` | Memory limit | `1Gi` |
| `resources.requests.cpu` | CPU request | `250m` |
| `resources.requests.memory` | Memory request | `512Mi` |
| `autoscaling.enabled` | Enable HPA | `false` |
| `autoscaling.minReplicas` | Minimum replicas | `1` |
| `autoscaling.maxReplicas` | Maximum replicas | `5` |
| `autoscaling.targetCPUUtilizationPercentage` | CPU utilization target | `80` |
| `persistence.enabled` | Enable persistent storage | `false` |
| `persistence.size` | Storage size | `1Gi` |
| `healthCheck.enabled` | Enable health checks | `true` |
| `healthCheck.path` | Health check path | `/docs` |

## Examples

### Basic deployment
```bash
helm install my-youtube-converter helm-chart/youtube-to-mp3/
```

### Production deployment with ingress
```yaml
# production-values.yaml
replicaCount: 3

image:
  repository: myregistry.com/youtube-to-mp3
  tag: "v1.0.0"

resources:
  limits:
    cpu: 2000m
    memory: 2Gi
  requests:
    cpu: 500m
    memory: 1Gi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "10"
  hosts:
    - host: youtube-converter.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: youtube-converter-tls
      hosts:
        - youtube-converter.example.com

persistence:
  enabled: true
  storageClass: fast-ssd
  size: 5Gi
```

```bash
helm install youtube-converter helm-chart/youtube-to-mp3/ -f production-values.yaml
```

### Development deployment with port-forward
```bash
helm install youtube-converter-dev helm-chart/youtube-to-mp3/ \
  --set replicaCount=1 \
  --set resources.requests.cpu=100m \
  --set resources.requests.memory=256Mi

# Access via port-forward
kubectl port-forward svc/youtube-converter-dev-youtube-to-mp3 8080:80
```

## Usage

Once deployed, you can access the API:

1. **Swagger UI**: `http://your-domain/docs`
2. **ReDoc**: `http://your-domain/redoc`
3. **Convert YouTube to MP3**: 
   ```bash
   curl -X POST "http://your-domain/convert/" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}' \
     --output audio.mp3
   ```

## Monitoring

### Check deployment status
```bash
kubectl get pods -l app.kubernetes.io/name=youtube-to-mp3
kubectl get svc -l app.kubernetes.io/name=youtube-to-mp3
```

### View logs
```bash
kubectl logs -l app.kubernetes.io/name=youtube-to-mp3 -f
```

### Check resource usage
```bash
kubectl top pods -l app.kubernetes.io/name=youtube-to-mp3
```

## Troubleshooting

### Common Issues

1. **Image pull errors**: Ensure the Docker image is built and available
   ```bash
   # Build and tag the image
   docker build -t youtube-to-mp3:latest .
   
   # For local clusters (minikube/kind)
   docker save youtube-to-mp3:latest | docker load
   ```

2. **Pod not starting**: Check logs and events
   ```bash
   kubectl describe pod <pod-name>
   kubectl logs <pod-name>
   ```

3. **Health check failures**: Verify the `/docs` endpoint is accessible
   ```bash
   kubectl port-forward <pod-name> 8000:8000
   curl http://localhost:8000/docs
   ```

## License

This project is licensed under the MIT License.