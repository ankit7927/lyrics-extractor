from lyricsmint import extractor
import requests, sys, threading

upload_url = "http://localhost:8000/api/song/create"# input("Enter upload url : ")
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
        try:
            if link == "":
                continue
            song_detail = extractor(request, link)
            response = request.post(url=upload_url, json=song_detail)
            print("uploaded -- " + str(response.status_code), "\n")
        except Exception as e:
            print(e)
            continue

for _ in range(20):
    threading.Thread(target=extract).start()
    
