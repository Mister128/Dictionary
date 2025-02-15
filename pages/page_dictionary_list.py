import flet as ft
from flet_route import Params, Basket
import os
import settings


class PageDictionayList:
    def __init__(self):
        self.result_data = None
        self.selected_files = set()
        self.select_all_checkbox = None

    def toggle_selection(self, page, e):
        """Handles the selection of files by clicking on a checkbox. 
        Adds or removes an index from the set of selected files and updates the page."""

        index = e.control.parent.index
        checkbox = e.control
        if checkbox.value:
            self.selected_files.add(index)
        else:
            self.selected_files.discard(index)
        page.update()

    def toggle_all_selection(self, page, e):
        """Toggles the selection of all files with a single click. 
        Sets the state of every checkbox based on the "Select All" checkbox."""

        all_checked = e.control.value
        checkboxes = [
            control for control in self.result_data.controls
            if isinstance(control, ft.Row) and isinstance(control.controls[0], ft.Checkbox)
        ]
        for checkbox in checkboxes:
            checkbox.controls[0].value = all_checked
        if all_checked:
            self.selected_files.update(range(len(checkboxes)))
        else:
            self.selected_files.clear()
        page.update()

    def bulk_delete(self, page):
        """Deletes multiple selected files at once. 
        Removes the selected files from the folder."""

        files_to_delete = [settings.files_list('./dictionaries')[i] for i in sorted(self.selected_files, reverse=True)]

        updated_rows = []
        for i, row in enumerate(self.result_data.controls):
            if i not in self.selected_files:
                updated_rows.append(row)
                row.index = len(updated_rows) - 1

        self.result_data.controls.clear()
        self.result_data.controls.extend(updated_rows)

        for filename in files_to_delete:
            settings.delete_file(filename)

        self.selected_files.clear()
        page.update()

    def file_edit(self, page, e):
        """Opens a text field to edit a selected file name. 
        Allows the user to edit a file name through a text input box."""

        index = e.control.parent.index
        filename = settings.files_list('./dictionaries')[index]
        edit_filename = ft.TextField(label=f'Edit "{filename}":', value=filename[:-5], width=200)
        confirm_button = ft.ElevatedButton(
            "Confirm Edit",
            color="#D1D1D1",
            on_click=lambda _: self.confirm_edit(page, index, edit_filename))
        cancel_button = ft.IconButton(
            icon=ft.icons.CLOSE,
            icon_color="#D1D1D1",
            on_click=lambda _: self.cancel_edit(page, index))
        edit_row = ft.Row([edit_filename, confirm_button, cancel_button])
        self.result_data.controls[index].controls[1] = edit_row
        page.update()

    def confirm_edit(self, page, index, edit_field):
        """Confirms the changes made to a file name. 
        Updates the file name and refreshes the UI."""

        new_value = edit_field.value.strip()
        if not new_value:
            return
        old_filename = settings.files_list('./dictionaries')[index]
        settings.rename_file(old_filename, new_value)
        self.result_data.controls[index].controls[2] = ft.Text(new_value + '.docx', size=20, selectable=True)
        self.result_data.controls[index].controls[1] = ft.IconButton(
            icon=ft.icons.CREATE_OUTLINED,
            icon_color="#D1D1D1",
            on_click=lambda e: self.file_edit(page, e))
        page.update()

    def cancel_edit(self, page, index):
        """Cancels the editing process and reverts back to the original file name. 
        Resets the file name to its initial state and closes the editing window."""

        filename = settings.files_list('./dictionaries')[index]
        self.result_data.controls[index].controls[2] = ft.Text(filename, size=20, selectable=True)
        self.result_data.controls[index].controls[1] = ft.IconButton(
            icon=ft.icons.CREATE_OUTLINED,
            icon_color="#D1D1D1",
            on_click=lambda e: self.file_edit(page, e))
        page.update()

    #----------------------------------------------------------------------------

    def view(self, page: ft.Page, params, basket: Basket):
        page.title = "Dictionary Files"
        
        files = settings.files_list('./dictionaries')

        upper_row = ft.Row([
            ft.IconButton(icon=ft.icons.ARROW_BACK,
                          on_click=lambda e: page.go('/settings'),
                          icon_color="#D1D1D1"),
            ft.IconButton(icon=ft.icons.DELETE,
                          icon_color="#D1D1D1",
                          on_click=lambda _: self.bulk_delete(page))
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        self.result_data = ft.ListView(height=470, expand=0, spacing=10)

        result_con = ft.Container(
            padding=10,
            margin=10,
            border=ft.border.all(1, "#D1D1D1"),
            content=ft.Column([self.result_data]),
        )

        self.select_all_checkbox = ft.Checkbox(
            label="Select All",
            value=False,
            active_color="#D1D1D1",
            on_change=lambda e: self.toggle_all_selection(page, e)
        )

        bottom = ft.Text(
            "Be careful when you delete the dictionary. It is FOREVER!",
            size=18)

        #----------------------------------------------------------------------------

        for i, filename in enumerate(files):
            row = ft.Row([
                ft.Checkbox(value=False,
                            active_color="#D1D1D1",
                            on_change=lambda e: self.toggle_selection(page, e)),
                ft.IconButton(
                    icon=ft.icons.CREATE_OUTLINED,
                    icon_color="#D1D1D1",
                    on_click=lambda e: self.file_edit(page, e)),
                ft.Text(filename, size=20, selectable=True)
            ], spacing=10)
            row.index = i
            self.result_data.controls.append(row)

        #----------------------------------------------------------------------------

        return ft.View(
            '/dictionaries',
            controls=[
                upper_row,
                self.select_all_checkbox,
                result_con,
                bottom
            ]
        )