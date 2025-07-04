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

- **🧠 Purpose**: Handles user authentication and profile access.
- **🧪 Port**: `5001`
- **🧰 Tech Stack**:
  - Language: Python
  - Framework: Flask
  - DB: PostgreSQL (AWS RDS)
- **🔐 Security**:
  - Password hashing with PBKDF2
  - JWT-based stateless authentication
- **📡 Communication**: REST (JSON)
- **🌍 Endpoints**:
  - `POST /login`
  - `GET /profile`
  - `GET /test-db`
  - `GET /health`
- **🎨 Design Pattern**: `KISS` (Keep It Simple)
- **🛠️ Notes**:
  - Supports CORS
  - Stateless design makes it scalable

---

## 2️⃣ **User SOAP Service** (Ruby / Sinatra)

- **🧠 Purpose**: Registers users via SOAP for legacy compatibility.
- **🧪 Port**: `5002`
- **🧰 Tech Stack**:
  - Language: Ruby
  - Framework: Sinatra
  - DB: PostgreSQL
- **🔐 Security**:
  - Passwords hashed with PBKDF2
- **📡 Communication**: SOAP (XML)
- **🌍 Endpoints**:
  - `POST /register`
  - `GET /health`
- **🎨 Design Pattern**: `SOLID` (separation of concerns)
- **🛠️ Notes**:
  - SOAP XML parsed with Nokogiri
  - Good for enterprise or older integrations

---

## 3️⃣ **Session Service** (Node.js / Express)

- **🧠 Purpose**: Manages session lifecycle (create, update, retrieve).
- **🧪 Ports**: `5020` (main), `5004` (subroutes)
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

---

## 4️⃣ **gRPC Image Delivery Service** (Python / Flask + gRPC)

- **🧠 Purpose**: Uploads and lists images using efficient binary protocol.
- **🧪 Port**: `5015`
- **🧰 Tech Stack**:
  - Language: Python
  - Framework: Flask + gRPC
  - Storage: MinIO (S3-compatible)
- **🔐 Security**:
  - Uploads are sanitized
  - Files are public-read via ACL
- **📡 Communication**: gRPC (Protocol Buffers)
- **📦 Methods**:
  - `uploadImage(file)`
  - `listImages()`
- **🎨 Design Pattern**: `POLA` (Principle of Least Astonishment)
- **🛠️ Notes**:
  - Scalable and optimized for internal service communication

---

## 5️⃣ **User Lookup SOAP (Go)**

- **🧠 Purpose**: Exposes SOAP-based lookup for usernames (useful for legacy).
- **🧪 Port**: `5016`
- **🧰 Tech Stack**:
  - Language: Go
  - Framework: net/http + Gorilla Mux
  - DB: PostgreSQL (Supabase)
- **🔐 Security**:
  - Strict CORS enforcement
- **📡 Communication**: SOAP (manually generated XML)
- **🌍 Endpoints**:
  - `GET /user/soap?username=...`
  - `GET /health`
- **🎨 Design Pattern**: `KISS`
- **🛠️ Notes**:
  - Ultra-lightweight and performant
  - Manual SOAP gives low-level control

---

## 6️⃣ **Session Tracker (Lightweight)**

- **🧠 Purpose**: Exposes last session time via unified endpoint (light version).
- **🧪 Port**: `5020`
- **🧰 Tech Stack**:
  - Language: Node.js
  - Framework: Express
  - DBs: PostgreSQL + MongoDB
- **📡 Communication**: REST
- **🌍 Endpoints**:
  - `GET /last-connection`
  - `GET /connected/health`
- **🎨 Design Principles**:
  - `KISS`: Lightweight, flat structure
  - `DRY`: Reused error handler
- **🛠️ Notes**:
  - Ideal for fast read-only access
  - Health checks included for load balancing

---
