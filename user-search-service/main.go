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

var db *sql.DB

// User structure
type User struct {
	ID       string `json:"id"`
	Username string `json:"username"`
}

// Initialize PostgreSQL connection using environment variables
func initDB() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("❌ Failed to load .env file")
	}

	host := os.Getenv("POSTGRESQL_HOST")
	portStr := os.Getenv("POSTGRESQL_PORT")
	user := os.Getenv("POSTGRESQL_USER")
	password := os.Getenv("POSTGRESQL_PASSWORD")
	dbname := os.Getenv("POSTGRESQL_DATABASE")

	port, err := strconv.Atoi(portStr)
	if err != nil {
		log.Fatal("Invalid port:", err)
	}

	connStr := fmt.Sprintf(
		"host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
		host, port, user, password, dbname,
	)

	db, err = sql.Open("postgres", connStr)
	if err != nil {
		log.Fatal("Database connection failed:", err)
	}

	err = db.Ping()
	if err != nil {
		log.Fatal("Database ping failed:", err)
	}

	fmt.Println("✅ Successfully connected to PostgreSQL")
}

// SOAP-style GET endpoint to search user by username
func getUserByUsernameSOAP(w http.ResponseWriter, r *http.Request) {
	username := r.URL.Query().Get("username")
	if username == "" {
		http.Error(w, "Username is required", http.StatusBadRequest)
		return
	}

	var user User
	err := db.QueryRow("SELECT id, username FROM \"user\" WHERE username = $1", username).Scan(&user.ID, &user.Username)
	if err != nil {
		http.Error(w, fmt.Sprintf("Database query error: %s", err), http.StatusInternalServerError)
		return
	}

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

	w.Header().Set("Content-Type", "text/xml")
	w.Write([]byte(soapResponse))
}

// Health check endpoint
func healthCheck(w http.ResponseWriter, r *http.Request) {
	err := db.Ping()
	if err != nil {
		http.Error(w, "❌ Unhealthy", http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("✅ Healthy"))
}

func main() {
	initDB()

	r := mux.NewRouter()
	r.HandleFunc("/user/soap", getUserByUsernameSOAP).Methods("GET")
	r.HandleFunc("/health", healthCheck).Methods("GET")

	c := cors.New(cors.Options{
		AllowedOrigins:   []string{"http://3.227.120.143:8080"},
		AllowedMethods:   []string{"GET", "POST"},
		AllowedHeaders:   []string{"Content-Type"},
		AllowCredentials: true,
	})

	handler := c.Handler(r)

	fmt.Println("🚀 SOAP service started on port 5016...")
	log.Fatal(http.ListenAndServe("0.0.0.0:5016", handler))
}
