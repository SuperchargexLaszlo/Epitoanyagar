#!/usr/bin/env python3
"""
Ár-frissítő scraper az epitoanyagar.hu-hoz.

Cél: havonta lefut (GitHub Action), frissíti a data/arak/*.json fájlokat és
a `frissitve` dátumot, majd commitol -> a Netlify automatikusan újraépít.

DEFENZÍV MŰKÖDÉS – sosem töri el az adatokat:
  * Ha egy anyaghoz be van állítva forrás (scraper/sources.json) ÉS az elérhető,
    a valós árral frissíti az `alap_ar`-t és arányosan a variánsokat.
  * Ha nincs forrás vagy a letöltés/parszolás hibázik, a MEGLÉVŐ árakat megtartja.
  * A `frissitve` dátumot minden futáskor a mai napra állítja (havi felülvizsgálat).

sources.json formátum (opcionális, lásd sources.example.json):
{
  "cement": { "url": "https://...", "selector": "span.price", "egyseg": "Ft/zsák (25 kg)" }
}
A selector szövegéből az első "12 345" / "12.345" / "12345 Ft" mintát olvassa ki.
"""
import json
import os
import re
import sys
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "..", "data")
ARAK_DIR = os.path.join(DATA_DIR, "arak")
SOURCES_FILE = os.path.join(BASE, "sources.json")

UA = "Mozilla/5.0 (compatible; epitoanyagar-bot/1.0; +https://epitoanyagar.hu)"
PRICE_RE = re.compile(r"(\d{1,3}(?:[ . ]\d{3})+|\d+)")


def today() -> str:
    # A GitHub Action a futás napját adja; env-ből felülírható teszthez.
    return os.environ.get("PRICE_DATE") or datetime.now(timezone.utc).strftime("%Y-%m-%d")


def load_sources() -> dict:
    if os.path.exists(SOURCES_FILE):
        try:
            with open(SOURCES_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"  ! sources.json nem olvasható: {e}")
    return {}


def fetch_price(url: str, selector: str):
    """Egy oldalról egyetlen ár kiolvasása. Hibánál None."""
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        print("  ! requests/bs4 nincs telepítve – forrás-scrape kihagyva")
        return None
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=20)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        el = soup.select_one(selector)
        if not el:
            return None
        m = PRICE_RE.search(el.get_text())
        if not m:
            return None
        return int(re.sub(r"[ . ]", "", m.group(1)))
    except Exception as e:
        print(f"  ! letöltés/parszolás hiba ({url}): {e}")
        return None


def apply_new_avg(ar_data: dict, uj_atlag: int) -> None:
    """Az új átlagár arányában skálázza a min/max/variáns értékeket."""
    regi = ar_data["alap_ar"]["atlag"]
    if not regi or uj_atlag <= 0:
        return
    faktor = uj_atlag / regi
    ar_data["alap_ar"]["atlag"] = uj_atlag
    ar_data["alap_ar"]["min"] = int(round(ar_data["alap_ar"]["min"] * faktor))
    ar_data["alap_ar"]["max"] = int(round(ar_data["alap_ar"]["max"] * faktor))
    for v in ar_data.get("variansok", []):
        v["ar"] = int(round(v["ar"] * faktor))


def main() -> int:
    sources = load_sources()
    datum = today()
    if not os.path.isdir(ARAK_DIR):
        print(f"HIBA: nincs meg a {ARAK_DIR}")
        return 1

    fajlok = sorted(f for f in os.listdir(ARAK_DIR) if f.endswith(".json"))
    frissitve_db = scraped_db = valtozott = 0

    for fn in fajlok:
        slug = fn[:-5]
        path = os.path.join(ARAK_DIR, fn)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        elozo = json.dumps(data, ensure_ascii=False, sort_keys=True)

        src = sources.get(slug)
        if src and src.get("url") and src.get("selector"):
            ar = fetch_price(src["url"], src["selector"])
            if ar:
                apply_new_avg(data, ar)
                scraped_db += 1
                print(f"  ✓ {slug}: új átlagár {ar} {data['alap_ar']['egyseg']}")

        # A dátum csak akkor frissül, ha az ár ténylegesen változott.
        # (Korábban minden futás átírta, így az oldal friss dátumot mutatott változatlan árakkal.)
        uj = json.dumps(data, ensure_ascii=False, sort_keys=True)
        if uj == elozo:
            continue
        data["frissitve"] = datum
        frissitve_db += 1
        valtozott += 1
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")

    print(f"\nKész. {frissitve_db} fájl dátumozva ({datum}), "
          f"{scraped_db} valós forrásból frissítve, {valtozott} tartalmilag változott.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
