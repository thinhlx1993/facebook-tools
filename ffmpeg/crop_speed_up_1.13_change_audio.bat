@echo off

if not exist "done" mkdir ""done" "
if not exist "crop" mkdir ""crop" "

Set "SrcDir=E:\Projects\thinh\facebook-tools\ffmpeg\Nhac"
Set "ExtLst=*.mp3"
Set "i=0"
For /F "Delims=" %%A In ('Where /R "%SrcDir%" %ExtLst%') Do (Set /A i+=1
    Call Set "$[%%i%%]=%%A")
Set /A rand=(%Random%%%i)+1
Echo "%rand%"


for %%f in (*.avi *.flv *.mkv *.mpg *.mp4) do (
	ffmpeg -i "%%f" -i "%SrcDir%\%rand%.mp3" -c:v copy -c:a aac -b:a 256k -map "0:0" -map "1:0" -shortest crop/"%%f" -y
	ffmpeg -i crop/"%%f" -vf "setpts=0.87*PTS,crop=in_w*85/100:in_h*85/100,scale=420:420" done/"%%f" -y
)