@echo off

if not exist "crop" mkdir ""crop" "
if not exist "done" mkdir ""done" "

for %%f in (*.avi *.flv *.mkv *.mpg *.mp4) do (
	call crop.bat "%%f"
)