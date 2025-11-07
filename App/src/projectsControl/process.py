from App.storage import app_state
from App.src.manifest.manifestCreator import MakerMPD
from App.src.projectsControl.DataControl import unpackingData

from pathlib import Path
import threading
import subprocess
import os

def processManager():
    process=app_state.PROCESS[app_state.viewed_process]
    app_state.PROCESS[process['index']]['threading'] = threading.Thread(target=start, args=(process,), daemon=True)
    app_state.PROCESS[process['index']]['threading'].start()



    app_state.PROCESS[process['index']]['threading'].join()
    if not app_state.PROCESS[process['index']]['status'] in ['stopped', 'error']:
        app_state.PROCESS[process['index']]['manage'].update_status('finish')


def unpacking():
    for project in app_state.projects:
        app_state.projects[project]


def command_creation(obj):
    cmd = ['ffmpeg']
    for key, value in obj.items():
        if key != 'output':
            cmd.append(key)
        if value:
            cmd.append(str(value))

    return(cmd)



def start(input_process):
    for project in input_process['queue']:
        data = unpackingData(project)

        for series in data:
            media = data[series]
            for mode in ['video', 'audio', 'subtitle']:
                for track in media[mode]:

                    if not media[mode][track]['status']:
                        continue
                    
                    for profile in media[mode][track]['converted']:
                        Path(os.path.dirname(media[mode][track]['converted'][profile]['output'])).mkdir(parents=True, exist_ok=True)
                        cmd = command_creation(media[mode][track]['converted'][profile])
                        
                        process = subprocess.Popen(
                            cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,  # FFmpeg пишет всё в stderr, поэтому перенаправляем
                            text=True,
                            encoding="utf-8",         
                            errors="replace", 
                            bufsize=1,  # Построчная буферизация
                        )

                        # Читаем вывод в реальном времени
                        for line in process.stdout:
                            app_state.PROCESS[input_process['index']]['logs'].append(line)
                            app_state.PROCESS[app_state.viewed_process]['show'].refresh_logs()
                            
                            
                            if any(err in line.lower() for err in ["error", "invalid", "failed", "averror"]):
                                app_state.PROCESS[input_process['index']]['manage'].update_status('error')
                                # return
                            
                            if app_state.PROCESS[input_process['index']]['status'] == 'stopped':
                                app_state.PROCESS[input_process['index']]['logs'].append('ПРОЦЕСС БЫЛ ПРИНУДИТЕЛЬНО ОСТАНОВЛЕН')
                                app_state.PROCESS[app_state.viewed_process]['show'].refresh_logs()
                                return
                            

                        process.stdout.close()   # <-- закрываем поток вручную
                        process.wait()  



            # debugStart = MakerMPD(global_path=media['output'])
            # debugStart.main_control()





