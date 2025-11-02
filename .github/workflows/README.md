# GitHub Actions Environment Variables and Secrets Setup Guide

## Required Secrets

### Container Registry
- `GITHUB_TOKEN` - Automatically provided by GitHub Actions

### Kubernetes Deployment
- `KUBE_CONFIG_STAGING` - Base64 encoded kubeconfig for staging cluster
- `KUBE_CONFIG_PRODUCTION` - Base64 encoded kubeconfig for production cluster

### Production Environment
- `PRODUCTION_DOMAIN` - Your production domain (e.g., api.yourcompany.com)

### Notifications (Optional)
- `SLACK_WEBHOOK_URL` - Slack webhook URL for deployment notifications

## Environment Setup

### Staging Environment
```yaml
name: staging
url: https://staging.yourcompany.com
protection_rules:
  - type: required_reviewers
    required_reviewers: 1
```

### Production Environment
```yaml
name: production
url: https://yourcompany.com
protection_rules:
  - type: required_reviewers
    required_reviewers: 2
  - type: wait_timer
    wait_timer: 5
```

## Repository Settings

### Branch Protection Rules
Configure branch protection for `main` branch:
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Include administrators
- Required status checks:
  - `test`
  - `security-scan`
  - `build`
  - `helm-lint`

### Actions Settings
- Allow GitHub Actions
- Allow actions created by GitHub
- Allow actions by Marketplace verified creators
- Allow specified actions (add your custom actions if any)

## Workflow Features

### 1. CI Workflow (`ci.yml`)
- **Triggers**: Push to main/develop, PRs to main
- **Jobs**:
  - Multi-version Python testing (3.9, 3.10, 3.11)
  - Code linting with flake8
  - Security scanning with safety and bandit
  - Docker image building and pushing
  - Helm chart validation
- **Outputs**: Docker image with tags, test coverage reports

### 2. CD Workflow (`cd.yml`)
- **Triggers**: Push to main, tags starting with 'v', releases
- **Jobs**:
  - Staging deployment (automatic from main)
  - Production deployment (from tags/releases)
  - Smoke tests and health checks
  - Automatic rollback on failure
  - Slack notifications

### 3. Security Workflow (`security.yml`)
- **Triggers**: Weekly schedule, push/PR to main
- **Jobs**:
  - Dependency vulnerability scanning
  - Container image security scanning
  - CodeQL code analysis
  - Secret scanning with TruffleHog

### 4. Performance Workflow (`performance.yml`)
- **Triggers**: Weekly schedule, manual dispatch
- **Jobs**:
  - Load testing with Locust
  - Benchmark testing with pytest-benchmark
  - Memory profiling
  - Performance report generation

### 5. Release Workflow (`release.yml`)
- **Triggers**: Git tags starting with 'v'
- **Jobs**:
  - Automatic changelog generation
  - Multi-architecture Docker builds
  - Helm chart packaging
  - Artifact signing with Cosign
  - Security scanning of release images

### 6. Cleanup Workflow (`cleanup.yml`)
- **Triggers**: Weekly schedule, manual dispatch
- **Jobs**:
  - Old container image cleanup
  - Workflow artifact cleanup
  - Cache cleanup

## Deployment Strategy

### Staging Deployment
- Automatic deployment on merge to `main`
- Single replica for resource efficiency
- Basic smoke tests
- No external traffic

### Production Deployment
- Triggered by version tags (e.g., `v1.0.0`)
- Multi-replica with auto-scaling
- Comprehensive health checks
- Blue-green deployment strategy
- Automatic rollback on failure

## Security Features

### Container Security
- Multi-stage Docker builds
- Non-root user execution
- Vulnerability scanning with Trivy
- Image signing with Cosign

### Code Security
- Dependency scanning with safety and pip-audit
- SAST with CodeQL
- Secret scanning with TruffleHog
- Security policy enforcement

### Infrastructure Security
- RBAC with minimal permissions
- Network policies in Kubernetes
- TLS termination with cert-manager
- Security contexts in pods

## Monitoring and Observability

### Metrics Collection
- Application metrics endpoint
- Resource usage monitoring
- Performance benchmarks
- Load testing results

### Alerting
- Deployment notifications
- Security scan alerts
- Performance degradation alerts
- Infrastructure health checks

## Usage Examples

### Creating a Release
```bash
git tag v1.0.0
git push origin v1.0.0
```

### Manual Performance Test
```bash
gh workflow run performance.yml \
  -f duration=30 \
  -f concurrent_users=100
```

### Emergency Rollback
```bash
kubectl rollout undo deployment/youtube-to-mp3 -n youtube-to-mp3-prod
```

## Troubleshooting

### Common Issues
1. **Failed deployments**: Check Kubernetes cluster connectivity and secrets
2. **Security scan failures**: Review and update dependencies
3. **Performance degradation**: Analyze load test results and resource usage
4. **Image build failures**: Verify Dockerfile and dependencies

### Debug Commands
```bash
# Check workflow status
gh run list --workflow=ci.yml

# View workflow logs
gh run view <run-id> --log

# Check deployment status
kubectl get deployments -n youtube-to-mp3-prod

# View pod logs
kubectl logs -f deployment/youtube-to-mp3 -n youtube-to-mp3-prod
```