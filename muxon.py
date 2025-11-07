from App.storage import app_state
import App.router as rout
from App.src.convertedition.DataControl import initialization_profiles

import asyncio

import flet as ft


def main(page_control: ft.Page):
    page_control.theme_mode = ft.ThemeMode.LIGHT
    app_state.page_control = page_control

    initialization_profiles()

    app_state.new_page(rout.Projects)
    page_control.update()  


    async def mainApp():
        while True:  
            if app_state.transition:
                page_control.title = app_state.page.title
                await control()
                app_state.transition = False
                
            await asyncio.sleep(0.1)


    # Функция переключения страниц
    async def control():
        page_control.controls.clear()

        page_control.add(rout.Navigation.link())
        page_control.add(app_state.page.link())
        page_control.update()

    # Запуск асинхронных задач
    page_control.loop.create_task(mainApp())



    

ft.app(target=main)