import flet as ft
from flet_route import Routing, path
from pages.main import MainPage
from pages.add_new_words import AddWords
from pages.show_words import ShowWords
from pages.trash import TrashBin

class Router:
    def __init__(self, page: ft.Page):
        self.page = page
        self.app_routes = [
            path(url='/', clear=True, view=MainPage().view),
            path(url='/add', clear=False, view=AddWords().view),
            path(url='/show', clear=False, view=ShowWords().view),
            path(url='/trash', clear=False, view=TrashBin().view)
        ]
        Routing(
            page=self.page,
            app_routes=self.app_routes
        )
        self.page.go(self.page.route)