from App.storage import app_state
import App.router as rout
from tkinter import Tk, filedialog
from App.src.projectsControl.DataControl import add_track, dataEdit, add_file
from App.src.convertedition.DataControl import transformation

import os
import flet as ft





class ConvertProfileDrop(ft.Dropdown):
    def __init__(self):
        super().__init__()
        self.value = app_state.EditorPage.mediainfo[app_state.EditorPage.viewed_files[-1]]['profile']
        self.hint_text = "Не выбрано!"
        self.options = []
        self.on_change = self.changeProf

        for profile in app_state.CONVERT_PROFILES:
            self.options.append(ft.dropdown.Option(profile))

    def changeProf(self, e):
        for media in app_state.EditorPage.viewed_files:
            app_state.EditorPage.mediainfo[media]['profile'] = self.value

        transformation()
        app_state.new_page(rout.Editor)


class LangDrop(ft.Dropdown):
    def __init__(self, lang):
        super().__init__()
        self.value = lang
        self.Label = "Выберите язык"
        self.hint_text = "Не выбрано!"
        self.on_change = self.changeLang
        self.border_color = ft.Colors.BLUE if self.value in app_state.LANGUAGE_LIST else ft.Colors.RED
        self.options = []
        
        for lang in app_state.LANGUAGE_LIST:
            self.options.append(ft.dropdown.Option(lang, f'{app_state.LANGUAGE_LIST[lang]} [{lang}]'))


    def changeLang(self, e):
        dataEdit('language', self.value)
        app_state.new_page(rout.Editor)


class addMedia(ft.ElevatedButton):
    def __init__(self):
        super().__init__(expand=True)
        self.text = '+ Файл'
        self.on_click = self.tracknum

    def tracknum(self, e):
        files = filedialog.askopenfiles(title="Выберите файл")
        if not files:
            return 

        data = [{"name": os.path.basename(f.name), "path": os.path.dirname(f.name)} for f in files]
        add_file(data)


        app_state.new_page(rout.Editor)

        


class actTrack(ft.ElevatedButton):
    def __init__(self, _uid):
        self._uid = _uid
        super().__init__(expand=True)
        self.text = app_state.EditorPage.mediainfo[app_state.EditorPage.viewed_files[-1]][app_state.EditorPage.info_mode][_uid]['title'] if app_state.EditorPage.info_mode != 'video' else 'video'
        self.on_click = self.tracknum

        self.content = ft.Column(
            controls=[
                ft.Text(self.text, size=15),
                ft.Text(_uid, size=10, color=ft.Colors.GREY),
            ],
            spacing=0,
            tight=True
        )


        self.style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=1),
            bgcolor=(ft.Colors.GREY_300 if self._uid == app_state.EditorPage.viewed_uid else ft.Colors.WHITE),
        )

    def tracknum(self, e):
        app_state.EditorPage.viewed_uid = self._uid
        app_state.new_page(rout.Editor)




class addTrack(ft.ElevatedButton):
    def __init__(self):
        super().__init__()
        self.text = self.messageMode()
        self.on_click = self.open_directory_dialog


    def messageMode(self):

        if app_state.EditorPage.info_mode == 'audio':
            return 'Добавить аудиодорожку'
        elif app_state.EditorPage.info_mode == 'subtitle':
            return 'Добавить субтитры'
        elif app_state.EditorPage.info_mode == 'video':
            return 'Добавить видеодорожку'
        elif app_state.EditorPage.info_mode == 'general':
            return 'Добавить контейнер для слияния'



    def open_directory_dialog(self, e):
        root = Tk()
        root.withdraw()  # Скрываем основное окно
        root.attributes('-topmost', True)  # Поверх других окон
        
        # Открываем диалог выбора директории
        list_cop = []

        if app_state.EditorPage.unification_mode:
            path = filedialog.askdirectory(title="Выберите папку")
            
            docker = [f for f in os.listdir(path) if any(f.lower().endswith(fmt) for fmt in app_state.MEDIA_FORMATS)]
            for meta in docker:

                list_cop.append(f'{path}/{meta}')
        else:
            path = filedialog.askopenfilename(title="Выберите файл")
            list_cop.append(path)


        if list_cop:  # Если папка выбрана
            add_track(list_cop)

        app_state.new_page(rout.Editor)
            



