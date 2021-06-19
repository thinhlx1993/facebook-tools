
for i in *.mp4; do
    echo "$i"
    ffmpeg -i "$i" -filter_complex "[0:v]setpts=0.87*PTS[v];[0:a]atempo=1.15[a];[0:v]crop=in_w*85/100:in_h*85/100;[0:v]scale=in_w:in_h" -map "[v]" -map "[a]" -strict -2 "done/${i}" -y
done

