import flet as ft
from flet_route import Params, Basket
import script

trash_list = []

class PageTrash:
    def __init__(self):
        self.trash = None

    def find_and_delete_row_by_text(self, text):
        """Находит и удаляет строку с указанным текстом."""
        for control in self.trash.controls[:]: 
            if isinstance(control, ft.Row) and control.controls[1].value == text:
                self.trash.controls.remove(control)
                break

    def word_add(self, page, e, word):
        if word in trash_list:
            script.add_word(word)
            trash_list.remove(word)
            self.find_and_delete_row_by_text(word) 
            page.update()

    #----------------------------------------------------------------------------

    def view(self, page: ft.Page, params, basket: Basket):
        page.window.height = 600
        page.title = "trash"

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
                              on_click=lambda e, w=word: self.word_add(page, e, w)),
                ft.Text(word, size=20, selectable=True)
                ], spacing=10)
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
