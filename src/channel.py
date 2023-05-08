import json
import os
from googleapiclient.discovery import build



class Channel:
    """Класс для ютуб-канала"""
    api_key = os.getenv('API_KEY')

    def __init__(self, channel_id: str) -> None:
        self.channel_id = channel_id
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        channel_data = self.youtube.channels().list(id=self.channel_id, part='snippet, statistics').execute()['items']
        self.channel_info = channel_data

    def print_info(self) -> None:
        print(self.channel_info)





