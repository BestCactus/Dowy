from pytubefix import YouTube
import sys
import os
from ffmpeg import FFmpeg
import re
import userpaths
import win32clipboard
import pickle
from tabulate import tabulate
from shutil import which
def main():
    os.system('')
    # Print colors strings
    print_red = '\033[31m'
    print_green = '\033[32m'
    print_yellow = '\033[33m'
    print_blue = '\033[1;34m'
    print_cyan = '\033[36m'
    print_purple = '\033[1;35m'

    print_bold = '\033[1;37m'
    print_underline = '\033[4;37m'

    print_reset = '\033[0m'

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

    def reset_pickle_file():
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

    # Initiating pickle file, first time running script
    if not os.path.exists(pickle_path):
        reset_pickle_file()

    update_pickle_variable()

    def is_syntax_of_key_correct(key):
        return bool(re.fullmatch(r'\w+', key))

    def add_or_change_pickle_data(regex, path):
        if regex in pickle_data:
            pickle_data[regex] = path.replace('/', '\\')
        else:
            if is_syntax_of_key_correct(regex):
                pickle_data[regex] = path.replace('/', '\\')
                print(pickle_data[regex])
            else:
                return False
        update_pickle_file()
        return True

    def delete_pickle_key(arg):
        is_key_found = False
        for key in pickle_data:
            if arg == key.replace('?', ''):
                is_key_found = True
                key_to_remove = key
        if is_key_found:
            del pickle_data[key_to_remove]
            update_pickle_file()
            return True
        return False
            
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
        print()
        print(print_green + 'Dowy' + print_reset, ' is a high video quality YouTube downloader with large customization options. You can download up to 4K with 256kbps of audio bitrate.', sep='')
        print()
        print(print_blue + "Usage:" + print_reset, f"  dowy {print_red}'{print_reset}<youtube_link>{print_red}'{print_reset} <resolution> <destination>")
        print('\n\n')
        headers = ['Command', 'Description']
        rows = [
            ['<youtube_link>', "It is recommended to use quotation marks around the YouTube link"], 
            ['-c, c', 'Use clipboard as the youtube link'],
            ['<resolution>', "Resolution of the video, shortcuts like 'fhd' or '4k' can be used. 'audio' will render only audio"], 
            ['<destination>', 'Disk destination for the video, shortcuts set up by Custom keywords settings, for more info type: dowy -f']
        ]
        print(tabulate(rows, headers=headers))
        print('\n\n')
        print('CUSTOM KEYWORDS')
        print()
        custom_folders_rows = [
            ['-f', 'Custom keywords settings, for more info type: dowy -f'], 
            ['-rmf', 'Remove Custom Folder keyword, for more info type: dowy -rmf'], 
            ['-rstf', 'Reset Custom keywords settings, default values will be restored']
        ]
        print(tabulate(custom_folders_rows, headers=headers))
        print('\n\n')
        print(print_yellow + '<youtube_link>' + print_reset)
        print("    You can type any non-age restricted link. It is RECOMENDED to use quotation marks '' around the link.")
        print(f"    For convenience, you can use {print_cyan}'dowy -c'{print_reset} for getting youtube link from your clipboard.")
        print()
        print(print_yellow + '<resolution>' + print_reset)
        print(f"    {print_purple}OPTIONAL{print_reset}, you can specify resolution of the video.")
        print('    If not specified, the resolutions available will be displayed and you can choose later.')
        print(f"    For convenience, you can use shortcuts, like {print_cyan}'fhd'{print_reset}, {print_cyan}'4k'{print_reset} or {print_cyan}'hd'{print_reset} ")
        print()
        print(print_yellow + '<destination>' + print_reset)
        print(f'    {print_purple}OPTIONAL{print_reset}, you can put whole path as the destination.')
        print('    If not specified, the destination will be the dir that you are running the command from.')
        print(f"    For convenience, you can use keywords set by you. They are default keywords like {print_cyan}'down'{print_reset} or {print_cyan}'desk'{print_reset}")
        print(f"     For more information, type {print_cyan}'dowy -f'{print_reset}")
        print('\n\n')
        print(print_blue + 'Example:' + print_reset, 'dowy c 4k down - Downloading video from clipboard in 4K to downloads folder')
        print()
        print(print_blue + "Usage:" + print_reset, f"  dowy {print_red}'{print_reset}<youtube_link>{print_red}'{print_reset} <resolution> <destination>")
        print()

    def print_pickle_file():
        update_pickle_variable()
        headers = ['Key words:', 'Path:']
        rows = []
        print()
        for key in pickle_data:
            rows.append([print_green + key.replace('?', '') + print_reset, print_cyan + pickle_data[key] + print_reset])
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        print()


        # Help page
    try:
        if re.search('help|-h|--help|-help', sys.argv[1]):
            help_page()
            sys.exit(0)
        # Custom keywords settings page
        elif re.search('-f', sys.argv[1]):
            try:
                if sys.argv[2] and sys.argv[3]:
                    if add_or_change_pickle_data(sys.argv[2], sys.argv[3]):
                        print_with_space(print_green + f'Change/Add of key: {sys.argv[2]} to: {sys.argv[3]} was successfull' + print_reset)
                    else:
                        print_with_space(print_red + 'Invalid characters found in key' + '\033[0m\nOnly letters and numbers are allowed')
            except Exception as e:
                print()
                print('CUSTOM KEYWORDS')
                print('    You can set a shortcut for any directory to use when downloading.')
                print('    When specified keyword is typed as one of the arguments, the set path will be used to download the video to.')
                print('    To change already existing keywords to different paths.')
                print(f"    To delete any shortcuts with {print_cyan}'dowy -rmf'{print_reset}, type that for more info.")
                print()
                print( print_yellow + 'Delete keyword:' + print_reset, 'dowy -rmf <keyword>')
                print( print_yellow + 'Usage:  ' + print_reset, "dowy -f <keyword> ", print_red + "'" + print_reset, "<path>", print_red + "'" + print_reset, '  - NO SPACES, PATH IN QUOTATIONS', sep='')
                print_pickle_file()
                print( print_yellow + 'Delete keyword:' + print_reset, 'dowy -rmf <keyword>')
                print( print_yellow + 'Usage:  ' + print_reset, "dowy -f <keyword> ", print_red + "'" + print_reset, "<path>", print_red + "'" + print_reset, '  - NO SPACES, PATH IN QUOTATIONS', sep='')
            sys.exit(0)
        # Remove folder settings page
        elif re.search('-rmf', sys.argv[1]):
            try:
                if sys.argv[2]:
                    if delete_pickle_key(sys.argv[2]):
                        print_with_space(print_green + 'File removed successfully' + print_reset)
                    else:
                        print_with_space(print_red + 'No such key found' + print_reset)
            except Exception as e:  
                print_pickle_file()
                print('Remove keyword from custom keywords')
                print(f"For more information, type {print_cyan}'dowy -f'{print_reset}")
                print( print_yellow + 'Usage:' + print_reset, 'dowy -rmf <keyword>')
                print('Error:', e)
            sys.exit(0)
        elif re.search('-rstf', sys.argv[1]):
                while True:
                    print('Are you sure you want to reset custom keywords?')
                    confirmation_input = input('    (Y/N)? ').lower()
                    if confirmation_input =='y':
                        reset_pickle_file()
                        print()
                        print(print_purple + 'Reset successfull' + print_reset)
                        sys.exit(0)
                    elif confirmation_input == 'n':
                        print()
                        print(print_green + 'Reset cancelled' + print_reset)
                        sys.exit(0)

    # If no args, display help page
    except Exception as e:
        help_page()
        sys.exit(0)

    # Finding args with regex, so users can put them in whatever order
    curr_directory = os.getcwd()
    link_argument = None
    resolution_argument = None
    dir_argument = None
    i = 0
    for argument in sys.argv:
        i = i+1
        if i == 1:
            continue
        global link_regex
        link_regex = r'^https://www\.youtube\.com/watch\?v=|https://youtu\.be/|-?c|clipboard'
        resolution_regex = "[0-9]+p|4k|2k|full hd|fhd|hd|only audio|audio"
        dir_regex = "[A-Z]:"
        if re.match(link_regex, argument.lower()):
            link_argument = argument
        elif re.match(resolution_regex, argument.lower()):
            resolution_argument = argument
        else:
            if re.search(dir_regex, argument.lower()):
                dir_argument = argument
            for key_regex in pickle_data:
                if re.match(key_regex, argument.lower()):
                    print('dir arg found, ', pickle_data[key_regex])
                    dir_argument = pickle_data[key_regex]
                    break


    # Youtube video URL or clipboard arg
    if link_argument:
        is_youtube_prefix = bool(re.search(r'^https://www\.youtube\.com/watch\?v=|https://youtu\.be/', link_argument))
        is_clipboard_flag = bool(re.search(r'-?c|clipboard', link_argument))
        if is_youtube_prefix:
            user_url = link_argument
        elif is_clipboard_flag:
            # accessing clipboard
            win32clipboard.OpenClipboard()
            try:
                user_url = win32clipboard.GetClipboardData()
            except Exception as e: 
                user_url = None
                print(f'{print_red}Cannot access clipboard, please try again{print_reset}', e)
                win32clipboard.CloseClipboard()
                sys.exit(1)
            win32clipboard.CloseClipboard()
        else:
            # deducting that it is v query value
            user_url = f'https://www.youtube.com/watch?v={link_argument}'
    try:
        video = YouTube(user_url)
        length = video.length
    except Exception as e:
        print(f'{print_red}Video URL invalid{print_reset}')
        print(f'URL:  {print_underline + user_url + print_reset}')
        sys.exit(1)


    # divider with size of console window
    divider = os.get_terminal_size().columns * "_"

    # Main info print
    print('')
    print(divider)
    print(f'{print_cyan}Title:{print_reset}   ', video.title)
    print(f'{print_green}Author:{print_reset}  ', video.author)

    # Length of video converted to minutes and hours
    if video.length >= 3600:
        length_hours = video.length // 3600
        length_extra_minutes = video.length % 3600 // 60
        length_extra_seconds = video.length % 60
        if not length_extra_minutes == 0 and not length_extra_seconds == 0:
            print(f'{print_purple}Length:{print_reset}   ', length_hours, 'h ', length_extra_minutes, 'min ', length_extra_seconds, 's ', sep='')
        elif not length_extra_minutes == 0:
            print(f'{print_purple}Length:{print_reset}   ', length_hours, 'h ', length_extra_minutes, 'min ', sep='')
        else: 
            print(f'{print_purple}Length:{print_reset}   ', length_hours, 'h ', sep='')
    elif video.length >= 60:
        length_minutes = video.length // 60
        length_extra_seconds = video.length % 60
        if not length_extra_seconds == 0:
            print(f'{print_purple}Length:{print_reset}   ', length_minutes, 'min ', length_extra_seconds, 's', sep='')
        else:
            print(f'{print_purple}Length:{print_reset}   ', length_minutes,'min', sep='')


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

    print(print_cyan + 'Resolutions:' + print_reset)
    for resolution in resolutions:
        print('  ', resolution)
    print('\t')

    # Checking if user gave resolution arg
    if resolution_argument:
        user_resolution = resolution_argument
        is_user_resolution_set = True
    else:
        is_user_resolution_set = False

    global video_for_render
    video_for_render = None
    def set_video_for_render(resolution):
        if video.streams.filter(res=resolution):
            video_for_render = video.streams.filter(res=resolution).first()
            return video_for_render
        return False

    # Seting video resolution, with shortcuts
    if(not is_user_resolution_set):
        user_resolution = input('Please select a resolution for render: \t')
    if not set_video_for_render(user_resolution):
        print('resolution not valid, prolly shortcut')
        low_case_user_resolution = user_resolution.lower()
        if low_case_user_resolution == '4k':
            video_for_render = set_video_for_render('2160p')
        if low_case_user_resolution == '2k':
            video_for_render = set_video_for_render('1440p')
        if low_case_user_resolution == 'fullhd' or low_case_user_resolution == 'fhd':
            video_for_render = set_video_for_render('1080p')
        if low_case_user_resolution == 'hd':
            video_for_render = set_video_for_render('720p')
        if low_case_user_resolution == 'only audio' or low_case_user_resolution == 'audio':
            video_for_render = 'no_video'
        if not video_for_render:
            print_with_space(f'{print_red}Invalid resolution{print_reset}')
            user_resolution = None
            is_user_resolution_set = False
    else:
        video_for_render = set_video_for_render(user_resolution)

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

    if not os.path.exists(video_destination):
        print(print_red + "Directory doesn't exist" + print_reset)
        print('Specified directory:    ', video_destination)
        sys.exit(1)

    # Check if ffmpeg installed, could install it if not
    if which('ffmpeg') is None:
        print(print_red + 'ffmpeg is not installed, please install it manually' + print_reset)
        print(f'Be sure to add in to {print_purple}PATH{print_reset} environment variable')
        print()
        sys.exit(1)

    # only audio handling - skiping video download
    if not video_for_render == 'no_video':
        print(f'{print_bold}Video{print_reset} download {print_yellow}started{print_reset}')
        print()
        video_for_render.download(windows_temp_path, 'dowy_youtube_video.mp4')
        print(f'\n{print_bold}Video{print_reset} download {print_green}completed{print_reset}')
        print()

    print(f'{print_bold}Audio{print_reset} download {print_yellow}started{print_reset}')
    print()

    # Audio download if video selected, otherwise download audio and exit
    if not video_for_render == 'no_video':
        audio = video.streams.filter(only_audio=True).order_by('abr').last()
        audio.download(windows_temp_path, 'dowy_youtube_audio.opus')
    else:
        audio = video.streams.filter(only_audio=True).order_by('abr').last()
        audio.download(video_destination)
        print()
        print(f'{print_bold}Audio{print_reset} processed {print_green}successfully{print_reset}')
        print_local_file_link(fr"{video_destination}\\{audio.default_filename}", f"{print_purple}Open your file{print_reset}")
        sys.exit(0)
    print_with_space(f'{print_bold}Audio{print_reset} download {print_green}completed{print_reset}')

    # Merging video and audio into final file
    ffmpeg = (
        FFmpeg()
        .option('y')
        .input(f"{windows_temp_path.replace('\\', '/')}/dowy_youtube_video.mp4")
        .input(f'{windows_temp_path.replace('\\', '/')}/dowy_youtube_audio.opus')
        .output(
            f'{video_destination}/{video_for_render.default_filename}.mp4', 
            {'codec:v': 'h264'}
        )
    )

    print(f'{print_yellow}Compiling started{print_reset}')
    print('This may take a while depending on the length of the video')
    ffmpeg.execute()
    print(f'{print_green}Compiling finished{print_green}')

    # Cleaning up temp files
    os.remove(f'{windows_temp_path}\\dowy_youtube_video.mp4')
    os.remove(f'{windows_temp_path}\\dowy_youtube_audio.opus')

    print_with_space(f'{print_green}Video processed successfully{print_reset}')
    print_local_file_link(fr"{video_destination}\\{video_for_render.default_filename}.mp4", f"{print_purple}Open your file{print_reset}")