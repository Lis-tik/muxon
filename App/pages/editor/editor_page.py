from App.storage import app_state
import App.router as rout
from App.pages.editor.control import UnificationButton, RuleButton, SampleMode, StatusCheck, StatusMediaFlag, ModeButton, addTrack, LangDrop, actTrack, EditingTitle, addMedia, ConvertProfileDrop, EditOutputPath, EditProjName
from App.src.projectsControl.DataControl import saveChange

import flet as ft


def modeCheck():
    if app_state.EditorPage.viewed_uid in app_state.EditorPage.mediainfo[app_state.EditorPage.viewed_files[-1]][app_state.EditorPage.info_mode]:
        app_state.EditorPage.viewed_track = app_state.EditorPage.mediainfo[app_state.EditorPage.viewed_files[-1]][app_state.EditorPage.info_mode][app_state.EditorPage.viewed_uid]
    else:
        app_state.EditorPage.viewed_uid = None

    if not app_state.EditorPage.viewed_uid:
        if app_state.EditorPage.mediainfo[app_state.EditorPage.viewed_files[-1]][app_state.EditorPage.info_mode]:
            return ft.Text('Необходимо выбрать дорожку')
        return ft.Text('Дорожки не обнаружены')
    
    if app_state.EditorPage.info_mode == 'audio':
        return audioChannel()
    elif app_state.EditorPage.info_mode == 'subtitle':
        return subtitleChannel()
    elif app_state.EditorPage.info_mode == 'video':
        return videoChannel()


def command_format(command):
    if not command:
        return
    res = ''
    for cm in command:
        res += f'{cm}, {command[cm]},\n'

    return res



def bashPreview():
    viewed = app_state.EditorPage.mediainfo[app_state.EditorPage.viewed_files[-1]][app_state.EditorPage.info_mode][app_state.EditorPage.viewed_uid]

    if not app_state.EditorPage.mediainfo[app_state.EditorPage.viewed_files[-1]]['profile']:
        return [ft.Text("Не выбран профиль конвертера. Данные будут перенесены без изменений")]
    
    
    
    bash_command = []
    for contain in viewed['converted']:
        cmd = viewed['converted'][contain]

        bash_command.append(
            ft.Container(
                content=ft.Text(
                    value=command_format(cmd),
                    style=ft.TextStyle(
                        font_family="Courier New",
                        size=14,
                        color=ft.Colors.BLACK87,
                        weight=ft.FontWeight.NORMAL
                    )
                ),
                bgcolor=ft.Colors.GREY_100,
                padding=10,
                border_radius=6,
                border=ft.border.all(1, ft.Colors.GREY_400),
                margin=5
            ),
        )


        bash_command.append(                
            ft.Row([
                ft.Text('Путь для сохранения: ', size=15, weight='bold'),
                EditOutputPath(contain)
            ],
            spacing=10,
            run_spacing=10
            )
        )

    return bash_command


def videoChannel():
    return ft.Container(
        ft.Column([
            ft.Text('Общие сведения и метаданные', size=18, weight='bold'),
            ft.Row([
                ft.Text(f"Разрешение сторон:", size=15, weight='bold'),
                ft.Text(f"{app_state.EditorPage.viewed_track['width']}x{app_state.EditorPage.viewed_track['height']}", size=15),
            ]),
            ft.Row([
                ft.Text(f"Кодек:", size=15, weight='bold'),
                ft.Text(f"{app_state.EditorPage.viewed_track['codec_name']}", size=15),
            ]),
            ft.Row([
                ft.Text(f"Индекс в контейнере:", size=15, weight='bold'),
                ft.Text(f"{app_state.EditorPage.viewed_track['index_contain']}", size=15),
            ]),
            ft.Row([
                ft.Text(f"Профиль:", size=15, weight='bold'),
                ft.Text(f"{app_state.EditorPage.viewed_track['profile']}", size=15),
            ]),
            ft.Row([
                ft.Text(f"fps:", size=15, weight='bold'),
                ft.Text(f"{app_state.EditorPage.viewed_track['r_frame_rate']}", size=15),
            ]),
            ft.Row([
                ft.Text(f"Битрейт:", size=15, weight='bold'),
                ft.Text(f"{app_state.EditorPage.viewed_track['bit_rate']}", size=15),
            ]),
            ft.Row([
                ft.Text(f"Количество кадров:", size=15, weight='bold'),
                ft.Text(f"{app_state.EditorPage.viewed_track['nb_frames']}", size=15),
            ]),
            ft.Row([
                ft.Text(f"Тип цветопередачи:", size=15, weight='bold'),
                ft.Text(f"{app_state.EditorPage.viewed_track['pix_fmt']}", size=15),
            ]),
            ft.Row([
                ft.Text(f"Дата добавления:", size=15, weight='bold'),
                ft.Text(f"{app_state.EditorPage.viewed_track['added_date']}", size=15),
            ]),

            ft.Divider(height=1),


            ft.Text('Предварительная команда конвертера', size=18, weight='bold'),
            ft.Column(bashPreview())
        ]),
        expand=True,
        bgcolor=ft.Colors.TRANSPARENT if int(app_state.EditorPage.viewed_track['status']) else ft.Colors.BLACK12
    )


