# Session Tracking Service - Node.js + MongoDB

## Description
This microservice is responsible for managing and storing user session data. It is built using Express.js and MongoDB and provides a dedicated route group for session-related endpoints. It also exposes a health check endpoint for orchestration tools.
 
## Features
- Connects to MongoDB to persist user sessions
- Loads environment variables from `.env` for configuration
- Middleware support for JSON parsing and authentication
- Modular route management using Express Router
- Health check endpoint to validate availability
- CORS configuration placeholder for frontend interaction

## Endpoints
| Endpoint              | Method | Description                          |
|-----------------------|--------|--------------------------------------|
| /api/sessions         | GET/POST/... | Handled in routes/sessions.js       |
| /session/health       | GET    | Simple status response               |

## Architecture Style
The service follows a **KISS (Keep It Simple, Stupid)** design principle. It is intentionally straightforward, using built-in middleware, organized route imports, and a flat structure.
 
### 📌 Why KISS is the Most Applicable Design Principle
The **KISS** principle fits this service perfectly due to its clarity and focus on essential responsibilities.
 
#### ✅ Justification:
1. **Clean routing structure**:
   - Session routes are offloaded to a separate module
2. **Minimal logic in `app.js`**:
   - Only connection setup and middleware
3. **Sensible defaults and fallback behavior**:
   - `.env` validation with early exit
4. **Lightweight and extensible**:
   - Easily scalable with more middleware or services if needed
 
#### ℹ️ Other Principles Present:
- **YAGNI**: Implements only necessary features
- **POLA**: Behavior aligns with common expectations (e.g., 200 OK on health)
 
## Communication Type
- **RESTful API** with JSON payloads
- Accessed via Express Router under `/api/sessions`
 
## External Communication Diagram
```
                    ┌────────────┐     REST/API     ┌────────────────────┐
                    │  Frontend  │◄────────────────►│  Session Service   │
                    └────────────┘                  └────────┬───────────┘
                                                             │
                                                     ┌───────▼────────┐
                                                     │   MongoDB      │
                                                     └────────────────┘
```

## Environment Variables
- `PORT`: Port the server listens on
- `MONGO_URI`: Connection string for MongoDB

## Running the Service
```bash
npm install
node app.js
```

## Best Practices Followed
- Early validation of required environment variables
- Modular route design for scalability
- Minimal setup with clear responsibilities
- Health-check endpoint for container orchestration

---
