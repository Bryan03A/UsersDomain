from flask import Flask, request, jsonify
import boto3
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://3.227.120.143:8080", "*"])

# Configuration MinIO  🚀
s3 = boto3.client('s3',
    endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

def create_bucket_if_not_exists(bucket_name):
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' already exists.")
    except Exception:
        s3.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' created.")

create_bucket_if_not_exists(BUCKET_NAME)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    file = request.files['file']
    filename = secure_filename(file.filename)
    
    try:
        s3.upload_fileobj(file, BUCKET_NAME, filename, ExtraArgs={'ACL': 'public-read'})
        
        url = f"{os.getenv('AWS_ENDPOINT_URL')}/{BUCKET_NAME}/{filename}"
        return jsonify({"message": "Image uploaded successfully", "url": url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/list_images', methods=['GET'])
def list_images():
    try:
        objects = s3.list_objects_v2(Bucket=BUCKET_NAME).get("Contents", [])
        urls = [f"{os.getenv('AWS_ENDPOINT_URL')}/{BUCKET_NAME}/{obj['Key']}" for obj in objects]
        return jsonify({"urls": urls})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5015)