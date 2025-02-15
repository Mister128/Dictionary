import flet as ft
from flet_route import Routing, path
from pages.page_main import PageMain
from pages.page_add_new_words import PageAddWords
from pages.page_show_words import PageShowWords
from pages.page_trash import PageTrash
from pages.page_settings import PageSettings
from pages.page_dictionary_list import PageDictionayList

class Router:
    def __init__(self, page: ft.Page):
        self.page = page
        self.app_routes = [
            path(url='/', clear=True, view=PageMain().view),
            path(url='/add', clear=False, view=PageAddWords().view),
            path(url='/show', clear=False, view=PageShowWords().view),
            path(url='/trash', clear=False, view=PageTrash().view),
            path(url='/settings', clear=False, view=PageSettings().view),
            path(url='/dictionaries', clear=False, view=PageDictionayList().view)
        ]
        Routing(
            page=self.page,
            app_routes=self.app_routes
        )
        self.page.go(self.page.route)