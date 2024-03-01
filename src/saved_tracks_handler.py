import os
import re


def clean_filename(filename):
    cleaned_filename = re.sub(r'[^\w\s.-]', '', filename)
    return cleaned_filename


def get_audio_files(directory=r'E:\Python\audioplayer\audio\saved'):
    files = []
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            if not file.endswith('.mp3'):
                files.append(file)
    if files:
        sorted_files: list = sorted(files,
                                    key=lambda x: os.path.getmtime(
                                        os.path.join(directory, x)))
        sorted_files.reverse()
        return sorted_files
    else:
        return files


def get_audio_mp3_path(filename):
    filename = clean_filename(filename)
    directory = r'E:\Python\audioplayer\audio\saved'
    path = os.path.join(directory, f'{filename}.mp3')
    return path


def get_image_path(filename):
    filename = clean_filename(filename)
    directory = r'E:\Python\audioplayer\audio\saved'
    path = os.path.join(directory, filename)
    return path


def delete_audiofile(filename):
    audio_path = get_audio_mp3_path(filename)
    image_path = get_image_path(filename)
    if os.path.exists(audio_path):
        os.remove(audio_path)
    if os.path.exists(image_path):
        os.remove(image_path)
