@echo off

if not exist "crop" mkdir ""crop" "
if not exist "done" mkdir ""done" "

Set "SrcDir=E:\Projects\thinh\facebook-tools\ffmpeg\Nhac"
Set "ExtLst=*.mp3"



for %%f in (*.avi *.flv *.mkv *.mpg *.mp4) do (
	call crop.bat "%%f"
)