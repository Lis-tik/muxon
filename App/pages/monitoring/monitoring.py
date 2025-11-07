from App.pages.monitoring.control import activeConvert, abortConvert, ModalThread, ThreadCreat, ThDrop, queueManage
from App.storage import app_state

import flet as ft


def accessThread():
    if not app_state.PROCESS:
        return ft.Text('Создайте поток')
    
    Tlist = []
    for thread in app_state.PROCESS:
        Tlist.append(thread['manage'])

    return ft.Column(Tlist)


def thread_menu():
    return ft.Container(
        content=ft.Column(
            [
                ThreadCreat(),
                accessThread()
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,            # растягиваем по вертикали
            alignment="start",      # прижимаем к верху
        ),
        bgcolor=ft.Colors.BLUE_GREY_50,
        shadow=ft.BoxShadow(blur_radius=2),
        padding=20,
        border_radius=15,
        expand=2,               # растягиваем весь контейнер
    )

def queuecalculation():
    if not app_state.PROCESS[app_state.viewed_process]['queue']:
        return ft.Text('Нет проектов в очереди', size=15)
    
    Tlist = []
    for index, project in enumerate(app_state.PROCESS[app_state.viewed_process]['queue']):
        Tlist.append(queueManage(project, index))
    
    return ft.Column(Tlist)


def info():
    if app_state.viewed_process == None:
        return ft.Container(
            ft.Text('Не выбран поток'),
            expand=6,
        )

    
    return ft.Container(
        content=ft.Column(
            [
                ft.Text((f'Процесс {app_state.viewed_process}'), size=20),

                ft.Column([
                    ft.Row([
                        ft.Text('Добавить проект в очередь потока', size=15, weight='bold'),
                        ThDrop()
                    ]),
                    queuecalculation()
                ]),
                ft.Row([
                    activeConvert(),
                    abortConvert()
                ]),
                app_state.PROCESS[app_state.viewed_process]['show']
            ],
            expand=True,
            alignment="start",
        ),
        expand=6,
    )

def monitoring():
    return ft.Row(
        [
            thread_menu(),
            info(),
        ],
        expand=True,                # растягиваем весь ряд
        vertical_alignment="start", # прижимаем к верху
    )
