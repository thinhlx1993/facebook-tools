import youtube_dl
import os

page_name = "Guff UK"
os.makedirs(f"downloaded/{page_name}", exist_ok=True)


with open("input.txt") as file:
    for line in file.readlines():
        link, views = line.split('-')
        views = views.replace('\n', '')
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                info_dict = ydl.extract_info(link, download=False)
                video_title = info_dict.get('title', None)
                ydl_opts = {'outtmpl': f'downloaded/{page_name}/{views}-{video_title}'}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([link])
            except Exception as ex:
                pass
