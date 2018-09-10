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

    char_map = dict()
    char_info = dict()

    for char in char_json:
        char_map[char["base_id"]] = char["name"]
        char_info[char["name"]] = _create_charinfo(char["name"], char["image"])

    return char_map, char_info


def _get_guild_units(guild_id, guild_data, ship_data):
    r = requests.get("https://swgoh.gg/api/guild/{0}/".format(guild_id))
    units_json = json.loads(r.text)
    
    for player in units_json[players]:
        for unit in player[units]:
            if unit in char_map:
                unit_name = char_map[unit]
                unit_data = guild_data[unit_name]
            else:
                unit_name = ship_map[unit]
                unit_data = ship_data[unit_name]

            owner = player["name"]
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
    char_info = dict()
    char_info["name"] = name
    char_info["img_url"] = img_url
    char_info["force_side"] = "unknown"
    char_info["total_count"] = 0
    char_info["total_gp"] = 0

    star_counts = dict()
    toon_count = dict()
    power_count = dict()
    
    for i in xrange(1, 8):
        star_counts[i] = list()
        toon_count[i] = 0
        power_count[i] = 0

    char_info["star_counts"] = star_counts
    char_info["toon_count"] = toon_count
    char_info["power_count"] = power_count

    return char_info


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
