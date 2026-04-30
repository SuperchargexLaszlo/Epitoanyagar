import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
ARAK_DIR = os.path.join(DATA_DIR, 'arak')

VAROS_SZORZOK = {
    "budapest": 1.08, "debrecen": 0.97, "miskolc": 0.95, "pecs": 0.94,
    "gyor": 1.02, "nyiregyhaza": 0.96, "kecskemet": 0.98, "szekesfehervar": 1.01,
    "szombathely": 0.99, "szolnok": 0.96, "erd": 1.05, "tatabanya": 1.00,
    "kaposvar": 0.93, "sopron": 1.03, "eger": 0.97, "veszprem": 0.98,
    "zalaegerszeg": 0.96, "dunaujvaros": 0.99, "nagykanizsa": 0.95,
    "hodmezovasarhely": 0.94
}

ANYAG_ARAK = {
    "cement":           {"min": 1200, "max": 1800, "atlag": 1450, "egyseg": "Ft/zsák (25 kg)",
                         "variansok": [{"nev": "CEM I 42.5N", "ar": 1600}, {"nev": "CEM II/B-V 32.5R", "ar": 1250}, {"nev": "CEM III (salak)", "ar": 1350}]},
    "beton":            {"min": 18000, "max": 26000, "atlag": 22000, "egyseg": "Ft/m³",
                         "variansok": [{"nev": "C12/15", "ar": 18500}, {"nev": "C20/25", "ar": 22000}, {"nev": "C25/30", "ar": 25000}]},
    "soder":            {"min": 4000, "max": 7000, "atlag": 5500, "egyseg": "Ft/tonna",
                         "variansok": [{"nev": "0-16 mm mosott", "ar": 4500}, {"nev": "16-32 mm mosott", "ar": 5500}, {"nev": "0-32 mm vegyes", "ar": 4000}]},
    "kavics":           {"min": 5000, "max": 9000, "atlag": 7000, "egyseg": "Ft/tonna",
                         "variansok": [{"nev": "4-8 mm", "ar": 6000}, {"nev": "8-16 mm", "ar": 7000}, {"nev": "16-32 mm", "ar": 8000}]},
    "homok":            {"min": 3500, "max": 6000, "atlag": 4500, "egyseg": "Ft/tonna",
                         "variansok": [{"nev": "Folyami homok", "ar": 4000}, {"nev": "Bányahomok", "ar": 3500}, {"nev": "Mosott homok", "ar": 5500}]},
    "zuzott-ko":        {"min": 4000, "max": 7500, "atlag": 5500, "egyseg": "Ft/tonna",
                         "variansok": [{"nev": "0-16 mm", "ar": 4500}, {"nev": "16-32 mm", "ar": 5500}, {"nev": "32-63 mm", "ar": 6000}]},
    "mesz":             {"min": 800, "max": 1400, "atlag": 1100, "egyseg": "Ft/zsák (25 kg)",
                         "variansok": [{"nev": "Oltott mész", "ar": 900}, {"nev": "Égetett mész", "ar": 1200}, {"nev": "Meszes kötőanyag", "ar": 1000}]},
    "tegla":            {"min": 80, "max": 150, "atlag": 110, "egyseg": "Ft/db",
                         "variansok": [{"nev": "NF tégla (250×120×65)", "ar": 90}, {"nev": "DF tégla (240×115×52)", "ar": 80}, {"nev": "Mélyhornyos tégla", "ar": 130}]},
    "poroton":          {"min": 280, "max": 550, "atlag": 380, "egyseg": "Ft/db",
                         "variansok": [{"nev": "P+W 30 (30 cm)", "ar": 320}, {"nev": "P+W 38 (38 cm)", "ar": 420}, {"nev": "P+W 44 (44 cm)", "ar": 520}]},
    "zsaluko":          {"min": 120, "max": 250, "atlag": 180, "egyseg": "Ft/db",
                         "variansok": [{"nev": "25 cm üreges", "ar": 130}, {"nev": "30 cm üreges", "ar": 170}, {"nev": "38 cm üreges", "ar": 230}]},
    "ytong":            {"min": 350, "max": 700, "atlag": 500, "egyseg": "Ft/db",
                         "variansok": [{"nev": "PP2/0.35 (20 cm)", "ar": 380}, {"nev": "PP4/0.6 (30 cm)", "ar": 520}, {"nev": "PP6/0.8 (40 cm)", "ar": 680}]},
    "b30-blokk":        {"min": 200, "max": 400, "atlag": 290, "egyseg": "Ft/db",
                         "variansok": [{"nev": "B30 normál", "ar": 220}, {"nev": "B30 sarok", "ar": 350}, {"nev": "B30 félblokk", "ar": 130}]},
    "tetocserep":       {"min": 350, "max": 900, "atlag": 580, "egyseg": "Ft/db",
                         "variansok": [{"nev": "Hódfarkú cserép", "ar": 380}, {"nev": "Hullámos cserép", "ar": 520}, {"nev": "Hornyolt cserép", "ar": 750}]},
    "eternit":          {"min": 1800, "max": 3500, "atlag": 2500, "egyseg": "Ft/m²",
                         "variansok": [{"nev": "Hullámos 6 mm", "ar": 1900}, {"nev": "Hullámos 8 mm", "ar": 2500}, {"nev": "Síklap 8 mm", "ar": 3200}]},
    "bitumenes-zsindely": {"min": 2500, "max": 5000, "atlag": 3500, "egyseg": "Ft/m²",
                         "variansok": [{"nev": "3 tab alap", "ar": 2600}, {"nev": "Laminált prémium", "ar": 4200}, {"nev": "Hexagon forma", "ar": 3800}]},
    "tetofolia":        {"min": 400, "max": 1200, "atlag": 700, "egyseg": "Ft/m²",
                         "variansok": [{"nev": "Alap párazáró (75 g/m²)", "ar": 420}, {"nev": "Lélegző fólia (115 g/m²)", "ar": 700}, {"nev": "Prémium diffúz (200 g/m²)", "ar": 1100}]},
    "kozetgyapot":      {"min": 800, "max": 1800, "atlag": 1200, "egyseg": "Ft/m²",
                         "variansok": [{"nev": "5 cm (50 mm)", "ar": 800}, {"nev": "10 cm (100 mm)", "ar": 1300}, {"nev": "15 cm (150 mm)", "ar": 1800}]},
    "uveggyapot":       {"min": 600, "max": 1500, "atlag": 950, "egyseg": "Ft/m²",
                         "variansok": [{"nev": "10 cm tekercs", "ar": 650}, {"nev": "15 cm tekercs", "ar": 950}, {"nev": "20 cm tekercs", "ar": 1400}]},
    "hungarocell":      {"min": 500, "max": 1600, "atlag": 950, "egyseg": "Ft/m²",
                         "variansok": [{"nev": "5 cm EPS 70", "ar": 520}, {"nev": "10 cm EPS 100", "ar": 950}, {"nev": "15 cm EPS 100", "ar": 1400}]},
    "eps":              {"min": 500, "max": 1600, "atlag": 950, "egyseg": "Ft/m²",
                         "variansok": [{"nev": "EPS 70 (5 cm)", "ar": 520}, {"nev": "EPS 100 (10 cm)", "ar": 950}, {"nev": "EPS 150 (15 cm)", "ar": 1400}]},
    "xps":              {"min": 900, "max": 2800, "atlag": 1700, "egyseg": "Ft/m²",
                         "variansok": [{"nev": "5 cm XPS", "ar": 950}, {"nev": "10 cm XPS", "ar": 1750}, {"nev": "15 cm XPS", "ar": 2600}]},
    "jarolap":          {"min": 2000, "max": 8000, "atlag": 4000, "egyseg": "Ft/m²",
                         "variansok": [{"nev": "Gazdaságos (30×30)", "ar": 2200}, {"nev": "Közép (60×60)", "ar": 4200}, {"nev": "Prémium (80×80)", "ar": 7500}]},
    "csempe":           {"min": 2500, "max": 12000, "atlag": 5500, "egyseg": "Ft/m²",
                         "variansok": [{"nev": "Alap (25×40)", "ar": 2700}, {"nev": "Design (30×60)", "ar": 5500}, {"nev": "Prémium (60×120)", "ar": 11000}]},
    "terko":            {"min": 3500, "max": 8000, "atlag": 5000, "egyseg": "Ft/m²",
                         "variansok": [{"nev": "Sima 6 cm", "ar": 3700}, {"nev": "Rácsos 6 cm", "ar": 4800}, {"nev": "Prémium 8 cm", "ar": 7500}]},
    "parkett":          {"min": 8000, "max": 30000, "atlag": 15000, "egyseg": "Ft/m²",
                         "variansok": [{"nev": "Többrétegű tölgy", "ar": 9000}, {"nev": "Tömör tölgy", "ar": 18000}, {"nev": "Prémium egzotikus", "ar": 28000}]},
    "laminalt-padlo":   {"min": 2500, "max": 7000, "atlag": 4000, "egyseg": "Ft/m²",
                         "variansok": [{"nev": "Alap AC3 (8 mm)", "ar": 2700}, {"nev": "Standard AC4 (10 mm)", "ar": 4200}, {"nev": "Prémium AC5 (12 mm)", "ar": 6500}]},
    "vinyl-padlo":      {"min": 3000, "max": 9000, "atlag": 5500, "egyseg": "Ft/m²",
                         "variansok": [{"nev": "LVT kattintós (4 mm)", "ar": 3200}, {"nev": "LVT ragasztós (2 mm)", "ar": 3800}, {"nev": "SPC prémium (6 mm)", "ar": 8500}]},
    "zartszelveny":     {"min": 1200, "max": 4000, "atlag": 2200, "egyseg": "Ft/fm",
                         "variansok": [{"nev": "40×40×2 mm", "ar": 1300}, {"nev": "60×60×3 mm", "ar": 2200}, {"nev": "80×80×4 mm", "ar": 3800}]},
    "szogvas":          {"min": 800, "max": 2500, "atlag": 1500, "egyseg": "Ft/fm",
                         "variansok": [{"nev": "L40×40×4", "ar": 850}, {"nev": "L60×60×6", "ar": 1600}, {"nev": "L80×80×8", "ar": 2400}]},
    "betonacél":        {"min": 280, "max": 420, "atlag": 340, "egyseg": "Ft/kg",
                         "variansok": [{"nev": "B500B Ø8 mm", "ar": 290}, {"nev": "B500B Ø12 mm", "ar": 340}, {"nev": "B500B Ø20 mm", "ar": 400}]},
    "horganyzott-lemez":{"min": 2500, "max": 5500, "atlag": 3800, "egyseg": "Ft/m²",
                         "variansok": [{"nev": "0.5 mm horganyzott", "ar": 2600}, {"nev": "0.8 mm horganyzott", "ar": 3800}, {"nev": "1.2 mm horganyzott", "ar": 5200}]},
    "trapezlemez":      {"min": 2000, "max": 5000, "atlag": 3200, "egyseg": "Ft/m²",
                         "variansok": [{"nev": "T-18 (0.5 mm)", "ar": 2100}, {"nev": "T-35 (0.7 mm)", "ar": 3300}, {"nev": "T-50 (0.9 mm)", "ar": 4800}]},
    "gipszkarton":      {"min": 1800, "max": 2800, "atlag": 2200, "egyseg": "Ft/lap",
                         "variansok": [{"nev": "Standard GKB 12.5 mm", "ar": 1850}, {"nev": "Vízálló GKBI 12.5 mm", "ar": 2400}, {"nev": "Tűzálló GKF 12.5 mm", "ar": 2700}]},
    "polikarbonat":     {"min": 3000, "max": 8000, "atlag": 5000, "egyseg": "Ft/m²",
                         "variansok": [{"nev": "4 mm üregkamrás", "ar": 3200}, {"nev": "10 mm üregkamrás", "ar": 5500}, {"nev": "4 mm tömör", "ar": 7500}]},
    "osb-lap":          {"min": 2500, "max": 5500, "atlag": 3800, "egyseg": "Ft/lap",
                         "variansok": [{"nev": "OSB3 9 mm (2440×1220)", "ar": 2700}, {"nev": "OSB3 15 mm (2440×1220)", "ar": 3900}, {"nev": "OSB3 22 mm (2440×1220)", "ar": 5200}]},
    "retegelt-lemez":   {"min": 4000, "max": 12000, "atlag": 7000, "egyseg": "Ft/lap",
                         "variansok": [{"nev": "Nyírfa 9 mm (2440×1220)", "ar": 4200}, {"nev": "Nyírfa 18 mm (2440×1220)", "ar": 7200}, {"nev": "Nyírfa 24 mm (2440×1220)", "ar": 11500}]},
    "vakolat":          {"min": 700, "max": 1800, "atlag": 1100, "egyseg": "Ft/zsák (25 kg)",
                         "variansok": [{"nev": "Gépi vakolat (30 kg)", "ar": 900}, {"nev": "Kézi vakolat (25 kg)", "ar": 1200}, {"nev": "Diszperziós vakolat", "ar": 1700}]},
    "ragaszto":         {"min": 600, "max": 1500, "atlag": 900, "egyseg": "Ft/zsák (25 kg)",
                         "variansok": [{"nev": "Normál csemperagasztó", "ar": 650}, {"nev": "Flex ragasztó C2", "ar": 1000}, {"nev": "Prémium S2 flex", "ar": 1450}]},
    "habarcs":          {"min": 500, "max": 1200, "atlag": 750, "egyseg": "Ft/zsák (25 kg)",
                         "variansok": [{"nev": "M5 falazóhabarcs", "ar": 520}, {"nev": "M10 falazóhabarcs", "ar": 750}, {"nev": "Hőtechnikai habarcs", "ar": 1150}]},
    "vizszigetelo":     {"min": 1500, "max": 5000, "atlag": 2800, "egyseg": "Ft/m²",
                         "variansok": [{"nev": "Bitumenes kenőanyag", "ar": 1600}, {"nev": "Flexibilis 2K-s", "ar": 2800}, {"nev": "Bitumenes lemez önragasztó", "ar": 4800}]},
    "fugazo":           {"min": 600, "max": 2500, "atlag": 1200, "egyseg": "Ft/kg",
                         "variansok": [{"nev": "Cement alapú normál", "ar": 650}, {"nev": "Cement alapú vízálló", "ar": 1200}, {"nev": "Epoxi fugázó", "ar": 2400}]},
    "gletteloanvag":    {"min": 500, "max": 1200, "atlag": 750, "egyseg": "Ft/zsák (20 kg)",
                         "variansok": [{"nev": "Bázis glett", "ar": 520}, {"nev": "Finomglett", "ar": 800}, {"nev": "Készglett diszperziós", "ar": 1150}]},
    "aljzatbeton":      {"min": 650, "max": 1200, "atlag": 850, "egyseg": "Ft/zsák (25 kg)",
                         "variansok": [{"nev": "F3 aljzatbeton", "ar": 680}, {"nev": "F4 aljzatbeton", "ar": 900}, {"nev": "Önterülő aljzat", "ar": 1150}]},
    "padlolapragaszto": {"min": 700, "max": 1600, "atlag": 1000, "egyseg": "Ft/zsák (25 kg)",
                         "variansok": [{"nev": "Normál padlóragasztó", "ar": 720}, {"nev": "Flex padlóragasztó", "ar": 1050}, {"nev": "Nehéz lapokhoz S2", "ar": 1550}]},
    "penotekercs":      {"min": 200, "max": 600, "atlag": 350, "egyseg": "Ft/m²",
                         "variansok": [{"nev": "2 mm PE hab", "ar": 210}, {"nev": "3 mm PE hab", "ar": 320}, {"nev": "5 mm PE hab akusztikai", "ar": 580}]},
    "szigetelofolia":   {"min": 150, "max": 500, "atlag": 280, "egyseg": "Ft/m²",
                         "variansok": [{"nev": "PE fólia 0.2 mm", "ar": 160}, {"nev": "Párazáró fólia", "ar": 280}, {"nev": "Diffúziónyitott fólia", "ar": 480}]},
    "geotextilia":      {"min": 200, "max": 700, "atlag": 400, "egyseg": "Ft/m²",
                         "variansok": [{"nev": "100 g/m² nem szőtt", "ar": 220}, {"nev": "200 g/m² nem szőtt", "ar": 400}, {"nev": "300 g/m² erősített", "ar": 680}]},
    "drencso":          {"min": 500, "max": 1500, "atlag": 900, "egyseg": "Ft/fm",
                         "variansok": [{"nev": "Ø100 mm perforált", "ar": 550}, {"nev": "Ø160 mm perforált", "ar": 950}, {"nev": "Ø200 mm korrugált", "ar": 1400}]},
    "tetoszeloec":      {"min": 800, "max": 2000, "atlag": 1300, "egyseg": "Ft/fm",
                         "variansok": [{"nev": "Alumínium 2 m", "ar": 850}, {"nev": "Acél horganyzott 2 m", "ar": 1100}, {"nev": "Réz 2 m", "ar": 1900}]},
    "horganyozott-szeg":{"min": 400, "max": 900, "atlag": 600, "egyseg": "Ft/kg",
                         "variansok": [{"nev": "Drótszeg 3.4×100 mm", "ar": 420}, {"nev": "Keret szeg 3.1×80 mm", "ar": 600}, {"nev": "Tető szeg 3.5×120 mm", "ar": 850}]},
    "csavar":           {"min": 800, "max": 2500, "atlag": 1400, "egyseg": "Ft/csomag (200 db)",
                         "variansok": [{"nev": "GK csavar 3.5×35", "ar": 850}, {"nev": "Fémcsavar 4.2×38", "ar": 1400}, {"nev": "Facsavar 5×80 TX", "ar": 2400}]},
    "duplexcsavar":     {"min": 500, "max": 1500, "atlag": 900, "egyseg": "Ft/csomag (100 db)",
                         "variansok": [{"nev": "Műanyag dübel 8×40", "ar": 520}, {"nev": "Fém dübel 10×50", "ar": 950}, {"nev": "Horgony dübel M12", "ar": 1450}]},
    "furatlefedo":      {"min": 80, "max": 250, "atlag": 140, "egyseg": "Ft/db",
                         "variansok": [{"nev": "STR dübel 8×200", "ar": 85}, {"nev": "TID dübel 10×200", "ar": 140}, {"nev": "Fém hőhídmentes 10×230", "ar": 240}]},
    "galvanizalt-anyascsavar": {"min": 600, "max": 1800, "atlag": 1000, "egyseg": "Ft/csomag (50 db)",
                         "variansok": [{"nev": "M8×50 galvanizált", "ar": 620}, {"nev": "M10×70 galvanizált", "ar": 1050}, {"nev": "M12×100 galvanizált", "ar": 1750}]},
    "habragaszto":      {"min": 1200, "max": 2800, "atlag": 1800, "egyseg": "Ft/db (750 ml)",
                         "variansok": [{"nev": "Alap PU ragasztó", "ar": 1250}, {"nev": "Flex PU ragasztó", "ar": 1850}, {"nev": "Prémium poliuretán", "ar": 2700}]},
    "epuletkarton":     {"min": 300, "max": 800, "atlag": 500, "egyseg": "Ft/m²",
                         "variansok": [{"nev": "400 g/m² bitumenes", "ar": 320}, {"nev": "500 g/m² bitumenes", "ar": 510}, {"nev": "700 g/m² erősített", "ar": 780}]},
    "sorolap":          {"min": 3000, "max": 9000, "atlag": 5500, "egyseg": "Ft/m²",
                         "variansok": [{"nev": "Klinker 30×30", "ar": 3200}, {"nev": "Gres kültéri 40×40", "ar": 5500}, {"nev": "Prémium 60×60", "ar": 8500}]},
    "fa-gerenda":       {"min": 1500, "max": 5000, "atlag": 2800, "egyseg": "Ft/fm",
                         "variansok": [{"nev": "Fenyő 10×10 cm", "ar": 1600}, {"nev": "Fenyő 14×14 cm", "ar": 2800}, {"nev": "Fenyő 20×20 cm", "ar": 4800}]},
    "deszka":           {"min": 600, "max": 2000, "atlag": 1100, "egyseg": "Ft/fm",
                         "variansok": [{"nev": "Fenyő 25×100 mm", "ar": 650}, {"nev": "Fenyő 25×150 mm", "ar": 980}, {"nev": "Fenyő 38×200 mm", "ar": 1900}]},
    "lec":              {"min": 200, "max": 600, "atlag": 380, "egyseg": "Ft/fm",
                         "variansok": [{"nev": "Tetőléc 50×30 mm", "ar": 210}, {"nev": "Állványléc 50×50 mm", "ar": 380}, {"nev": "Gipszkarton léc 60×27 mm", "ar": 550}]},
    "laminalt-gerenda": {"min": 3500, "max": 9000, "atlag": 5500, "egyseg": "Ft/fm",
                         "variansok": [{"nev": "BSH 80×160 mm", "ar": 3700}, {"nev": "BSH 120×200 mm", "ar": 5800}, {"nev": "BSH 160×240 mm", "ar": 8500}]},
    "szigeteloszalag":  {"min": 1500, "max": 4000, "atlag": 2500, "egyseg": "Ft/tekercs (50 m)",
                         "variansok": [{"nev": "PE légzáró szalag", "ar": 1600}, {"nev": "Butyl tömítőszalag", "ar": 2600}, {"nev": "Prémium párazáró szalag", "ar": 3800}]},
    "keszlet-habosito": {"min": 1200, "max": 3000, "atlag": 1800, "egyseg": "Ft/db (750 ml)",
                         "variansok": [{"nev": "Alap PU hab", "ar": 1250}, {"nev": "Tűzálló PU hab", "ar": 1900}, {"nev": "Prémium hőálló hab", "ar": 2900}]},
    "szilikon":         {"min": 700, "max": 2000, "atlag": 1200, "egyseg": "Ft/db (310 ml)",
                         "variansok": [{"nev": "Víztiszta szilikon", "ar": 750}, {"nev": "Szaniter szilikon", "ar": 1200}, {"nev": "Prémium UV-álló", "ar": 1900}]},
    "akriltomito":      {"min": 500, "max": 1500, "atlag": 900, "egyseg": "Ft/db (310 ml)",
                         "variansok": [{"nev": "Fehér akril", "ar": 520}, {"nev": "Festékkel festhető", "ar": 900}, {"nev": "Szürke prémium", "ar": 1450}]},
    "falazohalo":       {"min": 300, "max": 900, "atlag": 550, "egyseg": "Ft/m²",
                         "variansok": [{"nev": "145 g/m² standard", "ar": 320}, {"nev": "160 g/m² megerősített", "ar": 580}, {"nev": "200 g/m² prémium", "ar": 880}]},
    "alapozo":          {"min": 400, "max": 1500, "atlag": 800, "egyseg": "Ft/liter",
                         "variansok": [{"nev": "Mélyalapozó", "ar": 450}, {"nev": "Kontaktalapozó", "ar": 850}, {"nev": "Kültéri tapadóhíd", "ar": 1400}]},
    "belteri-festek":   {"min": 800, "max": 3500, "atlag": 1800, "egyseg": "Ft/liter",
                         "variansok": [{"nev": "Alap latex fehér", "ar": 850}, {"nev": "Mosható latex", "ar": 1800}, {"nev": "Prémium supermatt", "ar": 3400}]},
    "kulteri-festek":   {"min": 1200, "max": 5000, "atlag": 2800, "egyseg": "Ft/liter",
                         "variansok": [{"nev": "Alap homlokzatfesték", "ar": 1300}, {"nev": "Szilikon homlokzatfesték", "ar": 2900}, {"nev": "Prémium sziloxán", "ar": 4800}]},
}

