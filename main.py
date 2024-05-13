from lyricsmint import extractor
import requests, time

upload_url = ""

if __name__=="__main__":
    songs = []
    request = requests.Session()
    with open("page_links.txt", "r") as file:
        for linke in file.read().splitlines():
            song_detail = extractor(request, linke)
            songs.append(song_detail)
            time.sleep(2)

            request.post(url=upload_url, data=song_detail)

    request.close()