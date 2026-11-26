#!/usr/bin/env python3
"""Render THE WORLD TODAY - Wednesday 25 November 2026.

Build-time only: draws a 1024x1024 front-page PNG from the story list below
using Pillow. No network, no timestamps, fixed seed: two runs are identical.
"""
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

F_BLACK = "/usr/share/fonts/truetype/noto/NotoSans-Black.ttf"
F_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
F_SERIF_R = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# ---- palette ----
NAVY = (13, 27, 46)
NAVY2 = (18, 38, 64)
GOLD = (212, 175, 55)
RED = (178, 34, 34)
REDBG = (146, 20, 20)
PAPER = (250, 247, 240)
INK = (22, 24, 28)
MUTED = (92, 96, 104)
CARD = (255, 255, 255)
LINE = (205, 200, 188)
BLUE = (24, 78, 140)
TEAL = (14, 110, 105)

# ---- stories: (place, headline, dek, source) ----
HERO = ("HODEIDAH, YEMEN",
        "Saudi-led coalition strikes Hodeidah port",
        "Strikes hit the port after an evacuation order. The Houthis threaten "
        "Saudi Red Sea ports.",
        "REUTERS")

LEADS = [
    ("JIUQUAN, CHINA",
     "Shenzhou-24 lifts off with the first Pakistani in orbit",
     "Long March-2F lifts off at 00:18 UTC with Muhammad Zeeshan Ali, 40 - "
     "the first Pakistani in orbit.",
     "REUTERS / XINHUA"),
    ("ASIA MARKETS",
     "Asian shares plunge on tariff fears",
     "Korea -5.8%, Taiwan -4.7%, Nikkei -2.8% as the US trade chief readies a "
     "probe of excess industrial capacity.",
     "REUTERS"),
    ("WASHINGTON, US",
     "Pentagon audits curriculum in base schools",
     "The Pentagon audits lessons in about 160 schools on US bases under a "
     "$5.7m contract.",
     "AP"),
]

MIDS = [
    ("MIDDLETOWN, IOWA", "Army to detonate five tons of lead azide",
     "Five tons of unstable explosive are destroyed in a controlled blast.", "AP"),
    ("HONIARA", "Solomon Islands sign Australia treaty",
     "Australia becomes the primary security partner; no foreign base.", "REUTERS / AP"),
    ("PYONGYANG", "North Korea expels Swiss diplomat",
     "Envoy given 48 hours to leave; Pyongyang office ordered shut.", "REUTERS / AP"),
    ("BENGALURU", "Flipkart chief steps down after 11 years",
     "Kalyan Krishnamurthy leaves on 4 December; an interim chief takes over.", "REUTERS"),
    ("LONDON", "UK sent a sex-offender refugee to Eswatini",
     "A convicted offender was resettled in an undisclosed deal; he later died.", "BBC"),
    ("DARMSTADT", "Hera unveils first Dimorphos close-ups",
     "ESA reveals a stadium-sized crater on the asteroid moon.", "BBC"),
    ("WASHINGTON", "US Marshals reach 20,000 DC arrests",
     "Task force hits the milestone 15 months after launch.", "US MARSHALS / NBC"),
    ("CANBERRA", "Australia inflation jumps to 4.9%",
     "October CPI up from 4.3%; trimmed mean 3.8%.", "REUTERS"),
]

