import flet as ft
from flet_route import Params, Basket

class MainPage:
    def view(self, page: ft.Page, params, basket: Basket):

        page.title = "Dictionary"
        page.window.width = 500
        page.window.height = 400
        
        #----------------------------------------------------------------------------

        buttons = ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Icon(name=ft.Icons.ADD, color=ft.colors.GREEN, size=35),
                    ft.Text("Add word", size=18)],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center,
                on_click=lambda e: page.go('/add'),
                ink=True,
                ink_color=ft.colors.GREEN,
                width=200,
                height=200,
                border=ft.border.all(1, ft.colors.GREEN),
                border_radius=10),
            ft.Container(
                content=ft.Column([
                    ft.Icon(name=ft.Icons.BOOK, color=ft.colors.PURPLE, size=35),
                    ft.Text("Show words", size=18)],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center,
                on_click=lambda e: page.go('/show'),
                ink=True,
                ink_color=ft.colors.PURPLE,
                width=200,
                height=200,
                border=ft.border.all(1, ft.colors.PURPLE),
                border_radius=10
                ),
            ],
            ft.MainAxisAlignment.CENTER
        )

        trash = ft.Row([ft.Container(content=ft.Text("Trash"),
                        alignment=ft.alignment.center,
                        on_click=lambda e: page.go('/trash'),
                        ink=True,
                        ink_color="#6b6773",
                        width=50,
                        height=50,
                        border=ft.border.all(1, "#6b6773"),
                        border_radius=10)
            ],
            alignment=ft.MainAxisAlignment.END
        )
        #----------------------------------------------------------------------------

        return ft.View(
            '/',
            controls=[buttons, trash]
        )