class UnificationButton(ft.ElevatedButton):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.on_click = self.enable_unification_mode

        self.style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=1),
            bgcolor=(ft.Colors.GREY_300 if app_state.EditorPage.unification_mode else ft.Colors.WHITE)
        )

    def enable_unification_mode(self, e):
        app_state.EditorPage.unification_mode = not(app_state.EditorPage.unification_mode)

        if not app_state.EditorPage.unification_mode:
            app_state.EditorPage.viewed_files.clear()
        else:
            app_state.EditorPage.viewed_files.clear()
            for edit in app_state.EditorPage.mediainfo:
                app_state.EditorPage.viewed_files.append(edit)

        app_state.new_page(rout.Editor)


class RuleButton(ft.ElevatedButton):
    def __init__(self, text):
        super().__init__(expand=True)
        self.text = text
        self.on_click = self.modeFunc

        self.viewed = True if self.text in app_state.EditorPage.viewed_files else False

        self.style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=1),
            bgcolor=(ft.Colors.GREY_300 if self.viewed else ft.Colors.WHITE)
            )
    
    def modeFunc(self, e):
        if app_state.EditorPage.unification_mode:
            if not (self.text in app_state.EditorPage.viewed_files):
                app_state.EditorPage.viewed_files.append(self.text)
            else:
                app_state.EditorPage.viewed_files.remove(self.text)
        else:
            app_state.EditorPage.viewed_files = [self.text]
            
        app_state.new_page(rout.Editor)



class EditProjName(ft.Container):
    def __init__(self):
        super().__init__()
        self.active = False
        self.value = app_state.EditorPage.project_name
        self.content = ft.Row(self.processing())


    def on_input_change(self, e):
        self.value = e.control.value

    def processing(self):
        if not self.active:
            return [ft.Text(self.value, size=15, no_wrap=True, overflow=ft.TextOverflow.ELLIPSIS),
                    ft.ElevatedButton(content = ft.Icon(ft.Icons.EDIT, size=15, color=ft.Colors.BLUE_700), on_click=self.remote_active)]
        
        return [self.input_field,
                ft.ElevatedButton(content = ft.Icon(ft.Icons.CHECK, size=15, color=ft.Colors.BLUE_700), on_click=self.remote_active)]
    
    def remote_active(self, e):
        self.active = not(self.active)

        if not self.active:
            app_state.EditorPage.project_name = self.value
            app_state.new_page(rout.Editor)

        self.update()  




class EditOutputPath(ft.Container):
    def __init__(self, rule_name=''):
        super().__init__(expand=True)
        self.rule_name = rule_name
        self.value = self.mode_control()
        self.active = False

        self.input_field = ft.TextField(
            expand=True,
            value=self.value,
            on_change=self.on_input_change,
            autofocus=True,
            dense=True,
            content_padding=ft.padding.all(5),
            border_color=ft.Colors.BLUE,
        )

        self.content = ft.Row(
            controls=[
                self.processing(),
                ft.ElevatedButton(
                        content=ft.Icon(ft.Icons.EDIT, size=15, color=ft.Colors.BLUE_700),
                        on_click=self.remote_active
                    ),
                    ft.ElevatedButton(
                        content=ft.Icon(ft.Icons.FOLDER, size=15, color=ft.Colors.BLUE_700),
                        on_click=self.remote_path
                    ),
                      ],
            spacing=10,
            expand=True
        )

    def remote_active(self, e):
        return
    
    def remote_path(self, e):
        return

    def shorten_path(self, text, max_len=60):
        if len(text) <= max_len:
            return text
        return "..." + text[-max_len:]

    def on_input_change(self, e):
        self.value = e.control.value

    def processing(self):
        if not self.active:

            return ft.Container(
                content=ft.Text(
                    self.shorten_path(self.value) if self.value else "None",
                    no_wrap=True,
                    overflow=ft.TextOverflow.ELLIPSIS,
                )
            )
        
        return ft.Container(
                    content=self.input_field,
                    expand=True
                )

    def mode_control(self):
        if app_state.EditorPage.info_mode != 'general':
            return app_state.EditorPage.mediainfo[app_state.EditorPage.viewed_files[-1]][app_state.EditorPage.info_mode][app_state.EditorPage.viewed_uid]['converted'][self.rule_name]['output']
        
        return app_state.EditorPage.mediainfo[app_state.EditorPage.viewed_files[-1]]['output']
    



