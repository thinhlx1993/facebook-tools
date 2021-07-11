import youtube_dl
import os

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("filename")
args = parser.parse_args()

page_name = args.filename
os.makedirs(f"downloaded/{page_name}", exist_ok=True)

if os.path.isfile(f"links/{page_name}.txt"):
    with open(f"links/{page_name}.txt") as file:
        for line in file.readlines():
            link, views = line.split('-')
            views = views.replace('\n', '')
            ydl_opts = {}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                try:
                    info_dict = ydl.extract_info(link, download=False)
                    video_title = info_dict.get('title', None)
                    ext = info_dict.get('ext', None)
                    ydl_opts = {'outtmpl': f'downloaded/{page_name}/{views}-{video_title}'}
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([link])
                except Exception as ex:
                    pass