FAQ_TEMPLATES = [
    ("Mennyibe kerül {nev} 2026-ban?", "A(z) {nev} ára 2026-ban {min} – {max} {egyseg} között mozog, az átlagár {atlag} {egyseg}."),
    ("Hol lehet olcsón {nev_lower}t venni?", "A legjobb árakhoz érdemes több áruházat összehasonlítani: Bauhaus, OBI, Hornbach és helyi építőanyag-kereskedők. Online rendelésnél a szállítási költséget is vegyük figyelembe."),
    ("Mennyi {nev_lower} kell egy 100 m²-es házhoz?", "Ez erősen függ a felhasználástól és a tervtől. Pontos mennyiséget mindig szakemberrel, a tervdokumentáció alapján számoljon ki."),
    ("Változnak az árak városonként?", "Igen, Budapest és az agglomeráció jellemzően 5-10%-kal drágább az országos átlagnál. Vidéki városokban 3-7%-os kedvezmény is előfordulhat."),
    ("Mire figyelj {nev_lower} vásárlásakor?", "Ellenőrizd a minőségi tanúsítványt, hasonlítsd össze legalább 3 ajánlatot, és kérd be a szállítási díjat is. Nagyobb mennyiségnél alkudj kedvezményre."),
]

def get_anyag_ar(slug):
    clean = slug.replace("é", "e").replace("á", "a").replace("ő", "o").replace("ü", "u").replace("ó", "o").replace("ú", "u").replace("í", "i").replace("ö", "o")
    return ANYAG_ARAK.get(slug) or ANYAG_ARAK.get(clean)

