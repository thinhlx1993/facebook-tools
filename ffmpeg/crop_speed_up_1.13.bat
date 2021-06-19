@echo off

if not exist "done" mkdir ""done" "

for %%f in (*.avi *.flv *.mkv *.mpg *.mp4) do (
	ffmpeg -i "%%f" -vf "setpts=0.87*PTS,crop=in_w*85/100:in_h*85/100,scale=420:420" done/"%%f" -y
)