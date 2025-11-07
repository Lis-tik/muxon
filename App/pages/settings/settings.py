from App.pages.settings.control import OptionButton

import flet as ft

def settings():
    return ft.Container(
        ft.Row([
            ft.Column([
                OptionButton('Внешний вид (язык)'),
                OptionButton('Настройки режима «Объединение»')
            ], expand=1),
            ft.Column([
                ft.Text('Какие-то настройки')
            ], expand=3)
        ], expand=True)
    )
