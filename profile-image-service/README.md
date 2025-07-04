# Image Upload Service - Flask + MinIO (S3-compatible)

## Description
This microservice enables uploading and listing of images using Flask and an S3-compatible object storage like MinIO or AWS S3. It supports a health check endpoint for load balancers and can be configured via environment variables.

## Features
- Upload images to MinIO/S3-compatible storage
- List all uploaded images with public URLs
- Automatically create the bucket if it doesn’t exist
- REST API endpoints for integration with frontend or other services
- Health check endpoint for ALB/NLB readiness
- Built with environment-based configuration using `dotenv`
- CORS-ready setup for frontend access
- You can access the database client by entering the URL http://54.152.105.240:9001

## Endpoints
| Endpoint                 | Method | Description                                      |
|--------------------------|--------|--------------------------------------------------|
| /upload_image            | POST   | Uploads an image to the object storage           |
| /list_images             | GET    | Returns public URLs of all stored images         |
| /profile-image/health    | GET    | Verifies connection to object storage            |

## Architecture Style
The service follows a **KISS (Keep It Simple, Stupid)** architecture style. Its logic is straightforward and concise, avoiding unnecessary abstraction. The service focuses strictly on its core functionality: image handling.

### 📌 Why KISS is the Most Applicable Design Principle
The **KISS (Keep It Simple, Stupid)** principle best fits this service due to its focus on simplicity and clarity.

#### ✅ Justification:
1. **Minimal logic per endpoint**:
   - Each route does one thing: upload, list, or health check.
2. **Clear configuration**:
   - All operational details (bucket name, access keys, endpoint URL) come from environment variables.
3. **No overengineering**:
   - No use of classes, layers, or additional frameworks.
4. **Easy extensibility**:
   - New endpoints or validations can be added without breaking existing logic.

## Communication Type
- **RESTful API** over HTTP using standard methods (`GET`, `POST`)
- Uses JSON as the response format
- Accepts multipart/form-data for image uploads

## External Communication Diagram
```
                            ┌────────────┐     REST/API     ┌────────────────────┐
                            │  Frontend  │◄────────────────►│  Image Service     │
                            └────────────┘                  └────────┬───────────┘
                                                                     │
                                                               ┌─────▼──────┐
                                                               │  MinIO/S3  │
                                                               └────────────┘
```

## Environment Variables
- `AWS_ENDPOINT_URL`: MinIO/S3 endpoint (e.g., http://54.152.105.240:9000)
- `AWS_ACCESS_KEY_ID`: Your object storage access key
- `AWS_SECRET_ACCESS_KEY`: Your secret key
- `AWS_REGION`: Region (can be any string for MinIO)
- `AWS_BUCKET_NAME`: Bucket to upload files to

## Running the Service
```bash
pip install -r requirements.txt
python app.py
```

## Best Practices Followed
- Load balancer health check endpoint
- Defensive programming with error handling
- Secure file upload handling (`secure_filename`)
- Modular setup for switching between AWS S3 or MinIO
  
---
