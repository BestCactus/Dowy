from setuptools import setup, find_packages

with open("README.md", "r") as f:
    readme_text = f.read()


setup(
    entry_points = {
        'console_scripts': ['dowy=dowy.command_line:main'],
    },
    name='dowy', 
    version="0.6", 
    description='YouTube CLI 4K downloader for Windows', 
    long_description=readme_text, 
    long_description_content_type='text/markdown', 
    author="Vojtěch Fluger", 
    author_email="vojtech.fluger@gmail.com",
    license='MIT License',
    url="https://github.com/BestCactus/yt-4k-downloader", 
    download_url="https://pypi.org/project/dowy/",
    packages=find_packages(), 
    install_requires=[
        'pytubefix', 
        'python-ffmpeg', 
        'userpaths', 
        'pywin32', 
        'tabulate'
    ]
)