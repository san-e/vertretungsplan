from flask import Flask, current_app, jsonify
from vertretungs_backend import Vertretungsplan

app = Flask(__name__)

urls = [
    "https://gesamtschule-waldbroel.de/wp/schueler/heute/subst_001.htm",
    "https://gesamtschule-waldbroel.de/wp/schueler/morgen/subst_001.htm",
]


@app.route("/")
def index():
    return jsonify(Vertretungsplan(urls[0]).get_dict_representation())
