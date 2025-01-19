import os
import socket
import threading
import qrcode
from io import BytesIO
from flask import Flask, request, send_from_directory
from PyQt5.QtWidgets import (
    QApplication, QLabel, QVBoxLayout, QPushButton, QFileDialog, QMainWindow, QWidget
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

# Flask App Setup
flask_app = Flask(__name__)
DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")

def get_local_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

@flask_app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>File Transfer</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                text-align: center;
                background-color: #f9f9f9;
            }
            h1 {
                color: #333;
                margin-bottom: 20px;
            }
            form {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 10px;
                margin-bottom: 20px;
            }
            input[type="file"] {
                border: 1px solid #ccc;
                padding: 10px;
                border-radius: 5px;
                cursor: pointer;
            }
            button {
                padding: 10px 20px;
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background-color: #0056b3;
            }
            a {
                text-decoration: none;
                color: #007BFF;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>File Transfer</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" multiple>
            <button type="submit">Upload</button>
        </form>
        <a href="/files">View Uploaded Files</a>
    </body>
    </html>
    """

@flask_app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("file")
    for file in files:
        file.save(os.path.join(DOWNLOADS_FOLDER, file.filename))
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>File Uploaded</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin: 20px;
                background-color: #f9f9f9;
            }
            a {
                color: #007BFF;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>Upload Successful</h1>
        <a href="/">Go Back</a>
    </body>
    </html>
    """

@flask_app.route("/files")
def list_files():
    files = os.listdir(DOWNLOADS_FOLDER)
    file_links = [f"<a href='/download/{file}'>{file}</a>" for file in files]
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Uploaded Files</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin: 20px;
                background-color: #f9f9f9;
            }
            a {
                color: #007BFF;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>Uploaded Files</h1>
        """ + "<br>".join(file_links) + """
        <br><br>
        <a href="/">Go Back</a>
    </body>
    </html>
    """

@flask_app.route("/download/<filename>")
def download(filename):
    return send_from_directory(DOWNLOADS_FOLDER, filename)

def start_server():
    flask_app.run(host="0.0.0.0", port=5000)  # Uses the renamed Flask app object

# PyQt GUI Setup
class FileTransferApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Transfer App")
        self.setGeometry(100, 100, 400, 500)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Folder Selection Button
        self.folder_button = QPushButton("Select Folder")
        self.folder_button.clicked.connect(self.select_folder)
        self.layout.addWidget(self.folder_button)

        # QR Code Display
        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.qr_label)

        self.init_server()

    def select_folder(self):
        global DOWNLOADS_FOLDER
        folder = QFileDialog.getExistingDirectory(self, "Select Folder", DOWNLOADS_FOLDER)
        if folder:
            DOWNLOADS_FOLDER = folder
            print(f"Folder set to: {DOWNLOADS_FOLDER}")

    def generate_qr_code(self):
        ip = get_local_ip()
        url = f"http://{ip}:5000"
        qr = qrcode.make(url)

        # Convert QR code to QPixmap using BytesIO
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        buffer.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(buffer.read())
        self.qr_label.setPixmap(pixmap)
        self.qr_label.setFixedSize(300, 300)

    def init_server(self):
        # Generate and display QR code
        self.generate_qr_code()

        # Start the Flask server in a separate thread
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()

# Main Application
if __name__ == "__main__":
    import sys
    qt_app = QApplication(sys.argv)  # Renamed the QApplication object
    main_window = FileTransferApp()
    main_window.show()
    sys.exit(qt_app.exec_())
