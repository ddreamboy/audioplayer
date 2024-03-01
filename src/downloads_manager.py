from saved_tracks_handler import (
    get_audio_files,
    get_audio_mp3_path,
    get_image_path,
    delete_audiofile
)
import flet as ft


class DownloadsItem:
    def __init__(self, app, filename):
        self.app = app
        self.filename = filename
        self.image_src = get_image_path(filename)
        self.audio_src = get_audio_mp3_path(filename)
        self.cover = ft.Image(
                    src=self.image_src,
                    width=64,
                    height=64,
                    fit=ft.ImageFit.COVER,
                    repeat=ft.ImageRepeat.NO_REPEAT
                )
        self.name_text = ft.Text(
                    filename,
                    width=9 * 25
                    )
        self.play_bttn = ft.IconButton(
                    icon=ft.icons.PLAY_CIRCLE,
                    icon_color=ft.colors.WHITE,
                    on_click=lambda _: self.play_audio()
                )
        self.delete_bttn = ft.IconButton(
                    icon=ft.icons.DELETE,
                    icon_color=ft.colors.WHITE,
                    on_click=lambda _: self.delete_audio()
                )

    def play_audio(self):
        self.app.layout.bottombar.bottombar_height_update()
        self.app.layout.bottombar.audio_player.set_audio_elements(
            self.filename,
            self.image_src,
            self.audio_src
            )

    def delete_audio(self):
        delete_audiofile(self.filename)
        self.app.refresh_downloads()

    def build(self):
        action_items = ft.Column(
            [
                self.play_bttn,
                self.delete_bttn
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


class DownloadsPage(ft.UserControl):
    def __init__(self, app, page: ft.Page):
        super().__init__()
        self.app = app
        self.page = page
        self.downloads_audio = ft.ListView(
            expand=1,
            spacing=10
            )

    def build(self):
        self.set_downloads_list()
        view = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text('Мои загрузки')
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Divider(height=2),
                self.downloads_audio
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )
        return view

    def set_downloads_list(self):
        self.downloads_audio.controls = []
        filenames = get_audio_files()
        if filenames:
            for filenames in filenames:
                audiofile_item = DownloadsItem(self.app, filenames)
                audiofile_item = audiofile_item.build()
                self.downloads_audio.controls.append(audiofile_item)
                self.downloads_audio.controls.append(ft.Divider(height=1))
            self.page.update()
