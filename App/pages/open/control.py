import flet as ft
import App.router as rout
from App.src.projectsControl.DataControl import unpackingData, saveChange
from App.storage import app_state
from App.src.projectsControl.DataControl import saveChange

class ProjManageContainer(ft.Container):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.EDIT, size=24, color=ft.Colors.BLUE_700),
                ft.Column(
                    controls=[
                        ft.Text(self.data, 
                            size=18, 
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK87),
                        # ft.Row([
                        #     ft.Text(f"Последнее изменение:", size=12, color=ft.Colors.GREY_600),
                        #     ft.Text()
                        # ])
                    ],
                    spacing=0,
                ),
            ],
            spacing=10,
        )
        self.padding=ft.padding.all(15)
        self.border=ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.GREY_300))
        self.on_click = self.projectRule

    def projectRule(self, e):
        app_state.viewed_project = self.data
        app_state.EditorPage.mediainfo = unpackingData(self.data)
        app_state.EditorPage.project_name = self.data

        app_state.new_page(rout.Editor)


class dlg_modal(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        self.modal = True

        self.proj_nmae = ft.TextField(label="Имя проекта", width=200)

        
        self.title=ft.Text("Создание проекта")

        self.content = ft.Container(
            content=self.proj_nmae,
            width=220,
            height=80,
            padding=5
        )

        self.actions=[
                ft.TextButton("Создать", on_click=self.create),
                ft.TextButton("Отмена", on_click=lambda e: app_state.page_control.close(self)),
            ]
        self.actions_alignment=ft.MainAxisAlignment.END


    def create(self, e):
        if self.proj_nmae.value:
            app_state.viewed_project = self.proj_nmae.value
            app_state.page_control.close(self)
            app_state.EditorPage.project_name = self.proj_nmae.value

            saveChange()
            app_state.new_page(rout.Editor)
        
