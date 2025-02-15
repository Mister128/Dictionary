import flet as ft
from flet_route import Params, Basket
import settings
import script
import os

class PageSettings:
    def view(self, page: ft.Page, params, basket: Basket):
        page.title = "Settings"
        page.window.height = 700

        #----------------------------------------------------------------------------

        def theme_changed(e):
            page.theme_mode = (
                "dark"
                if page.theme_mode == "light"
                else "light"
            )
            settings.theme = page.theme_mode
            settings.push_changes_to_json()
            e.control.selected = not e.control.selected
            e.control.update()
            page.update()

        def add_new_dictionary(e):
            if settings_view.controls[11].value == '':
                page.open(check_info_alert)
            else:
                new_dictionary = settings_view.controls[11].value
                script.add_dictionary(new_dictionary)
                settings_view.controls[11].value = ''
                settings_view.controls[7].options.append(ft.dropdown.Option(f"{new_dictionary}.docx"))
                page.update()

        def change_settings_setup(e):
            settings.add_word_color = settings_view.controls[1].value
            settings.show_words_color = settings_view.controls[4].value
            settings.dictionary = settings_view.controls[7].value
            settings.push_changes_to_json()
        
        #----------------------------------------------------------------------------

        upper_row = ft.Row([
            ft.IconButton(
                icon=ft.icons.ARROW_BACK,
                icon_color="#D1D1D1",
                on_click=lambda e: page.go('/')),
            ft.IconButton(
                        icon=ft.icons.DARK_MODE,
                        selected_icon=ft.icons.SUNNY,
                        on_click=theme_changed,
                        selected=False,
                        style=ft.ButtonStyle(color={"selected": "#D1D1D1", "": "#D1D1D1"})
                    ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        settings_view = ft.Column([
            ft.Text("Choose the color for 'Add words'"),
            ft.Dropdown( #1
                    border_color="#D1D1D1",
                    on_change=change_settings_setup,
                    value=settings.add_word_color
                ), 
            ft.Divider(),
            ft.Text("Choose the color for 'Show words'"),
            ft.Dropdown( #4
                    border_color="#D1D1D1",
                    on_change=change_settings_setup,
                    value=settings.show_words_color
                ), 
            ft.Divider(),
            ft.Text("Choose your dictionary"),
            ft.Dropdown( #7
                border_color="#D1D1D1",
                on_change=change_settings_setup,
                value=settings.dictionary
            ), 
            ft.ElevatedButton(
                text="Show dictionary list",
                on_click=lambda e: page.go("/dictionaries"),
                color="#D1D1D1",
            ),
            ft.Divider(),
            ft.Text("Or create a new dictionary"),
            ft.TextField( #11
                label="Create new dictionary",
                border_color="#D1D1D1",
                suffix_text=".docx"), 
            ft.ElevatedButton(
                text="Create dictionary",
                on_click=add_new_dictionary,
                color="#D1D1D1"
            )
        ])
        
        check_info_alert = ft.AlertDialog(
            title=ft.Row(
                controls=[
                    ft.Icon(ft.icons.WARNING_SHARP,
                            color=settings.add_word_color,
                            size=50),
                    ft.Text("Enter the name of dictionary!")]
            )
        ) 

        #----------------------------------------------------------------------------

        for color in settings.colors:
            settings_view.controls[1].options.append(ft.dropdown.Option(color))
            settings_view.controls[4].options.append(ft.dropdown.Option(color))

        for file in settings.files_list("./dictionaries"):
            if ".docx" in file:
                settings_view.controls[7].options.append(ft.dropdown.Option(file))

        #----------------------------------------------------------------------------

        return ft.View(
            '/settings',
            controls=[
                upper_row,
                settings_view
            ]
        )