# briefs: (place, text, source)
BRIEFS = [
    ("MALAYSIA", "Malaysia buys 10 Boeing 787 Dreamliners.", "REUTERS"),
    ("STRAIT OF HORMUZ", "Iran says two tankers hit mines and caught fire.", "REUTERS"),
    ("ENGLAND", "England has the widest frailty gap of 31 nations.", "THE GUARDIAN"),
    ("LONDON", "Chess Classic opens; Abdusattorov wins round one.", "CHESS.COM"),
    ("NEW YORK", "Anthropic sinks to $73.85; value briefly under $1tn.", "REUTERS"),
    ("SOUTH KOREA", "Births rise 12.2% in September, fastest in nine months.", "YONHAP"),
    ("SAN FRANCISCO", "Anthropic posts a shorter Riemann proof.", "ANTHROPIC"),
    ("SAN FRANCISCO", "King tides peak; Bay Area roads flood.", "NWS"),
    ("NEW YORK", "Bitcoin sinks to $57,300 on hot US inflation.", "COINDESK"),
    ("UNITED STATES", "US economy grew 4.3% in Q3, revised up from 3.4%.", "BEA"),
    ("AUSTRALIA", "Ex-policeman guilty of Sydney double murder.", "BBC"),
    ("WASHINGTON", "Core inflation hits 3.3%; December hike all but set.", "BEA"),
    ("PARIS", "Roma end PSG's perfect Champions League record.", "UEFA"),
    ("UKRAINE", "My family died in Ukraine, a BBC journalist investigates.", "BBC"),
    ("UNITED STATES", "BBC revisits the FBI agent's cold case after last month's guilty verdict.", "BBC"),
    ("INDIA", "Sensex jumps over 2% as Asia's markets slide.", "THE HINDU BUSINESSLINE"),
    ("INDIA", "Amazon's exports from India reach $27 billion.", "THE HINDU BUSINESSLINE"),
    ("BOGOR, INDONESIA", "Dozens trapped as floodwater swamps a gold mine.", "REUTERS"),
    ("GHANA", "German-African business summit closes in Accra.", "AHK GHANA"),
    ("ENGLAND", "Middle-aged women least likely to quit smoking.", "THE GUARDIAN"),
    ("BRITAIN", "New tide measure may sharpen flood forecasts.", "THE GUARDIAN"),
    ("BRITAIN", "Immigration misperceptions widespread, study finds.", "SKY NEWS"),
    ("BRAZIL", "Latin America science forum meets in Brasilia.", "UNESCO"),
    ("WASHINGTON", "US proposes new tariffs on 14 trading partners.", "REUTERS"),
    ("SWITZERLAND", "Chess title match drawn; Gukesh-Sindarov level at 1-1.", "FIDE"),
    ("SOUTH KOREA", "'Hope' takes Best Film; 'Possible Love' wins four.", "SPORTS CHOSUN"),
]

KPI = [("KOSPI", "-5.8%"), ("NIKKEI", "-2.8%"), ("BRENT", "$90.97"),
       ("SENSEX", "+2.3%"), ("SZ-24 TESTS", "90+ PLANNED"), ("AUS CPI", "4.9%"),
       ("KOREA BIRTHS", "+12.2%")]

# pins: (number, label, lat, lon)
PINS = [
    (1, "Hodeidah", 15.0, 43.0),
    (2, "Jiuquan", 40.0, 100.0),
    (3, "Tokyo", 35.7, 139.7),
    (4, "Pentagon", 38.9, -77.0),
    (5, "Middletown", 40.8, -91.3),
    (6, "Honiara", -9.4, 160.0),
    (7, "Pyongyang", 39.0, 125.8),
    (8, "Bengaluru", 13.0, 77.6),
    (9, "London", 51.5, -0.1),
    (10, "Darmstadt", 49.87, 8.65),
    (11, "Washington", 38.9, -77.0),
    (12, "Canberra", -35.3, 149.1),
]

# ---- coarse land mask: (latitude, [(lon_start, lon_end), ...]) ----
LAND = [
    (72, [(-168, -95), (30, 180)]),
    (68, [(-168, -60), (5, 180)]),
    (64, [(-168, -55), (10, 178)]),
    (60, [(-165, -55), (5, 175)]),
    (56, [(-160, -55), (-10, 170)]),
    (52, [(-155, -55), (-10, 165)]),
    (48, [(-125, -65), (-10, 140)]),
    (44, [(-125, -70), (-10, 140)]),
    (40, [(-125, -75), (-10, 135)]),
    (36, [(-120, -80), (-10, 130)]),
    (32, [(-115, -85), (-10, 125)]),
    (28, [(-110, -80), (-10, 120)]),
    (24, [(-110, -80), (-5, 115)]),
    (20, [(-105, -85), (-15, 110)]),
    (16, [(-100, -80), (-15, 105)]),
    (12, [(-95, -75), (-15, 100)]),
    (8, [(-85, -75), (-13, 50), (95, 105)]),
    (4, [(-80, -75), (5, 45), (95, 105)]),
    (0, [(-80, -70), (10, 45), (100, 110)]),
    (-4, [(-80, -65), (10, 40), (105, 115)]),
    (-8, [(-75, -40), (10, 40), (110, 125)]),
    (-12, [(-70, -35), (12, 40), (115, 140)]),
    (-16, [(-65, -35), (12, 35), (115, 145)]),
    (-20, [(-60, -35), (12, 35), (115, 145)]),
    (-24, [(-55, -40), (15, 35), (120, 145)]),
    (-28, [(-55, -40), (15, 33), (130, 145)]),
    (-32, [(-55, -40), (18, 32), (135, 150)]),
    (-36, [(-70, -55), (140, 150)]),
    (-40, [(-70, -65), (145, 150)]),
    (-44, [(-70, -65)]),
]

