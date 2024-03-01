from pytube import YouTube
from youtubesearchpython import VideosSearch
from PIL import Image
from io import BytesIO
import moviepy.editor as mp
import requests
import flet as ft


def main(page: ft.Page):
    url = 'https://www.youtube.com/watch?v=9PUSwdStJdQ'
    output_path = 'test.mp3'
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

    audio1 = ft.Audio(
        src=url,
        autoplay=False,
        volume=1,
        balance=0,
    )

    page.overlay.append(audio1)
    page.add(
        ft.ElevatedButton("Play", on_click=lambda _: audio1.play())
    )


ft.app(target=main)
