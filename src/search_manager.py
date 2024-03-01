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
        download_audio_to_temp(self.link, self.title)
        audio_src = get_temp_path(self.title)
        self.app.layout.bottombar.bottombar_height_update()
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

    def build(self):
        search_view = ft.Row(
                    controls=[
                        self.search_field,
                        self.search_bttn
                    ]
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
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )
        return view

    def music_search(self, search_query):
        self.search_result.controls = []
        clean_temp_dir()
        if search_query:
            videos = search_videos(search_query)
            if videos:
                for video in videos:
                    search_result_item = SearchItem(self.app,
                                                    self.page,
                                                    video['title'],
                                                    video['link']
                                                    )
                    search_result_item = search_result_item.build()
                    self.search_result.controls.append(search_result_item)
                    self.search_result.controls.append(ft.Divider(height=1))
                self.page.update()
