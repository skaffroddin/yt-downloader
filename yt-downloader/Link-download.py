import os
import subprocess
import json
import time
import signal
import sys
from tqdm import tqdm

# Function to download a video
def download_video(url, path, status_file, command, resume=False):
    file_name = os.path.join(path, '%(title)s.%(ext)s')
    command_with_url = command + ['--output', file_name, url]

    if not resume and os.path.exists(file_name):
        print(f"File already exists: {file_name}")
        return

    if resume and not os.path.exists(file_name):
        print(f"Cannot resume: file does not exist: {file_name}")
        return

    print(f"Starting download: {url}")

    with open(status_file, 'a') as log_file:
        process = subprocess.Popen(command_with_url, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Track download progress
        try:
            for line in process.stdout:
                if "Downloading" in line:
                    print(line.strip())
                if "has been downloaded" in line:
                    print("Download complete!")
                    save_download_status(status_file, url, 'completed')
                    break
                if "failed" in line:
                    print("Download failed.")
                    save_download_status(status_file, url, 'failed')
                    break
        except KeyboardInterrupt:
            print("Download interrupted. Pausing...")
            process.send_signal(signal.SIGINT)  # Graceful interruption
            save_download_status(status_file, url, 'paused')
            return

    if process.returncode != 0:
        print(f"Download failed: {url}")
        save_download_status(status_file, url, 'failed')

def save_download_status(status_file, url, status):
    status_data = load_download_status(status_file)
    status_data[url] = status
    with open(status_file, 'w') as f:
        json.dump(status_data, f, indent=4)

def load_download_status(status_file):
    if os.path.exists(status_file):
        try:
            with open(status_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            print("Error reading or parsing status file. Starting with an empty status.")
            return {}
    return {}

def retry_download(url, path, status_file, command):
    retries = 3
    for attempt in range(retries):
        print(f"Retrying download ({attempt + 1}/{retries})...")
        download_video(url, path, status_file, command)
        status = load_download_status(status_file)
        if status.get(url) == 'completed':
            break
        time.sleep(5)  # Wait before retrying

def display_progress(url, status_file):
    status = load_download_status(status_file)
    if url in status:
        print(f"Status for {url}: {status[url]}")
    else:
        print(f"No status available for {url}")

def main():
    status_file = 'download_status.json'
    download_path = input("Enter the download path: ").strip()

    if not os.path.exists(download_path):
        os.makedirs(download_path)

    command = ['yt-dlp', '--progress', '--no-warnings']

    urls = [
        'https://www.youtube.com/watch?v=ZhYsfqQdSmU',
        'https://www.youtube.com/watch?v=LPvgMyfpCGM',
        'https://www.youtube.com/watch?v=lwJbgGutvvg',
        'https://www.youtube.com/watch?v=L0oHCRy5DQQ',
        'https://www.youtube.com/watch?v=0OKQDABQVQg',
        'https://www.youtube.com/watch?v=YbwPVciydTw',
        'https://www.youtube.com/watch?v=umZUAE3QUv4',
        'https://www.youtube.com/watch?v=neW0xoILQDw',
        'https://www.youtube.com/watch?v=NUXbO53W99c',
        'https://www.youtube.com/watch?v=Yc6r1f6nvjs',
        'https://www.youtube.com/watch?v=5gvYfJQx5fo',
        'https://www.youtube.com/watch?v=JB2_B3RwG-I',
        'https://www.youtube.com/watch?v=4zAYAusVTks',
        'https://www.youtube.com/watch?v=q4U7SuKVuTI',
    ]

    for url in urls:
        status = load_download_status(status_file)
        if url in status:
            if status[url] == 'paused':
                print(f"Resuming download: {url}")
                download_video(url, download_path, status_file, command, resume=True)
            elif status[url] == 'completed':
                print(f"Download already completed: {url}")
            elif status[url] == 'failed':
                print(f"Download failed previously: {url}. Restarting...")
                retry_download(url, download_path, status_file, command)
        else:
            download_video(url, download_path, status_file, command)

        # Display progress
        display_progress(url, status_file)

if __name__ == "__main__":
    main()

