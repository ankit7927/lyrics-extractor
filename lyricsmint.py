from bs4 import BeautifulSoup
import requests, sqlite3, sys

file_name = "page_links.txt"
db_path = "E:/company/lyricslibrary/db.sqlite3"
connection = sqlite3.connect(db_path)

# for i in connection.execute("SELECT name FROM sqlite_master").fetchall():
#     print(i)

# sys.exit()

def extractor(page_url):
    print(f"extracting : {page_url}", end="\n")

    page = requests.get(page_url)

    soup = BeautifulSoup(page.text, "html.parser")

    song_data = {}

    song_data["name"] = soup.find("span", "current").text

    song_data["publish"] = soup.find("time", "published")['datetime']

    song_data["lyrics"] = soup.find("div", "text-base lg:text-lg pb-2 text-center md:text-left").text.replace("\n", "\n")

    info_soup = soup.find_all("td", "w-3/4 px-5 font-bold border-b border-grey-light", limit=4)

    song_data["singer"] = info_soup[0].text.replace("\n", '')

    song_data["album"] = info_soup[1].text.replace("\n", '')

    song_data["writer"] = info_soup[2].text.replace("\n", '')

    song_data["music"] = info_soup[3].text.replace("\n", '')

    song_data["image"] = soup.find("img", "absolute w-full h-full border shadow-lg outline-none pin").attrs["src"].replace("mq","maxres")

    song_data["slug"] = song_data["name"].replace(" ", "-").lower()

    song_data["title"] = song_data["name"] + "-" + song_data["album"] + " | " + song_data["singer"]

    connection.execute("insert into api_songlyric values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (None, song_data["name"], song_data["album"], song_data["singer"], song_data["writer"], song_data["music"], song_data["slug"], song_data["title"], song_data["image"], song_data["publish"], song_data["lyrics"], ))
    connection.commit()

    print(f"inserted : {song_data["name"]}", end="\n")

file = open(file_name, "r")
for page_url in file.readlines():
    try:
        extractor(page_url=page_url)
    except Exception as e:
        print(e)

file.close()
