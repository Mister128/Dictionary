import flet as ft
from flet_route import Params, Basket
import script

class AddWords:
    def view(self, page: ft.Page, params, basket: Basket):

        page.title = "Add"

        #----------------------------------------------------------------------------

        def add_new(e):
            if add.controls[0].value == '':
                page.open(check_info_alert)
            else:
                new = add.controls[0].value
                script.add(new)
                add.controls[0].value = ''
                page.update()

        #----------------------------------------------------------------------------

        back = ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            icon_color=ft.colors.GREEN,
            on_click=lambda e: page.go('/'))
        
        add = ft.Column([
            ft.TextField(
                label="Enter",
                border_color=ft.colors.GREEN),
            ft.ElevatedButton(
                text="Add word", 
                color=ft.colors.GREEN,
                on_click=add_new)
            ])
        
        check_info_alert = ft.AlertDialog(
            title=ft.Row(
                controls=[
                    ft.Icon(ft.icons.WARNING_SHARP,
                            color=ft.colors.GREEN,
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