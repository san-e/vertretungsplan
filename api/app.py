from flask import Flask, current_app, jsonify

# import json
from collections import defaultdict

# import requests
# import os
from vertretungs_backend import Vertretungsplan

app = Flask(__name__)

urls = [
    "https://gesamtschule-waldbroel.de/wp/schueler/heute/subst_001.htm",
    "https://gesamtschule-waldbroel.de/wp/schueler/morgen/subst_001.htm",
]


@app.route("/")
def index():
    return jsonify(Vertretungsplan(urls[0]).get_dict_representation())
    # return current_app.send_static_file("index.html")


# @app.route("/player-api")
# def api():
#     def getPlayerlist():
#             url = f"https://api.discoverygc.com/api/Online/GetPlayers/{os.environ.get('discovery_api_key')}"
#             r = requests.get(url)

#             systems = defaultdict(int)
#             for player in r.json().get("players"):
#                 systems[sysToNickname[player.get("system")]] += 1


#             return jsonify({"playercount": systems, "total": sum(dict(systems).values()), "timestamp": r.json().get("timestamp")})

#     return getPlayerlist()
