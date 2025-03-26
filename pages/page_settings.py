import flet as ft
from flet_route import Params, Basket
import settings
import script
import os

class PageSettings:
    def view(self, page: ft.Page, params, basket: Basket):
        page.title = "Settings"
        page.window.height = 710

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
            new_dictionary = settings_view.controls[11].value
            if new_dictionary == '':
                page.open(check_info_alert_void)
            elif f"{new_dictionary}.docx" in settings.files_list():
                page.open(check_info_alert_have_name)
            else:
                script.add_dictionary(new_dictionary)
                settings_view.controls[11].value = ''
                settings_view.controls[7].options.append(ft.dropdown.Option(f"{new_dictionary}.docx"))
                page.update()

        def change_settings_setup(e):
            settings.add_word_color = settings_view.controls[1].value
            settings.show_words_color = settings_view.controls[4].value
            settings.dictionary = settings_view.controls[7].value
            settings.push_changes_to_json()

        def pick_files_result(e: ft.FilePickerResultEvent):
            no_docx = []
            already_have_name = []
            if e.files:
                selected_files = list(map(lambda f: f.path, e.files))
                for f in selected_files:
                    _, extention = os.path.splitext(f)
                    if extention != ".docx":
                        selected_files.remove(f)
                        no_docx.append(os.path.basename(f))
                    if os.path.exists(f"./dictionaries/{os.path.basename(f)}"):
                        selected_files.remove(f)
                        already_have_name.append(os.path.basename(f))
                if not no_docx and not already_have_name:
                    settings.import_docx(selected_files)
                    for file in selected_files:
                        settings_view.controls[7].options.append(ft.dropdown.Option(os.path.basename(file)))
                    page.update()
                else:
                    pass
                    alert_not_good_files(no_docx, already_have_name, selected_files)
            else:
                return

        def alert_not_good_files(no_docx, names, selected_files):
            alert = ft.AlertDialog(
                title=ft.Column(
                    controls=[
                    ft.Icon(ft.icons.WARNING_SHARP,
                            color="#D1D1D1",
                            size=50),
                    ft.Text(f"{', '.join(no_docx)} {'is not .docx' if no_docx else ''}"),
                    ft.Text(f"{', '.join(names)} {'is already exist' if names else ''}")
                ],
                alignment=ft.MainAxisAlignment.CENTER),
                actions=[
                    ft.ElevatedButton("cancel", on_click= lambda e: page.close(alert), color="#D1D1D1"),
                    ft.ElevatedButton("continue without this files", on_click= lambda e: continue_import(selected_files, alert), color="#D1D1D1"),
                ]
            )
            page.open(alert)
        
        def continue_import(selected_files, alert):
            settings.import_docx(selected_files)
            for file in selected_files:
                settings_view.controls[7].options.append(ft.dropdown.Option(os.path.basename(file)))
            page.update()
            page.close(alert)
        
        def export_selected_dictionaries(e):
            dialog_export = ft.AlertDialog(
                modal=True,
                title=ft.Text("Select dictionaries to export:"),
                content=ft.Column([ 
                    *[
                        ft.Checkbox(label=f"{file}", value=False, active_color="#D1D1D1")  
                        for file in settings.files_list()
                    ],
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                text="Cancel",
                                on_click=lambda e: page.close(dialog_export),
                                color="#D1D1D1"
                            ),
                            ft.ElevatedButton(
                                text="Continue",
                                on_click=lambda e: continue_export(dialog_export.content.controls[:-1], dialog_export),
                                color="#D1D1D1"
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END
                    )
                ]),
                actions_alignment=ft.MainAxisAlignment.END
            )
            page.open(dialog_export)

        def continue_export(checkboxes, dialog_export):
            selected_files = [
                checkbox.label
                for checkbox in checkboxes
                if checkbox.value
            ]
            
            if selected_files:
                paths = [f"./dictionaries/{file}" for file in selected_files]
                settings.export_docx(paths)
            
            page.close(dialog_export)
            
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
            ),
            ft.Divider(),
            ft.Row([
                ft.ElevatedButton(text="import", on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=True), color="#D1D1D1"),
                ft.ElevatedButton(text="export", on_click=export_selected_dictionaries, color="#D1D1D1"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            ft.Text("Please choose only '.docx' files. The rest will be missed")
        ])
        
        check_info_alert_void = ft.AlertDialog(
            title=ft.Row(
                controls=[
                    ft.Icon(ft.icons.WARNING_SHARP,
                            color="#D1D1D1",
                            size=50),
                    ft.Text("Enter the name of dictionary!")]
            )
        )

        check_info_alert_have_name = ft.AlertDialog(
            title=ft.Row(
                controls=[
                    ft.Icon(ft.icons.WARNING_SHARP,
                            color="#D1D1D1",
                            size=50),
                    ft.Text("This name is already exist!")]
            )
        )

        pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
        page.overlay.append(pick_files_dialog)
        #----------------------------------------------------------------------------

        for color in settings.colors:
            settings_view.controls[1].options.append(ft.dropdown.Option(color))
            settings_view.controls[4].options.append(ft.dropdown.Option(color))

        for file in settings.files_list():
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