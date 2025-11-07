# from App.pages.converter.control import 
from App.storage import app_state

import flet as ft


def variant():
    profList = []
    for profile in app_state.CONVERT_PROFILES:
        profList.append(
            ft.ElevatedButton(
                text=profile
            )
        )

    return profList



def converter():
    return ft.Container(
        content=ft.Row([
            ft.Column(variant())
        ])
    )