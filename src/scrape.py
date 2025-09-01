from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
import json
import sys

@dataclass
class Release:
    date: str
    artist: str
    album: str

url = "https://www.metacritic.com/browse/albums/release-date/coming-soon/date"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def get_upcoming_releases() -> list[Release]:
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    calendar = soup.find("div", class_="releaseCalendar")
    if not calendar:
        return []

    table = calendar.find("table", class_="musicTable")
    if not table:
        return []

    rows = table.find_all("tr")
    current_date = None
    releases: list[Release] = []

    for row in rows:
        # If this row is a date header
        if "module" in row.get("class", []):
            th = row.find("th")
            if th:
                current_date = th.get_text(strip=True)
            continue

        # Otherwise, it's a release row
        artist_td = row.find("td", class_="artistName")
        album_td = row.find("td", class_="albumTitle")

        if not artist_td or not album_td or not current_date:
            continue

        artist = artist_td.get_text(strip=True)
        album = album_td.get_text(strip=True)

        releases.append(Release(date=current_date, artist=artist, album=album))

    return releases

if __name__ == "__main__":
    releases = get_upcoming_releases()
    json.dump([release.__dict__ for release in releases], sys.stdout, ensure_ascii=False, indent=2)