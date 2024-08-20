from setuptools import setup, find_packages

setup(
    entry_points = {
        'console_scripts': ['dowy=dowy.command_line:main'],
    },
    name='dowy', 
    version=0.1, 
    packages=find_packages(), 
    install_requires=[
        'pytubefix', 
        'python-ffmpeg', 
        'userpaths', 
        'pywin32', 
        'tabulate'
    ]
)