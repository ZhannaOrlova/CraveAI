import os
import re
from typing import List, Dict
from cachetools import TTLCache
import httpx
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

class ChatAgent:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        self.query_cache = TTLCache(maxsize=100, ttl=3600)
        self.youtube_service = build('youtube', 'v3', developerKey=self.youtube_api_key) if self.youtube_api_key else None

    async def generate_queries(self, user_input: str) -> List[str]:
        """Generate search queries using DeepSeek API"""
        if not user_input.strip():
            return []

        if user_input in self.query_cache:
            return self.query_cache[user_input]

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    "https://api.deepseek.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={
                        "model": "deepseek-chat",
                        "messages": [{
                            "role": "user",
                            "content": f"Generate 5 specific YouTube search queries about: {user_input}. Return ONLY the queries, one per line."
                        }],
                        "temperature": 0.7
                    }
                )
                content = response.json()["choices"][0]["message"]["content"]
                queries = [q.strip() for q in content.split("\n") if q.strip()]
                self.query_cache[user_input] = queries[:5]
                return queries[:5]
        except Exception as e:
            raise Exception(f"Failed to generate queries: {str(e)}")

    def search_youtube_videos(self, query: str, max_results=3) -> List[Dict]:
        """Search YouTube for videos"""
        if not self.youtube_service:
            return []
            
        try:
            request = self.youtube_service.search().list(
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