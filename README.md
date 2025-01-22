# DDreamBoy AudioPlayer

Десктопный аудиоплеер с возможностью поиска и проигрывания музыки с YouTube. Приложение позволяет искать треки, проигрывать их онлайн и сохранять для последующего прослушивания офлайн.

## Особенности

- 🎵 Поиск музыки на YouTube
- 🎧 Онлайн проигрывание найденных треков
- 💾 Загрузка треков для офлайн прослушивания
- 📱 Современный минималистичный интерфейс
- 🎚️ Управление громкостью и позицией трека
- 📂 Менеджер загруженных треков

## Требования

- Python 3.8+
- Установленные зависимости из requirements.txt
- Операционная система Windows (для корректной работы с путями)

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/ddreamboy/audioplayer.git
cd audioplayer
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate     # Для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте необходимые директории для сохранения аудио:
```bash
mkdir -p audio/temp audio/saved
```

## Использование

1. Запустите приложение:
```bash
python src/main.py
```

2. Интерфейс приложения состоит из двух основных разделов:
   - **Поиск** (🔍): поиск и проигрывание треков с YouTube
   - **Загрузки** (💾): управление сохраненными треками

### Поиск музыки

1. Перейдите на вкладку "Поиск"
2. Введите название трека, исполнителя или клипа
3. Дождитесь результатов поиска
4. Используйте кнопки:
   - ▶️ для проигрывания трека онлайн
   - 💾 для сохранения трека

### Управление сохраненными треками

1. Перейдите на вкладку "Загрузки"
2. Для каждого трека доступны опции:
   - ▶️ проигрывание
   - 🗑️ удаление

### Управление воспроизведением

- ▶️/⏸️ Play/Pause
- 🔊 Регулировка громкости
- 📊 Перемотка с помощью слайдера

## Структура проекта

```
ddreamboy-audioplayer/
├── requirements.txt
└── src/
    ├── app_layout.py        # Основной layout приложения
    ├── audioplayer_manager.py # Управление воспроизведением
    ├── bottombar.py         # Нижняя панель управления
    ├── downloads_manager.py # Управление загрузками
    ├── main.py             # Точка входа
    ├── saved_tracks_handler.py # Обработка сохраненных треков
    ├── search_manager.py    # Поиск треков
    └── youtube_audio.py     # Взаимодействие с YouTube
```

## Технологии

- [Flet](https://flet.dev/) - Framework для создания кроссплатформенных приложений
- [PyTube](https://pytube.io/) - Библиотека для работы с YouTube
- [MoviePy](https://zulko.github.io/moviepy/) - Обработка аудио/видео файлов
- [PIL](https://python-pillow.org/) - Работа с изображениями

## Ограничения

- Максимальная длительность трека: 377 секунд
- Поддерживается только формат MP3
- Пути к директориям только для Windows

## Планы по развитию

- [ ] Добавить поддержку других ОС
- [ ] Реализовать очередь воспроизведения
- [ ] Добавить поддержку плейлистов
- [ ] Улучшить обработку ошибок
- [ ] Добавить настройки приложения
- [ ] Реализовать поиск по локальным файлам