def generate():
    os.makedirs(ARAK_DIR, exist_ok=True)
    anyagok = json.load(open(os.path.join(DATA_DIR, 'anyagok.json'), encoding='utf-8'))
    generated = 0
    for a in anyagok:
        slug = a['slug']
        ar = get_anyag_ar(slug)
        if ar is None:
            ar = {"min": 1000, "max": 3000, "atlag": 2000, "egyseg": "Ft/egység",
                  "variansok": [{"nev": "Alap változat", "ar": 2000}]}
        variansok = [{"nev": v["nev"], "ar": v["ar"], "egyseg": ar["egyseg"]} for v in ar["variansok"]]
        nev = a["nev"]
        nev_lower = nev.lower()
        faq = []
        for kerdes_t, valasz_t in FAQ_TEMPLATES:
            faq.append({
                "kerdes": kerdes_t.format(nev=nev, nev_lower=nev_lower),
                "valasz": valasz_t.format(nev=nev, nev_lower=nev_lower, min=f"{ar['min']:,}".replace(",", " "), max=f"{ar['max']:,}".replace(",", " "), atlag=f"{ar['atlag']:,}".replace(",", " "), egyseg=ar["egyseg"])
            })
        data = {
            "anyag_id": a["id"],
            "frissitve": "2026-04-30",
            "alap_ar": {"min": ar["min"], "max": ar["max"], "atlag": ar["atlag"], "egyseg": ar["egyseg"]},
            "variansok": variansok,
            "varos_szorzok": VAROS_SZORZOK,
            "faq": faq
        }
        out = os.path.join(ARAK_DIR, f"{slug}.json")
        json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        generated += 1
    print(f"Generalva: {generated} fajl -> data/arak/")

if __name__ == '__main__':
    generate()
