from App.storage import app_state
import flet as ft


def read_docx():
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Файл README.md не найден."


def Label():
    return ft.Column([
        ft.Text('Добро пожаловать в MUXON', size=20, weight='bold'),
        ft.TextButton(
            content=ft.Text(
                "Официальный GitHub разработчика",
                color="blue",
                size=15
            ),
            on_click=lambda e: app_state.page_control.launch_url(
                "https://github.com/Lis-tik/muxon"
            ),
            style=ft.ButtonStyle(padding=0)
        ),
    ])


def introductory():
    return ft.Container(
        content=ft.Row([          
            ft.Column([
                Label(),
                ft.Markdown(read_docx(), selectable=True)  
            ], spacing=20, scroll="adaptive")               
        ]),
        expand=True
    )
