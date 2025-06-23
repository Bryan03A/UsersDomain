package main

import (
	"database/sql"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"

	"github.com/gorilla/mux"
	"github.com/joho/godotenv"
	_ "github.com/lib/pq"
	"github.com/rs/cors"
)

// PostgreSQL database configuration constants
const (
	POSTGRESQL_HOST     = "aws-0-us-west-1.pooler.supabase.com"
	POSTGRESQL_PORT     = 6543
	POSTGRESQL_DATABASE = "postgres"
	POSTGRESQL_USER     = "postgres.imfqyzgimtercyyqeqof"
	POSTGRESQL_PASSWORD = "1997Guallaba"
)

var db *sql.DB

// User struct represents a user entity
type User struct {
	ID       string `json:"id"`
	Username string `json:"username"`
}

// Initialize the database from environment variables
func initDB() {
	// Load variables from .env file
	err := godotenv.Load()
	if err != nil {
		log.Fatal("❌ Error loading .env file")
	}

	// Read environment variables
	host := os.Getenv("POSTGRESQL_HOST")
	portStr := os.Getenv("POSTGRESQL_PORT")
	user := os.Getenv("POSTGRESQL_USER")
	password := os.Getenv("POSTGRESQL_PASSWORD")
	dbname := os.Getenv("POSTGRESQL_DATABASE")

	// Convert port to integer
	port, err := strconv.Atoi(portStr)
	if err != nil {
		log.Fatal("Invalid port:", err)
	}

	// Create connection string
	connStr := fmt.Sprintf(
		"host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
		host, port, user, password, dbname,
	)

	// Connect to the database
	db, err = sql.Open("postgres", connStr)
	if err != nil {
		log.Fatal("Error connecting to the database:", err)
	}

	err = db.Ping()
	if err != nil {
		log.Fatal("Error pinging the database:", err)
	}

	fmt.Println("✅ Successfully connected to PostgreSQL")
}

// SOAP function that fetches a user by username
func getUserByUsernameSOAP(w http.ResponseWriter, r *http.Request) {
	// Get username from SOAP request
	username := r.URL.Query().Get("username")
	if username == "" {
		http.Error(w, "Username is required", http.StatusBadRequest)
		return
	}

	// Query the database
	var user User
	err := db.QueryRow("SELECT id, username FROM \"user\" WHERE username = $1", username).Scan(&user.ID, &user.Username)
	if err != nil {
		http.Error(w, fmt.Sprintf("Database query error: %s", err), http.StatusInternalServerError)
		return
	}

	// Create SOAP response message
	soapResponse := fmt.Sprintf(`
		<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
			xmlns:web="http://www.example.org/webservice">
			<soapenv:Header/>
			<soapenv:Body>
				<web:getUserByUsernameResponse>
					<web:id>%s</web:id>
					<web:username>%s</web:username>
				</web:getUserByUsernameResponse>
			</soapenv:Body>
		</soapenv:Envelope>
	`, user.ID, user.Username)

	// Set response header as XML
	w.Header().Set("Content-Type", "text/xml")
	w.Write([]byte(soapResponse))
}

func main() {
	// Initialize the database
	initDB()

	// Create a router for the SOAP server
	r := mux.NewRouter()

	// Route to get a user by username
	r.HandleFunc("/user/soap", getUserByUsernameSOAP).Methods("GET")

	// Configure CORS
	c := cors.New(cors.Options{
		AllowedOrigins:   []string{"http://3.212.132.24:8080"}, // Allowed origin (frontend server)
		AllowedMethods:   []string{"GET", "POST"},
		AllowedHeaders:   []string{"Content-Type"},
		AllowCredentials: true,
	})

	// Apply CORS to routes
	handler := c.Handler(r)

	// Start HTTP server on all interfaces
	fmt.Println("Starting SOAP server on port 5016...")
	log.Fatal(http.ListenAndServe("0.0.0.0:5016", handler))
}
