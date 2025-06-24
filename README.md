# Message in a Bottle API

A FastAPI application that processes bottles with characters and coordinates to reveal hidden messages.

## Features

- POST `/collect-bottles` - Process bottles and reveal hidden messages
- GET `/` - Health check endpoint
- GET `/health` - Health check endpoint

## Local Development

### Prerequisites

- Python 3.11+
- pip

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:8080`

## Docker Deployment

### Build the Docker image

```bash
docker build -t message-in-bottle-api .
```

### Run the container

```bash
docker run -p 8080:8080 message-in-bottle-api
```

## OpenShift Deployment

### Using the OpenShift CLI (oc)

1. Login to your OpenShift cluster:
   ```bash
   oc login --token=<your-token> --server=<your-server>
   ```

2. Create a new project (if needed):
   ```bash
   oc new-project message-in-bottle
   ```

3. Build and deploy the application:
   ```bash
   oc new-app --name message-in-bottle-api --strategy=docker .
   ```

4. Expose the service:
   ```bash
   oc expose svc/message-in-bottle-api
   ```

5. Get the route URL:
   ```bash
   oc get route message-in-bottle-api
   ```

### Using the OpenShift Web Console

1. Navigate to your OpenShift web console
2. Create a new project
3. Go to "Developer" → "Add" → "From Git"
4. Enter your Git repository URL
5. Select "Dockerfile" as the build strategy
6. Deploy the application

## API Usage

### POST /collect-bottles

Process bottles with characters and coordinates to reveal the hidden message.

**Request Body:**
```json
[
  {
    "character": "H",
    "coordinates": {
      "x": 0,
      "y": 1
    }
  },
  {
    "character": "$",
    "coordinates": {
      "x": 12,
      "y": 5
    }
  }
]
```

**Response:**
```json
{
  "message": "The revealed message on the grid",
  "grid_dimensions": {
    "width": 13,
    "height": 6
  },
  "bottles_processed": 2
}
```

## Testing

You can test the API using curl:

```bash
curl -X POST "https://your-openshift-route/collect-bottles" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "character": "H",
      "coordinates": {
        "x": 0,
        "y": 1
      }
    },
    {
      "character": "$",
      "coordinates": {
        "x": 12,
        "y": 5
      }
    }
  ]'
```

## Health Checks

The application includes health check endpoints:

- `GET /` - Returns a simple status message
- `GET /health` - Returns health status

These endpoints can be used for OpenShift health checks and load balancer health monitoring. 