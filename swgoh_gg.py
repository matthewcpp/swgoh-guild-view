import requests
from bs4 import BeautifulSoup
from requests_toolbelt.threaded import pool

SWGOH_GG = u"http://swgoh.gg"


def create_charinfo(name, img_url, light_side):
    char_info = dict()
    char_info["name"] = name
    char_info["img_url"] = img_url;
    char_info["force_side"] = "light" if light_side else "dark"

    star_counts = dict()
    for i in xrange(1, 8):
        star_counts[i] = list()

    char_info["star_counts"] = star_counts

    return char_info


def get_member_info(member_name, r, guild_info):
    print "Processing: " + member_name
    soup = BeautifulSoup(r.text, "html.parser")

    char_list = soup.find_all("div", class_="collection-char")

    for char in char_list:
        name = char.find("div", class_="collection-char-name").string.encode('utf-8')
        img_url = char.find("img")["src"]

        classes = char.get('class', [])
        light_side = True if "collection-char-light-side" in classes else False

        has_character = len(char.find_all("div", class_="star")) > 0

        if has_character:
            star_count = 7 - len(char.find_all("div", class_="star-inactive"))

            if name not in guild_info:
                guild_info[name] = create_charinfo(name, img_url, light_side)

            char_info = guild_info[name]

            gear_lvl = char.find("div", class_="char-portrait-full-gear-level").string
            char_info["star_counts"][star_count].append("{0} ({1})".format(member_name, gear_lvl))



def get_guild_info(guild_url, progress):
    guild_info = dict()

    r = requests.get(guild_url)

    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")

        members = soup.find("tbody").find_all("a")
        p = progress.get(guild_url)
        progress.set(guild_url, p)

        processed_members = set()

        member_urls = list()
        member_names = list()

        for member_info in members:
            member_name = member_info.strong.string.encode('utf-8')
            member_url = u"{0}{1}collection".format(SWGOH_GG, member_info["href"])

            if member_name not in processed_members:
                member_names.append(member_name)
                member_urls.append(member_url)
                processed_members.add(member_name)
            else:
                print "Skipping duplicate member: {0}".format(member_name)

        p["progress"] = "Fetching member data"
        progress.set(guild_url, p)
        print p["progress"]

        request_pool = pool.Pool.from_urls(member_urls, None, num_processes=2)
        request_pool.join_all()

        p["progress"] = "Processing member data"
        progress.set(guild_url, p)
        print p["progress"]

        for i, resp in enumerate(request_pool.responses()):
            get_member_info(member_names[i], resp, guild_info)

    else:
        raise Exception("HTTP Error")

    return guild_info
