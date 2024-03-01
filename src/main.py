from app_layout import AppLayout
import flet as ft


class FreePlayerApp(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.page.on_route_change = self.route_change

    def build(self):
        self.layout = AppLayout(self, self.page)
        return self.layout

    def refresh_downloads(self):
        troute = ft.TemplateRoute(self.page.route)
        if troute.match('/downloads'):
            body = self.layout.set_favorite_view()
            self.page_content.controls[-1] = body
            self.page.update()

    def route_change(self, e):
        troute = ft.TemplateRoute(self.page.route)
        if troute.match('/'):
            self.page.go('/downloads')
        elif troute.match('/downloads'):
            body = self.layout.set_favorite_view()
            self.page_content.controls[-1] = body
        elif troute.match('/search'):
            body = self.layout.set_search_view()
            self.page_content.controls[-1] = body
        self.page.update()

    def initialize(self):
        body = self.layout.set_favorite_view()
        self.page_content = ft.Row(
            controls=[
                body
            ],
            expand=True
            )
        self.page.add(self.page_content)
        self.page.update()
        self.page.go("/")


def main(page: ft.Page):
    page.title = 'Free Player'
    page.window_width = 9 * 45
    page.window_height = 16 * 45
    page.window_resizable = False
    page.window_maximizable = False
    page.window_always_on_top = True
    page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=ft.colors.ORANGE,
            ),
        )
    app = FreePlayerApp(page)
    page.add(app)
    page.update()
    app.initialize()


ft.app(target=main)
