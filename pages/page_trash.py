import flet as ft
from flet_route import Params, Basket
import script

trash_list = []

class PageTrash:
    def __init__(self):
        self.trash = None

    def word_add(self, page, e, word):
        script.add_word(word)
        trash_list.remove(word)
        self.trash.controls.pop(e.control.parent.index)
        page.update()

    #----------------------------------------------------------------------------

    def view(self, page: ft.Page, params, basket: Basket):
        page.window.height = 600
        page.title = "trash"

        #----------------------------------------------------------------------------

        self.trash = ft.ListView(height=400, expand=0, spacing=10, clip_behavior=ft.ClipBehavior.ANTI_ALIAS)

        text = ft.Container(
            content=ft.Text("The last 10 words are stored here and delete when you close app", size=18), 
            height=50,
            alignment=ft.alignment.center)

        trash_container = ft.Container(
            padding=10,
            margin=10,
            border=ft.border.all(1, "#D1D1D1"),
            offset=ft.transform.Offset(-2, 0),
            content=ft.Column([self.trash]),
        )

        back = ft.IconButton(icon=ft.icons.ARROW_BACK, 
                            on_click=lambda e: page.go('/'), 
                            icon_color="#D1D1D1")
        
        #----------------------------------------------------------------------------
        
        for i, word in enumerate(trash_list):
            trash_container.offset = ft.transform.Offset(0, 0)
            row = ft.Row([
                ft.IconButton(icon=ft.icons.REPLAY, 
                              icon_color="#D1D1D1",
                              on_click=lambda _, w=word: self.word_add(page, _, w)),
                ft.Text(word, size=20, selectable=True)
                ], spacing=10)
            row.index = i
            self.trash.controls.append(row)

        #----------------------------------------------------------------------------

        return ft.View(
            "/trash",
            controls=[
                back,
                text,
                trash_container
            ]
        )