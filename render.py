#!/usr/bin/env python3
"""Broadsheet front page for Monday 23 November 2026.

Original renderer written for news-image-20261123. Draws a serif
newspaper page with Pillow: masthead, UTC timeline, four hero panels,
twelve small panels, a world map with numbered pins, 36 one-line
briefs, a date-check box and a footer. Output: entry.png (1024x1024).
Run: python3 render.py
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap

W = H = 1024
PAPER = (246, 240, 227)
INK = (26, 24, 22)
RED = (179, 35, 27)
GREY = (92, 86, 76)
RULE = (40, 38, 34)
SKY = (186, 214, 232)
SAND = (232, 214, 170)
SEA = (168, 205, 226)
GREEN = (70, 140, 90)
NAVY = (24, 42, 74)
GOLD = (214, 164, 32)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
NOTO = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
NOTO_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def wrap(text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(x, y, text, font, max_w, leading, fill=INK, max_lines=None):
    lines = wrap(text, font, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def badge(x, y, n, r=9):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=RED)
    f = F(SANS_B, 11 if n < 10 else 10)
    t = str(n)
    tw = d.textlength(t, font=f)
    d.text((x + r - tw / 2, y + r - 7), t, font=f, fill=(255, 255, 255))


def tag_line(x, y, tag, source):
    f = F(SANS_B, 8)
    col = {"CONFIRMED": (30, 110, 60), "REPORTED": (150, 100, 10),
           "CLAIM": (160, 40, 30)}[tag]
    d.text((x, y), tag, font=f, fill=col)
    tw = d.textlength(tag + "  ", font=f)
    d.text((x + tw, y), source.upper(), font=F(SANS, 8), fill=GREY)


# ---------------- illustrations (flat vector style, drawn in code) --------
def ill_ship(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    d.polygon([(x + 8, y + h - 16), (x + w - 8, y + h - 16),
               (x + w - 26, y + h - 4), (x + 26, y + h - 4)], fill=(60, 70, 80))
    d.rectangle([x + w // 2 - 16, y + h - 34, x + w // 2 + 16, y + h - 16],
                fill=(90, 100, 112))
    d.line([(x + w // 2, y + h - 34), (x + w // 2, y + 8)], fill=INK, width=2)
    d.polygon([(x + w - 30, y + 6), (x + w - 18, y + 14), (x + w - 34, y + 18)],
              fill=RED)
    d.ellipse([x + 14, y + 8, x + 30, y + 24], fill=GOLD)


def ill_chip(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 34, 44))
    cx, cy = x + w // 2, y + h // 2
    d.rectangle([cx - 20, cy - 14, cx + 20, cy + 14], fill=(70, 200, 120))
    for i in range(-2, 3):
        d.line([(cx + i * 10, cy - 14), (cx + i * 10, cy - 24)], fill=(170, 180, 190), width=2)
        d.line([(cx + i * 10, cy + 14), (cx + i * 10, cy + 24)], fill=(170, 180, 190), width=2)
    d.text((x + 6, y + 4), "NVDA", font=F(SANS_B, 10), fill=(200, 220, 200))


def ill_climate(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 220, 200))
    d.ellipse([x + 10, y + 6, x + 46, y + 42], fill=(240, 150, 60))
    tx = x + w - 34
    d.rectangle([tx, y + 6, tx + 8, y + h - 14], outline=INK, width=2)
    d.rectangle([tx + 2, y + 18, tx + 6, y + h - 14], fill=RED)
    d.ellipse([tx - 3, y + h - 20, tx + 11, y + h - 6], fill=RED)
    d.text((x + 52, y + 14), "COP31", font=F(SANS_B, 13), fill=INK)
    d.text((x + 52, y + 30), "ANTALYA", font=F(SANS, 9), fill=GREY)


def ill_building(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(216, 222, 230))
    d.rectangle([x + 14, y + 10, x + 58, y + h - 6], fill=(150, 150, 150))
    d.rectangle([x + 66, y + 20, x + 104, y + h - 6], fill=(120, 120, 120))
    for bx in (x + 20, x + 34, x + 72, x + 86):
        for by in range(y + 16, y + h - 12, 12):
            d.rectangle([bx, by, bx + 8, by + 7], fill=(70, 80, 95))
    d.polygon([(x + 58, y + 10), (x + 78, y + 30), (x + 58, y + 44)], fill=(90, 90, 90))
    d.polygon([(x + w - 34, y + 4), (x + w - 22, y + 16), (x + w - 38, y + 20)], fill=RED)


def ill_missile(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 240))
    d.polygon([(x + 10, y + h - 10), (x + w - 40, y + 12), (x + w - 28, y + 22),
               (x + 22, y + h - 4)], fill=(110, 120, 135))
    d.polygon([(x + w - 40, y + 12), (x + w - 16, y + 6), (x + w - 28, y + 22)], fill=RED)
    for i in range(3):
        d.line([(x + 8 + i * 8, y + h - 8), (x + 2 + i * 8, y + h - 2)], fill=(200, 120, 40), width=3)


def ill_aid(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 238, 230))
    cx, cy = x + w // 2, y + h // 2
    d.rectangle([cx - 5, cy - 14, cx + 5, cy + 14], fill=RED)
    d.rectangle([cx - 14, cy - 5, cx + 14, cy + 5], fill=RED)
    d.rectangle([x + 6, y + h - 12, x + w - 6, y + h - 8], fill=(160, 160, 150))


def ill_star(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 52, 110))
    cx, cy = x + w // 2, y + h // 2
    pts = []
    import math
    for i in range(10):
        r = 16 if i % 2 == 0 else 7
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=(250, 210, 60))


def ill_chart(x, y, w, h, up=True):
    d.rectangle([x, y, x + w, y + h], fill=(245, 245, 240))
    d.line([(x + 6, y + 4), (x + 6, y + h - 6), (x + w - 4, y + h - 6)], fill=INK, width=1)
    pts = [(x + 10, y + h - 12), (x + w // 3, y + h - 22),
           (x + 2 * w // 3, y + h - 16), (x + w - 10, y + 8)]
    if not up:
        pts = [(px, y + h - (py - y)) for px, py in pts]
    d.line(pts, fill=GREEN if up else RED, width=3)


def ill_shield(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 240, 248))
    cx = x + w // 2
    d.polygon([(cx - 16, y + 6), (cx + 16, y + 6), (cx + 16, y + h // 2),
               (cx, y + h - 6), (cx - 16, y + h // 2)], fill=(40, 90, 160))
    d.line([(cx - 7, y + h // 2 - 2), (cx - 2, y + h // 2 + 5), (cx + 8, y + 12)],
           fill=(255, 255, 255), width=3)


def ill_fire(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 236, 210))
    d.rectangle([x + 8, y + h - 18, x + w - 8, y + h - 4], fill=(130, 120, 110))
    for fx in (x + 18, x + w // 2, x + w - 24):
        d.polygon([(fx - 7, y + h - 18), (fx, y + 8), (fx + 7, y + h - 18)], fill=(235, 110, 30))
        d.polygon([(fx - 3, y + h - 18), (fx, y + 16), (fx + 3, y + h - 18)], fill=(250, 190, 60))


def ill_podium(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 242, 238))
    for i, bh in enumerate((16, 26, 12)):
        bx = x + 14 + i * 26
        d.rectangle([bx, y + h - 6 - bh, bx + 20, y + h - 6], fill=(90, 130, 170))
    d.text((x + 16, y + 4), "40.5", font=F(SANS_B, 13), fill=INK)


def ill_gov(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 236, 244))
    d.polygon([(x + 8, y + 14), (x + w // 2, y + 4), (x + w - 8, y + 14)], fill=(100, 110, 130))
    for i in range(4):
        cx = x + 16 + i * ((w - 32) // 3)
        d.rectangle([cx - 3, y + 16, cx + 3, y + h - 10], fill=(150, 155, 165))
    d.rectangle([x + 8, y + h - 10, x + w - 8, y + h - 6], fill=(100, 110, 130))


def ill_train(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(230, 238, 246))
    d.rectangle([x + 8, y + 12, x + w - 8, y + h - 12], fill=(60, 110, 180))
    for i in range(4):
        wx = x + 14 + i * ((w - 28) // 4)
        d.rectangle([wx, y + 16, wx + 12, y + 24], fill=(200, 225, 250))
    d.line([(x + 4, y + h - 8), (x + w - 4, y + h - 8)], fill=INK, width=2)


def ill_gauge(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(242, 240, 232))
    d.text((x + 8, y + 6), "51.7", font=F(SANS_B, 16), fill=INK)
    d.rectangle([x + 8, y + h - 12, x + w - 8, y + h - 8], fill=(200, 200, 190))
    d.rectangle([x + 8, y + h - 12, x + w - 30, y + h - 8], fill=GREEN)


def ill_cricket(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(220, 238, 220))
    d.polygon([(x + 20, y + h - 8), (x + w - 26, y + 8), (x + w - 16, y + 14),
               (x + 30, y + h - 4)], fill=(200, 160, 90))
    d.ellipse([x + w - 22, y + h - 18, x + w - 10, y + h - 6], fill=RED)


def ill_trophy(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(246, 240, 220))
    cx = x + w // 2
    top = y + max(3, h // 6)
    mid = y + max(12, h // 2)
    d.rectangle([cx - 14, top, cx + 14, mid], fill=GOLD)
    d.polygon([(cx - 14, mid), (cx + 14, mid), (cx + 5, mid + 6), (cx - 5, mid + 6)], fill=GOLD)
    d.rectangle([cx - 3, mid + 6, cx + 3, y + h - 8], fill=(170, 130, 40))
    d.rectangle([cx - 12, y + h - 8, cx + 12, y + h - 3], fill=(120, 90, 30))


ILLS = {"ship": ill_ship, "chip": ill_chip, "climate": ill_climate,
        "building": ill_building, "missile": ill_missile, "aid": ill_aid,
        "star": ill_star, "chart": lambda x, y, w, h: ill_chart(x, y, w, h, True),
        "shield": ill_shield, "fire": ill_fire, "podium": ill_podium,
        "gov": ill_gov, "train": ill_train, "gauge": ill_gauge,
        "cricket": ill_cricket, "trophy": ill_trophy}


# ---------------- story data ------------------------------------------------
HEROES = [
    dict(n=1, tag="AFRICA · UKRAINE WAR", ill="ship",
         head="Ukraine sinks Russian corvette in Benghazi",
         dek="Zelenskyy confirms sea drones sank the Mercury; a Baltic cargo ship was also hit.",
         vtag="CONFIRMED", src="Reuters · WSJ"),
    dict(n=2, tag="N. AMERICA · TECH", ill="chip",
         head="Nvidia board reinstates Jensen Huang",
         dek="Unanimous vote 11 days after he quit; Trump calls it “correct and proper”.",
         vtag="CONFIRMED", src="Reuters · USA Today"),
    dict(n=3, tag="GLOBAL · CLIMATE", ill="climate",
         head="COP31 collapses with no climate deal",
         dek="Longest UN climate summit ends with no text on fossil fuels or finance.",
         vtag="CONFIRMED", src="BBC · Al Jazeera"),
    dict(n=4, tag="EUROPE · UKRAINE WAR", ill="building",
         head="Russian strikes kill 15 near Kyiv",
         dek="Rescuers dig in Dymer rubble; Kryvyi Rih toll rises to 11.",
         vtag="REPORTED", src="AP · Reuters"),
]

PANELS = [
    dict(n=5, tag="MIDDLE EAST · IRAN WAR", ill="missile",
         head="Iran vows “all means” vs US blockade",
         dek="Tehran says it will confront the naval siege.",
         vtag="CLAIM", src="Al Jazeera"),
    dict(n=6, tag="MIDDLE EAST · GAZA", ill="aid",
         head="Israeli strikes kill 3, incl. UNRWA worker",
         dek="Adel al-Helou killed on duty.",
         vtag="REPORTED", src="Al Jazeera"),
    dict(n=7, tag="EUROPE · NATO", ill="star",
         head="NATO meets over missiles in Poland",
         dek="Rutte: defend “every inch”.",
         vtag="CONFIRMED", src="Reuters"),
    dict(n=8, tag="N. AMERICA · MARKETS", ill="chart",
         head="Futures rebound; gold near $3,600",
         dek="S&P +2.4%, Nasdaq +3%.",
         vtag="REPORTED", src="Investopedia"),
    dict(n=9, tag="N. AMERICA · TECH", ill="shield",
         head="CrowdStrike to buy Zscaler, $43.9bn",
         dek="All-stock; ~$10bn revenue.",
         vtag="CONFIRMED", src="Companies"),
    dict(n=10, tag="ASIA · DISASTER", ill="fire",
         head="24 dead in Banten factory fire",
         dek="~30 workers still missing.",
         vtag="REPORTED", src="Al Jazeera"),
    dict(n=11, tag="ASIA · POWER INDEX", ill="podium",
         head="India ranked Asia’s No. 3 power, 40.5",
         dek="US 78.9, China 73.6.",
         vtag="CONFIRMED", src="Lowy Institute"),
    dict(n=12, tag="ASIA · POLITICS", ill="gov",
         head="Seoul names first woman spy chief",
         dek="Kang Kum-sil to lead NIS.",
         vtag="CONFIRMED", src="Reuters"),
    dict(n=13, tag="EUROPE · LABOUR", ill="train",
         head="Belgium strike snarls transport",
         dek="Anti-austerity walkout.",
         vtag="CONFIRMED", src="Al Jazeera"),
    dict(n=14, tag="EUROPE · ECONOMY", ill="gauge",
         head="PMI 51.7: Germany up, France down",
         dek="Widest gap in 6 years.",
         vtag="CONFIRMED", src="S&P Global"),
    dict(n=15, tag="OCEANIA · CRICKET", ill="cricket",
         head="India and New Zealand draw in Wellington",
         dek="Flat pitch beats attacks.",
         vtag="CONFIRMED", src="ESPNcricinfo"),
    dict(n=16, tag="S. AMERICA · FOOTBALL", ill="trophy",
         head="Paredes collapses after Boca cup win",
         dek="Faints in TV interview.",
         vtag="CONFIRMED", src="Al Jazeera"),
]

BRIEFS = [
    ("EUROPE", [
        "France rejects EU budget draft, €1.78tn ceiling",
        "Merz wants deeper cuts; Babiš opposes €100bn Ukraine line",
        "NATO intel: Russia plans nuclear-armed satellite",
        "Bomb threats probe at German, Danish schools",
        "ConocoPhillips sells Norway unit for $3.9bn",
        "ABB to buy Ziehl-Abegg for $2.22bn",
        "Julius Baer assets CHF 553bn end-October",
        "French student leaders meet Macron government",
    ]),
    ("MIDDLE EAST", [
        "Three tankers attacked in Strait of Hormuz",
        "Oxfam: 99% of Gaza a “toxic wasteland”",
        "Lebanese families return to ruins in Nabatieh",
        "West Bank “military zones” seized by settlers",
        "Gaza hearing-aid batteries run out",
    ]),
    ("ASIA", [
        "Bangladesh: Hasina faces jail if she returns",
        "Thai court cuts lawmaker’s term 6→3 years",
        "Sensex falls 1,484 pts to 82,436; Nifty 25,350",
        "Rupee ends at 92.92 per dollar",
        "Tata Steel buys 26.6% of APL Apollo, ₹15,510 cr",
        "India offers Nepal $1.6bn flood-rebuild help",
        "Seoul holds defence-AI bill hearing",
        "AlphaFold3 opens 200m protein structures",
    ]),
    ("NORTH AMERICA", [
        "Democrats at 258 House seats, best since 1992",
        "Trump addresses Justice Department",
        "White House vets Fahey as Texas judge pick",
        "Anthropic IPO day 3: ~$89 after $83 debut",
        "Bitcoin back above $61,000",
        "SEC probing Nvidia accounting, sources say",
        "Oregon, Virginia sue SpaceX over Grok",
        "St. Johns River at record 5.67 m in Cocoa",
        "Kilauea eruption episode 57 continues",
    ]),
    ("SOUTH AMERICA · AFRICA", [
        "Brazil lower house votes on fiscal bill",
        "Peru IFS profit flat at $134m; $54m El Niño reserve",
        "Drones reportedly hit Cúcuta police command",
        "Mexico keeps arresting CJNG commanders",
        "Zambia commissions $3m Chikuni solar plant",
        "Six murdered by militants in Nangade",
    ]),
]

TIMELINE = [
    (2.67, "02:40 Vanuatu M6.5"),
    (8.02, "08:01 Macquarie M5.5"),
    (9.0, "09:00 PMI 51.7"),
    (12.38, "12:23 Banten search"),
    (14.6, "14:36 Trump at DOJ"),
    (16.63, "16:38 COP31 falls"),
]

DATE_CHECK = [
    ("Denmark expels Russian attaché", "Fri 21 Nov"),
    ("French court jails 3 police (Zecler)", "Sat 22 Nov"),
    ("Sarvam releases 105B checkpoint", "Sun 22 Nov"),
    ("German AI targeting test, Lithuania", "Sun 22 Nov"),
    ("Peru M6.7 Junín earthquake", "Fri 21 Nov"),
    ("Indonesia M6.8 quake, Timor-Leste", "Sat 22 Nov"),
    ("CAS ruling, Senegal AFCON appeal", "Tue 25 Nov · not yet"),
    ("FIDE title Game 1, Geneva", "Tue 25 Nov · not yet"),
]

# map pins: panel number -> (lon, lat)
PINS = {1: (20, 32), 2: (-122, 37), 3: (31, 37), 4: (30, 50), 5: (51, 36),
        6: (34, 31), 7: (19, 52), 8: (-74, 41), 9: (-98, 30), 10: (106, -6),
        11: (77, 29), 12: (127, 37), 13: (4, 51), 14: (9, 50), 15: (175, -41),
        16: (-58, -35)}

# ---------------- masthead --------------------------------------------------
d.rectangle([0, 0, W, 5], fill=RED)
d.text((14, 12), "THE WORLD'S NEWS OF ONE DAY", font=F(SANS_B, 11), fill=RED)
counts = "52 STORIES · 7 REGIONS · 17 FIELDS · ALL FROM THIS MONDAY"
cf = F(SANS_B, 11)
d.text((W - 14 - d.textlength(counts, font=cf), 12), counts, font=cf, fill=INK)
d.text((12, 26), "Monday 23 November 2026", font=F(SERIF_B, 56), fill=INK)
d.line([(12, 92), (W - 12, 92)], fill=RULE, width=3)
d.line([(12, 97), (W - 12, 97)], fill=RULE, width=1)

# ---------------- timeline --------------------------------------------------
ty = 102
d.text((12, ty), "THE DAY\nIN UTC", font=F(SANS_B, 10), fill=RED)
ax0, ax1, ay = 92, W - 40, ty + 20
d.line([(ax0, ay), (ax1, ay)], fill=INK, width=2)
d.text((ax0 - 4, ay + 4), "00:00", font=F(SANS, 8), fill=GREY)
d.text((ax1 - 24, ay + 4), "24:00", font=F(SANS, 8), fill=GREY)
tf = F(SANS_B, 8.5)
for i, (hr, label) in enumerate(TIMELINE):
    px = ax0 + (ax1 - ax0) * hr / 24.0
    d.ellipse([px - 3, ay - 3, px + 3, ay + 3], fill=RED)
    tw = d.textlength(label, font=tf)
    lx = min(max(px - tw / 2, ax0), W - 14 - tw)
    ly = ty - 4 if i % 2 == 0 else ay + 13
    d.text((lx, ly), label, font=tf, fill=INK)

# ---------------- hero + panel cards ---------------------------------------
def hero_card(x, y, w, h, s):
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    ILLS[s["ill"]](x + 1, y + 1, w - 2, 62)
    badge(x + 8, y + 70, s["n"])
    d.text((x + 32, y + 73), s["tag"], font=F(SANS_B, 9), fill=RED)
    yy = text_block(x + 8, y + 92, s["head"], F(SERIF_B, 21), w - 16, 24, max_lines=3)
    yy = text_block(x + 8, yy + 2, s["dek"], F(NOTO, 11), w - 16, 14, fill=(60, 56, 50), max_lines=3)
    tag_line(x + 8, y + h - 16, s["vtag"], s["src"])


def panel_card(x, y, w, h, s):
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    ILLS[s["ill"]](x + 1, y + 1, w - 2, 32)
    badge(x + 6, y + 38, s["n"], r=8)
    d.text((x + 26, y + 41), s["tag"], font=F(SANS_B, 7.5), fill=RED)
    yy = text_block(x + 6, y + 58, s["head"], F(SERIF_B, 13.5), w - 12, 16, max_lines=3)
    yy = text_block(x + 6, yy + 1, s["dek"], F(NOTO, 9), w - 12, 11, fill=(60, 56, 50), max_lines=2)
    tag_line(x + 6, y + h - 14, s["vtag"], s["src"])


hy, hh = 152, 218
hw = (W - 24 - 3 * 8) // 4
for i, s in enumerate(HEROES):
    hero_card(12 + i * (hw + 8), hy, hw, hh, s)

py, ph = hy + hh + 8, 146
pw = (W - 24 - 5 * 6) // 6
for r in range(2):
    for c in range(6):
        panel_card(12 + c * (pw + 6), py + r * (ph + 6), pw, ph, PANELS[r * 6 + c])

# ---------------- map --------------------------------------------------------
my = py + 2 * ph + 14
d.text((12, my), "WHERE IT HAPPENED", font=F(SANS_B, 11), fill=INK)
d.text((196, my), "3 = ANTALYA · COP31", font=F(SANS, 8), fill=GREY)
mx, mw, mh = 12, 330, 150
d.rectangle([mx, my + 16, mx + mw, my + 16 + mh], fill=SEA, outline=RULE)


def lonlat(lon, lat):
    return (mx + (lon + 180) / 360 * mw, my + 16 + (75 - lat) / 135 * mh)


# Simplified continent blobs (stylised, not to survey accuracy)
BLOBS = [
    [(-165, 60), (-120, 70), (-80, 65), (-65, 45), (-75, 35), (-85, 25),
     (-95, 18), (-105, 20), (-120, 35), (-135, 55), (-155, 58)],
    [(-78, 8), (-60, 10), (-50, 0), (-38, -12), (-48, -25), (-58, -38),
     (-68, -50), (-73, -40), (-72, -25), (-78, -10), (-80, 2)],
    [(-16, 16), (-5, 32), (12, 34), (28, 31), (38, 20), (48, 12), (42, -5),
     (35, -22), (28, -33), (18, -32), (13, -18), (9, 0), (-8, 5)],
    [(-9, 37), (-9, 44), (0, 46), (3, 52), (10, 57), (18, 60), (24, 60),
     (30, 60), (28, 68), (12, 66), (5, 58), (0, 50), (-4, 48), (-2, 43),
     (3, 42), (8, 44), (14, 45), (20, 40), (26, 38), (22, 37), (14, 40),
     (8, 44), (0, 38)],
    [(28, 41), (45, 42), (60, 45), (80, 50), (100, 55), (120, 52),
     (140, 48), (160, 52), (178, 62), (170, 66), (150, 70), (120, 73),
     (90, 75), (60, 69), (40, 64), (30, 55), (28, 48)],
    [(45, 12), (55, 24), (60, 25), (66, 25), (72, 20), (80, 13), (88, 22),
     (92, 16), (98, 10), (103, 5), (107, 12), (110, 20), (118, 25),
     (122, 30), (126, 38), (130, 42), (138, 35), (142, 40), (140, 48),
     (135, 45), (128, 40), (122, 32), (115, 23), (108, 15), (100, 8),
     (95, 16), (89, 22), (80, 15), (72, 20), (61, 25), (52, 26), (48, 28),
     (42, 15)],
    [(113, -22), (122, -17), (132, -11), (142, -11), (146, -18), (153, -27),
     (150, -37), (140, -38), (129, -32), (118, -35), (114, -28)],
    [(167, -45), (172, -41), (176, -38), (178, -37), (174, -35), (168, -46)],
]
for blob in BLOBS:
    d.polygon([lonlat(a, b) for a, b in blob], fill=SAND, outline=(150, 130, 90))
PIN_OFF = {4: (6, -8), 7: (10, 2), 13: (-10, -6), 14: (-4, 10), 3: (8, 6),
           5: (8, -6), 6: (-8, 6)}
for n, (lon, lat) in PINS.items():
    px, py2 = lonlat(lon, lat)
    ox, oy = PIN_OFF.get(n, (0, 0))
    px, py2 = px + ox, py2 + oy
    d.ellipse([px - 7, py2 - 7, px + 7, py2 + 7], fill=RED, outline=(255, 255, 255))
    f = F(SANS_B, 8)
    t = str(n)
    d.text((px - d.textlength(t, font=f) / 2, py2 - 5), t, font=f, fill=(255, 255, 255))
d.text((mx + 4, my + 16 + mh - 13), "Pins match panel numbers 1–16", font=F(SANS, 8), fill=NAVY)

# date check under map
dy = my + 16 + mh + 8
d.rectangle([12, dy, 342, dy + 118], outline=RED, width=1)
d.text((18, dy + 5), "DATE CHECK — LEFT OUT AS NOT 23 NOVEMBER", font=F(SANS_B, 9), fill=RED)
yy = dy + 22
for name, when in DATE_CHECK:
    d.text((18, yy), name, font=F(NOTO, 9), fill=INK)
    wf = F(SANS_B, 8)
    d.text((336 - d.textlength(when, font=wf), yy), when, font=wf, fill=GREY)
    yy += 11.5

# ---------------- briefs -----------------------------------------------------
bx = 352
d.text((bx, my), "ALSO ON MONDAY 23 NOVEMBER", font=F(SANS_B, 11), fill=INK)
col_w = (W - bx - 12 - 10) // 2
asia_items = BRIEFS[2][1]
left_groups = [BRIEFS[0], BRIEFS[1], ("ASIA", asia_items[:5])]
right_groups = [("ASIA (CONT.)", asia_items[5:]), BRIEFS[3], BRIEFS[4]]
cols = [(bx, left_groups), (bx + col_w + 10, right_groups)]
num = 17
bf = F(NOTO, 9.5)
hf = F(SANS_B, 9)
for cx, groups in cols:
    yy = my + 18
    for gname, items in groups:
        d.text((cx, yy), gname, font=hf, fill=RED)
        yy += 13
        for it in items:
            badge(cx, yy - 1, num, r=7)
            yy = text_block(cx + 19, yy, it, bf, col_w - 22, 11, max_lines=2)
            yy += 2
            num += 1
        yy += 4

# ---------------- footer -----------------------------------------------------
fy = H - 34
d.line([(12, fy), (W - 12, fy)], fill=RULE, width=1)
d.text((12, fy + 5),
       "Every story here happened, or was first reported, on Monday 23 November 2026. "
       "CLAIM = one side’s account, not independently confirmed.",
       font=F(NOTO, 9), fill=INK)
d.text((12, fy + 19),
       "Sources: Reuters, AP, AFP, Al Jazeera, BBC, WSJ, S&P Global, Investopedia, GDACS/USGS and others. Original drawings.",
       font=F(NOTO, 9), fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
