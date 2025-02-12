import flet as ft
import script
import pages.trash
from flet_route import Params, Basket

class ShowWords:
    def __init__(self):
        self.result_data = None

    def word_edit(self, page, e):
        index = e.control.parent.index
        data = script.get_words()
        edit_word = ft.TextField(label=f'Edit "{data[index]}":', value=data[index], width=200)
        confirm_button = ft.ElevatedButton(
            "Confirm Edit", 
            on_click=lambda _: self.confirm_edit(page, index, edit_word))
        cancel_button = ft.IconButton(
            icon=ft.icons.CLOSE, 
            icon_color=ft.colors.PURPLE, 
            on_click=lambda _: self.cancel_edit(page, index))
        edit_row = ft.Row([edit_word, confirm_button, cancel_button])
        self.result_data.controls[index].controls[1] = edit_row
        page.update()

    def confirm_edit(self, page, index, edit_field):
        new_value = edit_field.value.strip()
        if not new_value:
            return
        old_value = script.get_words()[index]
        script.remove_i_paragraph(old_value)
        script.add(new_value)
        self.result_data.controls[index].controls[2] = ft.Text(script.get_words()[index], size=20, selectable=True)
        self.result_data.controls[index].controls[1] = ft.IconButton(
            icon=ft.icons.CREATE_OUTLINED,
            icon_color=ft.colors.PURPLE,
            on_click=lambda e: self.word_edit(page, e))
        page.update()

    def cancel_edit(self, page, index):
        self.result_data.controls[index].controls[2] = ft.Text(script.get_words()[index], size=20, selectable=True)
        self.result_data.controls[index].controls[1] = ft.IconButton(
            icon=ft.icons.CREATE_OUTLINED,
            icon_color=ft.colors.PURPLE,
            on_click=lambda e: self.word_edit(page, e))
        page.update()

    def word_remove(self, page, e):
        index = e.control.parent.index
        data = script.get_words()
        pages.trash.trash_list.insert(0, data[index])
        while len(pages.trash.trash_list) > 10:
            pages.trash.trash_list.remove(pages.trash.trash_list[-1])
        script.remove_i_paragraph(data[index])
        self.result_data.controls.pop(index)
        page.update()

    #----------------------------------------------------------------------------

    def view(self, page: ft.Page, params, basket: Basket):
        page.title = "Dictionary"
        page.window.height = 800
        page.window.resizable = True

        def search_now(e):
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
                        ft.Text(x, size=20, selectable=True),
                    ])
                    row.index = i
                    self.result_data.controls.append(row)
                page.update()
            else:
                result_con.offset = ft.transform.Offset(-2, 0)
                self.result_data.controls.clear()
                page.update()

        data = script.get_words()

        self.result_data = ft.ListView(height=600, expand=0, spacing=10)

        result_con = ft.Container(
            padding=10,
            margin=10,
            border=ft.border.all(1, ft.colors.PURPLE),
            offset=ft.transform.Offset(-2, 0),
            content=ft.Column([self.result_data]),
        )

        for i, word in enumerate(data):
            result_con.offset = ft.transform.Offset(0, 0)
            row = ft.Row([
                ft.IconButton(
                    icon=ft.icons.DELETE,
                    icon_color=ft.colors.PURPLE,
                    on_click=lambda e: self.word_remove(page, e)),
                ft.IconButton(
                    icon=ft.icons.CREATE_OUTLINED,
                    icon_color=ft.colors.PURPLE,
                    on_click=lambda e: self.word_edit(page, e)),
                ft.Text(word, size=20, selectable=True)
            ], spacing=10)
            row.index = i
            self.result_data.controls.append(row)

        back = ft.IconButton(icon=ft.icons.ARROW_BACK,
                             on_click=lambda e: page.go('/'),
                             icon_color=ft.colors.PURPLE)

        txt_search = ft.TextField(label="Search", on_change=search_now)

        return ft.View(
            "/show",
            controls=[
                back,
                txt_search,
                result_con,
            ],
        )