class EditingTitle(ft.Container):
    def __init__(self):
        super().__init__()
        self.state = app_state.EditorPage.mediainfo[app_state.EditorPage.viewed_files[-1]][app_state.EditorPage.info_mode][app_state.EditorPage.viewed_uid]
        self.value = self.state['title']
        self.active = False
        self.border_color = ft.Colors.BLUE if self.value else ft.Colors.RED

        self.input_field = ft.TextField(
            value=self.value,
            on_change=self.on_input_change,
            autofocus=True,
            dense=True,
            content_padding=ft.padding.all(5),
            border_color=ft.Colors.BLUE
        )


        self.content = ft.Row(
            controls=self.processing(),
            spacing=10,
            expand=True
        )



    def on_input_change(self, e):
        self.value = e.control.value

    def processing(self):
        if not self.active:
            return [ft.Text(self.value, size=15, no_wrap=True, overflow=ft.TextOverflow.ELLIPSIS),
                    ft.ElevatedButton(content = ft.Icon(ft.Icons.EDIT, size=15, color=ft.Colors.BLUE_700), on_click=self.remote_active)]
        
        return [self.input_field,
                ft.ElevatedButton(content = ft.Icon(ft.Icons.CHECK, size=15, color=ft.Colors.BLUE_700), on_click=self.remote_active)]
    
    def remote_active(self, e):
        if not self.value:
            return
        
        self.active = not(self.active)
        self.content.controls = self.processing()
        
        if not self.active:
            dataEdit('title', self.value)
            # change_output(self.value)

            
            app_state.new_page(rout.Editor)

        self.update()
        
class SubfolderCheck(ft.Checkbox):
    def __init__(self):
        super().__init__()
        self.value = app_state.EditorPage.mediainfo[app_state.EditorPage.viewed_files[-1]][app_state.EditorPage.info_mode][app_state.EditorPage.viewed_uid]['subfolder']


class SampleMode(ft.Checkbox):
    def __init__(self):
        super().__init__()
        self.on_change = self.SampleModeFunc
        self.value = self.check()


    def check(self):
        for media in app_state.EditorPage.mediainfo:
            if not app_state.EditorPage.mediainfo[media]['status']:
                return False
        return True

 
    def SampleModeFunc(self, e):
        for media in app_state.EditorPage.mediainfo:
            app_state.EditorPage.mediainfo[media]['status'] = self.value

        app_state.new_page(rout.Editor)


class StatusCheck(ft.Checkbox):
    def __init__(self, file):
        super().__init__()
        self.file = file
        self.on_change = self.SampleModeFunc
        self.value = bool(app_state.EditorPage.mediainfo[self.file]['status']) 

    def SampleModeFunc(self, e):
        app_state.EditorPage.mediainfo[self.file]['status'] = int(not(app_state.EditorPage.mediainfo[self.file]['status']))
        app_state.new_page(rout.Editor)

        

class StatusMediaFlag(ft.Checkbox):
    def __init__(self, _uid):
        super().__init__()
        self._uid = _uid
        self.on_change = self.dataCheck
        self.value = bool(int(app_state.EditorPage.mediainfo[app_state.EditorPage.viewed_files[-1]][app_state.EditorPage.info_mode][self._uid]['status']))

    def dataCheck(self, e):
        for edit in app_state.EditorPage.viewed_files:
            app_state.EditorPage.mediainfo[edit][app_state.EditorPage.info_mode][self._uid]['status'] = not(bool(app_state.EditorPage.mediainfo[edit][app_state.EditorPage.info_mode][self._uid]['status']))
        app_state.new_page(rout.Editor)

        
     

class ModeButton(ft.ElevatedButton):
    def __init__(self, text, mode):
        super().__init__()
        self.text = text
        self.mode = mode
        self.on_click = self.infoModeTool

        self.active = True if app_state.EditorPage.info_mode == self.mode else False

        self.style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=1),
            bgcolor=(ft.Colors.GREY_300 if self.active else ft.Colors.WHITE)
            )
    

    def infoModeTool(self, e):
        app_state.EditorPage.info_mode = self.mode
        app_state.new_page(rout.Editor)


