import yt_dlp as youtube_dl
import os

class Downloader:
    def __init__(self):
        print("Downloader Initialized")

    def download(self, url):
        ydl_opts = {
            'format': 'best',
            'outtmpl': '%(title)s.%(ext)s',
            'noplaylist': True
        }
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                video_title = info_dict.get('title', None)
                video_ext = info_dict.get('ext', None)
                video_filename = f"{video_title}.{video_ext}"
                print(f"Downloaded: {video_filename}")
                return {'video': video_filename, 'description': video_title}
        except Exception as e:
            print(f"Error: {str(e)}")
            return None