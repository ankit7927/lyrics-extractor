from lyricsmint import extractor
import requests, sys, threading, time, logging
from logger import logger

upload_url = "https://rockerlyrics.pythonanywhere.com/api/song/create"# input("Enter upload url : ")
if upload_url == "":
    print("exiting upload url is none")
    sys.exit()

urls_list = []
request = requests.Session()

with open("page_links.txt", "r") as file:
    urls_list = file.read().splitlines()

def extract():
    while not len(urls_list) == 0 :
        link = urls_list.pop()
        if link == "":
            continue
        song_detail = extractor(request, link)
        res = request.post(url=upload_url, json=song_detail)
        print(f"response from server {res.status_code}")
        time.sleep(1)

if __name__ == "__main__":
    print("started")
    for _ in range(5):
        threading.Thread(target=extract).start()
    
