@echo off

if not exist "done" mkdir ""done" "

for %%f in (*.avi *.flv *.mkv *.mpg *.mp4) do (
	ffmpeg -i "%%f" -filter_complex "[0:v]setpts=0.87*PTS[v];[0:a]atempo=1.15[a];[0:v]crop=in_w*0.86:in_h*0.86" -map "[v]" -map "[a]" done/"%%f" -y
)