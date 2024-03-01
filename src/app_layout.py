from bottombar import Bottombar
from search_manager import SearchPage
from downloads_manager import DownloadsPage
import flet as ft


class AppLayout(ft.Column):
    def __init__(self, app, page: ft.Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.page = page
        self.bottombar = Bottombar(app, page)
        self.search = SearchPage(app, page)
        self.downloads = DownloadsPage(app, page)

    def set_favorite_view(self):
        body = self.downloads.build()
        return body

    def set_search_view(self):
        body = self.search.build()
        return body
