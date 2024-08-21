# DOWY - CLI 4K YouTube Downloader for PowerShell

High quality YouTube downloader for Windows CMD and PowerShell. Download any video with up to 4K resolution and 256kbps audio bitrate.
Lots of customization, handy features and easy installation.

❗**IMPORTANT**❗ When specifying any paths, links or keywords that have spaces or **`&`** character, use **quotation marks `''`**. Otherwise, the CLI will break, because how windows treats **`&`** character and spaces.

❗**IMPORTANT**❗This CLI is **heavily** dependent on the **ffmpeg** program. Please make sure you have that installed before using this CLI. Install with [this link](https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip). Unzip and add to **PATH** env. For more info, check some YouTube tutorial. :)

## Install:

Simple install with _PyPi_. Run terminal with Administrator rights, otherwise the CLI will not work

```bash
pip install dowy
```

## Usage:

Using Dowy is pretty straight forward and easy. Only one argument is required. All informations are on the help page.

### Help Page:

```
Dowy is a high video quality YouTube downloader with large customization options.
You can download up to 4K with 256kbps of audio bitrate.

Usage:   dowy '<youtube_link>' <resolution> <destination>



Command         Description
--------------  --------------------------------------------------------------------------------------------------------
<youtube_link>  It is recommended to use quotation marks around the YouTube link
-c, c           Use clipboard as the youtube link
<resolution>    Resolution of the video, shortcuts like 'fhd' or '4k' can be used. 'audio' will render only audio
<destination>   Disk destination for the video, shortcuts set up by Custom Keywords settings, for more info type: dowy -f



CUSTOM KEYWORDS

Command    Description
---------  --------------------------------------------------------------
-f         Custom Keywords settings, for more info type: dowy -f
-rmf       Remove Custom Folder keyword, for more info type: dowy -rmf
-rstf      Reset Custom Keywords settings, default values will be restored



<youtube_link>
    You can type any non-age restricted link. It is RECOMENDED to use quotation marks '' around the link.
    For convenience, you can use 'dowy -c' for getting youtube link from your clipboard.

<resolution>
    OPTIONAL, you can specify resolution of the video.
    If not specified, the resolutions available will be displayed and you can choose later.
    For convenience, you can use shortcuts, like 'fhd', '4k' or 'hd'

<destination>
    OPTIONAL, you can put whole path as the destination.
    If not specified, the destination will be the dir that you are running the command from.
    For convenience, you can use keywords set by you. They are default keywords like 'down' or 'desk'
     For more information, type 'dowy -f'

Example: dowy c 4k down - Downloading video from clipboard in 4K to downloads folder

Usage:   dowy '<youtube_link>' <resolution> <destination>
```

## Examples:

```bash
dowy 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' fhd desk
```

This downloads video in Full HD (1080p) into desktop folder. You can customize keywords and paths.

```bash
dowy -c 2k C:/my/path
```

Download video with link from **clipboard** in 2K (2160p) to the directory path `C:/my/path`

## Custom Keywords:

You can set a keyword to use when downloading, to save the file to specified directory.

#### List Keywords:

```bash
dowy -f
```

List all keywords and their paths with all information needed.

#### Set a new Keyword:

```bash
dowy -f my_folder 'C:/My Folder'
```

Set a new keyword shortcut to the directory path specified. Type the keyword, in this case `my_folder` when downloading the video.

#### Changing keyword path:

```bash
dowy -f down C:/Downloads
```

Change the path of `down` (Downloads personal folder) keyword shortcut.

#### Remove keyword:

```bash
dowy -rmf music
```

Removes keyword shortcut `music` (music personal folder).

#### Reset all keywords:

```bash
dowy -rstf
```

Resets all values for Custom Keywords settings. Default keywords and paths will be restored.

### Using Keywords:

```bash
dowy c 4k my_folder
```

This will download video with link from clipboard in 4K to directory path set for `my_folder` keyword.

## Support:

If you encounter any issues, you can open a new issue on GitHub.

All pull requests and collaborations are welcome. :)

## Links:

[PyPi Info](https://pypi.org/project/dowy/)

[My GitHub Profile](https://github.com/BestCactus)

## License:

[MIT](https://github.com/BestCactus/yt-4k-downloader/blob/main/LICENSE.txt)