EXCLUDED = ("NOT 25 NOV - LEFT OUT: Huawei verdict - Riyadh tower strike - "
            "Abu Dhabi talks - Real Madrid 5-1 PSV (all 24 Nov)")


def wrap(d, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_tag(d, x, y, text, fnt, fg, bg):
    w = d.textlength(text, font=fnt) + 10
    d.rounded_rectangle([x, y, x + w, y + 15], radius=3, fill=bg)
    d.text((x + 5, y + 2), text, font=fnt, fill=fg)
    return w


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    rng = random.Random(20261125)

    # ---- masthead ----
    d.rectangle([0, 0, W, 96], fill=NAVY)
    d.rectangle([0, 96, W, 99], fill=GOLD)
    d.text((24, 14), "THE WORLD TODAY", font=font(F_BLACK, 46), fill=(255, 255, 255))
    d.text((24, 66), "Wednesday 25 November 2026  -  38 stories from six continents",
           font=font(F_BOLD, 17), fill=GOLD)
    d.rounded_rectangle([W - 252, 22, W - 24, 74], radius=6, outline=GOLD, width=2)
    d.text((W - 238, 30), "38 STORIES", font=font(F_BLACK, 20), fill=(255, 255, 255))
    d.text((W - 238, 54), "6 CONTINENTS", font=font(F_BOLD, 12), fill=GOLD)

    # ---- KPI strip ----
    d.rectangle([0, 99, W, 138], fill=(238, 234, 224))
    x = 24
    kf = font(F_BOLD, 11)
    vf = font(F_BLACK, 17)
    for label, val in KPI:
        d.text((x, 104), label, font=kf, fill=MUTED)
        d.text((x, 118), val, font=vf, fill=RED)
        x += max(d.textlength(label, font=kf), d.textlength(val, font=vf)) + 26
        if x < W - 20:
            d.line([x - 13, 106, x - 13, 132], fill=LINE, width=1)

    # ---- hero ----
    hy, hh = 146, 168
    d.rectangle([24, hy, W - 24, hy + hh], fill=CARD, outline=LINE, width=1)
    d.rectangle([24, hy, W - 24, hy + 4], fill=RED)
    d.text((40, hy + 14), "1  " + HERO[0], font=font(F_BLACK, 13), fill=RED)
    for i, ln in enumerate(wrap(d, HERO[1], font(F_SERIF, 27), 620)):
        d.text((40, hy + 34 + i * 32), ln, font=font(F_SERIF, 27), fill=INK)
    for i, ln in enumerate(wrap(d, HERO[2], font(F_REG, 13), 620)):
        d.text((40, hy + 102 + i * 17), ln, font=font(F_REG, 13), fill=(52, 56, 64))
    draw_tag(d, 40, hy + 142, HERO[3], font(F_BOLD, 9), (255, 255, 255), NAVY2)

    # hero illustration: Hodeidah port on the Red Sea (labelled scene)
    ix0, iy0, ix1, iy1 = W - 330, hy + 4, W - 24, hy + hh
    d.rectangle([ix0, iy0, ix1, iy1], fill=(178, 210, 235))  # pale-blue sky
    d.ellipse([ix1 - 62, iy0 + 8, ix1 - 20, iy0 + 50], fill=(255, 225, 130))  # sun halo
    d.ellipse([ix1 - 56, iy0 + 14, ix1 - 26, iy0 + 44], fill=(255, 205, 60))  # sun
    # grey smoke plume rising behind the containers
    for (sx, sy, sr, sc) in [(ix0 + 52, iy0 + 66, 15, (150, 150, 150)),
                             (ix0 + 76, iy0 + 46, 19, (135, 135, 135)),
                             (ix0 + 102, iy0 + 28, 13, (160, 160, 160))]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=sc)
    # two dark gantry cranes (legs + top beams + booms), drawn behind the stacks
    CRANE = (38, 46, 58)
    for cx in (ix0 + 24, ix0 + 150):
        d.rectangle([cx, iy0 + 28, cx + 4, iy0 + 102], fill=CRANE)
        d.rectangle([cx + 30, iy0 + 28, cx + 34, iy0 + 102], fill=CRANE)
        d.rectangle([cx - 4, iy0 + 24, cx + 38, iy0 + 28], fill=CRANE)
        d.rectangle([cx + 34, iy0 + 25, cx + 62, iy0 + 28], fill=CRANE)
    # hook hanging from the first crane over the container stack
    d.line([ix0 + 66, iy0 + 28, ix0 + 66, iy0 + 56], fill=CRANE, width=2)
    d.rectangle([ix0 + 62, iy0 + 56, ix0 + 70, iy0 + 61], fill=CRANE)
    # two container stacks on the quay (red / blue / green)
    d.rectangle([ix0 + 18, iy0 + 84, ix0 + 66, iy0 + 102], fill=(196, 60, 48), outline=(30, 30, 30))
    d.rectangle([ix0 + 68, iy0 + 84, ix0 + 116, iy0 + 102], fill=(40, 90, 150), outline=(30, 30, 30))
    d.rectangle([ix0 + 22, iy0 + 66, ix0 + 66, iy0 + 84], fill=(40, 90, 150), outline=(30, 30, 30))
    d.rectangle([ix0 + 68, iy0 + 66, ix0 + 112, iy0 + 84], fill=(40, 130, 80), outline=(30, 30, 30))
    d.rectangle([ix0 + 150, iy0 + 84, ix0 + 198, iy0 + 102], fill=(40, 130, 80), outline=(30, 30, 30))
    d.rectangle([ix0 + 200, iy0 + 84, ix0 + 248, iy0 + 102], fill=(196, 60, 48), outline=(30, 30, 30))
    d.rectangle([ix0 + 154, iy0 + 66, ix0 + 198, iy0 + 84], fill=(196, 60, 48), outline=(30, 30, 30))
    d.rectangle([ix0 + 200, iy0 + 66, ix0 + 244, iy0 + 84], fill=(40, 90, 150), outline=(30, 30, 30))
    # concrete quay strip, then dark sea with wave lines
    d.rectangle([ix0, iy0 + 102, ix1, iy0 + 122], fill=(188, 182, 170))
    d.rectangle([ix0, iy0 + 122, ix1, iy1], fill=(22, 58, 92))
    for yy in range(iy0 + 128, iy1, 10):
        d.line([ix0 + 8, yy, ix1 - 8, yy], fill=(60, 110, 160), width=1)
    # cargo ship at berth: dark hull + five deck containers
    d.polygon([(ix0 + 168, iy0 + 130), (ix0 + 292, iy0 + 130),
               (ix0 + 282, iy0 + 152), (ix0 + 178, iy0 + 152)], fill=(28, 36, 48),
              outline=(110, 140, 170))
    for j, cc in enumerate([(196, 60, 48), (40, 90, 150), (40, 130, 80),
                            (196, 60, 48), (40, 90, 150)]):
        x0 = ix0 + 172 + j * 24
        d.rectangle([x0, iy0 + 118, x0 + 22, iy0 + 130], fill=cc, outline=(30, 30, 30))
    d.text((ix0 + 10, iy1 - 20), "HODEIDAH PORT - RED SEA",
           font=font(F_BOLD, 9), fill=(255, 255, 255))

    # ---- map + legend ----
    my, mh = 322, 138
    d.rectangle([24, my, 660, my + mh], fill=(232, 238, 244), outline=LINE, width=1)
    d.text((36, my + 6), "WHERE IT HAPPENED", font=font(F_BLACK, 12), fill=NAVY)
    mx0, my0, mx1, my1 = 36, my + 24, 648, my + mh - 8
    # dots
    for lat, spans in LAND:
        for lo0, lo1 in spans:
            for lon in range(int(lo0), int(lo1) + 1, 4):
                px = mx0 + (lon + 180) / 360 * (mx1 - mx0)
                py = my0 + (75 - lat) / 135 * (my1 - my0)
                d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=(120, 140, 165))
    # leader-line offsets for pins that would collide (same city / close cities)
    OFF = {4: (-18, 14), 5: (-14, -16), 9: (-16, -12), 10: (16, -6), 11: (18, -12)}
    for n, label, lat, lon in PINS:
        px = mx0 + (lon + 180) / 360 * (mx1 - mx0)
        py = my0 + (75 - lat) / 135 * (my1 - my0)
        ox, oy = OFF.get(n, (0, 0))
        cx, cy = px + ox, py + oy
        if (ox, oy) != (0, 0):
            d.line([px, py, cx, cy], fill=RED, width=1)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED, outline=(255, 255, 255), width=1)
        d.text((cx - 3, cy - 6), str(n), font=font(F_BOLD, 9), fill=(255, 255, 255))
    # legend
    lx = 676
    d.text((lx, my + 6), "THE PINS", font=font(F_BLACK, 12), fill=NAVY)
    lf = font(F_REG, 11)
    for i, (n, label, _la, _lo) in enumerate(PINS):
        yy = my + 26 + i * 9.5
        if i >= 12:
            break
        d.text((lx, yy), "%d  %s" % (n, label), font=lf, fill=INK)
    d.text((lx, my + 26 + 12 * 9.5 + 2), "1 hero + 3 leads + 8 mid stories",
           font=font(F_BOLD, 10), fill=MUTED)

    # ---- leads ----
    ly, lh = 468, 128
    cw = (W - 48 - 2 * 12) / 3
    for i, (place, head, dek, src) in enumerate(LEADS):
        x0 = 24 + i * (cw + 12)
        d.rectangle([x0, ly, x0 + cw, ly + lh], fill=CARD, outline=LINE, width=1)
        d.rectangle([x0, ly, x0 + cw, ly + 4], fill=NAVY2)
        d.text((x0 + 12, ly + 10), "%d  %s" % (i + 2, place), font=font(F_BLACK, 11), fill=RED)
        yy = ly + 28
        for ln in wrap(d, head, font(F_SERIF, 16), cw - 24):
            d.text((x0 + 12, yy), ln, font=font(F_SERIF, 16), fill=INK)
            yy += 19
        for ln in wrap(d, dek, font(F_REG, 11), cw - 24):
            d.text((x0 + 12, yy), ln, font=font(F_REG, 11), fill=(52, 56, 64))
            yy += 14
        draw_tag(d, x0 + 12, ly + lh - 22, src, font(F_BOLD, 8), (255, 255, 255), NAVY2)

    # ---- mids ----
    myy, mhh = 604, 148
    mcw = (W - 48 - 3 * 10) / 4
    for i, (place, head, dek, src) in enumerate(MIDS):
        r, c = divmod(i, 4)
        x0 = 24 + c * (mcw + 10)
        y0 = myy + r * (mhh / 2 + 8)
        h = mhh / 2
        d.rectangle([x0, y0, x0 + mcw, y0 + h], fill=CARD, outline=LINE, width=1)
        d.text((x0 + 9, y0 + 6), "%d  %s" % (i + 5, place), font=font(F_BLACK, 10), fill=BLUE)
        yy = y0 + 22
        for ln in wrap(d, head, font(F_BOLD, 12), mcw - 18):
            d.text((x0 + 9, yy), ln, font=font(F_BOLD, 12), fill=INK)
            yy += 14
        d.text((x0 + 9, y0 + h - 15), src, font=font(F_BOLD, 8), fill=MUTED)

    # ---- briefs ----
    by = 764
    d.text((24, by), "THE REST OF THE DAY - 26 BRIEFS", font=font(F_BLACK, 13), fill=NAVY)
    d.line([24, by + 19, W - 24, by + 19], fill=NAVY, width=2)
    bf = font(F_REG, 10)
    bfb = font(F_BOLD, 10)
    colw = (W - 48 - 24) / 2
    for i, (place, text, src) in enumerate(BRIEFS):
        col, row = divmod(i, 13)
        x0 = 24 + col * (colw + 24)
        yy = by + 25 + row * 14
        num = str(i + 13)
        d.text((x0, yy), num, font=bfb, fill=RED)
        d.text((x0 + 22, yy), place + " - ", font=bfb, fill=INK)
        tw = d.textlength(place + " - ", font=bfb)
        d.text((x0 + 22 + tw, yy), text, font=bf, fill=(52, 56, 64))

    # ---- date check ----
    dy = by + 25 + 13 * 14 + 6
    d.rectangle([24, dy, W - 24, dy + 26], fill=REDBG)
    d.text((36, dy + 7), "DATE CHECK", font=font(F_BLACK, 12), fill=(255, 255, 255))
    d.text((140, dy + 8), EXCLUDED, font=font(F_REG, 10), fill=(255, 235, 235))

    # ---- footer ----
    fy = dy + 32
    d.text((24, fy), "Sources: Reuters - AP - BBC - Xinhua - NBC News - The Guardian - "
           "Sky News - Yonhap - The Hindu BusinessLine - Chess.com - Anthropic - "
           "NWS - CoinDesk - BEA - UEFA - FIDE - UNESCO - Sports Chosun - AHK Ghana",
           font=font(F_BOLD, 8), fill=INK)

    # ---- deterministic grain for texture ----
    for _ in range(9000):
        x = rng.randint(0, W - 1)
        y = rng.randint(0, H - 1)
        v = rng.randint(0, 1)
        d.point((x, y), fill=(200, 200, 200) if v else (235, 235, 235))

    img.save(OUT, "PNG", optimize=True)
    print("saved", OUT)


if __name__ == "__main__":
    main()
