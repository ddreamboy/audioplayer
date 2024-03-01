from pytube import YouTube
from youtubesearchpython import VideosSearch
from PIL import Image
from io import BytesIO
import moviepy.editor as mp
import requests
import os
import re


def get_temp_path(filename):
    filename = clean_filename(filename)
    path = os.path.join(r'E:\Python\audioplayer\audio\temp', filename)
    return path


def get_saved_path(filename):
    filename = clean_filename(filename)
    path = os.path.join(r'E:\Python\audioplayer\audio\saved', filename)
    return path


def clean_filename(filename):
    cleaned_filename = re.sub(r'[^\w\s.-]', '', filename)
    return cleaned_filename


def clean_temp_dir():
    directory = r'E:\Python\audioplayer\audio\temp'
    files = os.listdir(directory)
    for file in files:
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            os.remove(file_path)


def download_audio_to_temp(url, filename):
    filename = f'{filename}.mp3'
    output_path = get_temp_path(filename)
    download_audio(url, output_path)


def download_audio_to_saved(url, filename):
    filename = f'{filename}.mp3'
    output_path = get_saved_path(filename)
    download_audio(url, output_path)


def download_audio(url, output_path):
    # Получаем объект YouTube
    yt = YouTube(url)

    # Получаем аудио поток
    audio_stream = yt.streams.filter(only_audio=True).first()

    # Получаем URL аудиофайла
    audio_url = audio_stream.url

    # Загружаем аудио и преобразуем его в формат MP3
    audio_clip = mp.AudioFileClip(audio_url)
    audio_clip.write_audiofile(output_path)

    # Освобождаем ресурсы
    audio_clip.close()


def search_videos(query, max_results=10):
    search_results = VideosSearch(query, limit=max_results).result()['result']
    videos = []
    for result in search_results:
        video = {
            'title': result['title'],
            'id': result['id'],
            'link': f"https://www.youtube.com/watch?v={result['id']}"
        }
        if result['duration']:
            video_duration = get_video_duration(video['link'])
            if video_duration <= 377:
                videos.append(video)
    return videos


def get_video_duration(url):
    yt = YouTube(url)
    duration = yt.length
    return duration


def get_video_thumbnail(url):
    yt = YouTube(url)
    thumbnail_url = yt.thumbnail_url
    return thumbnail_url


def save_video_thumbnail(url, output_path):
    response = requests.get(url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image.save(output_path, 'JPEG')  # Сохранение в формате JPEG


def download_cover_to_temp(url, filename):
    output_path = get_temp_path(filename)
    save_video_thumbnail(url, output_path)


def download_cover_to_saved(url, filename):
    output_path = get_saved_path(filename)
    save_video_thumbnail(url, output_path)
