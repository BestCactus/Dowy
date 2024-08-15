from pytubefix import YouTube
import sys
import os
import ffmpeg
import re
import userpaths
import win32clipboard
import pickle

pickle_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dowy_custom_folders.pkl')

# updating internal pickle variable
def update_pickle_variable():
    with open(pickle_path, 'rb') as f:
        global pickle_data
        pickle_data = pickle.load(f)

# updating pickle file on machine
def update_pickle_file():
    with open(pickle_path, 'wb') as f:
        pickle.dump(pickle_data, f)

# Initiating pickle file, first time running script
if not os.path.exists(pickle_path):
    first_pickle_data = {
        'downloads?': userpaths.get_downloads(), 
        'my ?downloads?': userpaths.get_downloads(),
        'down': userpaths.get_downloads(),
        'desktop': userpaths.get_desktop(), 
        'my ?desktop': userpaths.get_desktop(), 
        'desk': userpaths.get_desktop(), 
        'pictures?': userpaths.get_my_pictures(), 
        'my ?pictures?': userpaths.get_my_pictures(),
        'pics?': userpaths.get_my_pictures(),
        'videos': userpaths.get_my_videos(), 
        'my ?videos?': userpaths.get_my_videos(), 
        'vids?': userpaths.get_my_videos(),
        'music': userpaths.get_my_music(),
        'my ?music': userpaths.get_my_music(), 
        'mus': userpaths.get_my_music(),
        'documents?': userpaths.get_my_documents(), 
        'docs?': userpaths.get_my_documents()
    }
    with open(pickle_path, 'wb') as f:
        pickle.dump(first_pickle_data, f)

update_pickle_variable()

def is_syntax_of_key_correct(key):
    return bool(re.fullmatch(r'\w+', key))

def add_or_change_pickle_data(regex, path):
    if regex in pickle_data:
        pickle_data[regex] = path
    else:
        if is_syntax_of_key_correct(regex):
            pickle_data[regex] = path
            print(pickle_data[regex])
        else:
            return False
    update_pickle_file()
    return True

def delete_pickle_key(key):
    if key in pickle_data:
        del pickle_data[key]
    else:
        return False
    update_pickle_file()
    return True

# Clickable link to console
def print_local_file_link(file_path, display_text):
    formatted_path = file_path.replace('\\', '/')
    abs_path = os.path.abspath(formatted_path)
    file_url = f"file:///{abs_path}"
    print(f"\033]8;;{file_url}\033\\{display_text}\033]8;;\033\\")

def print_with_space(msg):
    print('')
    print(msg)
    print('')

def help_page():
    print('Help page')
    print('TODO')

try:
    # Help page
    if re.search('help|-h|--help|-help', sys.argv[2]):
        help_page()
        sys.exit(0)
    # Custom folders settings page
    elif re.search('-f', sys.argv[2]):
        try:
            if sys.argv[3] and sys.argv[4]:
                if add_or_change_pickle_data(sys.argv[3], sys.argv[4]):
                    print('')
                    print('\033[32m' + f'Change/Add of key: {sys.argv[3]} to: {sys.argv[4]} was successfull' + '\033[0m')
                    print('')
                else:
                    print('')
                    print('\033[31m' + 'Invalid characters found in key' + '\033[0m')
                    print('Only letters and numbers are allowed')
                    print('')
        except Exception as e:
            user_input_key = input('Provide a key word to change or add:  ')
            user_input_path = input('Provide a path for the key word:  ').replace('\\', '\\\\')
            if add_or_change_pickle_data(user_input_key, user_input_path):
                print('')
                print('\033[32m' + f'Change/Add of key: {user_input_key} to: {user_input_path} was successfull' + '\033[0m')
                print('')
            else:
                print('')
                print('\033[31m' + 'Invalid characters found in key' + '\033[0m')
                print('Only letters and numbers are allowed')
                print('')
        sys.exit(0)
    # Remove folder settings page
    elif re.search('-rmf', sys.argv[2]):
        try:
            if sys.argv[3]:
                if delete_pickle_key(sys.argv[3]):
                    print('')
                    print('\033[32m' + 'File removed successfully' + '\033[0m')
                    print('')
                else:
                    print('')
                    print('\033[31m' + 'No such key found' + '\033[0m')
                    print('')
        except Exception as e:
            user_input_key = input('Provide a key word to remove:  ')
            if delete_pickle_key(user_input_key):
                print('')
                print('\033[32m' + 'File removed successfully' + '\033[0m')
                print('')
            else:
                print('')
                print('\033[31m' + 'No such key found' + '\033[0m')
                print('')
        sys.exit(0)
