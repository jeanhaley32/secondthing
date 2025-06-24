#!/bin/bash

# OpenShift Deployment Script for Message in a Bottle API

set -e

echo "🚀 Deploying Message in a Bottle API to OpenShift..."

# Check if oc is installed
if ! command -v oc &> /dev/null; then
    echo "❌ OpenShift CLI (oc) is not installed. Please install it first."
    exit 1
fi

# Check if user is logged in
if ! oc whoami &> /dev/null; then
    echo "❌ Not logged in to OpenShift. Please run 'oc login' first."
    exit 1
fi

# Get project name from user or use default
PROJECT_NAME=${1:-"message-in-bottle"}

echo "📦 Creating project: $PROJECT_NAME"

# Create project if it doesn't exist
oc new-project $PROJECT_NAME --skip-config-write 2>/dev/null || echo "Project already exists"

# Switch to the project
oc project $PROJECT_NAME

echo "🔨 Building and deploying the application..."

# Create the application from current directory
oc new-app --name message-in-bottle-api --strategy=docker .

echo "⏳ Waiting for build to complete..."
oc logs -f bc/message-in-bottle-api

echo "🌐 Exposing the service..."
oc expose svc/message-in-bottle-api

echo "📋 Getting the route URL..."
ROUTE_URL=$(oc get route message-in-bottle-api -o jsonpath='{.spec.host}')

echo "✅ Deployment complete!"
echo "🌍 Your API is available at: https://$ROUTE_URL"
echo ""
echo "📝 Test the API with:"
echo "curl -X POST \"https://$ROUTE_URL/collect-bottles\" \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '[{\"character\":\"H\",\"coordinates\":{\"x\":0,\"y\":0}}]'"
echo ""
echo "🔍 View logs with: oc logs -f dc/message-in-bottle-api"
echo "🗑️  Delete deployment with: oc delete project $PROJECT_NAME" 