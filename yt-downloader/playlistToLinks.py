import requests
from bs4 import BeautifulSoup

def get_video_links_from_playlist(playlist_url):
    video_links = []
    response = requests.get(playlist_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Search for scripts containing video IDs
    for script in soup.find_all('script'):
        if script.string and 'var ytInitialData =' in script.string:
            start_index = script.string.find('var ytInitialData =') + len('var ytInitialData =')
            end_index = script.string.find(';', start_index)
            json_data = script.string[start_index:end_index].strip()
            try:
                import json
                data = json.loads(json_data)
                contents = data.get('contents', {})
                two_column_watch_next_results = contents.get('twoColumnWatchNextResults', {})
                playlist = two_column_watch_next_results.get('playlist', {})
                playlist_contents = playlist.get('playlistContents', {})
                videos = playlist_contents.get('videos', [])
                for video in videos:
                    video_id = video.get('videoId')
                    if video_id:
                        video_url = f"https://www.youtube.com/watch?v={video_id}"
                        if video_url not in video_links:
                            video_links.append(video_url)
            except Exception as e:
                print(f"Error parsing JSON data: {e}")
                continue

    return video_links

def main():
    playlist_url = input("Enter the YouTube playlist URL: ").strip()
    
    if not playlist_url.startswith('https://www.youtube.com/playlist?list='):
        print("Invalid URL. Please make sure it is a valid YouTube playlist URL.")
        return

    video_links = get_video_links_from_playlist(playlist_url)
    
    if video_links:
        print("Video links found:")
        for link in video_links:
            print(link)
    else:
        print("No video links found.")

if __name__ == '__main__':
    main()

