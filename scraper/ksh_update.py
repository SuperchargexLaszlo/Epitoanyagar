#!/usr/bin/env python3
"""
KSH-adatok automatikus frissítése az „Építőanyag árak alakulása” oldalhoz.

Letölti a KSH STADAT táblákat, kiszámolja a szükséges mutatókat, és frissíti a
data/statisztika.json fájlt. A fájl csak akkor íródik, ha a KSH-adat ténylegesen
változott – így a GitHub Action csak új KSH-közlés után commitol (és indít buildet).

Védőkorlátok:
  * Ha egy tábla nem tölthető le vagy nem értelmezhető, annak a résznek a régi
    értéke marad, a többi rész frissül.
  * Minden indexértéket tartományra ellenőriz (50–300); gyanús értéknél az adott
    rész nem frissül.
  * A kézzel írt „hirek” lista és egyéb, nem KSH-ból jövő mezők megmaradnak.

Futtatás:  python scraper/ksh_update.py            (frissít, ha van új adat)
           python scraper/ksh_update.py --dry-run  (csak kiírja, mi változna)
Kilépési kód: 0 mindig (hiba esetén is), hogy a workflow ne álljon le.
"""
import json
import os
import re
import sys
import time
from datetime import datetime, timezone

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover
    print("Hiányzik: pip install requests beautifulsoup4")
    sys.exit(0)

BASE = os.path.dirname(os.path.abspath(__file__))
STAT_FILE = os.path.join(BASE, "..", "data", "statisztika.json")
UA = {"User-Agent": "Mozilla/5.0 (compatible; epitoanyagar-bot/1.0; +https://epitoanyagar.hu)"}
HONAPOK = ["január", "február", "március", "április", "május", "június", "július",
           "augusztus", "szeptember", "október", "november", "december"]
HONAP_ROVID = ["jan.", "febr.", "márc.", "ápr.", "máj.", "jún.", "júl.", "aug.", "szept.", "okt.", "nov.", "dec."]
NEGYEDEK = ["I.", "II.", "III.", "IV."]
SZAKAGAZATOK = [
    ("23.3", "Tégla, cserép, kerámia építőanyag (23.3)"),
    ("23.6", "Beton-, gipsz-, cementtermék (23.6)"),
    ("16", "Fafeldolgozás (16)"),
    ("23.5", "Cement, mész, gipsz (23.5)"),
    ("23", "Nemfém ásványi termékek összesen (23)"),
]


def url(tabla: str) -> str:
    return f"https://www.ksh.hu/stadat_files/{tabla[:3]}/hu/{tabla}.html"


def letolt(tabla: str):
    """A tábla sorai cellaszöveg-listaként (több <table> esetén egymás után)."""
    utolso_hiba = None
    for probalkozas in range(3):
        time.sleep(3 if probalkozas == 0 else 30)  # a KSH tűzfala a gyors egymás utáni kéréseket blokkolja
        try:
            r = requests.get(url(tabla), headers=UA, timeout=90)
            r.raise_for_status()
            if b"Request Rejected" in r.content[:500]:
                raise RuntimeError("a KSH tűzfala elutasította a kérést")
            break
        except Exception as e:  # noqa: BLE001
            utolso_hiba = e
    else:
        raise RuntimeError(f"letöltés sikertelen: {utolso_hiba}")
    # A STADAT oldalak ISO-8859-2 kódolásúak (a fejléc megadja); ha nincs megadva, abból indulunk ki.
    kod = r.encoding if r.encoding and r.encoding.lower() not in ("iso-8859-1",) else "iso-8859-2"
    html = r.content.decode(kod, errors="replace")
    s = BeautifulSoup(html, "html.parser")
    sorok = []
    for tb in s.find_all("table"):
        for tr in tb.find_all("tr"):
            sorok.append([c.get_text(" ", strip=True) for c in tr.find_all(["th", "td"])])
        sorok.append(["__TABLA_VEGE__"])
    return sorok


