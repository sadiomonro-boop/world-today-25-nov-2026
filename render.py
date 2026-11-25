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
HERO = ("GULF OF FINLAND",
        "Finland detects a new strike on a Russian warship",
        "Finnish forces say they detected a strike on a Russian navy vessel in "
        "the Gulf of Finland. Ukraine's Security Service says it carried out "
        "the attack.",
        "REUTERS / AL JAZEERA")

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
    ("HODEIDAH, YEMEN",
     "Saudi-led coalition strikes Hodeidah port",
     "Strikes hit the port after an evacuation order. The Houthis threaten "
     "Saudi Red Sea ports.",
     "REUTERS"),
]

MIDS = [
    ("MOSCOW", "Leaked Russian records put war dead at 720,000",
     "An investigation cites leaked records on the war's toll.", "INVESTIGATION"),
    ("UNITED STATES", "Abrego Garcia leaves US for Spain",
     "Kilmar Abrego Garcia self-deports, ending a two-year legal battle.", "BBC"),
    ("CARTAGENA", "Gunmen hold hostages in a supermarket",
     "Armed men seize about 20 hostages after a failed armoured-truck robbery.", "AP"),
    ("TURKIYE", "Military helicopter crashes; 5 killed",
     "Five dead as a Turkish military helicopter goes down on a training flight.", "WIRE"),
    ("DR CONGO", "Rebels call off advance on Bunia",
     "Rebels pull back after days of fighting around the eastern city.", "WIRE"),
    ("UNITED NATIONS", "Five women killed every hour by relatives",
     "UN figures for 2025: a woman is killed by a partner or relative every 12 minutes.", "UN"),
    ("CUBA", "WHO chief: end the US fuel blockade",
     "The WHO director-general urges an end to the US fuel blockade on Cuba.", "WIRE"),
    ("POLAND", "Russian drone briefly enters Polish airspace",
     "Warsaw reports a Russian drone crossing its airspace during strikes on Ukraine.", "REUTERS"),
]

# briefs: (place, text, source)
BRIEFS = [
    ("GAZA", "Israeli strike kills a Hamas internal security chief.", "BBC"),
    ("TAIWAN", "China-linked AI fakes smear election candidates, BBC Verify finds.", "BBC"),
    ("SYRIA", "Land-mine casualties soar, two years after the war.", "BBC"),
    ("NORTH KOREA", "Christians say they were spied on, beaten and jailed.", "BBC"),
    ("UNITED STATES", "Thomas Markle indicted over child sex abuse images.", "BBC"),
    ("VATICAN", "Pope Leo XIV applies for a mail-in US midterm ballot.", "WIRE"),
    ("FRANCE", "Students plan nationwide protests over education reforms.", "WIRE"),
    ("PHILIPPINES", "Mount Mayon eruption raises fears of a bigger event.", "WIRE"),
    ("EU / CANADA", "Brussels and Ottawa plan closer AI collaboration.", "WIRE"),
    ("GERMANY", "Audi profit falls sharply on a weak China market.", "WIRE"),
    ("BANGLADESH", "Garment workers clash with police in pay protests.", "WIRE"),
    ("BRITAIN", "UK sanctions Houthi officials over abuse claims.", "WIRE"),
    ("POLAND", "EU court: Poland violated an Afghan migrant's rights.", "WIRE"),
    ("ECUADOR", "Floods reach the Galapagos as El Nino worries grow.", "WIRE"),
    ("ZAMBIA", "Opposition figure charged with treason.", "WIRE"),
    ("BANGLADESH", "Hasina sets 16 December for her return home.", "WIRE"),
    ("CHINA", "Official sentenced to death for leaking 35 state secrets.", "WIRE"),
    ("SUDAN", "RSF commander breaks with his faction.", "WIRE"),
    ("YEMEN", "Army: ~700 strikes hit Houthi positions; ~97 fighters killed.", "WIRE"),
    ("SAUDI ARABIA", "Iranian hackers hit hospitals and aviation with AI identities.", "WIRE"),
    ("AUSTRALIA", "Canberra warns US-China rivalry is straining safeguards.", "WIRE"),
    ("CHINA", "Shanghai party chief Chen Jining falls in a corruption probe.", "WIRE"),
    ("VIENNA", "IAEA names a sanctioned Russian as deputy chief; Kyiv objects.", "WIRE"),
    ("IRAQ / EGYPT", "Baghdad and Cairo agree to deepen economic ties.", "WIRE"),
    ("ISRAEL", "Eisenkot clinches a first coalition deal; Lieberman joins.", "WIRE"),
    ("PAKISTAN", "Islamabad eyes a $1.21bn disbursement next month.", "WIRE"),
]

