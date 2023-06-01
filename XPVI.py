import os
import sys
import re
from subprocess import Popen, PIPE, STDOUT
try:
    from subprocess import CREATE_NO_WINDOW
except:
    CREATE_NO_WINDOW = None

scripts_dir = os.path.dirname(
    os.path.realpath(
        sys.executable
    )
)

def __raw_video_device_data():
    has_ffmpeg = True
    try:
        proc = Popen(['ffmpeg', '-version'],
                     creationflags=CREATE_NO_WINDOW, stderr=STDOUT,
                     stdout=PIPE)
    except:
        try:
            proc = Popen(['ffmpeg', '-version'],
                         stderr=STDOUT, stdout=PIPE)
        except:
            has_ffmpeg = False
    if not has_ffmpeg:
        raise RuntimeError('ffmpeg not found')
    formats = [
        'alsa',
        'android_camera',
        'avfoundation',
        'bktr',
        'decklink',
        'dshow',
        'fbdev',
        'gdigrab',
        'iec61883',
        'jack',
        'kmsgrab',
        'lavfi',
        'libcdio',
        'libdc1394',
        'openal',
        'oss',
        'pulse',
        'sndio',
        'video4linux2',
        'v4l2',
        'vfwcap',
        'x11grab',
    ]
    raw_video_device_data = ''
    for fmt in formats:
        try:
            raw_video_device_data += Popen(
                [
                    'ffmpeg',
                    '-f',
                    fmt,
                    '-list_devices',
                    'true',
                    '-i',
                    'x'
                ],
                creationflags=CREATE_NO_WINDOW,
                stderr=STDOUT, stdout=PIPE
            ).communicate()[0].decode('utf-8') + '\n'
        except:
            raw_video_device_data += Popen(
                [
                    'ffmpeg',
                    '-f',
                    fmt,
                    '-list_devices',
                    'true',
                    '-i',
                    'x'
                ],
                stderr=STDOUT, stdout=PIPE
            ).communicate()[0].decode('utf-8') + '\n'
    return raw_video_device_data

def __find_devices(kind):
    matches = re.findall(r'"(.+)"\s+\(' + kind + '\)', __raw_video_device_data())
    return matches

def get_all_video_devices():
    return list(enumerate(__find_devices('video')))

def get_all_audio_devices():
    return list(enumerate(__find_devices('audio')))

def get_id_from_video_device(name):
    ID = -1
    for device in get_all_video_devices():
        if device[1] == name:
            ID = device[0]
            break
    return ID

def get_id_from_audio_device(name):
    ID = -1
    for device in get_all_audio_devices():
        if device[1] == name:
            ID = device[0]
            break
    return ID

def get_video_device_from_id(ID):
    name = ""
    for device in get_all_video_devices():
        if device[0] == ID:
            name = device[1]
            break
    return name

def get_audio_device_from_id(ID):
    name = ""
    for device in get_all_audio_devices():
        if device[0] == ID:
            name = device[1]
            break
    return name

global env
env = {}

def save_env():
    global env
    if os.path.exists(os.path.join(scripts_dir, 'XPVI.env')):
        os.remove(os.path.join(scripts_dir, 'XPVI.env'))
    with open(os.path.join(scripts_dir, 'XPVI.env'), 'w') as fp:
        fp.write(str(env))

def load_env():
    global env
    if not os.path.exists(os.path.join(scripts_dir, 'XPVI.env')):
        save_env()
    with open(os.path.join(scripts_dir, 'XPVI.env'), 'r') as fp:
        env = eval(fp.read())

load_env()

if __name__ == '__main__':
    __raw_video_device_data()
    if len(sys.argv) == 2 and sys.argv[1] == 'v*':
        print(get_all_video_devices())
    elif len(sys.argv) == 2 and sys.argv[1] == 'a*':
        print(get_all_audio_devices())
    elif len(sys.argv) == 3 and sys.argv[1] == 'v2i':
        if os.path.exists(sys.argv[2]):
            print(sys.argv[2])
        else:
            print(str(get_id_from_video_device(sys.argv[2])))
    elif len(sys.argv) == 3 and sys.argv[1] == 'a2i':
        if os.path.exists(sys.argv[2]):
            print(sys.argv[2])
        else:
            print(str(get_id_from_audio_device(sys.argv[2])))
    elif len(sys.argv) == 3 and sys.argv[1] == 'i2v':
        if os.path.exists(sys.argv[2]):
            print(sys.argv[2])
        else:
            try:
                print(get_video_device_from_id(int(sys.argv[2])))
            except:
                pass
    elif len(sys.argv) == 3 and sys.argv[1] == 'i2a':
        if os.path.exists(sys.argv[2]):
            print(sys.argv[2])
        else:
            try:
                print(get_audio_device_from_id(int(sys.argv[2])))
            except:
                pass
    elif len(sys.argv) == 5 and sys.argv[1] == 'set':
        ID = str(get_id_from_video_device(sys.argv[2]))
        if os.path.exists(sys.argv[2]):
            ID = sys.argv[2]
        if ID == '-1':
            ID = str(get_id_from_audio_device(sys.argv[2]))
        if ID == '-1':
            print('Error@DeviceName')
        elif sys.argv[3] is None or len(sys.argv[3]) == 0:
            print('Error@Key')
        elif str(sys.argv[4]) == 'NULL':
            env.pop(sys.argv[2] + '\\' + sys.argv[3])
            save_env()
        else:
            env[sys.argv[2] + '\\' + sys.argv[3]] = str(sys.argv[4])
            save_env()
    elif len(sys.argv) == 4 and sys.argv[1] == 'get':
        ID = str(get_id_from_video_device(sys.argv[2]))
        if os.path.exists(sys.argv[2]):
            ID = sys.argv[2]
        if ID == '-1':
            ID = str(get_id_from_audio_device(sys.argv[2]))
        if ID == '-1':
            print('Error@DeviceName')
        elif sys.argv[3] is None or len(sys.argv[3]) == 0:
            print('Error@Key')
        else:
            load_env()
            if sys.argv[3] == 'ALL':
                tmp1 = [k for k in env if k.startswith(sys.argv[2] + '\\')]
                tmp2 = {}
                for tmp in tmp1:
                    tmp2[tmp] = env[tmp]
                print(str(tmp2))
            else:
                print(str(env[sys.argv[2] + '\\' + sys.argv[3]]))
    else:
        print('syntax:')
        print('v* (get_all_video_devices)')
        print('a* (get_all_audio_devices)')
        print('v2i name (get_id_from_video_device)')
        print('a2i name (get_id_from_audio_device)')
        print('i2v id (get_video_device_from_id)')
        print('i2a id (get_audio_device_from_id)')
        print('set name key value (set_value)')
        print('set name key "NULL" (delete_key)')
        print('get name key (get_value)')
        print('get name "ALL" (get_values)')
else:
    print("Error: Apps should use the XPVI cli")
