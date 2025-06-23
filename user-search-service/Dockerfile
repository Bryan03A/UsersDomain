# Use a Go base image
FROM golang:1.24-alpine

# Set working directory inside the container
WORKDIR /app

# Copy project files to the container
COPY go.mod go.sum ./
RUN go mod download

# Copy source code to the container
COPY . .

# Expose the port where the service runs
EXPOSE 5016

# Command to start the application
CMD ["go", "run", "main.go"]