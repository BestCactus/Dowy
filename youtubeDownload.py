from pytubefix import YouTube
import sys
import os
import ffmpeg
import re

currDirectory = sys.argv[1]

print('Current Directory: ', currDirectory)

if len(sys.argv) > 2:
   isYoutubePrefix = bool(re.search("^https://www.youtube.com/watch?v=", sys.argv[2]))
   if isYoutubePrefix:
        userUrl = sys.argv[2]
   else:
        userUrl = f'https://www.youtube.com/watch?v={sys.argv[2]}'
else:
    userUrl = input('Please enter URL of desired video: \t')

video = YouTube(userUrl)

def on_progress(stream, chunk, bytes_remaining):
    progress = round((1 - bytes_remaining / stream.filesize) * 100,2)
    print(f'Progress: {progress}%  ', f"Megabytes remaining: {round(bytes_remaining/1000000, 2)}MB")

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

if len(sys.argv) > 3:
    userResolution = sys.argv[3]
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
        if not videoForRender:
            printWithSpace('Invalid resolution')
            userResolution = None
            isUserResolutionSet = False

scriptDir = os.path.dirname(os.path.abspath(__file__))
tempFolderPath = os.path.join(scriptDir, "Temp")

printWithSpace('Video download started')

if len(sys.argv) > 4:
    directoryArgument = sys.argv[4].lower()
    if directoryArgument == 'downloads' or directoryArgument == 'down':
        videoDestination = "D:/STAHOVÁNÍ"
        videoForRender.download(tempFolderPath, 'video.mp4')
    elif directoryArgument == 'desktop' or directoryArgument == "desk":
        videoDestination = "C:/Users/vojta/OneDrive/Plocha"
        videoForRender.download(tempFolderPath, 'video.mp4')
    elif directoryArgument == 'pictures' or directoryArgument == 'pic':
        videoDestination = "C:/Users/vojta/OneDrive/Obrázky"
        videoForRender.download(tempFolderPath, 'video.mp4')
    elif directoryArgument == 'videos' or directoryArgument == 'vid':
        videoDestination = "C:/Users/vojta/Videos"
        videoForRender.download(tempFolderPath, 'video.mp4')
    elif directoryArgument == 'music' or directoryArgument == 'mus':
        videoDestination = "C:/Users/vojta/Music"
        videoForRender.download(tempFolderPath, 'video.mp4')
    else:
        videoDestination = directoryArgument
        videoForRender.download(tempFolderPath, 'video.mp4')
else:
    videoDestination = currDirectory
    videoForRender.download(tempFolderPath, 'video.mp4')

printWithSpace('Video download completed')
print('Audio download started')
print('\t')

audio = video.streams.filter(only_audio=True).order_by('abr').last()
audio.download(tempFolderPath, 'audio.opus')

printWithSpace('Audio download completed')

inputVideo = ffmpeg.input("C:/CustomScripts/Temp/video.mp4")
inputAudio = ffmpeg.input('C:/CustomScripts/Temp/audio.opus')


outputFileName = video.title.lower()
outputFileName = re.sub(r'[<>:"/\\|?*!,]', '', outputFileName)
outputFileName = re.sub(r'\.+$', '', outputFileName)
outputFileName = re.sub(r'\s+', '_', outputFileName)

output = ffmpeg.output(inputVideo, inputAudio, f'{videoDestination}/{outputFileName}.mp4', vcodec='copy', acodec='aac')


output.run()

os.remove(f'{tempFolderPath}\\video.mp4')
os.remove(f'{tempFolderPath}\\audio.opus')