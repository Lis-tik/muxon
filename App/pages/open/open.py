import flet as ft
from tkinter import Tk, filedialog
from App.storage import app_state
import App.router as rout
import os
from pathlib import Path
# from App.src.projectsControl.DataControl import start_getinfo
from App.src.projectsControl.DataControl import saveChange

from App.pages.open.control import ProjManageContainer, dlg_modal



def open_directory_dialog():
    # Создаем скрытое окно Tkinter
    root = Tk()
    root.withdraw()  # Скрываем основное окно
    root.attributes('-topmost', True)  # Поверх других окон
    
    # Открываем диалог выбора директории
    directory = filedialog.askdirectory(title="Выберите папку")
    

    if directory:  # Если папка выбрана
        app_state.EditorPage.project_name = directory.split('/')[-1]
        Path(f"./UserData/projects/{app_state.EditorPage.project_name}/data.json").mkdir(parents=True, exist_ok=True)


        app_state.viewed_project = app_state.EditorPage.project_name
        # app_state.EditorPage.global_path = directory
        app_state.EditorPage.files = [f for f in os.listdir(directory) if any(f.lower().endswith(fmt) for fmt in app_state.MEDIA_FORMATS)]
        # start_getinfo(directory)

        saveChange()
        app_state.new_page(rout.Editor)


        


def project_header():

    buttonList = []
    buttonList.append(ft.ElevatedButton('Создать новый проект', on_click=lambda e: app_state.page_control.open(dlg_modal())))

    for project in app_state.projects:
        buttonList.append(ProjManageContainer(project))

    return buttonList
    



def projects_library():
    return ft.Column([
            ft.Text("Откройте сохраненный проект или создайте новый!", size=20, weight='bold'),
            ft.Column(project_header())
        ],        
        expand=True,
        spacing=20
    )


def projects_manage():
    Path(f"./UserData/projects").mkdir(parents=True, exist_ok=True)

    for project in [f for f in os.listdir('./UserData/projects')]:
        app_state.projects[project] = {
            'name': 'project',
            'editdate': '',
            'ThStatus': None
        }
    return projects_library()
    


    
        

