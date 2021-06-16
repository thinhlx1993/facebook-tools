from bs4 import BeautifulSoup
import os

if os.path.isfile("input.txt"):
    os.remove("input.txt")


page_name = "Guff UK.html"
html_doc = open(f"../template/{page_name}", encoding="utf-8")
soup = BeautifulSoup(html_doc, 'html.parser')

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
                with open(f"input.txt", 'a') as file:
                    file.write(f"{href}-{view_count} \n")
                    file.close()
                print(href, view_count)
            # elif "K" in view_count:
            #     view_count = view_count.replace("K", "").replace("Views", "")
            #     view_count = float(view_count)
            #     # if view_count > 700:
            #     print(href, view_count)
            #     with open(f"{page_name}.txt", 'a') as file:
            #         file.write(f"{href}-{view_count} \n")
            #         file.close()
