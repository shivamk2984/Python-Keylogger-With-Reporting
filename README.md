# Advanced Python Keylogger

## Description

This project is an advanced Python-based keylogger that captures keystrokes, takes screenshots, and periodically emails the encrypted logs and images to a specified email address. The logs and screenshots are encrypted using the `cryptography` library, ensuring the captured data remains secure.

## Features

- Captures keystrokes and logs them to a file.
- Takes screenshots at regular intervals.
- Encrypts the log file and screenshots using `Fernet` symmetric encryption.
- Periodically emails the encrypted data to a specified email address.
- Runs as a background process on Windows systems.
- Securely stores the encryption key.
- Provides a user-friendly GUI for decrypting logs.

## Prerequisites

- Python 3.x
- A Gmail account (with an app-specific password if 2FA is enabled).

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Open `keylogger_enc.py` and update the following variables with your email credentials:
   ```python
   EMAIL_ADDRESS = "your-email-id"
   EMAIL_PASSWORD = "your-app-password"
   EMAIL_TO = "your-reciever-email"
   ```

2. You can also adjust the `SCREENSHOT_INTERVAL` and `EMAIL_INTERVAL` as needed.

## Usage

1. Run the keylogger script:
   ```bash
   python keylogger_enc.py
   ```
   The script will start running in the background.

2. To decrypt the logs, run the decryption script:
   ```bash
   python decrypt_log.py
   ```
   A GUI window will open. Click the "Decrypt Log File" button and select the encrypted `log.txt` file you received in your email. The decrypted content will be displayed in the text area.

## Stopping the Keylogger

To stop the keylogger, open the Task Manager, go to the "Details" tab, find "python.exe" or "pythonw.exe", and end the process.

## Disclaimer

This tool is for educational purposes only. The user is responsible for any misuse of this software.
