import os
import subprocess
import time
import json
import signal

def load_download_status(status_file):
    if os.path.exists(status_file):
        with open(status_file, 'r') as f:
            return json.load(f)
    return {}

def save_download_status(status_file, status):
    with open(status_file, 'w') as f:
        json.dump(status, f, indent=4)

def download_video(url, path, status_file, retries=3):
    command = ['yt-dlp', '--continue', '--output', os.path.join(path, '%(title)s.%(ext)s'), url]
    status = load_download_status(status_file)
    if url in status and status[url] == 'completed':
        print(f"Video {url} already downloaded.")
        return
    attempt = 0
    while attempt < retries:
        try:
            print(f"Attempting to download {url} (Attempt {attempt + 1})")
            process = subprocess.Popen(command)
            process.wait()  # Wait for download to complete
            if process.returncode == 0:
                print(f"Successfully downloaded {url}")
                status[url] = 'completed'
                save_download_status(status_file, status)
                return
            else:
                print(f"Failed to download {url} on attempt {attempt + 1}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")
        attempt += 1
        time.sleep(10)  # Wait before retrying
    print(f"Failed to download {url} after {retries} attempts")
    status[url] = 'failed'
    save_download_status(status_file, status)

def pause_download(process):
    print("Pausing download...")
    process.send_signal(signal.SIGSTOP)

def resume_download(process):
    print("Resuming download...")
    process.send_signal(signal.SIGCONT)

def download_playlist(url, path, status_file, retries=3):
    command = ['yt-dlp', '--continue', '--output', os.path.join(path, '%(title)s.%(ext)s'), url]
    status = load_download_status(status_file)
    try:
        process = subprocess.Popen(command)
        process.wait()  # Wait for playlist download to complete
        print(f"Successfully downloaded playlist {url}")
        status[url] = 'completed'
        save_download_status(status_file, status)
    except subprocess.CalledProcessError as e:
        print(f"Failed to download playlist {url}: {e}")
        status[url] = 'failed'
        save_download_status(status_file, status)

def main():
    print("YouTube Downloader")
    print("1. Download Single Video")
    print("2. Download Playlist")
    print("3. Resume Downloads")
    print("4. Pause Download")
    print("5. Exit")

    status_file = 'download_status.json'
    ongoing_processes = {}

    while True:
        choice = input("Enter your choice (1/2/3/4/5): ")
        if choice == '1':
            url = input("Enter the YouTube URL: ")
            path = input("Enter the download path (leave blank to save in current directory): ")
            if not path:
                path = '.'
            download_video(url, path, status_file)
        elif choice == '2':
            url = input("Enter the YouTube playlist URL: ")
            path = input("Enter the download path (leave blank to save in current directory): ")
            if not path:
                path = '.'
            download_playlist(url, path, status_file)
        elif choice == '3':
            print("Resuming downloads...")
            status = load_download_status(status_file)
            for video_url, state in status.items():
                if state != 'completed':
                    download_video(video_url, '.', status_file)
        elif choice == '4':
            print("Pausing a download...")
            pid = int(input("Enter the process ID to pause: "))
            process = ongoing_processes.get(pid)
            if process:
                pause_download(process)
            else:
                print("Invalid process ID.")
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, 4, or 5.")

if __name__ == "__main__":
    main()
