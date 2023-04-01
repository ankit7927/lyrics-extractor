from bs4 import BeautifulSoup
import logging as logger
import requests
import psutil

album_url = "https://lyricsmint.com/albums?page="
album_post_url = "http://localhost:5000/private/album"

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
    logger.info(f"getting data for page {str(rp)}")
    page = request_session.get(album_url+str(rp))

    soup = BeautifulSoup(page.text, "html.parser")

    list_album_soup = soup.find_all(
        "a", "h-auto w-full block text-black bg-white no-underline mt-1")

    for i in list_album_soup:
        data = {}
        album_slug = i.attrs["href"].replace("/", '')
        data["name"] = i.find(
            "h3", "text-black text-xl text-left st-gradient-head").text
        data["year"] = i.find(
            "span", "my-2 inline-block p-1 px-2 text-left text-white text-xs rounded font-thin st-gradient").text

        album_page = request_session.get("https://lyricsmint.com/"+album_slug)
        album_page_soup = BeautifulSoup(album_page.text, 'html.parser')

        img_soup = album_page_soup.find(
            "section", "relative font-sans h-auto w-full bg-black text-white flex flex-col justify-center bg-cover")

        image_url = img_soup.attrs["style"].split(
            ' ')[1].replace("url(", '').replace(");", '')

        image_data = request_session.get(image_url).content

        album_img = {"album-image": (data["name"]+"-album.jpg", image_data)}

        try:
            logger.info("sending data to server")
            res = request_session.post(album_post_url, data=data, files=album_img)
            logger.info("data sent succesfully")
        except Exception as e:
            logger.exception(e)

net_io_counters_end = psutil.net_io_counters()

bytes_sent = net_io_counters_end.bytes_sent - net_io_counters_start.bytes_sent
bytes_recv = net_io_counters_end.bytes_recv - net_io_counters_start.bytes_recv


mb_sent = bytes_sent / 1024 / 1024
mb_recv = bytes_recv / 1024 / 1024

logger.warning(f"MB recievd : {mb_recv:.2f} || MB send : {mb_sent:.2f}")