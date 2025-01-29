from flask import Flask, request, render_template, redirect
from google.cloud import storage
import os

app = Flask(__name__)

# Configuring google cloud storage
BUCKET_NAME = 'flask-image-storage'


@app.route('/')
def index():
    """Display the upload form and list uploaded images."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blobs = bucket.list_blobs()

    image_urls = [blob.public_url for blob in blobs]

    return render_template('index.html', images=image_urls)

@app.route("/upload", methods=["POST"])

def upload():
    """Handles the image upload."""
    if "file" not in request.files:
        return "No file uploaded", 400
    
    file = request.files["file"]

    if file.filename == "":
        return "No selectedd file", 400
        
    # Upload to Google Cloud Storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(file.filename)
    blob.upload_from_file(file)

    # Make the file publicly accessible
    blob.make_public()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)