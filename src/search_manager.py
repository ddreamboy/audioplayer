from youtube_audio import (
    search_videos,
    download_cover_to_temp,
    get_temp_path,
    get_video_thumbnail,
    clean_temp_dir,
    download_audio_to_temp,
    download_cover_to_saved,
    download_audio_to_saved
)
import flet as ft
import time


class SearchItem(ft.UserControl):
    def __init__(self, app, page, title, link):
        super().__init__()
        self.app = app
        self.page = page
        self.title = title
        self.link = link
        self.thumbnail_url = get_video_thumbnail(link)
        download_cover_to_temp(self.thumbnail_url, title)
        self.image_src = get_temp_path(title)
        self.cover = ft.Image(
                    src=self.image_src,
                    width=64,
                    height=64,
                    fit=ft.ImageFit.COVER,
                    repeat=ft.ImageRepeat.NO_REPEAT
                )
        self.name_text = ft.Text(
                    title,
                    width=9 * 25
                    )
        self.play_bttn = ft.IconButton(
                    icon=ft.icons.PLAY_CIRCLE,
                    icon_color=ft.colors.WHITE,
                    on_click=lambda _: self.play_audio()
                )
        self.download_bttn = ft.IconButton(
                    icon=ft.icons.DOWNLOAD,
                    icon_color=ft.colors.WHITE,
                    on_click=lambda _: self.download_audio()
                )

    def play_audio(self):
        self.app.layout.bottombar.audio_player.show_progress_starting_track()
        download_audio_to_temp(self.link, self.title)
        audio_src = get_temp_path(self.title)
        self.app.layout.bottombar.audio_player.set_audio_elements(
            self.title,
            self.thumbnail_url,
            f'{audio_src}.mp3'
            )

    def download_audio(self):
        download_audio_to_saved(self.link, self.title)
        download_cover_to_saved(self.thumbnail_url, self.title)
        self.app.refresh_downloads()

    def build(self):
        action_items = ft.Column(
            [
                self.play_bttn,
                self.download_bttn
            ]
        )
        view = ft.Row(
            [
                self.cover,
                self.name_text,
                action_items
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        return view


class SearchPage(ft.UserControl):
    def __init__(self, app, page: ft.Page):
        super().__init__()
        self.app = app
        self.page = page
        self.search_field = ft.TextField(
            hint_text='Трек, клип, исполнитель...',
            border=ft.InputBorder.UNDERLINE,
            on_change=self.change_track
        )
        self.search_bttn = ft.IconButton(
                            icon=ft.icons.SEARCH,
                            icon_color=ft.colors.WHITE,
                            on_click=lambda _:
                            self.music_search(self.search_field.value)
                        )
        self.search_result = ft.ListView(
            expand=1,
            spacing=10
            )
        self.query_count = 0

    def build(self):
        search_view = ft.Row(
                    controls=[
                        self.search_field,
                        # self.search_bttn
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
        view = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text('Музыкально-информационный поиск')
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Divider(height=2),
                search_view,
                ft.Divider(height=2),
                self.search_result
            ],
            expand=True
        )
        return view

    def music_search(self, search_query):
        self.progress_ring = ft.Row(
            [
                ft.Text(),
                ft.ProgressRing()
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        self.search_result.controls = []
        self.search_result.controls.append(self.progress_ring)
        self.page.update()
        clean_temp_dir()
        if search_query:
            self.search_field.disabled = True
            self.page.update()
            videos = search_videos(search_query)
            if videos:
                for video in videos:
                    self.search_result.controls.remove(self.progress_ring)
                    search_result_item = SearchItem(self.app,
                                                    self.page,
                                                    video['title'],
                                                    video['link']
                                                    )
                    search_result_item = search_result_item.build()
                    self.search_result.controls.append(search_result_item)
                    if self.search_field.disabled:
                        self.search_field.disabled = False
                    self.search_result.controls.append(ft.Divider(height=1))
                    self.search_result.controls.append(self.progress_ring)
                    self.page.update()
                self.search_result.controls.pop()
                if self.search_field.disabled:
                        self.search_field.disabled = False
                self.page.update()
            else:
                self.search_result.controls.pop()
                error_text = ft.Row(
                    [
                        ft.Text(
                            f'По запросу "{search_query}" не удалось ничего найти',
                            width=300
                            )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
                self.search_result.controls.append(error_text)
                if self.search_field.disabled:
                        self.search_field.disabled = False
                self.page.update()
        
    def change_track(self, e):
        query = e.control.value
        self.query_count += 1
        time.sleep(1)
        if query and self.query_count == 1:
            self.music_search(e.control.value)
        self.query_count -= 1
        
