Here is the **README** file content for your YouTube Downloader script:

---

# YouTube Downloader Script

A simple, menu-driven Python script that allows you to download YouTube videos and playlists using `yt-dlp`. It includes options to download videos, pause/resume downloads, download from a list of URLs, and handle various download qualities (best, medium, low).

## Features

- **Download Single Video**: Allows downloading individual videos from YouTube.
- **Download Playlist**: Allows downloading all videos from a YouTube playlist.
- **Download from URL List File**: You can input a text file containing a list of YouTube video URLs to download.
- **Pause and Resume Downloads**: Pause and resume downloads using process IDs.
- **Custom Video Quality**: Choose the video quality (best, medium, low) for downloading.
- **Progress Feedback**: Shows progress of the download in real time.
- **Error Logging**: Logs errors and events to a file for troubleshooting.
- **Download Status Saving**: Keeps track of download status (completed/failed) using a JSON file.
- **Retry Mechanism**: Retries failed downloads for a specified number of attempts.

## Requirements

- Python 3.x
- **yt-dlp**: A powerful YouTube video downloader. Install it via:

```bash
pip install yt-dlp
```

## Installation

1. **Clone this repository** or **download the script**:

   ```bash
   git clone https://github.com/yourusername/youtube-downloader.git
   ```

2. **Install dependencies**:

   ```bash
   pip install yt-dlp
   ```

3. **Run the script**:

   ```bash
   python youtube_downloader.py
   ```

## Usage

1. **Download Single Video**:
   - Enter the YouTube video URL.
   - Enter the download path (leave blank to save in the current directory).
   - Choose the video quality: `best`, `medium`, or `low`.

2. **Download Playlist**:
   - Enter the YouTube playlist URL.
   - Enter the download path.
   - Choose the video quality: `best`, `medium`, or `low`.

3. **Download from URL List File**:
   - Prepare a text file with a list of YouTube video URLs (one URL per line).
   - Enter the file path when prompted.
   - Enter the download path and quality.

4. **Pause and Resume Downloads**:
   - You can pause ongoing downloads using the process ID.
   - Resume any paused downloads by simply selecting the "Resume" option in the menu.

5. **Check Progress**: The download progress is shown in real time during the download.

6. **Exit**: Choose option 6 to exit the script.

## Command Line Options

- **-f** or **--format**: Specifies the video quality (e.g., `best`, `medium`, `low`). If not specified, it defaults to `best`.
  
- **-o** or **--output**: Specifies the output path and filename template. Default is `%(title)s.%(ext)s`.

## Status File

The script saves the download status for each video in a file called `download_status.json`. The status file keeps track of which videos have been successfully downloaded (`'completed'`) and which have failed (`'failed'`). This file is used to resume or retry downloads.

## Logging

All errors and important events are logged in the `download_log.txt` file for troubleshooting purposes.

## Example

```bash
YouTube Downloader
1. Download Single Video
2. Download Playlist
3. Download from URL List File
4. Resume Downloads
5. Pause Download
6. Exit
Enter your choice (1/2/3/4/5/6): 1
Enter the YouTube URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Enter the download path (leave blank to save in current directory): 
Enter the video quality (best/medium/low): best
```

## Contributing

Feel free to fork this repository, submit issues, or create pull requests if you want to contribute. If you encounter any bugs or have feature requests, please open an issue.

## License

This project is open-source and available under the [MIT License](LICENSE).

---

### **Troubleshooting**

- **Error Logs**: Check `download_log.txt` for detailed logs in case of issues.
- **Retrying Failed Downloads**: If a download fails, the script will retry up to 3 times (default). You can adjust the retry count in the script.

---

### **Notes**

- Ensure you have `yt-dlp` installed and that it's working correctly on your system.
- If a download is interrupted, you can resume it or pause and resume as needed.

