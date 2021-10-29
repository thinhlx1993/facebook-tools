import os
import subprocess
import re
import json
import threading
import PySimpleGUI as sg
import pyautogui
import logging

import youtube_dl
from bs4 import BeautifulSoup
import os

retry_time = 0
stop_threads = False
pyautogui.FAILSAFE = False
# create logger with 'spam_application'
logger = logging.getLogger('application')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('app.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


def download_video(table_data, current_index, window, ten_phim):
    os.makedirs(f"downloaded/{ten_phim}", exist_ok=True)
    for idx, row in enumerate(table_data):
        if idx >= current_index:
            link, views, status = row
            ydl_opts = {}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                try:
                    info_dict = ydl.extract_info(link, download=False)
                    video_title = info_dict.get('title', None)
                    ext = info_dict.get('ext', None)
                    ydl_opts = {'outtmpl': f'downloaded/{ten_phim}/{views}-{video_title}'}
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([link])
                    window.write_event_value('-THREAD-', [idx, True])  # put a message into queue for GUI
                except Exception as ex:
                    print(ex)
                    window.write_event_value('-THREAD-', [idx, False])
                    pass


def crawl_movie(page_name, filter_number):

    try:
        filter_number = int(filter_number)
    except Exception as ex:
        logger.error(ex)
        filter_number = 0

    if not os.path.isfile(page_name):
        return []

    html_doc = open(page_name, encoding="utf-8")
    soup = BeautifulSoup(html_doc, 'html.parser')
    table_data = []

    for parent in soup.find_all(class_='n851cfcs'):
        child = parent.find(class_="bi6gxh9e")
        href = None
        view_count = None
        if child:
            href_el = child.find("a")
            href = href_el.get('href')
            views = parent.find_all(class_="bnpdmtie")
            for view in views:
                if "Views" in view.text:
                    view_count = view.text
                    break
            if view_count and href:
                if "M" in view_count:
                    view_count_float = view_count.replace("M", "").replace("Views", "")
                    view_count = float(view_count_float)*1000000
                elif "K" in view_count:
                    view_count = view_count.replace("K", "").replace("Views", "")
                    view_count = float(view_count)*1000
                else:
                    view_count = 0

                if view_count > filter_number or filter_number == 0:
                    if view_count > 1000000:
                        view_count = f"{view_count/1000000}M"
                    elif 1000000 > view_count > 1000:
                        view_count = f"{view_count/1000}K"
                    table_data.append([
                        href,
                        view_count,
                        "waiting"
                    ])
    return table_data


if __name__ == '__main__':
    # browserExe = "movies.exe"
    # os.system("taskkill /f /im " + browserExe)
    sg.theme('DarkAmber')  # Add a touch of color
    # All the stuff inside your window.
    headings = ['links', 'likes', 'status']  # the text of the headings

    layout = [[sg.Text('views filter'), sg.InputText("0", key="input_number")],
              [sg.Text('Ten Phim'), sg.InputText(key="ten_phim")],
              [sg.Table(values=[],
                        headings=headings,
                        display_row_numbers=True,
                        justification='right',
                        auto_size_columns=False,
                        col_widths=[50, 15, 15],
                        vertical_scroll_only=False,
                        num_rows=24, key='table')],
              [sg.Button('Start download'),
               sg.Button('Pause'),
               sg.Button('Remove link'),
               sg.Input(key='file_browser', enable_events=True, visible=False), sg.FileBrowse(button_text="Load HTML file", enable_events=True),
               sg.Button('Remove All Links'),
               sg.Button('Cancel')]]

    # Create the Window
    window = sg.Window('Douyin Downloader', layout)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        print(f'{event} You entered {values}')
        print('event', event)
        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            # browserExe = "movies.exe"
            # os.system("taskkill /f /im " + browserExe)
            break
        elif event == 'Get Links Online':
            sg.Popup('Bat dau lay links videos. Vui long khong dong cua so!', keep_on_top=True, title="Chu y!")
            x = threading.Thread(target=crawl_movie, args=(values[0], window, ))
            x.start()
        elif event == 'Start download':
            window.Element('Start download').Update(text="Downloading")
            stop_threads = False
            current_index = 0
            if len(values['table']) > 0:
                current_index = values['table'][0]
            table_data = window.Element('table').Get()
            thread = threading.Thread(target=download_video, args=(table_data, current_index, window, values.get("ten_phim", ""),), daemon=True)
            thread.start()
        elif event == 'Remove All Links':
            window.Element('table').Update(values=[])
        elif event == 'Pause':
            window.Element('Start download').Update(text="Resume")
            stop_threads = True
        elif event == 'file_browser':
            if os.path.isfile(values['file_browser']):
                table_data = window.Element('table').Get()
                table_data += crawl_movie(values['file_browser'], values['input_number'])
                window.Element('table').Update(values=table_data)
                window.Element('table').Update(select_rows=[0])
        elif event == 'Remove link':
            removed = values['table']
            table_data = window.Element('table').Get()
            for item in reversed(removed):
                table_data.pop(item)
            window.Element('table').Update(values=table_data)
        elif event == '-THREAD-':
            idx, download_status = values['-THREAD-']
            logger.debug(f"download status: {idx} {download_status} {len(table_data)}")
            table_data = window.Element('table').Get()
            if download_status:
                table_data[idx][-1] = 'Downloaded'
            else:
                table_data[idx][-1] = 'Error'
            window.Element('table').Update(values=table_data, select_rows=[idx])
            window.Refresh()
            if idx == len(table_data) - 1:
                window.Element('Start download').Update(text="Start download")
                pyautogui.alert("Download complete")
        elif event == 'GetLinksSuccessfully':
            with open("movies.json") as json_file:
                data = json.load(json_file)
                table_data = []
                for item in data:
                    link_season = item['link_season']
                    for ep in item['episodes']:
                        table_data.append([
                            link_season,
                            ep['episode_name'],
                            ep['link_episode'],
                            "waiting"
                        ])

                window.Element('table').Update(values=table_data, select_rows=[0])
    window.close()
