from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from typing import Optional, List
import os
from dotenv import load_dotenv

load_dotenv()

class YouTubeTranscriptFetcher:
    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        if "youtu.be/" in url:
            return url.split("youtu.be/")[-1].split("?")[0]
        if "v=" in url:
            return url.split("v=")[1].split("&")[0]
        return None

    @staticmethod
    def get_transcript(video_url: str) -> Optional[str]:
        try:
            video_id = YouTubeTranscriptFetcher.extract_video_id(video_url)
            if not video_id:
                return None
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return " ".join([entry["text"] for entry in transcript])
        except Exception as e:
            print(f"Transcript error: {e}")
            return None

class YouTubeAPI:
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.service = build('youtube', 'v3', developerKey=self.api_key) if self.api_key else None

    def search_videos(self, query: str, max_results=5) -> List[dict]:
        if not self.service:
            return []
        try:
            request = self.service.search().list(
                q=query,
                part="id,snippet",
                maxResults=max_results,
                type="video"
            )
            response = request.execute()
            return [{
                "title": item["snippet"]["title"],
                "video_id": item["id"]["videoId"],
                "url": f"https://youtu.be/{item['id']['videoId']}"
            } for item in response.get("items", [])]
        except Exception as e:
            print(f"YouTube API error: {e}")
            return []