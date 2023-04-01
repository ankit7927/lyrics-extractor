from bs4 import BeautifulSoup
import logging as logger
import requests
import psutil

album_url = "https://lyricsmint.com/albums?page="
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

for rp in range(1, 9):
    logger.critical(f"getting data for page {str(rp)}")

    page = requests.get(album_url+str(rp))

    soup = BeautifulSoup(page.text, "html.parser")

    list_album_soup = soup.find_all(
        "a", "h-auto w-full block text-black bg-white no-underline mt-1")

    album_slug_list = []

    for i in list_album_soup:
        album_slug_list.append(i.attrs["href"])
    logger.info("extracted album slugs")

    for inx, i in enumerate(album_slug_list):
        logger.info(f">> page {rp} >> song {inx}")
        album_url = "https://lyricsmint.com/album"+i

        album_page = requests.get(album_url)

        album_soup = BeautifulSoup(album_page.text, "html.parser")

        song_soup_list = album_soup.find_all(
            "a", "h-auto w-full block text-black no-underline")

        for song_soup in song_soup_list:
            temp_url = "https://lyricsmint.com"

            page = requests.get(temp_url+song_soup.attrs["href"])

            soup = BeautifulSoup(page.text, "html.parser")

            try:

                song_name = soup.find(
                    "h3", "text-base text-center uppercase pb-5").text

                song_name = song_name.replace(" Song Info", '').replace("\"", '')

                dicription = soup.find(
                    "div", "entry-summary text-center text-grey-lighter font-normal text-sm mt-4 leading-normal").text

                publish_date = soup.find("time", "published")

                publish_date = publish_date['datetime']

                lyrics = soup.find(
                    "div", "text-base lg:text-lg pb-2 text-center md:text-left")

                info_soup = soup.find_all(
                    "td", "w-3/4 px-5 border-b border-grey-light font-bold", limit=4)


                song_info = {
                    "name": song_name,
                    "dic": dicription.replace("\n", ''),
                    "release_date": publish_date,
                    "lyric": str(lyrics),
                    "singer": info_soup[0].text.replace("\n", ''),
                    "album": info_soup[1].text.replace("\n", ''),
                    "lyrics_by": info_soup[2].text.replace("\n", ''),
                    "music_by": info_soup[3].text.replace("\n", '')
                }

                image_soup = soup.find(
                    "section", "relative font-sans h-auto w-full text-white flex flex-col justify-center bg-black bg-center bg-no-repeat bg-cover")

                artist_image_url = image_soup.attrs["style"].split(
                    ' ')[1].replace("url(", '').replace(");", '')

            

            
                logger.info("sending data to server")

                image_data = request_session.get(artist_image_url).content

                song_img = {
                    "song-image": (song_info["name"]+"-song.jpg", image_data)}

                res = request_session.post(song_post_url, data=song_info, files=song_img)

                logger.info(f"got response => {res.status_code}")
            
            except Exception as e:
                logger.exception(e)

net_io_counters_end = psutil.net_io_counters()

bytes_sent = net_io_counters_end.bytes_sent - net_io_counters_start.bytes_sent
bytes_recv = net_io_counters_end.bytes_recv - net_io_counters_start.bytes_recv


mb_sent = bytes_sent / 1024 / 1024
mb_recv = bytes_recv / 1024 / 1024


logger.warning(f"MB recievd : {mb_recv:.2f} || MB send : {mb_sent:.2f}")


