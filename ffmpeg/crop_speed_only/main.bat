@echo off
Set crop=0.95
Set speed=1.05
Set width=1080
Set height=1080
Set overlay_width=180
Set SrcDir="C:\overlay"
Set ExtLst="*.mp4"
Set volume=10
Set "i=0"
For /F "Delims=" %%A In ('Where /R "%SrcDir%" %ExtLst%') Do (Set /A i+=1 
        Call Set "$[%%i%%]=%%A")
Set /A rand="(%Random%%%i)+1"
Echo "%rand%"

ffmpeg -i %1 -i "C:\overlay\%rand%.mp4" -filter_complex "[0:v]crop=in_w*%crop%:in_h*%crop%:in_w*0.1:in_h*0.2[v1];[v1]scale=%width%:%height%[v2];[v2]setpts=1/%speed%*PTS[v3];[1]scale=%overlay_width%:-1[e];[v3][e]overlay=0:0:shortest=1[v4];[0:a]atempo=%speed%[a0];[1:a]atempo=1,volume=%volume%[a1];[a0][a1]amix=inputs=2:duration=shortest[a2]" -map "[v4]" -map "[a2]" -preset ultrafast -crf 24 -shortest done/%1 -y