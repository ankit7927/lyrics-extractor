from bs4 import BeautifulSoup
import logging as logger
import requests
import psutil

album_url = "https://lyricsmint.com/artists?page="
artist_post_url = "http://localhost:5000/private/artist"

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

for rp in range(2, 9):
    logger.info(f"getting data for page {str(rp)}")
    page = request_session.get(album_url+str(rp))

    soup = BeautifulSoup(page.text, "html.parser")

    list_artist_soup = soup.find_all(
        "a", "relative flex flex-col h-full justify-center text-left text-black text-middle transition-property-bg transition-fast transition-timing-ease-in hover:bg-magenta hover:text-white")

    for inx, i in enumerate(list_artist_soup):
        logger.info(f">> page {rp} > artist {inx}")
        artist_page = request_session.get(
            "https://lyricsmint.com"+i.attrs["href"])

        page_soup = BeautifulSoup(artist_page.text, "html.parser")

        try:
            artist_data = {}

            artist_data["name"] = artist_name = page_soup.find(
                "h1", "text-white text-3xl sm:text-3xl md:text-3xl lg:text-4xl xl:text-5xl").text.replace("\n", '')
            
            artist_name.replace(" ", "+")

            image_soup = page_soup.find(
                "section", "relative font-sans h-auto w-full bg-black text-white flex flex-col justify-center bg-cover")

            artist_image_url = image_soup.attrs["style"].split(
                ' ')[1].replace("url(", '').replace(");", '')

            image_data = request_session.get(artist_image_url).content

            artist_img = {
                "artist-image": (artist_data["name"]+"-artist.jpg", image_data)}

            logger.info("sending data to server")
            res = request_session.post(artist_post_url, data=artist_data, files=artist_img)
            logger.info("data sent succesfully")
        except Exception as e:
            print(e)
            logger.exception(e)


net_io_counters_end = psutil.net_io_counters()

bytes_sent = net_io_counters_end.bytes_sent - net_io_counters_start.bytes_sent
bytes_recv = net_io_counters_end.bytes_recv - net_io_counters_start.bytes_recv


mb_sent = bytes_sent / 1024 / 1024
mb_recv = bytes_recv / 1024 / 1024

logger.warning(f"MB recievd : {mb_recv:.2f} || MB send : {mb_sent:.2f}")


