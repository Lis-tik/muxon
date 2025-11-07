from App.storage import app_state
import App.router as rout

import flet as ft


def navigation():
    return ft.Row(
        controls=[
            ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon(ft.Icons.MENU, size=16),
                    ft.Text("Менеджер проектов", size=14),
                ], spacing=8),
                style=ft.ButtonStyle(
                    padding=ft.padding.symmetric(horizontal=16, vertical=12),
                    shape=ft.RoundedRectangleBorder(radius=6),
                ),
                on_click=lambda e: app_state.new_page(rout.Projects),
            ),
            ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon(ft.Icons.DRIVE_FILE_RENAME_OUTLINE, size=16),
                    ft.Text("Редактор контейнера", size=14),
                ], spacing=8),
                style=ft.ButtonStyle(
                    padding=ft.padding.symmetric(horizontal=16, vertical=12),
                    shape=ft.RoundedRectangleBorder(radius=6),
                ),
                on_click=lambda e: app_state.new_page(rout.Editor),
            ),
            ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon(ft.Icons.SETTINGS_SUGGEST, size=16),
                    ft.Text("Профили конвертера", size=14),
                ], spacing=8),
                style=ft.ButtonStyle(
                    padding=ft.padding.symmetric(horizontal=16, vertical=12),
                    shape=ft.RoundedRectangleBorder(radius=6),
                ),
                on_click=lambda e: app_state.new_page(rout.Converter),
            ),
            ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon(ft.Icons.SYNC, size=16),
                    ft.Text("Процесс", size=14),
                ], spacing=8),
                style=ft.ButtonStyle(
                    padding=ft.padding.symmetric(horizontal=16, vertical=12),
                    shape=ft.RoundedRectangleBorder(radius=6),
                ),
                on_click=lambda e: app_state.new_page(rout.Monitoring),
            ),
            ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon(ft.Icons.INFO_OUTLINED, size=16),
                    ft.Text("Информация", size=14),
                ], spacing=8),
                style=ft.ButtonStyle(
                    padding=ft.padding.symmetric(horizontal=16, vertical=12),
                    shape=ft.RoundedRectangleBorder(radius=6),
                ),
                on_click=lambda e: app_state.new_page(rout.Introductory),
            ),
            # ft.ElevatedButton(
            #     content=ft.Row([
            #         ft.Icon(ft.Icons.SETTINGS, size=16),
            #         ft.Text("Настройки", size=14),
            #     ], spacing=8),
            #     opacity=1.0,
            #     style=ft.ButtonStyle(
            #         padding=ft.padding.symmetric(horizontal=16, vertical=12),
            #         shape=ft.RoundedRectangleBorder(radius=6),
            #     ),
            #     on_click=lambda e: app_state.new_page(rout.Settings),
            # ),
        ],
        spacing=8,
        run_spacing=8,
        alignment=ft.MainAxisAlignment.START,
    )