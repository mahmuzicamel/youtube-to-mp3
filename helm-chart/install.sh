#!/bin/bash

# YouTube to MP3 Helm Chart Installation Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
RELEASE_NAME="youtube-to-mp3"
NAMESPACE="default"
ENVIRONMENT="dev"
VALUES_FILE=""

# Function to print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -r, --release-name NAME    Release name (default: youtube-to-mp3)"
    echo "  -n, --namespace NAMESPACE  Kubernetes namespace (default: default)"
    echo "  -e, --environment ENV      Environment: dev|prod (default: dev)"
    echo "  -f, --values-file FILE     Custom values file"
    echo "  -h, --help                 Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                                    # Install with default settings"
    echo "  $0 -e prod -n production              # Install production version"
    echo "  $0 -r my-converter -f custom.yaml    # Install with custom values"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -r|--release-name)
            RELEASE_NAME="$2"
            shift 2
            ;;
        -n|--namespace)
            NAMESPACE="$2"
            shift 2
            ;;
        -e|--environment)
            ENVIRONMENT="$2"
            shift 2
            ;;
        -f|--values-file)
            VALUES_FILE="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            print_error "Unknown option $1"
            usage
            exit 1
            ;;
    esac
done

# Validate environment
if [[ "$ENVIRONMENT" != "dev" && "$ENVIRONMENT" != "prod" ]]; then
    print_error "Environment must be 'dev' or 'prod'"
    exit 1
fi

# Check if helm is installed
if ! command -v helm &> /dev/null; then
    print_error "Helm is not installed. Please install Helm first."
    exit 1
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    print_error "kubectl is not installed. Please install kubectl first."
    exit 1
fi

# Check if we can connect to Kubernetes cluster
if ! kubectl cluster-info &> /dev/null; then
    print_error "Cannot connect to Kubernetes cluster. Please check your kubeconfig."
    exit 1
fi

print_info "Starting installation of YouTube to MP3 service..."
print_info "Release name: $RELEASE_NAME"
print_info "Namespace: $NAMESPACE"
print_info "Environment: $ENVIRONMENT"

# Create namespace if it doesn't exist
if ! kubectl get namespace "$NAMESPACE" &> /dev/null; then
    print_info "Creating namespace: $NAMESPACE"
    kubectl create namespace "$NAMESPACE"
fi

# Prepare helm command
HELM_CMD="helm install $RELEASE_NAME helm-chart/youtube-to-mp3/ --namespace $NAMESPACE"

# Add values file based on environment or custom file
if [[ -n "$VALUES_FILE" ]]; then
    if [[ ! -f "$VALUES_FILE" ]]; then
        print_error "Values file not found: $VALUES_FILE"
        exit 1
    fi
    HELM_CMD="$HELM_CMD -f $VALUES_FILE"
    print_info "Using custom values file: $VALUES_FILE"
elif [[ "$ENVIRONMENT" == "prod" ]]; then
    HELM_CMD="$HELM_CMD -f helm-chart/values-prod.yaml"
    print_info "Using production values"
else
    HELM_CMD="$HELM_CMD -f helm-chart/values-dev.yaml"
    print_info "Using development values"
fi

# Install the chart
print_info "Installing Helm chart..."
if eval "$HELM_CMD"; then
    print_info "✅ Installation completed successfully!"
    echo ""
    print_info "To check the status:"
    echo "  kubectl get pods -n $NAMESPACE -l app.kubernetes.io/name=youtube-to-mp3"
    echo ""
    print_info "To view logs:"
    echo "  kubectl logs -n $NAMESPACE -l app.kubernetes.io/name=youtube-to-mp3 -f"
    echo ""
    print_info "To access the service:"
    if [[ "$ENVIRONMENT" == "dev" ]]; then
        echo "  kubectl port-forward -n $NAMESPACE svc/$RELEASE_NAME-youtube-to-mp3 8080:80"
        echo "  Then visit: http://localhost:8080/docs"
    else
        echo "  Check your ingress configuration for external access"
    fi
else
    print_error "❌ Installation failed!"
    exit 1
fi