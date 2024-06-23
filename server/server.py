from flask import Flask, jsonify, Response
from flask_cors import CORS
from vertretungs_backend import Vertretungsplan

app = Flask(__name__)
CORS(app)

urls = [
    "https://gesamtschule-waldbroel.de/wp/schueler/heute/subst_001.htm",
    "https://gesamtschule-waldbroel.de/wp/schueler/morgen/subst_001.htm",
]

API_USAGE = """<!--
tag:
    jahrgang:
        stunde:
            fach1:
                fach:
                lehrperson:
                raum:
                text:
            fach2:...
-->\n"""


@app.route("/")
def index():
    return api()


@app.route("/api")
def api():
    return jsonify(
        {
            "heute": Vertretungsplan(urls[0]).get_dict_representation(),
            "morgen": Vertretungsplan(urls[1]).get_dict_representation(),
        }
    )
