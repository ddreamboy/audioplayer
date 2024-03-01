from audioplayer_manager import AudioPlayer
import flet as ft


class Bottombar(ft.UserControl):
    def __init__(self, app, page: ft.Page):
        super().__init__()
        self.app = app
        self.page = page
        self.downloads_bttn = ft.IconButton(
                        icon=ft.icons.DOWNLOAD,
                        icon_color=ft.colors.ORANGE,
                        on_click=lambda _: self.route_change('/downloads')
                    )
        self.search_bttn = ft.IconButton(
                        icon=ft.icons.SEARCH,
                        icon_color=ft.colors.WHITE,
                        on_click=lambda _: self.route_change('/search')
                    )
        self.routing_items = ft.Row(
                controls=[
                    self.downloads_bttn,
                    self.search_bttn,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=60
            )
        self.height = 90
        self.audio_player = AudioPlayer(self.app, self.page)
        self.page.bottom_appbar = self.build()

    def bottombar_height_update(self):
        self.bottombar_view.height = 200

    def build(self):
        self.bottombar_items = ft.Column(
                controls=[
                    ft.Text(visible=False),
                    self.routing_items
                ],
            )
        self.bottombar_view = ft.BottomAppBar(
            content=self.bottombar_items,
            height=self.height
        )
        return self.bottombar_view

    def route_change(self, route):
        self.page.route = route
        if route == '/downloads':
            self.downloads_bttn.icon_color = ft.colors.ORANGE
            self.search_bttn.icon_color = ft.colors.WHITE
        elif route == '/search':
            self.downloads_bttn.icon_color = ft.colors.WHITE
            self.search_bttn.icon_color = ft.colors.ORANGE
        self.page.update()
