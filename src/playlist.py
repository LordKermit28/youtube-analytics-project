import os
from googleapiclient.discovery import build
import datetime
from src.video import PLVideo

API_KEY = os.getenv('API_KEY')


class PlayList:
    def __init__(self, id_playlist):
        self.id_playlist = id_playlist
        self.title = self._get_title()
        self.url = f"https://www.youtube.com/playlist?list={id_playlist}"
        self.videos = self._get_videos()

    def __str__(self):
        return f'{self.title}'

    def _get_title(self):
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        request = youtube.playlists().list(
            part='snippet',
            id=self.id_playlist
        )
        response = request.execute()
        return response['items'][0]['snippet']['title']

    def _get_videos(self):
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=self.id_playlist,
            maxResults=50
        )
        response = request.execute()
        videos = []
        for item in response['items']:
            video_id = item['contentDetails']['videoId']
            pl_video = PLVideo(video_id, self.id_playlist)
            videos.append(pl_video)
        return videos

    def _get_duration(self, id_video):
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        request = youtube.videos().list(
            part='contentDetails',
            id=id_video
        )
        response = request.execute()
        duration_iso = response['items'][0]['contentDetails']['duration']
        duration = datetime.timedelta()
        parts = duration_iso[2:].split('M')
        if len(parts) == 1:
            seconds = parts[0].rstrip('S')
            duration += datetime.timedelta(seconds=int(seconds))
        else:
            minutes, seconds = parts
            seconds = seconds.rstrip('S')
            duration += datetime.timedelta(minutes=int(minutes), seconds=int(seconds))
        return duration

    @property
    def total_duration(self):
        duration = datetime.timedelta()
        for video in self.videos:
            duration += self._get_duration(video.video_id)
        return duration



    def _get_best_video(self):
        best_video = None
        max_likes = 0
        for video in self.videos:
            if video.likes_count > max_likes:
                best_video = video
                max_likes=video.likes_count
        return best_video


    def show_best_video(self):
        return f'https://youtu.be/{self._get_best_video().video_id}'


