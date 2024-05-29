from bs4 import BeautifulSoup

def extractor(request, page_url) ->dict:
    print(f"extracting : {page_url}")

    page = request.get(page_url)

    soup = BeautifulSoup(page.text, "html.parser")

    song_data = {}

    song_data["slug"] = page_url.split('/').pop()

    song_data["name"] = soup.find("span", "current").text

    song_data["publish"] = soup.find("time", "published")['datetime']

    x = soup.find("div", "text-base lg:text-lg pb-2 text-center md:text-left")

    song_data["lyrics"] = str(x)

    info_soup = soup.find_all("td", "w-3/4 px-5 font-bold border-b border-grey-light", limit=4)

    song_data["singer"] = info_soup[0].get_text(separator="", strip=True).split(",")

    song_data["album"] = info_soup[1].get_text(separator="", strip=True)

    song_data["writer"] = info_soup[2].get_text(separator="", strip=True).split(",")

    song_data["music"] = info_soup[3].get_text(separator="", strip=True)

    thumb_link = soup.find("img", "absolute w-full h-full border shadow-lg outline-none pin")

    if thumb_link is not None :
        song_data["ytvid"] = thumb_link.attrs["src"][27:38]
        song_data["thumbnail"] = thumb_link.attrs["src"].replace("mq","maxres")
    else:
        song_data["ytvid"] = ""
        song_data["thumbnail"] = ""

    print("song data collected ", song_data["slug"])

    return song_data

