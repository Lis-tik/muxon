import json
import os
from pathlib import Path
from App.storage import app_state





def transformation():

    for file in app_state.EditorPage.viewed_files:
        media = app_state.EditorPage.mediainfo[file]

        for mode in ['video', 'audio', 'subtitle']:
            for track in media[mode]:
                if app_state.CONVERT_PROFILES[media['profile']][mode]:
                    if app_state.CONVERT_PROFILES[media['profile']][mode]['quality']:
                        
                        for quality in app_state.CONVERT_PROFILES[media['profile']][mode]['quality']:
                            if app_state.CONVERT_PROFILES[media['profile']][mode]['quality'][quality]['comment_qual'] <= media[mode][track]['height']:
                                
                                command = {}
                                for key in app_state.CONVERT_PROFILES[media['profile']][mode]['arguments']:
                                    if key == 'OPTIONS':
                                        for option in app_state.CONVERT_PROFILES[media['profile']][mode]['arguments']['OPTIONS']:
                                            command[f'-{option}'] = str(app_state.CONVERT_PROFILES[media['profile']][mode]['arguments']['OPTIONS'][option])

                                    command['-i'] = f'{media['path']}/{media['name']}'
                                    command['-map'] = f'0:{media[mode][track]['index_contain']}'

                                    rule = app_state.CONVERT_PROFILES[media['profile']][mode]['quality'][quality]
                                    for opt in rule:
                                        if opt != 'comment_qual':
                                            command[f'-{opt}'] = str(rule[opt])

                                    if key != 'OPTIONS':
                                        value = app_state.CONVERT_PROFILES[media['profile']][mode]['arguments'][key]
                                        command[f'-{key}'] = str(value) if value else 0


                                command[f'output'] = f'{media['output']}/{mode}/{quality}/{mode}{app_state.FORMAT_TYPES[command['-f']]}'
                                # if command not in media[mode][track]['converted'][quality['name']]:
                                media[mode][track]['converted'][quality] = command
                                    
                    else:
                        command = {
                                    '-i': str(f'{media[mode][track]['path']}'),
                                    '-map': f'0:{media[mode][track]['index_contain']}'
                                }

                        command = {}

                        for key in app_state.CONVERT_PROFILES[media['profile']][mode]['arguments']:
                            value = app_state.CONVERT_PROFILES[media['profile']][mode]['arguments'][key]

                            if key == 'i':
                                value = str(f'{media[mode][track]['path']}')

                            elif key == 'map':
                                value = f'0:{media[mode][track]['index_contain']}'

                            command[f'-{key}'] = str(value) if value else 0

                        command[f'output'] = (f'{media['output']}/{mode}/{media[mode][track]['title']}/{mode}{app_state.FORMAT_TYPES[command['-f']]}')

                        # if command not in media[mode][track]['converted'][quality['name']]:
                        media[mode][track]['converted']['default'] = command




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