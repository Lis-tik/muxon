from App.src.projectsControl.intelligence import get_intelligence
from App.src.debugcontrol import debug_analysis
from App.storage import app_state

import json
from pathlib import Path
from datetime import datetime



# def autopath(path):
#     for media in app_state.EditorPage.viewed_files: 
#         series_name, ext = os.path.splitext(app_state.EditorPage.mediainfo[media]['name'])
#         app_state.EditorPage.mediainfo[media]['output'] = f'{path}/{app_state.viewed_project} [MUXON]/{series_name}'

#         for mode in ['audio', 'video', 'subtitle']:
#             for track in app_state.EditorPage.mediainfo[media][mode]:
#                 app_state.EditorPage.mediainfo[media][mode][track]['output'] = f'{app_state.EditorPage.mediainfo[media]['output']}/{mode}/'



def add_track(new_data):
    app_state.fixation = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for index, value in enumerate(app_state.EditorPage.viewed_files):
        get_intelligence({"name": value}, new_data[index])


def add_file(data):
    app_state.fixation = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for addData in data:
        # get_intelligence({"name": name, "path": path})
        get_intelligence(addData)



def dataEdit(key, new_value):
    for media in app_state.EditorPage.viewed_files:
        if not (app_state.EditorPage.viewed_uid in app_state.EditorPage.mediainfo[media][app_state.EditorPage.info_mode]):
            print(f"Предупреждение! В файле {media} не обнаружена аудиодорожка с uid [{app_state.EditorPage.viewed_uid}]")
            continue
            
        app_state.EditorPage.mediainfo[media][app_state.EditorPage.info_mode][app_state.EditorPage.viewed_uid][key] = new_value

    debug_analysis()



    # if len(os.listdir(aud_lt)) < len(self.main_data):
    #     print(f'Предупреждение! В директории {aud_lt} с аудио, файлов меньше, чем в основной директории!')


def unpackingData(proj):
    with open(f'./UserData/projects/{proj}/data.json', 'r', encoding='utf-8') as file:
        
        data = json.load(file)
        copy = {}
        for media in data['content']:
            copy[media['name']] = media

        return copy
  
        



def saveChange():
    if (not app_state.EditorPage) or (not app_state.EditorPage.project_name):
        return
    
    data = {
        "name": app_state.EditorPage.project_name,
        "changeData": str(datetime.now()),
        "content": []
    }

    if app_state.EditorPage.mediainfo:
        for cont in app_state.EditorPage.mediainfo:
            data['content'].append(app_state.EditorPage.mediainfo[cont])



    file_path = Path(f"./UserData/projects/{app_state.viewed_project}/data.json")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.touch(exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

