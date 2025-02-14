import flet as ft
from flet_route import Params, Basket
import settings

class PageSettings:
    def view(self, page: ft.Page, params, basket: Basket):
        page.title = "Settings"

        def change_color_add_word(e):
            settings.add_word_color = colors.controls[1].value
            settings.push_changes_to_json()
        
        def change_color_show_words(e):
            settings.show_words_color = colors.controls[4].value
            settings.push_changes_to_json()

        colors = ft.Column([
            ft.Text("Choose the color for 'Add words'"),
            ft.Dropdown(
                    options=[
                        ft.dropdown.Option("purple"),
                        ft.dropdown.Option("green"),
                        ft.dropdown.Option("red"),
                        ft.dropdown.Option("indigo"),
                        ft.dropdown.Option("blue"),
                        ft.dropdown.Option("cyan"),
                        ft.dropdown.Option("amber"),
                        ft.dropdown.Option("orange"),
                        ft.dropdown.Option("yellow"),
                        ft.dropdown.Option("brown")
                    ],
                    label=settings.add_word_color,
                    border_color="#6b6773",
                    on_change=change_color_add_word
                ),
            ft.Divider(),
            ft.Text("Choose the color for 'Show words'"),
            ft.Dropdown(
                    options=[
                        ft.dropdown.Option("purple"),
                        ft.dropdown.Option("green"),
                        ft.dropdown.Option("red"),
                        ft.dropdown.Option("indigo"),
                        ft.dropdown.Option("blue"),
                        ft.dropdown.Option("cyan"),
                        ft.dropdown.Option("amber"),
                        ft.dropdown.Option("orange"),
                        ft.dropdown.Option("yellow"),
                        ft.dropdown.Option("brown")
                    ],
                    label=settings.show_words_color,
                    border_color="#6b6773",
                    on_change=change_color_show_words
                )
        ])

        back = ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            icon_color="#6b6773",
            on_click=lambda e: page.go('/'))


        return ft.View(
            '/settings',
            controls=[
                back,
                colors
            ]
        )