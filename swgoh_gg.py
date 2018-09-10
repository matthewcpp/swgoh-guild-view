import requests
import json
import copy

from bs4 import BeautifulSoup

char_map = None
char_info = None

ship_map = None
ship_info = None


def _get_characters(url):
    r = requests.get(url)
    char_json = json.loads(r.text)

    cmap = dict()
    cinfo = dict()

    for char in char_json:
        cmap[char["base_id"]] = char["name"]
        cinfo[char["name"]] = _create_charinfo(char["name"], char["image"])

    return cmap, cinfo


def _get_guild_units(guild_id, guild_data, gship_data):
    r = requests.get("https://swgoh.gg/api/guild/{0}/".format(guild_id))
    units_json = json.loads(r.text)

    for player in units_json["players"]:
        for unit in player["units"]:
            if unit["data"]["base_id"] in char_map:
                unit_name = char_map[unit["data"]["base_id"]]
                unit_data = guild_data[unit_name]
            else:
                unit_name = ship_map[unit["data"]["base_id"]]
                unit_data = ship_data[unit_name]

            owner = player["data"]["name"]
            star_level = unit["data"]["rarity"]
            unit_data["toon_count"][star_level] += 1
            unit_data["total_count"] += 1
            unit_data["total_gp"] += unit["data"]["power"]
            unit_data["power_count"][star_level] += unit["data"]["power"]
            unit_data["star_counts"][star_level].append({
                "player": owner,
                "power": unit["data"]["power"],
                "level": unit["data"]["level"]
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
    c_info = dict()
    c_info["name"] = name
    c_info["img_url"] = img_url
    c_info["force_side"] = "unknown"
    c_info["total_count"] = 0
    c_info["total_gp"] = 0

    star_counts = dict()
    toon_count = dict()
    power_count = dict()

    for i in xrange(1, 8):
        star_counts[i] = list()
        toon_count[i] = 0
        power_count[i] = 0

    c_info["star_counts"] = star_counts
    c_info["toon_count"] = toon_count
    c_info["power_count"] = power_count

    return c_info


def get_guild_data(guild_id):
    global char_map
    global char_info

    global ship_info
    global ship_map

    if char_info is None:
        char_map, char_info = _get_characters("https://swgoh.gg/api/characters/?format=json")

    if ship_info is None:
        ship_map, ship_info = _get_characters("https://swgoh.gg/api/ships/?format=json")

    char_data = copy.deepcopy(char_info)
    ship_data = copy.deepcopy(ship_info)

    _get_guild_units(guild_id, char_data, ship_data)

    return char_data, ship_data
