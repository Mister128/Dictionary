import flet as ft
from flet_route import Routing, path
from pages.page_main import MainPage
from pages.page_add_new_words import AddWords
from pages.page_show_words import ShowWords
from pages.page_trash import TrashBin
from pages.page_settings import PageSettings

class Router:
    def __init__(self, page: ft.Page):
        self.page = page
        self.app_routes = [
            path(url='/', clear=True, view=MainPage().view),
            path(url='/add', clear=False, view=AddWords().view),
            path(url='/show', clear=False, view=ShowWords().view),
            path(url='/trash', clear=False, view=TrashBin().view),
            path(url='/settings', clear=False, view=PageSettings().view)
        ]
        Routing(
            page=self.page,
            app_routes=self.app_routes
        )
        self.page.go(self.page.route)