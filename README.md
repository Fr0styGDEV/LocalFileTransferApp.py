# File Transfer App

A simple, standalone Python-based application for transferring files between a mobile device and a PC over a local network. This app features a QR code for easy connection and allows the user to select a folder for saving files.

## Features
- File upload from mobile devices.
- Dynamic QR code generation for easy connection.
- Customizable save folder on the PC.
- Cross-platform compatibility.
- Responsive web interface for mobile devices.

## Requirements

### Python Libraries
- Flask
- PyQt5
- qrcode
- Pillow

Install the required libraries with:
```bash
pip install flask pyqt5 qrcode[pil]
```

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/file-transfer-app.git
   cd file-transfer-app
   ```
2. Run the application:
   ```bash
   python main.py
   ```
3. Scan the QR code displayed in the application window using your mobile device.
4. Use the web interface to upload files to the selected folder.

## Packaging into an Executable
To create a standalone `.exe` file:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Run the following command:
   ```bash
   pyinstaller --onefile --noconsole --icon=custom_icon.ico main.py
   ```
3. The executable will be available in the `dist/` folder.

## Custom Icon
To use a custom icon:
- Place an `.ico` file named `custom_icon.ico` in the same directory as `main.py`.
- Include the `--icon=custom_icon.ico` option when packaging with PyInstaller.

## Folder Structure
```
file-transfer-app/
├── main.py          # Main application script
├── custom_icon.ico  # Custom icon for the application
├── static/          # Static files for Flask (if needed)
└── README.md        # Project README
```

## Known Issues
- Ensure that the PC and mobile device are on the same local network.
- Disable firewall restrictions if the connection is blocked.

## Contributing
Feel free to submit issues or pull requests to improve this application.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

