import flet as ft
import script
import pages.page_trash
import settings
from flet_route import Params, Basket

class PageShowWords:
    def __init__(self):
        self.result_data = None
        self.selected_words = set()
        self.select_all_checkbox = None 

    def toggle_selection(self, page, e):
        """ Handles the selection of words by clicking on a checkbox.
        Adds or removes an index from the set of selected words and updates the page. """

        index = e.control.parent.index
        checkbox = e.control
        if checkbox.value:
            self.selected_words.add(index)
        else:
            self.selected_words.discard(index)
        page.update()

    def toggle_all_selection(self, page, e):
        """ Toggles the selection of all words with a single click.
        Sets the state of every checkbox based on the "Select All" checkbox. """

        all_checked = e.control.value
        checkboxes = [
            control for control in self.result_data.controls
            if isinstance(control, ft.Row) and isinstance(control.controls[0], ft.Checkbox)
        ]
        for checkbox in checkboxes:
            checkbox.controls[0].value = all_checked
        if all_checked:
            self.selected_words.update(range(len(checkboxes)))
        else:
            self.selected_words.clear()
        page.update()

    def bulk_delete(self, page):
        """ Deletes multiple selected words at once. 
        Removes the selected words from the dictionary and adds them to the trash bin. """

        words_to_delete = [script.get_words()[i] for i in sorted(self.selected_words, reverse=True)]
        
        updated_rows = []
        for i, row in enumerate(self.result_data.controls):
            if i not in self.selected_words:
                updated_rows.append(row)
                row.index = len(updated_rows) - 1
        
        self.result_data.controls.clear()
        self.result_data.controls.extend(updated_rows)
        
        for word in words_to_delete:
            script.remove_i_paragraph(word)
            
        pages.page_trash.trash_list.extend(words_to_delete)
        while len(pages.page_trash.trash_list) > 10:
            pages.page_trash.trash_list.remove(pages.page_trash.trash_list[-1])
        self.selected_words.clear()
        page.update()

    def word_edit(self, page, e):
        """ Opens a text field to edit a selected word.
        Allows the user to edit a word through a text input box. """

        index = e.control.parent.index
        data = script.get_words()
        edit_word = ft.TextField(label=f'Edit "{data[index]}":', value=data[index], width=200)
        confirm_button = ft.ElevatedButton(
            "Confirm Edit", 
            color=settings.show_words_color,
            on_click=lambda _: self.confirm_edit(page, index, edit_word))
        cancel_button = ft.IconButton(
            icon=ft.icons.CLOSE, 
            icon_color=settings.show_words_color, 
            on_click=lambda _: self.cancel_edit(page, index))
        edit_row = ft.Row([edit_word, confirm_button, cancel_button])
        self.result_data.controls[index].controls[1] = edit_row
        page.update()

    def confirm_edit(self, page, index, edit_field):
        """ Confirms the changes made to a word.
        Updates the dictionary with the new word and refreshes the UI. """

        new_value = edit_field.value.strip()
        if not new_value:
            return
        old_value = script.get_words()[index]
        script.remove_i_paragraph(old_value)
        script.add_word(new_value)
        self.result_data.controls[index].controls[2] = ft.Text(script.get_words()[index], size=20, selectable=True)
        self.result_data.controls[index].controls[1] = ft.IconButton(
            icon=ft.icons.CREATE_OUTLINED,
            icon_color=settings.show_words_color,
            on_click=lambda e: self.word_edit(page, e))
        page.update()

    def cancel_edit(self, page, index):
        """ Cancels the editing process and reverts back to the original word.
        Resets the word to its initial state and closes the editing window. """

        self.result_data.controls[index].controls[2] = ft.Text(script.get_words()[index], size=20, selectable=True)
        self.result_data.controls[index].controls[1] = ft.IconButton(
            icon=ft.icons.CREATE_OUTLINED,
            icon_color=settings.show_words_color,
            on_click=lambda e: self.word_edit(page, e))
        page.update()

    #----------------------------------------------------------------------------

    def view(self, page: ft.Page, params, basket: Basket):        
        page.title = "Dictionary"
        page.window.height = 850
        page.window.resizable = True

        #----------------------------------------------------------------------------

        def search_now(e):
            """Performs a search operation on the provided text. """
            data = script.get_words()
            my_search = e.control.value
            result = []

            for word in data:
                if my_search in word:
                    result_con.offset = ft.transform.Offset(0, 0)
                    result.append(word)
            page.update()

            if result:
                self.result_data.controls.clear()
                for i, x in enumerate(result):
                    row = ft.Row([
                        ft.Checkbox(value=False, on_change=lambda e: self.toggle_selection(page, e)),
                        ft.Text(x, size=20, selectable=True),
                    ])
                    row.index = i
                    self.result_data.controls.append(row)
                page.update()
            else:
                result_con.offset = ft.transform.Offset(-2, 0)
                self.result_data.controls.clear()
                page.update()

        #----------------------------------------------------------------------------

        data = script.get_words()

        self.result_data = ft.ListView(height=600, expand=0, spacing=10)

        result_con = ft.Container(
            padding=10,
            margin=10,
            border=ft.border.all(1, settings.show_words_color),
            offset=ft.transform.Offset(-2, 0),
            content=ft.Column([self.result_data]),
        )

        self.select_all_checkbox = ft.Checkbox(
            label="Select All",
            value=False,
            active_color=settings.show_words_color,
            on_change=lambda e: self.toggle_all_selection(page, e)
        )

        for i, word in enumerate(data):
            result_con.offset = ft.transform.Offset(0, 0)
            row = ft.Row([
                ft.Checkbox(value=False,
                           active_color=settings.show_words_color, 
                           on_change=lambda e: self.toggle_selection(page, e)),
                ft.IconButton(
                    icon=ft.icons.CREATE_OUTLINED,
                    icon_color=settings.show_words_color,
                    on_click=lambda e: self.word_edit(page, e)),
                ft.Text(word, size=20, selectable=True)
            ], spacing=10)
            row.index = i
            self.result_data.controls.append(row)

        upper_row = ft.Row([
            ft.IconButton(icon=ft.icons.ARROW_BACK,
                         on_click=lambda e: page.go('/'),
                         icon_color=settings.show_words_color),
            ft.IconButton(icon=ft.icons.DELETE,
                         icon_color=settings.show_words_color,
                         on_click=lambda _: self.bulk_delete(page))
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        txt_search = ft.TextField(label="Search", on_change=search_now)

        #----------------------------------------------------------------------------

        return ft.View(
            "/show",
            controls=[
                upper_row,
                txt_search,
                self.select_all_checkbox,
                result_con,
            ],
        )