def subtitleChannel():
    return ft.Container(
        ft.Column([
            ft.Row([
                ft.Text("Описание (имя) субтитров:", size=15, weight='bold'),
                EditingTitle()
            ]),
            ft.Row([
                ft.Text(f"Язык субтитров:", size=15, weight='bold'),
                LangDrop(app_state.EditorPage.viewed_track['language']),
            ]),
            ft.Row([
                ft.Text(f"Формат:", size=15, weight='bold'),
                ft.Text(f"{app_state.EditorPage.viewed_track['format']}", size=15),
            ]),
            ft.Row([
                ft.Text(f"Источник:", size=15, weight='bold'),
                ft.Text(f"{app_state.EditorPage.viewed_track['path'] if app_state.EditorPage.viewed_track['path'] else '[в составе контейнера]'}", size=15),
            ]),
            ft.Row([
                ft.Text(f"Дата добавления:", size=15, weight='bold'),
                ft.Text(f"{app_state.EditorPage.viewed_track['added_date']}", size=15),
            ]),
            ft.Divider(height=1),

            ft.Text('Предварительная команда конвертера', size=18, weight='bold'),
            ft.Column(bashPreview())

        ]),
        expand=True,
        bgcolor=ft.Colors.TRANSPARENT if int(app_state.EditorPage.viewed_track['status']) else ft.Colors.BLACK12
    )



def audioChannel():
    return ft.Container(
        ft.Column([
            ft.Row([
                ft.Text("Описание (имя) аудиодорожки:", size=15, weight='bold'),
                EditingTitle()
            ]),
            ft.Row([
                ft.Text(f"Язык аудиодорожки:", size=15, weight='bold'),
                LangDrop(app_state.EditorPage.viewed_track['language']),
            ]),
            ft.Row([
                ft.Text(f"Индекс в контейнере:", size=15, weight='bold'),
                ft.Text(f"{app_state.EditorPage.viewed_track['index_contain']}", size=15),
            ]),
            ft.Row([
                ft.Text(f"Длительность:", size=15, weight='bold'),
                ft.Text(f"{app_state.EditorPage.viewed_track['duration']}", size=15),
            ]),
            ft.Row([
                ft.Text(f"Кодек аудиодорожки:", size=15, weight='bold'),
                ft.Text(f"{app_state.EditorPage.viewed_track['codec_name']}", size=15),
            ]),
            ft.Row([
                ft.Text(f"Количество каналов:", size=15, weight='bold'),
                ft.Text(f"{app_state.EditorPage.viewed_track['channels']}", size=15),
            ]),
            ft.Row([
                ft.Text(f"Битрейт:", size=15, weight='bold'),
                ft.Text(f"{app_state.EditorPage.viewed_track['bit_rate']}", size=15),
            ]),
            ft.Row([
                ft.Text(f"Источник:", size=15, weight='bold'),
                ft.Text(f"{app_state.EditorPage.viewed_track['path'] if app_state.EditorPage.viewed_track['path'] else '[в составе контейнера]'}", size=15),
            ]),
            ft.Row([
                ft.Text(f"Дата добавления:", size=15, weight='bold'),
                ft.Text(f"{app_state.EditorPage.viewed_track['added_date']}", size=15),
            ]),
            ft.Divider(height=1),

            ft.Text('Предварительная команда конвертера', size=18, weight='bold'),
            ft.Column(bashPreview())
        ]),
        expand=True,
        bgcolor=ft.Colors.TRANSPARENT if int(app_state.EditorPage.viewed_track['status']) else ft.Colors.BLACK12
    )

