from pytubefix import YouTube
import sys
import os
import ffmpeg
import re
import signal

def signal_handler(sig, frame):
    print()
    print('CTRL + C detected, exiting...')
    print('Cleaning up')
    try:
        os.remove(f'{tempFolderPath}\\video.mp4')
        os.remove(f'{tempFolderPath}\\audio.opus')
    except Exception as e:
        print('Failed to remove temp files', e)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def print_local_file_link(file_path, display_text):
    # Replace backslashes with forward slashes for the URL format
    formatted_path = file_path.replace('\\', '/')
    # Convert to absolute path
    abs_path = os.path.abspath(formatted_path)
    # Format the path as a file URL
    file_url = f"file:///{abs_path}"
    # Print the link
    print(f"\033]8;;{file_url}\033\\{display_text}\033]8;;\033\\")


currDirectory = sys.argv[1]
i = 0

link_argument = None
resolution_argument = None
dir_argument = None
for argument in sys.argv:
    if i < 2:
        i = i + 1
        continue
    link_regex = r'^https://www\.youtube\.com/watch\?v='
    resolution_regex = "[0-9]+p|4k|2k|full hd|fhd|hd|only audio|audio"
    dir_regex = "[A-Z]:|down|desk|pic|vid|mus"
    if bool(re.search(link_regex, argument)):
        link_argument = argument
    elif bool(re.search(resolution_regex, argument.lower())):
        resolution_argument = argument
    elif bool(re.search(dir_regex, argument)):
        dir_argument = argument.lower()
    i = i + 1
    

print('link arg', link_argument)
print('resolution arg', resolution_argument)
print('dir arg', dir_argument)


if link_argument:
   isYoutubePrefix = bool(re.search(r'^https://www\.youtube\.com/watch\?v=', link_argument))
   if isYoutubePrefix:
        userUrl = link_argument
   else:
        userUrl = f'https://www.youtube.com/watch?v={link_argument}'
else:
    userUrl = input('Please enter URL of desired video: \t')

video = YouTube(userUrl)

def on_progress(stream, chunk, bytes_remaining):
    progress = round((1 - bytes_remaining / stream.filesize) * 100,2)
    print(f'\rProgress: {progress}% ', f" Megabytes remaining: {round(bytes_remaining/1000000, 2)}MB", end='')


video.register_on_progress_callback(on_progress)

print('\t')
print('Title:   ', video.title)
print('Author:  ', video.author)
print('Length:  ', video.length, 's')
print('_____________________________________________________________________________________________')
print('\t')
print('\t')

def printWithSpace(msg):
    print('\t')
    print(msg)
    print('\t')

def setVideoForRender(resolution):
    if video.streams.filter(res=resolution):
        global videoForRender
        videoForRender = video.streams.filter(res=resolution).first()
        global isResolutionValid
        isResolutionValid = True
        return True

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

videoForRender = None
if resolution_argument:
    userResolution = resolution_argument
    isUserResolutionSet = True
else:
    isUserResolutionSet = False

isResolutionValid = False
while isResolutionValid == False:
    if(not isUserResolutionSet):
        userResolution = input('Please select a resolution for render: \t')
    if not setVideoForRender(userResolution):
        lowCaseUserResolution = userResolution.lower()
        if lowCaseUserResolution == '4k':
            setVideoForRender('2160p')
        if lowCaseUserResolution == '2k':
            setVideoForRender('1440p')
        if lowCaseUserResolution == 'full hd' or lowCaseUserResolution == 'fhd':
            setVideoForRender('1080p')
        if lowCaseUserResolution == 'hd':
            setVideoForRender('720p')
        if lowCaseUserResolution == 'only audio' or lowCaseUserResolution == 'audio':
            videoForRender = 'no_video'
            isResolutionValid = True
        if not videoForRender:
            printWithSpace('Invalid resolution')
            userResolution = None
            isUserResolutionSet = False

scriptDir = os.path.dirname(os.path.abspath(__file__))
tempFolderPath = os.path.join(scriptDir, "Temp")

if dir_argument:
    if dir_argument == 'downloads' or dir_argument == 'down':
        videoDestination = "D:/STAHOVÁNÍ"
    elif dir_argument == 'desktop' or dir_argument == "desk":
        videoDestination = "C:/Users/vojta/OneDrive/Plocha"
    elif dir_argument == 'pictures' or dir_argument == 'pic':
        videoDestination = "C:/Users/vojta/OneDrive/Obrázky"
    elif dir_argument == 'videos' or dir_argument == 'vid':
        videoDestination = "C:/Users/vojta/Videos"
    elif dir_argument == 'music' or dir_argument == 'mus':
        videoDestination = "C:/Users/vojta/Music"
    else:
        videoDestination = dir_argument
else:
    videoDestination = currDirectory

if not videoForRender == 'no_video':
    printWithSpace('Video download started')
    videoForRender.download(tempFolderPath, 'video.mp4')
    printWithSpace('Video download completed')
else:
    print('No video download')

print('Audio download started')
print('\t')

if not videoForRender == 'no_video':
    audio = video.streams.filter(only_audio=True).order_by('abr').last()
    audio.download(tempFolderPath, 'audio.opus')
else:
    audio = video.streams.filter(only_audio=True).order_by('abr').last()
    audio.download(videoDestination)
    print('Audio processed successfully')
    print_local_file_link(fr"{videoDestination}\\{audio.default_filename}", "Open your file")
    sys.exit(0)
printWithSpace('Audio download completed')

inputVideo = ffmpeg.input("C:/CustomScripts/Temp/video.mp4")
inputAudio = ffmpeg.input('C:/CustomScripts/Temp/audio.opus')


outputFileName = video.title.lower()
outputFileName = re.sub(r'[<>:"/\\|?*!,]', '', outputFileName)
outputFileName = re.sub(r'\.+$', '', outputFileName)
outputFileName = re.sub(r'\s+', '_', outputFileName)

output = ffmpeg.output(inputVideo, inputAudio, f'{videoDestination}/{outputFileName}.mp4', vcodec='copy', acodec='aac')

print('Compiling started')
output.run(quiet=True, overwrite_output=True)
print('Compiling finished')

os.remove(f'{tempFolderPath}\\video.mp4')
os.remove(f'{tempFolderPath}\\audio.opus')

printWithSpace('Video processed successfully')
print_local_file_link(fr"{videoDestination}\\{outputFileName}.mp4", "Open your file")