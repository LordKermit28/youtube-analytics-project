import json
import os
from googleapiclient.discovery import build


class Channel:
    api_key = os.getenv('API_KEY')

    @classmethod
    def get_service(cls):
        youtube = build('youtube', 'v3', developerKey=cls.api_key)
        return youtube

    def __init__(self, channel_id):
        youtube = self.get_service()
        request = youtube.channels().list(part='snippet,statistics', id=channel_id)
        response = request.execute()


        if response.get('items'):
            channel_info = response['items'][0]
            self.id_channel = channel_info['id']
            self.title = channel_info['snippet']['title']
            self.description = channel_info['snippet']['description']
            self.url = f"https://www.youtube.com/channel/{channel_id}"
            self.subscriber_count = int(channel_info['statistics']['subscriberCount'])
            self.video_count = int(channel_info['statistics']['videoCount'])
            self.view_count =int(channel_info['statistics']['viewCount'])
        else:
            raise Exception(f"Не найден канал по данному id: {channel_id}")

    def __str__(self):
        return f'{self.title}: {self.url}'

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        return self.subscriber_count - other.subscriber_count

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __eq__(self, other):
        return self.subscriber_count == other.subscriber_count

    def __str__(self):
        return f"{self.title} ({self.subscriber_count})"

    def print_info(self):
        print(f"id канала: {self.id_channel}")
        print(f"название канала: {self.title}")
        print(f"описание канала: {self.description}")
        print(f"ссылка на канал: {self.url}")
        print(f"количество подписчиков: {self.subscriber_count}")
        print(f"количество видео: {self.video_count}")
        print(f"общее количество просмотров: {self.view_count}")

    def to_json(self, filename):
        data = {
            'channel_id': self.id_channel,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        with open(filename, 'w') as f:
            json.dump(data, f)

