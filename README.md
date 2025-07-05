# 🧭 Microservices Architecture Overview

This document provides a high-level overview of each microservice in the system.

## 📌 Includes:
- 🎯 Purpose
- 💻 Language & Framework
- 🔌 Communication Style
- 🛢️ Database/Storage
- 🔐 Security Notes
- 🎨 Design Pattern
- 🔍 Endpoints
- ⚙️ Configuration Details

---

## 1️⃣ **Auth Service** (Python / Flask)
- **🧠 Purpose**: Handles user authentication and profile access, and emits events for an event-driven architecture.
- **🧪 Port**: `5001`
- **🧰 Tech Stack**:
- &nbsp; - Language: Python
- &nbsp; - Framework: Flask
- &nbsp; - DB: PostgreSQL (AWS Instance)
- &nbsp; - Messaging: RabbitMQ for event-driven communication
- **🛢️ Database**:
- &nbsp; - Type: Relational
- &nbsp; - Engine: PostgreSQL
- &nbsp; - Hosted on AWS RDS
- **🔐 Security**:
- &nbsp; - Password hashing with PBKDF2-HMAC-SHA256
- &nbsp; - JWT-based stateless authentication (tokens expire after 1 hour)
- **📡 Communication**: REST (JSON) + Event-Driven (RabbitMQ)
- &nbsp; - Emits events on the `auth-events` queue in RabbitMQ
- **🌍 Endpoints**:
- &nbsp; - `POST /login`
- &nbsp; - `GET /profile`
- &nbsp; - `GET /test-db`
- &nbsp; - `GET /auth/health`
- &nbsp; - `GET /test-event` (publishes test event to RabbitMQ)
- **📬 Event-Driven Messaging**:
- &nbsp; - Queue: `auth-events`
- &nbsp; - Example events: `UserLoggedIn`, `TestEvent`
- &nbsp; - RabbitMQ broker host: `52.5.219.178`, port `5672`
- **🎨 Design Pattern**: `KISS` (Keep It Simple)
- **🛠️ Notes**:
- &nbsp; - Supports CORS
- &nbsp; - Stateless design enables easy scalability

---

## 2️⃣ **User SOAP Service** (Ruby / Sinatra)
- **🧠 Purpose**: Registers users via SOAP for legacy compatibility, and publishes events to RabbitMQ for event-driven workflows.
- **🧪 Port**: `5002`
- **🧰 Tech Stack**:
- &nbsp; - Language: Ruby
- &nbsp; - Framework: Sinatra
- &nbsp; - DB: PostgreSQL
- &nbsp; - Messaging: RabbitMQ for event publishing
- **🛢️ Database**:
- &nbsp; - Type: Relational
- &nbsp; - Engine: PostgreSQL
- **🔐 Security**:
- &nbsp; - Passwords hashed with PBKDF2-HMAC-SHA256
- **📡 Communication**: SOAP (XML) + Event-Driven (RabbitMQ)
- &nbsp; - Emits events on the `user-events` queue in RabbitMQ
- **🌍 Endpoints**:
- &nbsp; - `POST /register` (SOAP endpoint for user registration)
- &nbsp; - `GET /user-soap/health`
- **📬 Event-Driven Messaging**:
- &nbsp; - Queue: `user-events`
- &nbsp; - Example event: `UserRegistered`
- &nbsp; - RabbitMQ broker configured via environment variables (`RABBITMQ_HOST`, `RABBITMQ_PORT`, `RABBITMQ_QUEUE`)
- **🎨 Design Pattern**: `KISS` (Keep It Simple)
- **🛠️ Notes**:
- &nbsp; - Supports CORS
- &nbsp; - Parses SOAP XML with Nokogiri
- &nbsp; - Suitable for enterprise or legacy system integrations

---

## 3️⃣ **Session Service** (Node.js / Express)

- **🧠 Purpose**: Manages session lifecycle (create, update, retrieve).
- **🧪 Ports**: `5004`
- **🧰 Tech Stack**:
  - Language: JavaScript
  - Framework: Express
  - DBs: PostgreSQL + MongoDB
- **🔐 Security**:
  - JWT token middleware
