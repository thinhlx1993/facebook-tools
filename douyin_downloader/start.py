import os
import subprocess
import re
import json
import threading
import PySimpleGUI as sg
from downloader import run, download_one
from bs4 import BeautifulSoup
import os

regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$'''
retry_time = 0


def crawl_movie(page_name):
    if not os.path.isfile(page_name):
        return []

    html_doc = open(page_name, encoding="utf-8")
    soup = BeautifulSoup(html_doc, 'html.parser')
    table_data = []

    for parent in soup.find_all("li"):
        video_href = None
        video_like = None
        for link in parent.find_all('a'):
            href = link.get('href')
            if "https://www.douyin.com/video" in href:
                # print(href)
                video_href = href
        for span in parent.find_all('span', class_="_4c7753003fcad283963e6dd5d4aa5f1e-scss"):
            # print(span.text)
            video_like = span.text

        if video_href:
            print(f"{video_href}-{video_like} Likes")
            table_data.append([
                video_href,
                video_like,
                "waiting"
            ])

    return table_data


if __name__ == '__main__':
    # browserExe = "movies.exe"
    # os.system("taskkill /f /im " + browserExe)
    sg.theme('DarkAmber')  # Add a touch of color
    # All the stuff inside your window.
    headings = ['links', 'likes', 'status']  # the text of the headings

    layout = [[sg.Table(values=[],
                        headings=headings,
                        display_row_numbers=True,
                        justification='right',
                        auto_size_columns=False,
                        col_widths=[50, 15, 15],
                        vertical_scroll_only=False,
                        num_rows=24, key='table')],
              [sg.Button('Start download'),
               sg.Button('Remove link'),
               sg.Input(key='file_browser', enable_events=True, visible=False), sg.FileBrowse(button_text="Load HTML file", enable_events=True),
               sg.Button('Cancel')]]

    # Create the Window
    window = sg.Window('Douyin Downloader', layout)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        print('You entered ', values)
        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            browserExe = "movies.exe"
            os.system("taskkill /f /im " + browserExe)
            break
        elif event == 'Get Links Online':
            sg.Popup('Bat dau lay links videos. Vui long khong dong cua so!', keep_on_top=True, title="Chu y!")
            x = threading.Thread(target=crawl_movie, args=(values[0], window, ))
            x.start()
        elif event == 'Start download':
            table_data = window.Element('table').Get()
            thread = threading.Thread(target=run, args=(table_data, window,), daemon=True)
            thread.start()
        elif event == 'file_browser':
            table_data = crawl_movie(values['file_browser'])
            window.Element('table').Update(values=table_data)
            window.Element('table').Update(select_rows=[0])
        elif event == 'Download':
            idx = values['table'][0]
            table_data = window.Element('table').Get()
            thread = threading.Thread(target=download_one, args=(table_data, idx, window,), daemon=True)
            thread.start()
        elif event == 'Remove link':
            removed = values['table']
            table_data = window.Element('table').Get()
            for item in removed:
                table_data.pop(item)
            window.Element('table').Update(values=table_data)
        elif event == '-THREAD-':
            idx, download_status = values['-THREAD-']
            table_data = window.Element('table').Get()
            if download_status:
                table_data[idx][-1] = 'Downloaded'
            else:
                table_data[idx][-1] = 'Error'
            window.Element('table').Update(values=table_data, select_rows=[idx])
            window.Refresh()
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
