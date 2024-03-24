from bs4 import BeautifulSoup
import requests

def formate_lyric(data):
    splitter = "---"
    llist = []
    for x in data.find_all("p"):
        z = BeautifulSoup(str(x).replace("\n<br/>", "--"), "html.parser")
        llist.append(z.text)
    
    return splitter.join(llist)
    

def extractor(page_url) ->dict:
    print(f"extracting : {page_url}", end="\n")

    page = requests.get(page_url)

    soup = BeautifulSoup(page.text, "html.parser")

    song_data = {}

    song_data["name"] = soup.find("span", "current").text

    song_data["publish"] = soup.find("time", "published")['datetime']

    x = soup.find("div", "text-base lg:text-lg pb-2 text-center md:text-left")

    song_data["lyrics"] = formate_lyric(x)

    info_soup = soup.find_all("td", "w-3/4 px-5 font-bold border-b border-grey-light", limit=4)

    song_data["singer"] = info_soup[0].text.replace("\n", '')

    song_data["album"] = info_soup[1].text.replace("\n", '')

    song_data["writer"] = info_soup[2].text.replace("\n", '')

    song_data["music"] = info_soup[3].text.replace("\n", '')

    song_data["image"] = soup.find("img", "absolute w-full h-full border shadow-lg outline-none pin").attrs["src"].replace("mq","maxres")

    song_data["slug"] = song_data["name"].replace(" ", "-").lower()

    song_data["title"] = song_data["name"] + " - " + song_data["album"] + " | " + song_data["singer"]

    return song_data
