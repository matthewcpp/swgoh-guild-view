import requests
import json
import copy

from bs4 import BeautifulSoup

char_map = None
char_info = None


def _get_characters():
    r = requests.get("https://swgoh.gg/api/characters/")
    char_json = json.loads(r.text)

    char_map = dict()
    char_info = dict()

    for char in char_json:
        char_map[char["base_id"]] = char["name"]
        char_info[char["name"]] = _create_charinfo(char["name"], char["image"])

    _get_force_sides(char_info)

    return char_map, char_info


def _get_guild_units(guild_id, guild_data):
    r = requests.get("https://swgoh.gg/api/guilds/{0}/units/".format(guild_id))
    units_json = json.loads(r.text)

    for unit in units_json:
        char_name = char_map[unit]
        char_data = guild_data[char_name]

        owners = sorted(units_json[unit], reverse=True, key=lambda o: o["power"])

        for owner in owners:
            star_level = owner["character_stars"]

            char_data["star_counts"][star_level].append({
                "player": owner["player"],
                "power": owner["power"],
                "level": owner["character_level"]
            })


def _get_force_sides(char_info):
    r = requests.get("https://swgoh.gg")
    soup = BeautifulSoup(r.text, "html.parser")

    characters = soup.find_all("li", class_="character")

    for character in characters:
        name = character.find("h5").string
        data = character.get("data-tags")
        char_info[name]["force_side"] = "light" if data.find("light side") is not -1 else "dark"


def _create_charinfo(name, img_url):
    char_info = dict()
    char_info["name"] = name
    char_info["img_url"] = img_url
    char_info["force_side"] = "unknown"

    star_counts = dict()
    for i in xrange(1, 8):
        star_counts[i] = list()

    char_info["star_counts"] = star_counts

    return char_info


def get_guild_data(guild_id):
    global char_map
    global char_info

    if char_info is None:
        char_map, char_info = _get_characters()

    char_data = copy.deepcopy(char_info)
    _get_guild_units(guild_id, char_data)

    return char_data