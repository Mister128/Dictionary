import flet as ft
from router import Router
import settings
import json

def main(page: ft.Page):
    with open("preset.json") as f:
        data = json.load(f)
        settings.add_word_color = str(data["add_word_color"])
        settings.show_words_color = str(data["show_words_color"])

    page.window.full_screen = False
    page.theme_mode = "dark"
    page.window.resizable = False
    page.window.alignment = ft.alignment.top_center
    Router(page)


if __name__ == '__main__':
    ft.app(target=main)