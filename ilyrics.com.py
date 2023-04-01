from bs4 import BeautifulSoup
import logging as logger
import requests
import psutil

album_url = "https://www.ilyricshub.com/bollywood-songs-lyrics/"
song_post_url =""
inp= input("Enter Song Post URL : ")   ##"http://localhost:5000/private/song"

if inp == "-":
    song_post_url = "http://localhost:5000/private/song"
elif inp == "":
    raise Exception("Song Post Url must provided ")

logger.basicConfig(
    level=logger.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logger.FileHandler("logs.log"),  # Log to a file
        logger.StreamHandler()  # Log to the console
    ]
)

request_session = requests.Session()

net_io_counters_start = psutil.net_io_counters()


page = request_session.get(album_url)

page_soup = BeautifulSoup(page.text, 'html.parser')

list_album_year = page_soup.find_all("ul", "movie-list")


for list_album in list_album_year:

    for i in list_album.find_all("a"):

        album_song_list_url = "https://www.ilyricshub.com"+i.attrs["href"]

        album_song_list_page = request_session.get(album_song_list_url)

        album_song_list_soup = BeautifulSoup(album_song_list_page.text, "html.parser")

        song_urls = album_song_list_soup.find_all("h2", "post-title entry-title")

        for j in song_urls:

            try:
                song_data = {}

                song_url = j.find("a").attrs["href"]
                
                song_page = request_session.get(song_url)

                song_page_soup = BeautifulSoup(song_page.text, "html.parser")

                song_data["dic"]  = song_page_soup.find("div", "song_decsp").text.replace("\n", '')

                image_url = song_page_soup.find("div", "song_img").find("img").attrs["data-lazy-src"]

                image_data = request_session.get(image_url).content

                song_info = song_page_soup.find_all("tr", limit=5)

                song_data["name"] = song_info[0].text.replace("\n", '').replace("Song:", '')

                song_data["album"] = song_info[1].text.replace("\n", '').replace("Movie:", '')

                song_data["singer"] = song_info[2].text.replace("\n", '').replace("Singer:", '')

                song_data["lyrics_by"] = song_info[3].text.replace("\n", '').replace("Lyrics:", '')

                song_data["music_by"] = song_info[4].text.replace("\n", '').replace("Music:", '')

                song_data["release_date"] = start_year

                temp = ""
                for k in song_page_soup.find("div", "song_lyrics").find_all("p"):
                    temp = temp+str(k)
                
                song_data["lyric"] = temp

                song_img = {"song-image": (song_data["name"]+"-song.jpg", image_data)}

                res = request_session.post(song_post_url, data=song_data, files=song_img)

                logger.info(f"got response => {res.status_code}")
            except Exception as e:
                logger.error(e)
            #break
        #break
    #break
   



    start_year = start_year-1







net_io_counters_end = psutil.net_io_counters()

bytes_sent = net_io_counters_end.bytes_sent - net_io_counters_start.bytes_sent
bytes_recv = net_io_counters_end.bytes_recv - net_io_counters_start.bytes_recv


mb_sent = bytes_sent / 1024 / 1024
mb_recv = bytes_recv / 1024 / 1024


logger.warning(f"MB recievd : {mb_recv:.2f} || MB send : {mb_sent:.2f}")


