import flet as ft
from flet_route import Params, Basket
import script
import settings

class PageAddWords:
    def view(self, page: ft.Page, params, basket: Basket):
        page.title = "Add"

        #----------------------------------------------------------------------------

        def add_new(e):
            if add.controls[0].value == '':
                page.open(check_info_alert)
            else:
                new = add.controls[0].value
                script.add_word(new)
                add.controls[0].value = ''
                page.update()

        #----------------------------------------------------------------------------

        back = ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            icon_color=settings.add_word_color,
            on_click=lambda e: page.go('/'))
        
        add = ft.Column([
            ft.TextField(
                label="Enter",
                border_color=settings.add_word_color),
            ft.ElevatedButton(
                text="Add word", 
                color=settings.add_word_color,
                on_click=add_new)
            ])
        
        check_info_alert = ft.AlertDialog(
            title=ft.Row(
                controls=[
                    ft.Icon(ft.icons.WARNING_SHARP,
                            color=settings.add_word_color,
                            size=50),
                    ft.Text("Enter the word!")]
            )
        )
        
        #----------------------------------------------------------------------------

        return ft.View(
            '/add',
            controls=[
                back,
                add
            ]
        )