def szam(s):
    s = (s or "").replace("\xa0", "").replace(" ", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def ev_of(s):
    m = re.match(r"^(\d{4})\.?$", (s or "").strip())
    return m.group(1) if m else None


def index_ok(*vals):
    return all(v is not None and 50 <= v <= 300 for v in vals)


def pct(v):
    """Index (előző = 100) → változás %-ban, 1 tizedesre."""
    return round(v - 100, 1)


# ---------------------------------------------------------------- táblák

def lak0011():
    szint, yoy, szakasz = [], [], ""
    for r in letolt("lak0011"):
        if len(r) == 1:
            szakasz = r[0]
            continue
        ev = ev_of(r[0]) if r else None
        if not ev or len(r) < 4:
            continue
        e, m, a = szam(r[1]), szam(r[2]), szam(r[3])
        if not index_ok(e, m, a):
            continue
        if "2015" in szakasz:
            if int(ev) >= 2015:
                szint.append({"ev": ev, "anyag": a, "munkaero": m, "osszes": e})
        elif "előző" in szakasz.lower():
            yoy.append({"ev": ev, "anyag": pct(a), "munkaero": pct(m), "osszes": pct(e)})
    if len(szint) < 5 or len(yoy) < 5:
        raise ValueError("lak0011: kevés sor")
    return szint, yoy


def lak0035():
    out, szakasz, ev = [], "", None
    for r in letolt("lak0035"):
        if len(r) == 1:
            szakasz = r[0]
            continue
        if len(r) < 5 or "előző év" not in szakasz.lower():
            continue
        ev = ev_of(r[0]) or ev
        if r[1] not in NEGYEDEK or not ev:
            continue
        e, m, a = szam(r[2]), szam(r[3]), szam(r[4])
        if not index_ok(e, m, a):
            continue  # még nincs adat
        out.append({"n": f"{ev} {r[1]}", "anyag": pct(a), "munkaero": pct(m), "osszes": pct(e)})
    out = [x for x in out if int(x["n"][:4]) >= 2021]
    if len(out) < 8:
        raise ValueError("lak0035: kevés sor")
    return out


def lak0012():
    """Új családi ház fajlagos költsége (ezer Ft/m²), 2020a-tól."""
    fejlec, adat = [], {}
    for r in letolt("lak0012"):
        if r and r[0] == "__TABLA_VEGE__":
            fejlec = []
            continue
        if r and r[0].startswith("Megnevezés"):
            fejlec = r[1:]
            continue
        if fejlec and r and r[0].strip().lower().startswith("új családi ház"):
            for ev, v in zip(fejlec, r[1:]):
                n = szam(v)
                if n:
                    adat[ev.strip()] = int(n)
    kulcsok = [k for k in adat if re.match(r"^20\d\d", k) and (k >= "2021" or k == "2020a")]
    kulcsok.sort(key=lambda k: (k[:4], k))
    out = [{"ev": k, "ertek": adat[k]} for k in kulcsok]
    if len(out) < 4 or not all(200 <= x["ertek"] <= 3000 for x in out):
        raise ValueError("lak0012: hibás adat")
    return out


def ara0031():
    out = {}
    for r in letolt("ara0031"):
        ev = ev_of(r[0]) if r else None
        if ev and len(r) >= 2 and index_ok(szam(r[1])):
            out[ev] = pct(szam(r[1]))
    if len(out) < 5:
        raise ValueError("ara0031: kevés sor")
    return out


def ara0061():
    """Építőipari termelői ár, legfrissebb negyedév, előző év azonos negyedéve = 100."""
    szakasz, ev, utolso = "", None, None
    for r in letolt("ara0061"):
        if len(r) == 1:
            szakasz = r[0].lower()
            continue
        if len(r) < 6 or not szakasz.startswith("előző év azonos"):
            continue
        ev = ev_of(r[0]) or ev
        if r[1] in NEGYEDEK and index_ok(szam(r[2]), szam(r[3])):
            utolso = {"negyed": f"{ev} {r[1]}", "epitoipari_ar": pct(szam(r[2])), "epuletek": pct(szam(r[3]))}
    if not utolso:
        raise ValueError("ara0061: nincs adat")
    return utolso


def ara0059():
    sorok = letolt("ara0059")
    evek = [ev_of(c) for c in sorok[0][1:]]
    evek = [e for e in evek if e]
    oszlopok = [(e, h) for e in evek for h in range(12)]  # (év, hónap index)
    mom, decota, szakasz = {}, {}, ""
    kodok = {k for k, _ in SZAKAGAZATOK}
    for r in sorok:
        if len(r) == 1:
            szakasz = r[0].lower()
            continue
        if not r or r[0] not in kodok or len(r) < 2 + len(oszlopok):
            continue
        ertekek = [szam(v) for v in r[2:2 + len(oszlopok)]]
        if szakasz.startswith("előző hó"):
            mom[r[0]] = ertekek
        elif "december" in szakasz:
            decota[r[0]] = ertekek
    if set(mom) != kodok:
        raise ValueError("ara0059: hiányzó szakágazat")
    # utolsó kitöltött hónap
    utolso_i = max(i for i, v in enumerate(mom["23"]) if v is not None)
    u_ev, u_ho = oszlopok[utolso_i]
    teljes_evek = [e for e in evek[1:] if int(e) < int(u_ev) or u_ho == 11]
    adatok = []
    for kod, nev in SZAKAGAZATOK:
        m = mom[kod][:utolso_i + 1]
        if any(v is None or not 80 <= v <= 130 for v in m):
            raise ValueError(f"ara0059: hibás havi érték ({kod})")
        szint, L = [], 100.0
        for v in m:
            L *= v / 100
            szint.append(L)
        eves = {}
        for e in teljes_evek:
            i0 = evek.index(e) * 12
            akt = sum(szint[i0:i0 + 12]) / 12
            elo = sum(szint[i0 - 12:i0]) / 12
            eves[e] = round(akt / elo * 100 - 100, 1)
        yoy = round(szint[utolso_i] / szint[utolso_i - 12] * 100 - 100, 1)
        d = decota.get(kod, [None] * len(oszlopok))[utolso_i]
        adatok.append({"kod": kod, "nev": nev, "eves": eves, "utolso_yoy": yoy,
                       "dec_ota": pct(d) if index_ok(d) else None})
    return {
        "evek": teljes_evek[-3:],
        "utolso_honap": f"{u_ev}. {HONAPOK[u_ho]}",
        "utolso_honap_rovid": f"{u_ev}. {HONAP_ROVID[u_ho]}",
        "elozo_dec": f"{int(u_ev) - 1}. december",
        "adatok": adatok,
    }


def ara0073():
    sorok = letolt("ara0073")
    evek = [ev_of(c) for c in sorok[0][2:]]
    evek = [e for e in evek if e]
    szakasz, sor = "", None
    for r in sorok:
        if len(r) == 1:
            szakasz = r[0].lower()
            continue
        if r and r[0] == "04.3.1" and "előző év azonos" in szakasz:
            sor = r
            break
    if not sor:
        raise ValueError("ara0073: nincs 04.3.1 sor")
    havi = []
    for bi, e in enumerate(evek):
        blokk = sor[2 + bi * 13: 2 + bi * 13 + 13]  # [súly, jan..dec]
        for h, v in enumerate(blokk[1:13]):
            n = szam(v)
            if n is not None:
                if not index_ok(n):
                    raise ValueError("ara0073: hibás érték")
                havi.append({"ev": e, "h": h, "ertek": pct(n)})
    decemberek = [{"ev": x["ev"], "ertek": x["ertek"]} for x in havi if x["h"] == 11 and int(x["ev"]) >= 2019]
    utolso8 = [{"ho": f"{HONAP_ROVID[x['h']]}" if x["ev"] == havi[-1]["ev"] else f"{x['ev']}. {HONAP_ROVID[x['h']]}",
                "ertek": x["ertek"]} for x in havi[-8:]]
    u = havi[-1]
    return {"decemberek": decemberek, "havi": utolso8,
            "utolso": {"honap": f"{u['ev']}. {HONAPOK[u['h']]}", "ertek": u["ertek"]}}


def epi0013():
    szakasz, ev, utolso, kum = "", None, None, None
    for r in letolt("epi0013"):
        if len(r) == 1:
            szakasz = r[0].lower()
            continue
        if len(r) < 5:
            continue
        ev = ev_of(r[0]) or ev
        t, uj = szam(r[2]), szam(r[3])
        if t is None or uj is None or not 30 <= t <= 300 or not 10 <= uj <= 400:
            continue  # még nincs adat
        if szakasz == "havonta" and r[1] in HONAPOK:
            utolso = {"honap": f"{ev}. {r[1]}", "termeles": pct(t), "uj_szerzodesek": round(uj - 100, 1)}
        elif "kumul" in szakasz:
            kum = {"idoszak": f"{ev}. {r[1]}", "termeles": pct(t)}
    if not utolso or not kum:
        raise ValueError("epi0013: nincs adat")
    return {**utolso, "kumulalt_idoszak": kum["idoszak"], "kumulalt": kum["termeles"]}


# ---------------------------------------------------------------- összerakás

def main():
    dry = "--dry-run" in sys.argv
    with open(STAT_FILE, encoding="utf-8") as f:
        st = json.load(f)
    regi = json.dumps({k: v for k, v in st.items() if k != "frissitve"}, ensure_ascii=False, sort_keys=True)
    hibak = []

    def probal(nev, fn):
        try:
            return fn()
        except Exception as e:  # noqa: BLE001
            hibak.append(f"{nev}: {e}")
            print(f"  ! {nev}: {e} – a régi érték marad")
            return None

    r11 = probal("lak0011", lak0011)
    r31 = probal("ara0031", ara0031)
    if r11:
        szint, yoy = r11
        st["anyagkoltseg_szint_2015"] = {
            "cim": "Lakásépítés anyagköltség-indexe (2015 = 100)", "forras": "KSH 18.1.1.11",
            "url": url("lak0011"), "adatok": szint}
        for y in yoy:
            y["epitoipari_ar"] = (r31 or {}).get(y["ev"])
        st["eves_valtozas"] = {
            "cim": "Éves változás az előző évhez képest (%)",
            "forras": "KSH 18.1.1.11 (lakásépítési költségindex), 1.1.1.31 (építőipari termelői árindex)",
            "adatok": [y for y in yoy if int(y["ev"]) >= 2019]}

    r35 = probal("lak0035", lak0035)
    if r35:
        st["negyedeves_anyag"] = {
            "cim": "Lakásépítés anyagköltsége, változás az előző év azonos negyedévéhez (%)",
            "forras": "KSH 18.2.1.7", "url": url("lak0035"), "adatok": r35}

    r12 = probal("lak0012", lak0012)
    if r12:
        st["fajlagos_koltseg"] = {
            "cim": "Fajlagos lakásépítési költség, új családi ház (ezer Ft/m²)", "forras": "KSH 18.1.1.12",
            "url": url("lak0012"),
            "megjegyzes": "2020-ban a KSH frissítette a becslési modellt (2020a), ezért a 2020 előtti értékek nem hasonlíthatók közvetlenül.",
            "adatok": r12}

    r59 = probal("ara0059", ara0059)
    if r59:
        st["szakagazatok"] = {"cim": "Építőanyag-gyártók belföldi termelői árai, változás (%)",
                              "forras": "KSH 1.2.1.23 havi láncindexeiből számolva", "url": url("ara0059"), **r59}

    r73 = probal("ara0073", ara0073)
    if r73:
        st["fogyasztoi_04_3_1"] = {
            "cim": "Lakásjavítási és -karbantartási anyagok fogyasztói ára, változás az előző év azonos hónapjához (%)",
            "forras": "KSH 1.2.1.7 (04.3.1)", "url": url("ara0073"), **r73}

    r61 = probal("ara0061", ara0061)
    r13 = probal("epi0013", epi0013)
    t = st.get("termelo", {})
    if r61:
        t.update(r61)
        t["url"] = url("ara0061")
    if r13:
        t["termeles"] = r13
        t["termeles_url"] = url("epi0013")
    st["termelo"] = t
    st.pop("termelo_2026", None)
    st.pop("kovetkezo_ksh_kozles", None)

    uj = json.dumps({k: v for k, v in st.items() if k != "frissitve"}, ensure_ascii=False, sort_keys=True)
    if uj == regi:
        print(f"Nincs új KSH-adat. ({len(hibak)} hiba)")
        return 0
    st["frissitve"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if dry:
        print("Változna (dry-run):")
        print(json.dumps(st, ensure_ascii=False, indent=1)[:3000])
        return 0
    with open(STAT_FILE, "w", encoding="utf-8") as f:
        json.dump(st, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"statisztika.json frissítve ({st['frissitve']}). Hibák: {hibak or 'nincs'}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        print(f"Váratlan hiba: {e}")
        sys.exit(0)
