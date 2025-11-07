from App.storage import app_state

import hashlib
import os

import ffmpeg




def generate_unique_uid(id, prefix=""):
    uid = hashlib.md5(str(id).encode()).hexdigest()
    return f"{prefix}_{uid}" if prefix else uid



def get_intelligence(new_data, inherits=0):

    if not inherits:
        prode_file = f'{new_data['path']}/{new_data['name']}'   
    else:
        prode_file = inherits


    probe = ffmpeg.probe(prode_file)

    # print(probe)
    if not (new_data['name'] in app_state.EditorPage.mediainfo):
        app_state.EditorPage.mediainfo[new_data['name']] = { 
            'name': new_data['name'],
            'path': new_data['path'],
            "extension": (os.path.splitext(prode_file)[1])[1:],
            'type': probe['format']['format_long_name'],
            'duration': float(probe['format']['duration']),
            'bitrate': float(probe['format']['bit_rate']),
            'status': 1,
            'profile': 0,
            'output': '',
            'video': {},
            'audio': {},
            'subtitle': {}
        }



    for stream in probe['streams']:
        if stream['codec_type'] == 'video' and (app_state.EditorPage.info_mode == 'video' or app_state.EditorPage.info_mode == 'general'):
            video_data_add = videostream(stream, prode_file)
            uid = generate_unique_uid(f'{video_data_add['index_contain']}_{app_state.fixation}', 'video')
            app_state.EditorPage.mediainfo[new_data['name']]['video'][uid] = video_data_add

        elif stream['codec_type'] == 'audio' and (app_state.EditorPage.info_mode == 'audio' or app_state.EditorPage.info_mode == 'general'):
            new_audio_chanel = audiostream(stream, prode_file)
            uid = generate_unique_uid(f'{new_audio_chanel['index_contain']}_{new_audio_chanel['title']}_{app_state.fixation}', 'audio')
            app_state.EditorPage.mediainfo[new_data['name']]['audio'][uid] = new_audio_chanel

        elif stream['codec_type'] == 'subtitle' and (app_state.EditorPage.info_mode == 'subtitle' or app_state.EditorPage.info_mode == 'general'):
            new_subtitle_chanel = subtitles(stream, prode_file)
            uid = generate_unique_uid(f'{new_subtitle_chanel['index_contain']}_{new_subtitle_chanel['title']}_{app_state.fixation}', 'subtitle')
            app_state.EditorPage.mediainfo[new_data['name']]['subtitle'][uid] = new_subtitle_chanel






def videostream(stream, path=0):
    data = {
        'width': stream.get('width'),
        'height': stream.get('height'),
        'pix_fmt': stream.get('pix_fmt', 'unknown'),
        'profile': stream.get('profile', 'unknown'),
        'nb_frames': stream.get('nb_frames', 'unknown'),
        'bit_rate': stream.get('bit_rate', 'unknown'),
        'r_frame_rate': eval(stream.get("r_frame_rate", 'unknown')),
        'codec_name': stream.get('codec_name', 'unknown'),
        'index_contain': stream['index'],  
        'added_date': app_state.fixation,
        'status': 1,
        'path': path,
        'subfolder': 1,
        'converted': {}
    }
    return data
    

def audiostream(stream, path=0):
    tags = stream.get('tags', {}) 

    data = {
        'index_contain': stream['index'],  
        'codec_name': stream.get('codec_name', 'unknown'),  
        'language': stream.get('tags', {}).get('language', 'unknown'),  
        'title': tags.get('title', f'unknown'),  
        'channels': stream.get('channels', 'unknown'),  
        'sample_rate': stream.get('sample_rate', 'unknown'), 
        'bit_rate': stream.get('bit_rate', 'unknown'),  
        'duration': stream.get('duration', 'unknown'),  
        'added_date': app_state.fixation,
        'status': 1,
        'path': path,
        'subfolder': 1,
        'converted': {}

    }
    return data

def subtitles(stream, path=0):
    data = {
        'index_contain': stream['index'],  
        'format': stream.get('codec_name', 'unknown'),
        'language': stream.get('tags', {}).get('language', 'unknown'),
        'title':  stream.get('tags', {}).get('title', 'unknown'),
        'forced': int(stream.get('disposition', {}).get('forced', 0) == 1),
        'default': int(stream.get('disposition', {}).get('default', 0) == 1),
        'is_bitmap': int(stream.get('codec_name', '').lower() in ['dvd_subtitle', 'hdmv_pgs_subtitle', 'xsub']),
        'is_text': int(stream.get('codec_name', '').lower() in ['subrip', 'ass', 'ssa', 'mov_text', 'webvtt']),
        'added_date': app_state.fixation,
        'status': 1,
        'path': path,
        'subfolder': 0,
        'converted': {}
    }
    return data
