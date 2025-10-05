#!/usr/bin/env python3

from flask import Flask, request, jsonify, render_template
import national_db as prgdb
from qr_gen import create_qr_site

app = Flask(__name__)

# set ip (default is '127.0.0.1' you can change it)
IP_ADDR = '127.0.0.1'
# if you want to run it as server in local network, set 'IP_ADDR' to your ip in local network 

# set port (default is '5000', you can change it)
PORT = 5000

# create database file if not exist
prgdb.creat_db('static/db/messages.db')

if not IP_ADDR:
    raise ValueError("Empty IP_ADDR, please set your ip in 'IP_ADDR'.\n(dont set '0.0.0.0', set your valid ip)")
if not PORT:
    raise ValueError("Empty PORT, please set port in 'PORT'")

#-------------------------------
# create qr code
url = f"http://{IP_ADDR}:{PORT}"
create_qr_site(url)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# you can delete/hashing this lines if you want to set qr code manually
# if you delete/hashing this lines, you can set ip address `IP_ADDR = '0.0.0.0'`

# set root of the site
@app.route('/')
def form():
    return render_template('form.html')

# set display page
@app.route('/display')
def display():
    return render_template('display.html')

# set POST api to get data from JS
@app.route('/api/post', methods=['POST'])
def api_post():
    # get data as json from api
    data = request.get_json(silent=True)
    # check if 'data' is not dict
    if not isinstance(data, dict):
        return jsonify({"ok": False, "error": "Invalid JSON"}), 400

    # format a 'name' and 'text'
    name = (data.get('name') or "").strip().capitalize()
    text = (data.get('text') or "").strip()

    # check 'name' and 'text' is exist
    if not name or not text:
        return jsonify({"ok": False, "error": "name and text are required"}), 400

    # add user adn text to database and check if added 
    try:
        res = prgdb.add_user({"name": name, "text": text})
    except Exception as e:
        app.logger.exception("DB error on add_user")
        return jsonify({"ok": False, "error": "server error"}), 500

    if not res.get("ok"):
        # duplicate => 409 Conflict
        return jsonify({"ok": False, "error": res.get("error", "duplicate")}), 409

    return jsonify({"ok": True}), 201

# set GET api to send data to JS
@app.route('/api/get', methods=['GET'])
def api_get():
    # send data from database to 'display' page
    try:
        # get name and text from database and delete it
        msgs = prgdb.pop_messages(limit=500)
        return jsonify(msgs)
    except Exception:
        app.logger.exception("DB error on pop_messages")
        return jsonify([]), 500

# run the app
if __name__ == '__main__':
    app.run(host=IP_ADDR, port=PORT, debug=True)
