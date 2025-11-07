from App.src.projectsControl.process import processManager
from App.src.projectsControl.DataControl import saveChange
from App.storage import app_state
import App.router as rout

import flet as ft




class ThDrop(ft.Dropdown):
    def __init__(self):
        super().__init__()
        self.value = None
        self.Label = "Добавить новый проект в очередь потока"
        self.hint_text = "+ Выбрать проект"
        self.on_change = self.changeLang
        self.options = []
        
        for project in app_state.projects:
            self.options.append(ft.dropdown.Option(project))


    def changeLang(self, e):
        if not self.value in app_state.PROCESS[app_state.viewed_process]['queue']:
            app_state.PROCESS[app_state.viewed_process]['queue'].append(self.value)

        app_state.new_page(rout.Monitoring)


class activeConvert(ft.ElevatedButton):
    def __init__(self):
        super().__init__(expand=False)
        self.content = ft.Row([
                        ft.Icon(ft.Icons.PLAY_ARROW, size=20, color=ft.Colors.BLUE_700),
                        ft.Text('Запуск')
                    ], tight=True)
        
        self.on_click = self.tracknum

    def control_state(self):
        if app_state.PROCESS[app_state.viewed_process]['status'] != 'stopped':
            return ft.Row([
                        ft.Icon(ft.Icons.PLAY_ARROW, size=20, color=ft.Colors.BLUE_700),
                        ft.Text('Запуск')
                    ], tight=True)
        
        ft.Row([
            ft.Icon(ft.Icons.PAUSE, size=20, color=ft.Colors.BLUE_700),
            ft.Text('Пауза')
        ], tight=True)


    def tracknum(self, e):
        app_state.PROCESS[app_state.viewed_process]['manage'].update_status('running')
        # app_state.PROCESS[app_state.viewed_process]['status'] = 'running'
        saveChange()
        processManager()




class abortConvert(ft.ElevatedButton):
    def __init__(self):
        super().__init__(expand=False)
        self.on_click = self.abort_convert
        self.content = ft.Row([
                        ft.Icon(ft.Icons.STOP, size=20, color=ft.Colors.BLUE_700),
                        ft.Text('Прервать')
                    ], tight=True)
        
    def abort_convert(self, e):
        app_state.PROCESS[app_state.viewed_process]['manage'].update_status('stopped')

        print(app_state.viewed_process, app_state.PROCESS[app_state.viewed_process]['status'])


        

class logWindow(ft.Container):
    def __init__(self, index):
        self.index = index

        # Создаем ListView для логов
        self.list_view = ft.ListView(
            expand=True,
            spacing=1,
            padding=5,
            auto_scroll=False  # автоматически скроллит вниз при добавлении элементов
        )

        super().__init__(
            content=ft.Container(
                content=self.list_view,
                padding=10,
                expand=True,
                bgcolor=ft.Colors.BLUE_GREY_50
            ),
            expand=True,
            padding=10,
        )

    def _get_logs_list(self, limit=20):
        logs_list = app_state.PROCESS[self.index]['logs']
        if isinstance(logs_list, list):
            return logs_list[-limit:] if logs_list else [":"]
        return [str(logs_list)]

    def refresh_logs(self):
        self.list_view.controls.clear()  # очищаем текущий список
        for line in self._get_logs_list():
            self.list_view.controls.append(ft.Text(line, size=12, font_family="Consolas"))

        if self.list_view.page is not None:
            self.list_view.scroll_to(offset=-1, duration=0)
            self.list_view.update()


class queueManage(ft.Container):
    def __init__(self, project, index):
        super().__init__(expand=True)
        self.index = index
        self.project = project
        self.content = ft.Column([
                    ft.Row([
                        ft.ElevatedButton(content=ft.Icon(ft.Icons.DELETE, size=12, color=ft.Colors.BLUE_700), on_click=self.removal),
                        ft.Text(f'{index+1}. {project}', size=12)
                    ]),
                    ft.Divider(height=1)
                ])
        
    def removal(self, e):
        app_state.PROCESS[app_state.viewed_process]['queue'].remove(self.project)
        app_state.new_page(rout.Monitoring)



class ModalThread(ft.Container):
    def __init__(self, index):
        super().__init__(expand=True)
        self.index = index
        self.on_click = self.viewed
        self.status = 'waiting'
        self.progress = ft.Text(0, size=23, weight='bold')
        self.status_label = ft.Text(f"{self.commentmove()}", size=12)

        self.content = ft.Container(
            content=ft.Row([
                    ft.Column(
                    [
                        ft.Text(f"Поток {self.index}", size=15, weight='bold'),
                        ft.Row(
                            [
                                ft.Text('Статус:', size=12, weight='bold'),
                                self.status_label,
                            ],
                            spacing=5,
                        ),
                    ],
                    spacing=5
                ),
                ft.Container(expand=True),
                # self.progress
            ]),
            bgcolor=self.movecolor(),         # мягкий зелёный, не режет глаз
            padding=10,
            border_radius=10,                    # скруглённые края
            ink=True,                            # эффект клика
            on_click=self.on_click,              # если есть метод обработки
            shadow=ft.BoxShadow(blur_radius=4, spread_radius=1, color=ft.Colors.BLACK12),
            margin=ft.margin.only(bottom=8)      # отступ снизу от следующего блока
        )

    def commentmove(self):
        COMMENT = {
            "waiting": 'Ожидает действий',
            "running": 'В процессе',
            "pause": 'Приостановлено',
            "stopped": 'Принудительно завершено',
            "finish": 'Успешное завершение',
            "error": 'Непредвиденная ошибка',
        }

        return COMMENT[self.status]
    
    def movecolor(self):
        STATUS_COLORS = {
            "waiting": ft.Colors.AMBER_100,
            "running": ft.Colors.PURPLE_200,
            "pause": ft.Colors.PURPLE_100,
            "stopped": ft.Colors.PINK_100,
            "finish": ft.Colors.GREEN_100,
            "error": ft.Colors.RED_200,
        }

        return STATUS_COLORS[self.status]
    

    def update_status(self, status):
        app_state.PROCESS[self.index]['status'] = status
        self.status = status

        self.progress.value = app_state.PROCESS[self.index]['progress']
        self.status_label.value = self.commentmove()
        self.content.bgcolor = self.movecolor()
        self.content.update()


    def viewed(self, e):
        app_state.viewed_process = app_state.PROCESS[self.index]['index']
        app_state.new_page(rout.Monitoring)



class ThreadCreat(ft.Container):
    def __init__(self):
        super().__init__(expand=True)
        self.content = ft.Row([
            ft.ElevatedButton('+ Создать поток', on_click=self.create),
            ft.ElevatedButton(content=ft.Icon(ft.Icons.DELETE, size=15, color=ft.Colors.BLUE_700), on_click=self.removal)
        ])



    def create(self, e):
        app_state.PROCESS.append({
            "index": len(app_state.PROCESS),
            "progress": 0,
            "threading": None,
            "queue": [],
            "timeout": 0,
            "manage": ModalThread(len(app_state.PROCESS)),
            "show": logWindow(len(app_state.PROCESS)),
            "logs": [],
            "status": 'waiting'
            })
        
        app_state.new_page(rout.Monitoring)

    def removal(self, e):
        if app_state.PROCESS:
            del app_state.PROCESS[-1]
            app_state.viewed_process = app_state.PROCESS[-1]['index'] if app_state.PROCESS else None

            app_state.new_page(rout.Monitoring)



# class startConvert(ft.ElevatedButton):
#     def __init__(self):
#         super().__init__(expand=True)
#         self.text = '+ Создать поток'project