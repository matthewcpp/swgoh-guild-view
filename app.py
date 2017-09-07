from flask import Flask, jsonify, request, abort
import thread

from werkzeug.contrib.cache import SimpleCache

import swgoh_gg

app = Flask(__name__)
cache = SimpleCache()

def get_guild_info(guild_url):
    guild_info = swgoh_gg.get_guild_info(guild_url, cache)

    guild_data = dict()
    guild_data["status"] = "complete"
    guild_data["data"] = guild_info

    cache.set(guild_url, guild_data, timeout=5 * 3600)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/view_guild')
@app.route('/view_guild/')
def view_guild():
    return app.send_static_file('view_guild.html')

@app.route('/guild_data')
def guild_data():
    guild_name = request.args.get('guild_name')
    guild_id = request.args.get('guild_id')

    if guild_name is None or guild_id is None:
        abort(404)
    else:
        guild_url = "http://swgoh.gg/g/{0}/{1}/".format(guild_id, guild_name)

        guild_info = cache.get(guild_url)

        if guild_info is None:

            guild_info = {"status": "processing"}
            guild_info["progress"] = dict()
            guild_info["progress"]["processed"] = 0
            guild_info["progress"]["total"] = 1

            cache.set(guild_url, guild_info)
            thread.start_new_thread(get_guild_info, (guild_url,))

        return jsonify(guild_info)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
