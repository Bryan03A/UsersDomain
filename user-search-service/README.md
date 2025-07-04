# Service Overview: User SOAP Microservice
 
This microservice is designed to provide user information through a SOAP-style HTTP GET endpoint. It connects to a PostgreSQL database to retrieve user data by username and exposes a health check endpoint to monitor service status. The service uses Gorilla Mux for routing and supports CORS for a specific frontend origin. 

## Architectural Style

The architecture of this service follows a **Microservices** pattern, focusing on a single responsibility — user information retrieval. The communication style is **SOAP over HTTP**, which is somewhat uncommon in modern microservices but suits legacy systems or strict contract-based communication.

The service operates as a stateless RESTful HTTP server with SOAP messaging format, making it interoperable with systems expecting XML-based SOAP envelopes.

## Communication Type

- **Request/Response (Synchronous communication)**: The client sends a request with a username parameter and waits for the XML SOAP response with user details.
- **HTTP/1.1 protocol**: Transport layer for SOAP messages.
  
## Endpoints

| Endpoint           | Method | Description                         | Response Content-Type  |
|--------------------|--------|-----------------------------------|-----------------------|
| `/user/soap`       | GET    | Retrieves user data by username via SOAP response | `text/xml`            |
| `/user-search/health` | GET    | Health check endpoint, returns service status      | `text/plain` (text)   |

## Key Components Explained

- **Database Initialization (`initDB`)**: Loads environment variables for PostgreSQL config, opens connection, and verifies connectivity.
- **User struct**: Defines the user data structure returned by the service (ID and Username).
- **`getUserByUsernameSOAP` Handler**: Reads `username` query param, queries the DB, formats a SOAP XML response, and sends it back.
- **`healthCheck` Handler**: Simple DB ping test to ensure the service and DB connection are alive.
- **CORS configuration**: Allows cross-origin requests only from the specified frontend URL with GET and POST methods.

## Console Diagram of Communication Flow

```text
+-------------+          HTTP GET /user/soap?username={username}          +---------------+
|  Client     | --------------------------------------------------------->|  User SOAP    |
| (Frontend)  |                                                           |  Microservice |
+-------------+                                                           +------+--------+
                                                                                 |
                                                                                 | Query DB for user by username
                                                                                 |
                                                                          +------+------+
                                                                          | PostgreSQL  |
                                                                          +-------------+
                                                                                 |
                                                                                 | Returns user info (id, username)
                                                                                 |
+-------------+ <---------------------------------------------------------+------+--------+
|  Client     |             SOAP XML response with user info              |  User SOAP    |
| (Frontend)  |                                                           |  Microservice |
+-------------+                                                           +---------------+

+-------------+          HTTP GET /user-search/health            +---------------+
|  Health     | ------------------------------------------------>|  User SOAP    |
|  Monitor    |                                                  |  Microservice |
+-------------+                                                  +-------+-------+
                                                                         |
                                                                         | DB ping check
                                                                         |
                                                                  +------+------+
                                                                  | PostgreSQL  |
                                                                  +------+------+
                                                                         |
                                                                         | Returns OK / Error
                                                                         |
+-------------+ <-------------------------------------------------+------+--------+
|  Health     |          "✅ Healthy" or "❌ Unhealthy"          |  User SOAP    |
|  Monitor    |                                                   |  Microservice |
+-------------+                                                   +---------------+
``` 

## Summary
 
This microservice is a specialized, SOAP-based user information provider built with Go, connecting securely to PostgreSQL. It uses synchronous HTTP communication with SOAP XML responses and enforces CORS for a specific frontend origin. The architecture is simple, modular, and focused, adhering to microservice principles with clear separation of concerns and health monitoring.
