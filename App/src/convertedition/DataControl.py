from App.storage import app_state

from pathlib import Path
import json
import os

def transformation():

    for file in app_state.EditorPage.viewed_files:
        media = app_state.EditorPage.mediainfo[file]

        for mode in ['video', 'audio', 'subtitle']:
            for track in media[mode]:
                if app_state.CONVERT_PROFILES[media['profile']][mode]:
                    for profile_change in app_state.CONVERT_PROFILES[media['profile']][mode]:

                        command = {}
                        for key in app_state.CONVERT_PROFILES[media['profile']][mode][profile_change]:
                            value = app_state.CONVERT_PROFILES[media['profile']][mode][profile_change][key]

                            if key[0] == '#':
                                continue

                            if key == 'i':
                                value = str(f'{media[mode][track]['path']}')

                            elif key == 'map':
                                value = f'0:{media[mode][track]['index_contain']}'

                            command[f'-{key}'] = str(value) if value else 0

                        
                        savePath = profile_change if profile_change[0] != '#' else media[mode][track]['title']
                        command[f'output'] = (f'{media['output']}/{mode}/{savePath}/{mode}{app_state.FORMAT_TYPES[command['-f']]}')

                        # if command not in media[mode][track]['converted'][quality['name']]:
                        media[mode][track]['converted'][savePath] = command




def editProfiles(key, new_value):
    return


def initialization_profiles():
    Path(f"./UserData/ffmpegProfiles").mkdir(parents=True, exist_ok=True)

    profiles_list = [f for f in os.listdir('./UserData/ffmpegProfiles')]
    for profile in profiles_list:
        with open(f'./UserData/ffmpegProfiles/{profile}', 'r', encoding='utf-8') as file:
            data = json.load(file)
            app_state.CONVERT_PROFILES[data['profile']['name']] = data['profile']



def changeSave():
    return