# If no args, display help page
except Exception as e:
    help_page()
    sys.exit(0)

# Finding args with regex, so users can put them in whatever order
curr_directory = sys.argv[1] # arg given by .bat file
link_argument = None
resolution_argument = None
dir_argument = None
i = 0
for argument in sys.argv:
    if i < 2:
        i = i + 1
        continue
    link_regex = r'^https://www\.youtube\.com/watch\?v=|https://youtu\.be/|c'
    resolution_regex = "[0-9]+p|4k|2k|full hd|fhd|hd|only audio|audio"
    dir_regex = "[A-Z]:"
    if re.search(link_regex, argument.lower()):
        link_argument = argument
    elif re.search(resolution_regex, argument.lower()):
        resolution_argument = argument
    else:
        for key_regex in pickle_data:
            if re.search(key_regex, argument.lower()):
                dir_argument = pickle_data[key_regex]
                break

i = i + 1

# Youtube video URL or clipboard arg
if link_argument:
    is_youtube_prefix = bool(re.search(r'^https://www\.youtube\.com/watch\?v=|https://youtu\.be/', link_argument))
    is_clipboard_flag = bool(re.search(r'c', link_argument))
    if is_youtube_prefix:
        user_url = link_argument
    elif is_clipboard_flag:
        # accessing clipboard
        win32clipboard.OpenClipboard()
        try:
            user_url = win32clipboard.GetClipboardData()
        except TypeError:
            user_url = None
            print('Cannot access clipboard, please try again')
        win32clipboard.CloseClipboard()
    else:
        # deducting that it is v query value
        user_url = f'https://www.youtube.com/watch?v={link_argument}'
        # Trying to access video to check if link is correct
        try:
            YouTube(user_url).title
        except Exception as e:
            print('Video link or code invalid')
            sys.exit(1)

video = YouTube(user_url)

# divider with size of console window
divider = os.get_terminal_size().columns * "_"

# Main info print
print('')
print(divider)
print('Title:   ', video.title)
print('Author:  ', video.author)

# Length of video converted to minutes and hours
if video.length >= 3600:
    length_hours = video.length // 3600
    length_extra_minutes = video.length % 3600 // 60
    length_extra_seconds = video.length % 60
    if not length_extra_minutes == 0 and not length_extra_seconds == 0:
        print('Length:   ', length_hours, 'h ', length_extra_minutes, 'min ', length_extra_seconds, 's ', sep='')
    elif not length_extra_minutes == 0:
        print('Length:   ', length_hours, 'h ', length_extra_minutes, 'min ', sep='')
    else: 
        print('Length:   ', length_hours, 'h ', sep='')
elif video.length >= 60:
    length_minutes = video.length // 60
    length_extra_seconds = video.length % 60
    if not length_extra_seconds == 0:
        print('Length:   ', length_minutes, 'min ', length_extra_seconds, 's', sep='')
    else:
        print('Length:   ', length_minutes,'min', sep='')


print(divider)
print('')
print('')

# checking available resolutions, not the best way to do so
resolutions = []
if(video.streams.filter(res='2160p')):
    resolutions.append('2160p - 4K')
if(video.streams.filter(res='1440p')):
    resolutions.append('1440p - 2K')
if(video.streams.filter(res='1080p')):
    resolutions.append('1080p - Full HD')
if(video.streams.filter(res='720p')):
    resolutions.append('720p - HD')
