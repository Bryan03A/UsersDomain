from flask import Flask, jsonify
from sqlalchemy import text
from config.config import Config
from models.user_model import db
from routes.auth_routes import auth_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
app.register_blueprint(auth_bp)

@app.route('/auth/health')
def health():
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.route('/test-db')
def test_db():
    try:
        result = db.session.execute(text("SELECT NOW()")).fetchone()
        return jsonify({"message": "Successful connection", "timestamp": str(result[0])})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)