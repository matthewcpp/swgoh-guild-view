from flask import Flask, jsonify, request, abort, render_template

import swgoh_gg

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/view_guild')
@app.route('/view_guild/')
def view_guild():
    return app.send_static_file('view_guild.html')

@app.route('/guild_data')
@app.route('/guild_data/')
def guild_data():
    guild_id = request.args.get('guild_id')

    if guild_id is None:
        abort(404)
    else:
        guild_info = swgoh_gg.get_guild_data(guild_id)

        return jsonify(guild_info)


@app.route('/guild_table')
@app.route('/guild_table/')
def guild_table():
    guild_id = request.args.get('guild_id')

    if guild_id is None:
        abort(404)
    else:
        guild_info = swgoh_gg.get_guild_data(guild_id)

        return render_template("html_table.html", data=guild_info)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