if(video.streams.filter(res='480p')):
    resolutions.append('480p - SD')
if(video.streams.filter(res='360p')):
    resolutions.append('360p')
if(video.streams.filter(res='240p')):
    resolutions.append('240p')
if(video.streams.filter(res='144p')):
    resolutions.append('144p')

print('Resolutions:')
for resolution in resolutions:
    print('  ', resolution)
print('\t')

# Checking if user gave resolution arg
video_for_render = None
if resolution_argument:
    user_resolution = resolution_argument
    is_user_resolution_set = True
else:
    is_user_resolution_set = False

def set_video_for_render(resolution):
    if video.streams.filter(res=resolution):
        global video_for_render
        video_for_render = video.streams.filter(res=resolution).first()
        global is_resolution_valid
        is_resolution_valid = True
        return True

# Seting video resolution, with shortcuts
is_resolution_valid = False
while is_resolution_valid == False:
    if(not is_user_resolution_set):
        user_resolution = input('Please select a resolution for render: \t')
    if not set_video_for_render(user_resolution):
        low_case_user_resolution = user_resolution.lower()
        if low_case_user_resolution == '4k':
            set_video_for_render('2160p')
        if low_case_user_resolution == '2k':
            set_video_for_render('1440p')
        if low_case_user_resolution == 'full hd' or low_case_user_resolution == 'fhd':
            set_video_for_render('1080p')
        if low_case_user_resolution == 'hd':
            set_video_for_render('720p')
        if low_case_user_resolution == 'only audio' or low_case_user_resolution == 'audio':
            video_for_render = 'no_video'
            is_resolution_valid = True
        if not video_for_render:
            print_with_space('Invalid resolution')
            user_resolution = None
            is_user_resolution_set = False

windows_temp_path = 'C:\\Windows\\Temp'

#Progress bar func
def on_progress(stream, _chunk, bytes_remaining):
    progress = round((1 - bytes_remaining / stream.filesize) * 100,2)
    print()
    print(f'\rProgress: {progress}% ', f" Megabytes remaining: {round(bytes_remaining/1000000, 2)}MB", end='')
video.register_on_progress_callback(on_progress)


# Setting path for final file, if no path provided, it will set current dir as target
if dir_argument:
        video_destination = dir_argument
else:
    video_destination = curr_directory

# only audio handling - skiping video download
if not video_for_render == 'no_video':
    print_with_space('Video download started')
    video_for_render.download(windows_temp_path, 'dowy_youtube_video.mp4')
    print_with_space('Video download completed')
else:
    print('No video download')

print('Audio download started')
print('\t')

# Audio download if video selected, otherwise download audio and exit
if not video_for_render == 'no_video':
    audio = video.streams.filter(only_audio=True).order_by('abr').last()
    audio.download(windows_temp_path, 'dowy_youtube_audio.opus')
else:
    audio = video.streams.filter(only_audio=True).order_by('abr').last()
    audio.download(video_destination)
    print('Audio processed successfully')
    print_local_file_link(fr"{video_destination}\\{audio.default_filename}", "Open your file")
    sys.exit(0)
print_with_space('Audio download completed')

# Merging video and audio into final file
input_video = ffmpeg.input(f"{windows_temp_path.replace('\\', '/')}/dowy_youtube_video.mp4")
input_audio = ffmpeg.input(f'{windows_temp_path.replace('\\', '/')}/dowy_youtube_audio.opus')
output = ffmpeg.output(input_video, input_audio, f'{video_destination}/{video_for_render.default_filename}.mp4', vcodec='copy', acodec='aac')

print('Compiling started')
output.run(quiet=True, overwrite_output=True)
print('Compiling finished')

# Cleaning up temp files
os.remove(f'{windows_temp_path}\\dowy_youtube_video.mp4')
os.remove(f'{windows_temp_path}\\dowy_youtube_audio.opus')

print_with_space('Video processed successfully')
print_local_file_link(fr"{video_destination}\\{video_for_render.default_filename}.mp4", "Open your file")