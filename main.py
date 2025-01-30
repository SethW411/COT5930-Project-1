import os
from flask import Flask, request, render_template, redirect, send_file
from google.cloud import storage

# 1. Flask Hello World
app = Flask(__name__)

@app.route('/hello')
def hello_world():
    """Return a basic hello world response."""
    return "Hello, World!"

# 2. Add other Flask endpoints
@app.route('/')
def index():
    """Display the upload form and list uploaded images from Cloud Storage."""

    # Fetch image URLs from Cloud Storage
    image_urls = get_image_urls()

    # Upload form HTML
    index_html = """
    <form method="post" enctype="multipart/form-data" action="/upload">
        <div>
            <label for="file">Choose file to upload</label>
            <input type="file" id="file" name="form_file" accept="image/jpeg"/>
        </div>
        <div>
            <button>Submit</button>
        </div>
    </form>
    <h2>Uploaded Images</h2>
    <ul>
    """

    # 7. Loop through images and add them to the HTML
    for url in image_urls:
        index_html += f'<li><img src="{url}" alt="Uploaded Image" width="200"></li>'

    index_html += "</ul>"
    return index_html

# 8. Handle image upload
@app.route("/upload", methods=["POST"])
def upload():
    """Handles the image upload."""
    if "form_file" not in request.files:
        return "No file uploaded", 400
    
    file = request.files["form_file"]

    if file.filename == "":
        return "No selected file", 400

    # Upload to Google Cloud Storage and get the public URL
    public_url = upload_to_gcs(BUCKET_NAME, file)

    return redirect("/")

# 9 & 10. List uploaded image files from Cloud Storage
@app.route('/files')
def list_files():
    """Lists uploaded image files from Google Cloud Storage."""
    return get_image_urls()

# Cloud Storage Configuration
storage_client = storage.Client()
BUCKET_NAME = 'flask-image-storage'

def upload_to_gcs(bucket_name, file):
    """Upload file to Google Cloud Storage."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file.filename)

    # Move the file stream pointer to the beginning
    file.seek(0)

    # Upload file
    blob.upload_from_file(file)

    # Make the file publicly accessible
    blob.make_public()
    return blob.public_url  # Return the public URL of the uploaded file

def get_image_urls():
    """Fetch URLs of all uploaded images from Google Cloud Storage."""
    bucket = storage_client.bucket(BUCKET_NAME)
    blobs = bucket.list_blobs()
    
    urls = [blob.public_url for blob in blobs]  # Get public URLs
    return urls

# 11. Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