KPI = [("KOSPI", "-5.8%"), ("NIKKEI", "-2.8%"), ("BRENT", "$90.09"),
       ("WAR DEAD", "720,000"), ("WOMEN / HOUR", "5"),
       ("SZ-24 TESTS", "90+"), ("TO ADEN", "60 km")]

# pins: (number, label, lat, lon)
PINS = [
    (1, "Gulf of Finland", 60.0, 24.0),
    (2, "Jiuquan", 40.0, 100.0),
    (3, "Seoul", 37.5, 127.0),
    (4, "Hodeidah", 15.0, 43.0),
    (5, "Moscow", 55.7, 37.6),
    (6, "Madrid", 40.4, -3.7),
    (7, "Cartagena", 10.4, -75.5),
    (8, "Ankara", 39.9, 32.8),
    (9, "Bunia", 1.6, 30.2),
    (10, "Geneva", 46.2, 6.1),
    (11, "Havana", 23.1, -82.4),
    (12, "Warsaw", 52.2, 21.0),
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

    # hero illustration: night sea, ship, drones
    ix0, iy0, ix1, iy1 = W - 330, hy + 4, W - 24, hy + hh
    d.rectangle([ix0, iy0, ix1, iy1], fill=(16, 34, 58))
    for i in range(40):  # stars
        d.point((rng.randint(ix0 + 4, ix1 - 4), rng.randint(iy0 + 4, iy0 + 55)),
                fill=(220, 220, 200))
    d.rectangle([ix0, iy0 + 96, ix1, iy1], fill=(24, 62, 96))  # sea
    for yy in range(iy0 + 100, iy1, 12):  # wave lines
        d.line([ix0 + 8, yy, ix1 - 8, yy], fill=(60, 110, 160), width=1)
    hull = (150, 160, 180)
    d.polygon([(ix0 + 40, iy0 + 96), (ix0 + 250, iy0 + 96), (ix0 + 235, iy0 + 70),
               (ix0 + 60, iy0 + 70)], fill=hull, outline=(220, 225, 235))  # hull
    d.rectangle([ix0 + 120, iy0 + 46, ix0 + 150, iy0 + 70], fill=hull,
                outline=(220, 225, 235))
    d.rectangle([ix0 + 155, iy0 + 52, ix0 + 175, iy0 + 70], fill=hull,
                outline=(220, 225, 235))
    d.line([ix0 + 95, iy0 + 70, ix0 + 95, iy0 + 38], fill=hull, width=3)
    d.polygon([(ix0 + 95, iy0 + 38), (ix0 + 118, iy0 + 46), (ix0 + 95, iy0 + 50)],
              fill=RED)  # flag
    for dx, dy in [(90, 26), (190, 16), (240, 30)]:  # drones
        cx, cy = ix0 + dx, iy0 + dy
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=GOLD, outline=(255, 255, 255))
        d.line([cx, cy, cx + 18, cy + 34], fill=GOLD, width=1)
    d.text((ix0 + 10, iy1 - 20), "GULF OF FINLAND - NIGHT",
           font=font(F_BOLD, 9), fill=(200, 210, 225))

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
    for n, label, lat, lon in PINS:
        px = mx0 + (lon + 180) / 360 * (mx1 - mx0)
        py = my0 + (75 - lat) / 135 * (my1 - my0)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
        d.text((px - 3, py - 6), str(n), font=font(F_BOLD, 9), fill=(255, 255, 255))
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
    bf = font(F_REG, 11)
    bfb = font(F_BOLD, 11)
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
    d.text((24, fy), "All stories happened, or were first reported, on Wednesday 25 November 2026.  "
           "Sources: AP - Reuters - AFP - BBC - Al Jazeera - Xinhua - UEFA - UN",
           font=font(F_BOLD, 11), fill=INK)

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