- **📡 Communication**: REST (JSON)
- **🌍 Endpoints**:
  - `GET /last-connection`
  - `POST /api/sessions`
  - `GET /api/sessions/:userId`
  - `PUT /api/sessions/:userId`
  - `DELETE /api/sessions/:userId`
  - `GET /api/sessions/verify`
  - `GET /health`
- **🎨 Design Pattern**: `DRY` + `Modular`
- **🛠️ Notes**:
  - Controllers, routes, and middlewares split
  - Supports both SQL and NoSQL
  - Event-driven: publishes and consumes events via RabbitMQ (queues and topics configurable)

---

## 4️⃣ **Image Delivery Service** (Python / Flask)

- **🧠 Purpose**: Uploads and lists images using an efficient binary protocol.
- **🧪 Port**: `5015`
- **🧰 Tech Stack**:
  - Language: Python
  - Framework: Flask + REST
  - Storage: MinIO (S3-compatible object storage)
- **🔐 Security**:
  - Uploads sanitized using `secure_filename`
  - Uploaded files are public-read via ACL
- **📡 Communication**: REST
- **📦 Methods**:
  - `uploadImage(file)`
  - `listImages()`
- **🎨 Design Pattern**: `POLA` (Principle of Least Astonishment)
  - Clear and minimal API surface for expected behavior
  - Stateless service relying on external object storage
  - No hidden complexity or side effects
- **🛠️ Notes**:
  - Scalable and optimized for internal service communication
  - Uses object storage (MinIO) instead of traditional databases
  - No relational or NoSQL database involved; data persistence is through object storage (blob store)
  - Stateless service; relies on external storage for data

---

## 5️⃣ **User Lookup SOAP Service** (Go / net/http + Gorilla Mux)

- **🧠 Purpose**: Exposes SOAP-based lookup for usernames (useful for legacy).
- **🧪 Port**: `5016`
- **🧰 Tech Stack**:
  - Language: Go
  - Framework: net/http + Gorilla Mux
- **🛢️ Database**:
  - DB: PostgreSQL (EC2)
  - Relational PostgreSQL database.
  - Stores user `id` and `username`.
  - Accessed via raw SQL queries.
- **🔐 Security**:
  - Strict CORS enforcement allowing only `http://3.227.120.143:8080`
- **📡 Communication**: SOAP (manually generated XML)
- **🌍 Endpoints**:
  - `GET /user/soap?username=...`
  - `GET /user-search/health`
- **🎨 Design Pattern**: `KISS` (Keep It Simple, Stupid)
  - Simple and minimalistic KISS approach.
  - No complex frameworks, manual SOAP handling.
  - Focused on clarity, performance, and ease of maintenance.
- **🛠️ Notes**:
  - Ultra-lightweight and performant implementation
  - Manual SOAP XML generation offers low-level control and flexibility
  - Uses standard Go database/sql with PostgreSQL driver
  - Handles health checks via simple DB ping

---

## 6️⃣ **Connected Service** (Node.js / Express)

- **🧠 Purpose**: Manages user session lifecycle including creation, update, and retrieval of last connection.
- **🧪 Port**: `5020`
- **🧰 Tech Stack**:
  - Language: JavaScript
  - Framework: Express
  - DBs:
    - PostgreSQL (relational)
    - MongoDB (NoSQL document store)
- **🛢️ Database**:
  - PostgreSQL stores user data with relational schema.
  - MongoDB stores session documents with timestamps.
  - Combines SQL and NoSQL for efficient session tracking and user management.
- **🔐 Security**:
  - Supports CORS (configurable)
- **📡 Communication**: REST (JSON)
- **🌍 Endpoints**:
  - `GET /last-connection?username=...` — retrieves the last session time relative to now
  - `GET /connected/health` — health check for both DB connections
- **🎨 Design Pattern**: `DRY` + `Modular`
  - Separation of concerns: DB clients, schema definitions, error handling, and routing clearly modularized.
  - Uses async/await for clean asynchronous flow.
- **🛠️ Notes**:
  - Integrates two types of databases for complementary functionality.
  - Uses `moment` library for human-friendly timestamps.
  - Handles graceful error responses with helper function.
  - Health endpoint verifies connectivity to both databases.

---
