import yt_dlp
from tqdm import tqdm
import sys
import os
import re

# Initialize the progress bar variable
progress_bar = None

def clear_console_line():
    """Clear the current line in the console."""
    sys.stdout.write("\033[K")
    sys.stdout.flush()

def progress_hook(d):
    global progress_bar

    if d['status'] == 'downloading':
        if progress_bar:
            # Update progress bar with the difference in downloaded bytes
            progress_bar.update(d['downloaded_bytes'] - progress_bar.n)
        else:
            # Create a new progress bar
            total_bytes = d.get('total_bytes', d.get('total_bytes_estimate'))
            if total_bytes:
                progress_bar = tqdm(total=total_bytes, unit='B', unit_scale=True, unit_divisor=1024, dynamic_ncols=True, desc=d.get('filename', 'Downloading'))
    
    elif d['status'] == 'finished':
        # Close the progress bar when download is finished
        if progress_bar:
            progress_bar.close()
            progress_bar = None
            clear_console_line()

def display_status(title, progress_info):
    """Display the status of the download, including title and progress."""
    clear_console_line()
    print(f"{title} {progress_info}", end='\r')

def download_video(url, download_path):
    # Set up yt-dlp options
    ydl_opts = {
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'noplaylist': True  # To ensure only individual videos are downloaded, no playlists
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        title = info_dict.get('title', 'Unknown Title')
        display_status(title, "Starting download...")
        ydl.download([url])
        display_status(title, "Download completed")

# Main function to handle user input and start download
if __name__ == "__main__":
    download_path = input("Enter the download path: ").rstrip('/')  # Ensure no trailing slash
    url_file = input("Enter the path to the file with URLs: ")

    with open(url_file, 'r') as file:
        urls = [line.strip() for line in file]

    for url in urls:
        print("\n" + "="*50)
        download_video(url, download_path)
        print("="*50)
