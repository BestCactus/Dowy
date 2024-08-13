from pytubefix import YouTube
import sys
import ffmpeg

if len(sys.argv) > 1:
   userUrl = sys.argv[1]
else:
    userUrl = input('Please enter URL of desired video: \t')


video = YouTube(userUrl)

print('\t')
print('Title:   ', video.title)
print('Author:  ', video.author)
print('Length:  ', video.length, 's')
print('_____________________________________________________________________________________________')
print('\t')
print('\t')


print(video.streams.filter(progressive=True).all())

def printWithSpace(msg):
    print('\t')
    print(msg)
    print('\t')

def setVideoForRender(resolution):
    if video.streams.filter(res=resolution):
        global videoForRender
        videoForRender = video.streams.filter(res=resolution).filter(progressive=True).first()
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

if len(sys.argv) > 2:
    userResolution = sys.argv[2]
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

if len(sys.argv) > 3:
    directoryArgument = sys.argv[3].lower()
    if directoryArgument == 'downloads' or directoryArgument == 'down':
        videoForRender.download("D:/STAHOVÁNÍ")
    elif directoryArgument == 'desktop' or directoryArgument == "desk":
        videoForRender.download("C:/Users/vojta/OneDrive/Plocha")
    elif directoryArgument == 'pictures' or directoryArgument == 'pic':
        videoForRender.download("C:/Users/vojta/OneDrive/Obrázky")
    elif directoryArgument == 'videos' or directoryArgument == 'vid':
        videoForRender.download("C:/Users/vojta/Videos")
    elif directoryArgument == 'music' or directoryArgument == 'mus':
        videoForRender.download("C:/Users/vojta/Music")
    else:
        videoForRender.download(directoryArgument)
else:
    videoForRender.download("D:/STAHOVÁNÍ")