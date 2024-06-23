from bs4 import BeautifulSoup, ResultSet, Tag
import requests
from dataclasses import dataclass
from typing import List, Dict, Tuple
from collections import defaultdict


@dataclass
class Stunde:
    stunde: str
    lehrperson: Tuple[str, str]
    fach: Tuple[str, str]
    raum: Tuple[str, str]
    text: Tuple[str, str]

    def wird_vertreten(self) -> bool:
        return self.lehrperson[1].isalpha() and self.lehrperson[0] != self.lehrperson[1]

    def ausfall(self) -> bool:
        return not self.lehrperson[1].isalpha() or not all(
            x.isalnum() or x.isspace() for x in self.raum[1]
        )

    def kommentar(self) -> str:
        return ". ".join(self.text)

    def lehrer(self) -> str:
        return self.lehrperson[0]

    def vertreter(self) -> str:
        if self.wird_vertreten:
            return self.lehrperson[1]
        else:
            return ""

    def fach_(self) -> str:
        return self.fach_[0]

    def raumwechsel(self) -> bool:
        return not self.raum[0] == self.raum[1]


class Vertretungsplan:
    column_names: List[str]
    stunden: Dict[str, Stunde]

    def __init__(self, url: str):
        html_data: str = requests.get(url).text
        soup: BeautifulSoup = BeautifulSoup(html_data, "html.parser")
        main_table: ResultSet = soup.find_all("table", class_="mon_list")
        assert len(main_table) == 1
        rows: ResultSet = main_table[0].find_all("tr")
        self.column_names = [x.text.strip().lower() for x in rows[0].find_all("th")]
        rows.pop(0)
        stunden = defaultdict(list)
        row: Tag
        for row in rows:
            columns: ResultSet = row.find_all("td")
            if len(columns) != len(self.column_names):
                continue

            klasse = columns[0].text
            columns.pop(0)
            args = {
                "stunde": columns[0].text,
                "lehrperson": (columns[1].text.strip(), columns[2].text.strip()),
                "fach": (columns[3].text.strip(), columns[4].text.strip()),
                "raum": (columns[5].text.strip(), columns[6].text.strip()),
                "text": (columns[7].text.strip(), columns[8].text.strip()),
            }
            stunden[klasse].append(Stunde(**args))
        self.stunden = dict(stunden)

    def get_dict_representation(self):
        json = defaultdict(list)
        for jahrgang, stunden in self.stunden.items():
            for stunde in stunden:
                json[jahrgang].append(vars(stunde))
        return dict(json)


if __name__ == "__main__":
    vertretungsplan = Vertretungsplan(url=urls[0])
    import json

    with open("aaa.json", "w") as f:
        json.dump(vertretungsplan.get_dict_representation(), f, indent=1)
    klasse = "12"
    print(f"Klasse {klasse}:")
    for stunde in vertretungsplan.stunden[klasse]:
        if stunde.wird_vertreten():
            print(
                f"Die {stunde.stunde}. Stunde {stunde.fach()} von {stunde.lehrer()} wird von {stunde.vertreter()} vertreten."
            )
        elif stunde.ausfall():
            print(
                f"Die {stunde.stunde}. Stunde {stunde.fach()} von {stunde.lehrer()} fällt aus!{(' Kommentar: ' + stunde.kommentar()) if any(x.isalpha() for x in stunde.kommentar()) else ''}"
            )
        elif stunde.raumwechsel():
            print(
                f"Die {stunde.stunde}. Stunde {stunde.fach()} von {stunde.lehrer()} findet in {stunde.raum[1]} anstatt von {stunde.raum[0]} statt."
            )


# data = defaultdict(str)
# for i in range(len(table_rows) - 1):
#     i += 1
#     row = table_rows[i]
#     for j, entry in row.find_all("th"):
#         data[columns[j]] = entry
