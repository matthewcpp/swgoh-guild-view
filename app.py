from flask import Flask, jsonify, request, abort, render_template
import thread
import threading
import time

import Queue

from werkzeug.contrib.cache import SimpleCache

import swgoh_gg

app = Flask(__name__)
cache = SimpleCache()
queue = Queue.Queue()
guild_lock = threading.Lock()
is_processing = False
CACHE_LIFE_HOURS = 5 * 3600


def get_guild_info(guild_url):
    global is_processing
    guild_info = swgoh_gg.get_guild_info(guild_url, cache)

    guild_data = dict()
    guild_data["status"] = "complete"
    guild_data["data"] = guild_info

    cache.set(guild_url, guild_data, timeout=CACHE_LIFE_HOURS)

    with guild_lock:
        if queue.empty():
            is_processing = False
        else:
            next_url = queue.get()

            guild_info = create_guild_info("processing")
            cache.set(next_url, guild_info)
            thread.start_new_thread(get_guild_info, (next_url,))

def create_guild_info(status):
    guild_info = {"status": status}
    guild_info["progress"] = "Initializing"

    return guild_info

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
        guild_info = query_guild_info(guild_url)

        return jsonify(guild_info)

@app.route('/guild_table')
def guild_data_table():
    guild_name = request.args.get('guild_name')
    guild_id = request.args.get('guild_id')

    if guild_name is None or guild_id is None:
        abort(404)
    else:
        guild_url = "http://swgoh.gg/g/{0}/{1}/".format(guild_id, guild_name)
        guild_info = query_guild_info(guild_url)

        while guild_info["status"] != "complete":
            guild_info = cache.get(guild_url)
            time.sleep(1)

        keys = guild_info["data"].keys()
        keys.sort()
        return render_template("html_table.html", data=guild_info["data"], keys=keys)

def query_guild_info(guild_url):
    global is_processing

    guild_info = cache.get(guild_url)

    with guild_lock:
        if guild_info is None:
            if queue.empty() and not is_processing:
                is_processing = True

                guild_info = create_guild_info("processing")
                thread.start_new_thread(get_guild_info, (guild_url,))
            else:
                guild_info = create_guild_info("queued")
                queue.put(guild_url)

            cache.set(guild_url, guild_info, timeout=CACHE_LIFE_HOURS)

    return guild_info

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
