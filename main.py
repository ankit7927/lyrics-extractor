from lyricsmint import extractor
import requests, sys, json

if __name__=="__main__":
    upload_url = "http://localhost:8000/api/song/create"# input("Enter upload url : ")
    if upload_url == "":
        print("exiting upload url is none")
        sys.exit()

    request = requests.Session()
    with open("page_links.txt", "r") as file:
        for linke in file.read().splitlines():
            try:
                song_detail = extractor(request, linke)
                request.post(url=upload_url, json=song_detail)
                print("uploaded --")
            except Exception as e:
                print(e)

    request.close()