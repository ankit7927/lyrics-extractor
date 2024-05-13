from lyricsmint import extractor
import requests, time, sys

if __name__=="__main__":
    upload_url = input("Enter upload url : ")
    if upload_url == "":
        print("exiting upload url is none")
        sys.exit()

    request = requests.Session()
    with open("page_links.txt", "r") as file:
        for linke in file.read().splitlines():
            song_detail = extractor(request, linke)

            time.sleep(2)

            request.post(url=upload_url, data=song_detail)

    request.close()