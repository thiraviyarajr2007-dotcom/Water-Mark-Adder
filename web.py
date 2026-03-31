from flask import Flask, request, send_file
import os
import threading

from worker import process_images
from zip_utils import zip_images

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_FOLDER = os.path.join(BASE_DIR, "input")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")

os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 🔥 STATUS VARIABLE
status = "idle"


# 🔧 BACKGROUND TASK
def background_task(text, angle, opacity):
    global status
    status = "processing"

    try:
        process_images(INPUT_FOLDER, OUTPUT_FOLDER, text, angle, opacity)
        zip_images(OUTPUT_FOLDER, "result.zip")
        status = "done"
        print("Processing Completed ✅")
    except Exception as e:
        status = "error"
        print("Error:", e)


# 🏠 HOME PAGE
@app.route('/')
def home():
    return '''
    <h2>Upload Images</h2>
    <form method="POST" action="/upload" enctype="multipart/form-data">
        
        <input type="file" name="images" multiple><br><br>

        <input type="text" name="text" placeholder="Watermark Text"><br><br>

        <input type="number" name="angle" placeholder="Angle (e.g 45)"><br><br>

        <input type="number" name="opacity" placeholder="Opacity (0-255)"><br><br>

        <button type="submit">Upload</button>
    </form>
    '''


# 📤 UPLOAD
@app.route('/upload', methods=['POST'])
def upload():
    global status

    files = request.files.getlist("images")
    text = request.form.get("text", "WATERMARK")
    angle = int(request.form.get("angle", 45))
    opacity = int(request.form.get("opacity", 80))

    # 🔥 Clear old files
    for f in os.listdir(INPUT_FOLDER):
        os.remove(os.path.join(INPUT_FOLDER, f))

    for f in os.listdir(OUTPUT_FOLDER):
        os.remove(os.path.join(OUTPUT_FOLDER, f))

    if os.path.exists("result.zip"):
        os.remove("result.zip")

    # Save uploaded files
    for file in files:
        file.save(os.path.join(INPUT_FOLDER, file.filename))

    # Start background processing
    thread = threading.Thread(
        target=background_task,
        args=(text, angle, opacity)
    )
    thread.start()

    # 🔥 Auto status check page
    return '''
    <h2>Processing Images...</h2>
    <p>Please wait ⏳</p>

    <script>
    setInterval(async () => {
        let res = await fetch('/status');
        let text = await res.text();

        if (text === "done") {
            window.location.href = "/download";
        }

        if (text === "error") {
            alert("Error occurred during processing ❌");
        }
    }, 2000);
    </script>
    '''


# 📊 STATUS
@app.route('/status')
def check_status():
    return status


# 📥 DOWNLOAD
@app.route('/download')
def download():
    return send_file("result.zip", as_attachment=True)


# ▶️ RUN
if __name__ == "__main__":
    app.run(debug=True)