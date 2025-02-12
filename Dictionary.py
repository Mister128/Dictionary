import flet as ft
from router import Router

def main(page: ft.Page):
    page.window.full_screen = False
    page.theme_mode = "dark"
    page.window.resizable = False
    page.window.alignment = ft.alignment.top_center
    Router(page)


if __name__ == '__main__':
    ft.app(target=main)