def durationtranslation():
    duration = app_state.EditorPage.mediainfo[app_state.EditorPage.viewed_files[-1]]['duration']
    hours = int(duration // 3600)
    minutes = int((duration % 3600) // 60)
    seconds = int(duration % 60)
    milliseconds = int((duration - int(duration)) * 1000)

    return f"{hours:02}:{minutes:02}:{seconds:02}:{milliseconds:03}"

def GeneralInfo():
    return ft.Container(
        ft.Column([
            addTrack(),
            ft.Text(f'{app_state.EditorPage.viewed_files[-1]}', size=17, weight='bold'),
            ft.Row([
                ft.Text(f"Общая длительность:", size=15, weight='bold'),
                ft.Text(durationtranslation(), size=15),
            ]),
            ft.Row([
                ft.Text(f"Общий битрейт:", size=15, weight='bold'),
                ft.Text(f"{app_state.EditorPage.mediainfo[app_state.EditorPage.viewed_files[-1]]['bitrate']}", size=15),
            ]),
            ft.Row([
                ft.Text(f"Тип файла:", size=15, weight='bold'),
                ft.Text(f"{app_state.EditorPage.mediainfo[app_state.EditorPage.viewed_files[-1]]['extension']} ({app_state.EditorPage.mediainfo[app_state.EditorPage.viewed_files[-1]]['type']})", size=15),
            ]),
            ft.Row([
                ft.Text('Путь для сохранения: ', size=15, weight='bold'),
                EditOutputPath()
            ]),
            ft.Divider(height=1),

            ft.Text('Выбор профиля конвертера', size=18, weight='bold'),
            ConvertProfileDrop()
        ])
    )




def includedButton():
    filesMain = []

    mode_menu = ft.Column([
        ft.Row([
            addMedia(),
            UnificationButton('Режим объединения (BETA)'),
        ]),
        ft.Divider(height=1)
    ])

    filesMain.append(mode_menu)

    filesMain.append(SampleMode())
    
    if app_state.EditorPage.mediainfo:
        for file in app_state.EditorPage.mediainfo:
            loop = ft.Row([
                StatusCheck(file),
                RuleButton(file)
            ])
            filesMain.append(loop)

    return filesMain


def Information():
    return ft.Row(
        controls=[                    
            # Левый блок - список файлов (1/4)
            ft.Container(
                content=ft.Column(
                    controls=includedButton(),
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO,
                ),
                expand=1,  # 1 часть из 4
                border=ft.border.all(1, ft.Colors.GREY_400),
                border_radius=10,
                padding=10,
                margin=ft.margin.symmetric(vertical=10),
            ),
            # Правый блок - метаданные (3/4)
            metaData()
        ],
        expand=True,
        spacing=10,
        vertical_alignment=ft.CrossAxisAlignment.START
    )

def metaData():
    return ft.Container(
        content=ft.Column([
            ft.Divider(height=1),
            ft.Row(   # кнопки сверху
                [
                    ModeButton("Общее", 'general'),
                    ModeButton("Видео", 'video'),
                    ModeButton("Аудио", 'audio'),
                    ModeButton("Субтитры", 'subtitle')
                ],
                alignment="start",
            ),
            ft.Divider(height=1),
            distributionData()
        ],
        scroll=ft.ScrollMode.AUTO,
        ),
        padding=20,
        bgcolor=ft.Colors.BLUE_GREY_50,
        border_radius=15,
        shadow=ft.BoxShadow(blur_radius=2),
        expand=3,
    )



def distributionData():
    if not app_state.EditorPage.viewed_files:
        return ft.Container(
            content=ft.Row([ft.Text("Выберете файл для просмотра информации", size=15)])
        )
    
    content=[]
    if app_state.EditorPage.info_mode != "general":
        content.append(addTrack())
        for tracks in app_state.EditorPage.mediainfo[app_state.EditorPage.viewed_files[-1]][app_state.EditorPage.info_mode]:
            track = ft.Row([
                StatusMediaFlag(str(tracks)),
                actTrack(str(tracks))
            ])
            content.append(track)


    if app_state.EditorPage.info_mode == 'general':
        return GeneralInfo()


    return ft.Container(
        ft.Row([
            ft.Column(content, expand=1),
            ft.Column([modeCheck()], expand=3)
        ], 
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.START)
    )



def get_editor_page():
    saveChange()
    if not app_state.EditorPage:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text('Выберите или создайте новый проект', size=20, weight='bold'),
                    ft.ElevatedButton('Вернуться к менеджеру проектов', on_click=lambda e: app_state.new_page(rout.Projects)),
                ],
                alignment="center",
                horizontal_alignment="center",
            ),
            expand=True,
            alignment=ft.alignment.center  # <-- именно это центрирует весь блок на экране
        )
    

    return ft.Column(
        controls=[
            EditProjName(),
            # ft.Text(app_state.viewed_project, size=20, weight='bold'),
            Information()
        ],
        expand=True,
        spacing=20,
    )

