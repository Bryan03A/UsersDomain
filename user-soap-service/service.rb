require 'sinatra'
require 'nokogiri'
require 'pg'
require 'dotenv'
require 'openssl'
require 'securerandom'
require 'sinatra/cross_origin'

# Enable Cross-Origin Requests (CORS)
configure do
  enable :cross_origin
end

# Preflight request configuration
options '*' do
  allowed_origin = 'http://3.227.120.143:8080'
  origin = request.env['HTTP_ORIGIN']

  if origin == allowed_origin
    response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Vary'] = 'Origin'
  end

  response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
  response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
  200
end

# Load environment variables
Dotenv.load

# Initialize PostgreSQL connection
DB = PG.connect(
  dbname: ENV['POSTGRESQL_DATABASE'],
  host: ENV['POSTGRESQL_HOST'],
  port: ENV['POSTGRESQL_PORT'],
  user: ENV['POSTGRESQL_USER'],
  password: ENV['POSTGRESQL_PASSWORD']
)

# Create users table if it doesn't exist
def create_table
  query = <<-SQL
    CREATE TABLE IF NOT EXISTS "user" (
      id UUID PRIMARY KEY,
      username VARCHAR(80) UNIQUE NOT NULL,
      password VARCHAR(200) NOT NULL,
      first_name VARCHAR(100) NOT NULL,
      last_name VARCHAR(100) NOT NULL,
      dni VARCHAR(20) UNIQUE NOT NULL,
      email VARCHAR(120) UNIQUE NOT NULL,
      city VARCHAR(100) NOT NULL
    );
  SQL

  DB.exec(query)
end

# Store user data in the database
def store_user(username, hashed_password, first_name, last_name, dni, email, city)
  user_id = SecureRandom.uuid
  query = <<-SQL
    INSERT INTO "user" (id, username, password, first_name, last_name, dni, email, city)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
    RETURNING id;
  SQL
  result = DB.exec_params(query, [user_id, username, hashed_password, first_name, last_name, dni, email, city])
  result[0]['id']
end

# Hash password using PBKDF2-HMAC-SHA256
def hash_password(password)
  salt = 'salt' # In production, use a unique random salt per user
  iterations = 1000
  key_length = 64
  hashed = OpenSSL::PKCS5.pbkdf2_hmac(password, salt, iterations, key_length, 'sha256')
  hashed.unpack1('H*')
end

# Health check endpoint for Load Balancer
get '/health' do
  begin
    DB.exec("SELECT 1")
    status 200
    "Service is healthy"
  rescue => e
    status 500
    "Database connection failed: #{e.message}"
  end
end

# SOAP-based user registration endpoint
post '/register' do
  request.body.rewind
  payload = request.body.read

  return "No SOAP request body found." if payload.empty?

  begin
    doc = Nokogiri::XML(payload)
    ns = { 'user' => 'http://example.com/user' }

    username = doc.xpath('//user:username', ns).text.strip
    password = doc.xpath('//user:password', ns).text.strip
    first_name = doc.xpath('//user:first_name', ns).text.strip
    last_name = doc.xpath('//user:last_name', ns).text.strip
    dni = doc.xpath('//user:dni', ns).text.strip
    email = doc.xpath('//user:email', ns).text.strip
    city = doc.xpath('//user:city', ns).text.strip

    hashed_password = hash_password(password)
    user_id = store_user(username, hashed_password, first_name, last_name, dni, email, city)

    content_type :xml
    "<soapenv:Envelope xmlns:soapenv='http://schemas.xmlsoap.org/soap/envelope/' xmlns:us='http://example.com/userservice'>
      <soapenv:Header/>
      <soapenv:Body>
        <us:registerUserResponse>
          <us:message>User registered successfully</us:message>
          <us:id>#{user_id}</us:id>
        </us:registerUserResponse>
      </soapenv:Body>
    </soapenv:Envelope>"
  rescue => e
    status 500
    "Error processing SOAP request: #{e.message}"
  end
end

# Initialize the users table
create_table

# Start the Sinatra server
set :bind, '0.0.0.0'
set :port, 5002
puts "🚀 User SOAP service is running on port 5002..."