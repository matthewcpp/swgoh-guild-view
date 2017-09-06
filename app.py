from flask import Flask, jsonify
import thread

from werkzeug.contrib.cache import SimpleCache

import swgoh_gg

app = Flask(__name__)
cache = SimpleCache()

def get_guild_info(guild_url):
    guild_info = swgoh_gg.get_guild_info(guild_url)

    guild_data = dict()
    guild_data["status"] = "complete"
    guild_data["data"] = guild_info

    cache.set(guild_url, guild_data, timeout=5 * 3600)

@app.route('/')
def homepage():
    return app.send_static_file('index.html')

@app.route('/guild_data')
def guild_data():
    guild_url = "http://swgoh.gg/g/5481/scruffy-nerfed-herders/"

    guild_info = cache.get(guild_url)

    if guild_info is None:
        guild_info = {"status": "processing"}
        cache.set(guild_url, guild_info)
        thread.start_new_thread(get_guild_info, (guild_url,))

    return jsonify(guild_info)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
