import os


from googleapiclient.discovery import build

API_KEY = os.getenv('API_KEY')

class Video:

    def __init__(self, video_id: str):
        self.video_id = video_id
        self.title = self._get_title()
        self.link = f"https://www.youtube.com/watch?v={video_id}"
        self.views_count = self._get_video_info('viewCount')
        self.likes_count = self._get_video_info('likeCount')

        youtube = build('youtube', 'v3', developerKey=API_KEY)
        request = youtube.videos().list(
            part="snippet",
            id=self.video_id
        )
        response = request.execute()
        self.title = response['items'][0]['snippet']['title']

    def __str__(self):
        return self.title

    def _get_title(self):
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        request = youtube.videos().list(
            part='snippet',
            id=self.video_id
        )
        response = request.execute()
        return response['items'][0]['snippet']['title']

    def _get_video_info(self, data_type: str):
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        request = youtube.videos().list(
            part='statistics',
            id=self.video_id
        )
        response = request.execute()
        return int(response['items'][0]['statistics'][data_type])


class PLVideo(Video):
    def __init__(self, video_id, id_playlist):
        super().__init__(video_id)
        self.id_playlist = id_playlist
        self.title = self._get_title()
        self.link = f"https://www.youtube.com/watch?v={video_id}"
        self.views_count = self._get_video_info('viewCount')
        self.likes_count = self._get_video_info('likeCount')


    def __str__(self):
        return f'{self.title}'





