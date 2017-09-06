from flask import Flask, render_template
import StringIO

from werkzeug.contrib.cache import SimpleCache

import swgoh_gg

app = Flask(__name__)
cache = SimpleCache()

@app.route('/')
def homepage():

    guild_url = "http://swgoh.gg/g/5481/scruffy-nerfed-herders/"

    guild_info = cache.get(guild_url)

    if guild_info is None:
        guild_info = swgoh_gg.get_guild_info(guild_url)
        cache.set(guild_url, guild_info, timeout=5 * 3600)

    return render_template('index.html', guild_info=guild_info)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
