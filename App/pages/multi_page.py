from App.storage import app_state
import App.router as rout

import flet as ft


def get_page_content():
    return ft.Column(
        controls=[
            ft.Text(f"Это Страница {app_state.page.data}", size=30, weight="bold"),
            ft.Text("Здесь может быть любой контент...", size=16),
            ft.ElevatedButton(
                "Назад",
                on_click=lambda e: app_state.new_page(rout.Page_Home),  # Возврат на главную
            ),
        ],
        alignment="center",
        horizontal_alignment="center",
    )