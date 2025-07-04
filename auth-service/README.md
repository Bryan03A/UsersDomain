# Authentication Microservice - Flask (JWT + PostgreSQL)

## Description
This microservice handles basic authentication operations including login and profile retrieval using JWTs. It also exposes health check and database diagnostics endpoints. It follows the **KISS (Keep It Simple, Stupid)** architecture principle to ensure maintainability and simplicity.

## Features
- JWT-based authentication
- PostgreSQL integration via SQLAlchemy
- Password hashing with PBKDF2
- Health check endpoint for load balancers
- CORS ready (commented but pre-configured)

## Endpoints

| Endpoint     | Method | Description                                       |
|--------------|--------|---------------------------------------------------|
| /health      | GET    | Load balancer health check (DB ping)             |
| /test-db     | GET    | Manual DB connection test (returns timestamp)    |
| /login       | POST   | Login with username/email + password, returns JWT|
| /profile     | GET    | Returns current user's profile info via JWT      |


## Architecture: KISS
This service is built using a minimalist architecture, ensuring that each component has a single responsibility:

- **Flask**: Simple web framework with minimal setup.
- **SQLAlchemy**: ORM used only where necessary (e.g., `User` model).
- **JWT**: Used for stateless user sessions.
- **Environment Variables**: Handled by `dotenv` for secure config management.
- **Password Hashing**: PBKDF2 used directly with `hashlib` to avoid external dependencies.

This approach makes the service easy to understand, maintain, and deploy.

## Dependencies
- Flask
- Flask-CORS
- Flask-SQLAlchemy
- python-dotenv
- PyJWT
- PostgreSQL

## External Connections Diagram

```
                      ┌──────────────┐        JWT      ┌──────────────┐
                      │  Frontend /  │◄───────────────►│   Flask App  │
                      │   Client     │                 └──────┬───────┘
                      └──────────────┘                        │
                                                              │ DB URI
                                                        ┌─────▼──────┐
                                                        │ PostgreSQL │
                                                        └────────────┘
```

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Used to sign JWT tokens
- `SQLALCHEMY_TRACK_MODIFICATIONS`: Optional, set to `False` by default

## Running the Service
```bash
pip install -r requirements.txt
python app.py
```

## Recommendations
- In production, run behind a WSGI server like Gunicorn
- Use HTTPS and random per-user salts for secure password hashing
- Secure environment variables using a secrets manager (AWS Secrets Manager, Vault, etc.)

---
