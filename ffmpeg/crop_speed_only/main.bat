@echo off
Set crop=0.85
Set speed=1.15
Set width=1080
Set heigh=1080
Set overlay_width=180

ffprobe -v error -of flat=s=_ -select_streams v:0 -show_entries stream=width %1 >> width.txt
ffprobe -v error -of flat=s=_ -select_streams v:0 -show_entries stream=height %1 >> height.txt
FOR /f "tokens=5 delims==_" %%i in (width.txt) do @set width=%%i
FOR /f "tokens=5 delims==_" %%i in (height.txt) do @set height=%%i
echo width=%width%
echo height=%height%
del width.txt && del height.txt
ffmpeg -i %1 -i "C:\overlay.mp4" -filter_complex "[0:v]crop=in_w*%crop%:in_h*%crop%:in_w*0.1:in_h*0.2[v1];[v1]scale=%width%:%height%[v2];[v2]setpts=1/%speed%*PTS[v3];[1]scale=%overlay_width%:-1[e];[v3][e]overlay=main_w-(overlay_w+10):main_h-(overlay_h+10):shortest=1[v4];[0:a]atempo=%speed%[a]" -map "[v4]" -map "[a]" -preset ultrafast -crf 24 -shortest done/%1 -y