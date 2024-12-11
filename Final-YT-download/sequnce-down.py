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

def download_video(url, path, status_file, retries=3, index=None):
    command = ['yt-dlp', '--continue', '--output', os.path.join(path, f'{str(index).zfill(3)}-%(title)s.%(ext)s'), url]
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
    command = ['yt-dlp', '--flat-playlist', '--dump-json', url]
    status = load_download_status(status_file)

    try:
        # Fetch playlist video details in JSON format
        playlist_info = subprocess.check_output(command)
        playlist = json.loads(playlist_info)

        for index, video in enumerate(playlist, start=1):
            video_url = f"https://www.youtube.com/watch?v={video['id']}"
            print(f"Starting download for {video_url}")
            download_video(video_url, path, status_file, retries, index)

        print(f"Successfully downloaded playlist {url}")
        status[url] = 'completed'
        save_download_status(status_file, status)

    except subprocess.CalledProcessError as e:
        print(f"Failed to download playlist {url}: {e}")
        status[url] = 'failed'
        save_download_status(status_file, status)

def batch_download_from_file(file_path, path, status_file):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return
    with open(file_path, 'r') as file:
        urls = file.readlines()
    for url in urls:
        url = url.strip()
        if url:
            print(f"Starting download for {url}")
            if 'playlist' in url:
                download_playlist(url, path, status_file)
            else:
                download_video(url, path, status_file)

def main():
    print("YouTube Downloader")
    print("1. Download Single Video")
    print("2. Download Playlist")
    print("3. Batch Download from File")
    print("4. Resume Downloads")
    print("5. Pause Download")
    print("6. Exit")

    status_file = 'download_status.json'
    ongoing_processes = {}

    while True:
        choice = input("Enter your choice (1/2/3/4/5/6): ")
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
            file_path = input("Enter the file path containing URLs: ")
            path = input("Enter the download path (leave blank to save in current directory): ")
            if not path:
                path = '.'
            batch_download_from_file(file_path, path, status_file)
        elif choice == '4':
            print("Resuming downloads...")
            status = load_download_status(status_file)
            for video_url, state in status.items():
                if state != 'completed':
                    download_video(video_url, '.', status_file)
        elif choice == '5':
            print("Pausing a download...")
            pid = int(input("Enter the process ID to pause: "))
            process = ongoing_processes.get(pid)
            if process:
                pause_download(process)
            else:
                print("Invalid process ID.")
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, 4, 5, or 6.")

if __name__ == "__main__":
    main()
