# https://www.youtube.com/watch?v=XHcDHSWRCRQ
__author__ = 'Deca'
from cx_Freeze import setup, Executable

setup(
    name = 'Imgurbot',
    version = "1.2",
    description = "Imgurbot",
    executables = [Executable("imgur.py")],
    )
