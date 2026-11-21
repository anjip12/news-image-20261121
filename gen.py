"""Front page for Saturday 21 November 2026, drawn from scratch with Pillow.

One 1024x1024 broadsheet: a navy hero on the missiles in Poland, two
market/climate panels, three small panels, a twelve-item world-in-brief
strip and a ticker. Every number on the page was checked against a
20-21 November 2026 source before it was drawn. Deterministic: no
clock, no random, no network.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 240, 224)
NAVY = (22, 35, 63)
NAVY2 = (30, 48, 84)
RED = (179, 32, 46)
REDBRIGHT = (205, 45, 60)
GOLD = (201, 151, 0)
AMBER = (232, 178, 38)
INK = (22, 35, 63)
GREY = (92, 96, 104)
WHITE = (255, 255, 255)
CREAM = (250, 246, 236)
SKY = (58, 102, 168)
YEL = (240, 196, 55)

FD = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FD, "DejaVuSerif-Bold.ttf")
SERIF_R = os.path.join(FD, "DejaVuSerif.ttf")
SANS = os.path.join(FD, "DejaVuSans.ttf")
SANS_B = os.path.join(FD, "DejaVuSans-Bold.ttf")


def f(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, width):
    """Greedy word wrap; returns a list of lines that fit width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, font, fill, width, leading):
    """Draw a wrapped paragraph; returns the y after the last line."""
    for line in wrap(d, text, font, width):
        d.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def card(d, box, fill, outline=None, width=2, radius=10):
    d.rounded_rectangle(box, radius=radius, fill=fill,
                        outline=outline, width=width)


def kicker(d, x, y, text, fill=RED, size=15):
    d.text((x, y), text, font=f(SANS_B, size), fill=fill)
    return y + size + 8


def headline(d, x, y, text, font, fill, width, leading):
    for line in wrap(d, text, font, width):
        d.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def masthead(d):
    y = 22
    d.text((26, y), "THE WORLD IN ONE DAY",
           font=f(SERIF, 56), fill=NAVY)
    d.text((880, y + 14), "No. 21", font=f(SERIF, 30), fill=GREY)
    d.rectangle([26, 92, 998, 96], fill=NAVY)
    d.rectangle([26, 100, 998, 104], fill=RED)
    d.text((26, 112), "SATURDAY 21 NOVEMBER 2026",
           font=f(SANS_B, 28), fill=RED)
    d.text((640, 118), "21 stories  ·  6 regions  ·  one front page",
           font=f(SANS, 17), fill=GREY)
    return 152


def burst(d, cx, cy, r, fill=AMBER):
    for ang in range(0, 360, 45):
        import math
        x2 = cx + int(r * math.cos(math.radians(ang)))
        y2 = cy + int(r * math.sin(math.radians(ang)))
        d.line([cx, cy, x2, y2], fill=fill, width=4)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=fill)


def hero(d, y0):
    x0, x1, h = 26, 998, 292
    card(d, [x0, y0, x1, y0 + h], NAVY, radius=12)
    # left column: kicker, headline, body, casualty chips
    lx, lw = 48, 430
    kicker(d, lx, y0 + 18, "WAR IN EUROPE  ·  NATO", fill=GOLD, size=15)
    yy = headline(d, lx, y0 + 44, "RUSSIAN MISSILES LAND IN POLAND",
                  f(SERIF, 38), WHITE, lw, 44)
    body = ("Two missiles and a drone came down on NATO soil in "
            "Russia's overnight barrage on Ukraine. PM Tusk called it "
            "\u201ca deliberate provocation\u201d; NATO chief Rutte flies "
            "to Warsaw today.")
    yy = para(d, lx, yy + 4, body, f(SANS, 14), (226, 232, 240), lw, 18)
    # casualty chips: number on top, label below, inside the chip
    cy = y0 + h - 56
    for cx, cw, big, small in [(lx, 132, "8+", "killed in Ukraine"),
                               (lx + 142, 168, "2",
                                "embassies hit in Kyiv")]:
        card(d, [cx, cy, cx + cw, cy + 44], REDBRIGHT, radius=8)
        d.text((cx + 12, cy + 4), big, font=f(SANS_B, 18), fill=WHITE)
        d.text((cx + 12, cy + 24), small, font=f(SANS, 11), fill=WHITE)
    d.text((lx + 322, cy + 6), "No one hurt\nin Poland",
           font=f(SANS_B, 13), fill=(226, 232, 240))
    # right column: schematic map + barrage bars
    mx, my, mw, mh = 512, y0 + 18, 462, 168
    card(d, [mx, my, mx + mw, my + mh], WHITE, radius=8)
    # Poland (left) / Ukraine (right), split at x=300 inside the box
    d.rectangle([mx + 2, my + 2, mx + 298, my + mh - 2], fill=(238, 240, 244))
    d.rectangle([mx + 300, my + 2, mx + mw - 2, my + 84], fill=SKY)
    d.rectangle([mx + 300, my + 86, mx + mw - 2, my + mh - 2], fill=YEL)
    d.text((mx + 14, my + 8), "POLAND", font=f(SANS_B, 16), fill=NAVY)
    d.text((mx + 312, my + 8), "UKRAINE", font=f(SANS_B, 16), fill=WHITE)
    d.text((mx + 312, my + 30), "BELARUS", font=f(SANS, 11), fill=(210, 220, 235))
    d.text((mx + 388, my + 118), "RUSSIA", font=f(SANS, 11), fill=(120, 90, 40))
    d.ellipse([mx + 372, my + 96, mx + 382, my + 106], fill=WHITE)
    d.text((mx + 388, my + 94), "Kyiv", font=f(SANS_B, 13), fill=NAVY)
    d.text((mx + 330, my + 38), "Nowa D\u0119ba drills", font=f(SANS_B, 11),
           fill=WHITE)
    # dashed red arc from Ukraine down into Poland, below the BELARUS label
    for i in range(12):
        t = i / 11.0
        ax = mx + 440 - int(260 * t)
        ay = my + 52 + int(48 * t * t)
        d.ellipse([ax, ay, ax + 7, ay + 4], fill=RED)
    burst(d, mx + 210, my + 96, 16)
    burst(d, mx + 120, my + 60, 12)
    d.ellipse([mx + 168, my + 128, mx + 176, my + 136], fill=AMBER)
    d.text((mx + 14, my + mh - 42), "Kh-101 down near", font=f(SANS, 12),
           fill=RED)
    d.text((mx + 14, my + mh - 26), "Nowy Lipowiec", font=f(SANS_B, 13),
           fill=RED)
    d.text((mx + 296, my + mh - 26), "Rudnik nad Sanem \u00b7 Mo\u0142odycz",
           font=f(SANS, 10), fill=(90, 70, 20))
    # barrage bars under the map
    by = my + mh + 12
    d.text((mx, by), "THE BARRAGE IN ONE NIGHT",
           font=f(SANS_B, 13), fill=GOLD)
    by += 20
    for label, val, frac in [("Drones", "400+", 1.0),
                             ("Missiles", "110", 0.28)]:
        d.text((mx, by), label, font=f(SANS, 13), fill=(226, 232, 240))
        d.rectangle([mx + 74, by + 2, mx + 74 + int(300 * frac), by + 14],
                    fill=REDBRIGHT)
        d.text((mx + 382, by - 1), val, font=f(SANS_B, 14), fill=WHITE)
        by += 22
    return y0 + h


def slope_chart(d, x, y, w, h, label, start, end, pct):
    """Two-point week chart: only the verified Mon/Fri closes, joined.
    High price sits at the top, so a falling week slopes down."""
    d.rectangle([x, y, x + w, y + h], outline=(190, 190, 185), width=1)
    d.line([x + 6, y + 12, x + w - 6, y + h - 10], fill=RED, width=3)
    d.ellipse([x + 2, y + 8, x + 10, y + 16], fill=RED)
    d.ellipse([x + w - 10, y + h - 14, x + w - 2, y + h - 6], fill=RED)
    d.text((x + 4, y + 20), start, font=f(SANS, 11), fill=GREY)
    d.text((x + w - 54, y + h - 40), end, font=f(SANS, 11), fill=GREY)
    d.text((x, y + h + 4), label, font=f(SANS_B, 12), fill=NAVY)
    d.text((x + w - 52, y + h + 4), pct, font=f(SANS_B, 12), fill=RED)


def markets_climate(d, y0):
    h = 194
    # markets panel
    card(d, [26, y0, 512, y0 + h], WHITE, outline=NAVY, width=2, radius=10)
    kicker(d, 44, y0 + 12, "MARKETS  ·  NEW YORK", size=14)
    headline(d, 44, y0 + 34, "AI TRADE CRASHES: INTO CORRECTION",
             f(SERIF, 24), NAVY, 300, 28)
    d.text((360, y0 + 34), "-3.7%", font=f(SANS_B, 40), fill=RED)
    d.text((362, y0 + 78), "S&P 500 Friday", font=f(SANS, 13), fill=GREY)
    slope_chart(d, 44, y0 + 100, 200, 48, "S&P 500  Mon \u2192 Fri",
                "7,562", "6,910", "-8.6% wk")
    slope_chart(d, 272, y0 + 100, 200, 48, "Nasdaq  Mon \u2192 Fri",
                "25,137", "22,618", "-10.0% wk")
    d.text((44, y0 + 176),
           "Nasdaq -5.3% Fri, worst week since Mar 2020. Nvidia -14% Fri.",
           font=f(SANS, 12), fill=GREY)
    # climate panel
    card(d, [528, y0, 998, y0 + h], WHITE, outline=NAVY, width=2, radius=10)
    kicker(d, 546, y0 + 12, "CLIMATE  ·  ANTALYA", size=14)
    headline(d, 546, y0 + 34, "COP31 RUNS INTO OVERTIME",
             f(SERIF, 24), NAVY, 300, 28)
    d.ellipse([548, y0 + 104, 622, y0 + 178], outline=NAVY, width=3)
    d.ellipse([560, y0 + 112, 610, y0 + 170], outline=NAVY, width=2)
    d.line([548, y0 + 141, 622, y0 + 141], fill=NAVY, width=2)
    d.text((640, y0 + 100), "1.5\u00b0C", font=f(SANS_B, 40), fill=RED)
    para(d, 640, y0 + 148,
         "Draft deal drops fossil fuels; first COP text to admit the "
         "Paris limit will be overshot.",
         f(SANS, 13), INK, 330, 17)
    return y0 + h


def small_panels(d, y0):
    h = 156
    cols = [(26, 318, "BRUSSELS SUMMIT", "UK-EU RESET: THREE DEALS SIGNED",
             "\u00a35.1bn", "a year: food deal",
             "Food checks end, carbon markets link, youth mobility for "
             "100,000 a year."),
            (360, 318, "CYCLONE  ·  INDIA", "AKVAN SPARES ODISHA",
             "372,000", "evacuated; no deaths",
             "209 mm of rain in a day; 1,450 babies born safe in storm "
             "shelters."),
            (694, 278, "ULAANBAATAR", "PRESIDENT QUITS \u2014 A FIRST",
             "96 of 104", "MPs backed it",
             "Khurelsukh Ukhnaa steps down amid graft claims; an early "
             "election follows.")]
    for x, w, kick, head, big, sub, body in cols:
        card(d, [x, y0, x + w, y0 + h], WHITE, outline=NAVY, width=2,
             radius=10)
        kicker(d, x + 16, y0 + 10, kick, size=13)
        headline(d, x + 16, y0 + 30, head, f(SERIF, 19), NAVY, w - 32, 22)
        d.text((x + 16, y0 + 80), big, font=f(SANS_B, 26), fill=NAVY)
        d.text((x + 16, y0 + 108), sub, font=f(SANS, 12), fill=GREY)
        para(d, x + 16, y0 + 124, body, f(SANS, 11), INK, w - 32, 12)
    return y0 + h


BRIEF = [
    ("DENMARK", "Plot to kill rapper Kyivstoner foiled; attach\u00e9 expelled."),
    ("CUBA", "US teacher freed after nearly 10 years detained."),
    ("INDIA\u2013JAPAN", "Japanese troops to drill missiles on Indian ranges."),
    ("GOLD", "\u22129.5% in a week to $3,512; worst week in 8 months."),
    ("KRYVYI RIH", "Strike kills 2, injures 42, incl. 4 children."),
    ("BRITAIN", "1,000+ drones for Ukraine in \u00a3260m package."),
    ("HORMUZ", "Tanker strike and fire in the strait (UKMTO)."),
    ("SPACE", "JAXA drops Hayabusa2's 2031 asteroid landing."),
    ("BRAZIL", "Ex-president Bolsonaro taken to hospital."),
    ("SIBERIA", "Military plane crash kills all 17 aboard."),
    ("CYBER", "JPMorgan, Visa, Mastercard hit via vendors."),
    ("PAKISTAN", "Suicide bombing at checkpoint kills 5, injures 13."),
]


def brief_strip(d, y0):
    h = 126
    card(d, [26, y0, 998, y0 + h], CREAM, outline=NAVY, width=2, radius=10)
    d.text((44, y0 + 8), "WORLD IN BRIEF \u2014 12 MORE STORIES",
           font=f(SANS_B, 15), fill=RED)
    cell_w, cell_h = 232, 30
    for i, (lead, text) in enumerate(BRIEF):
        col, row = i % 4, i // 4
        x = 44 + col * 238
        y = y0 + 32 + row * 32
        full = lead + " \u2014 " + text
        lines = wrap(d, full, f(SANS, 12), cell_w)
        d.text((x, y), lines[0], font=f(SANS, 12), fill=INK)
        if len(lines) > 1:
            d.text((x, y + 14), lines[1], font=f(SANS, 12), fill=INK)
    return y0 + h


def footer(d, y0):
    d.rectangle([26, y0, 998, y0 + 30], fill=NAVY)
    d.text((40, y0 + 7), "ALSO TODAY",
           font=f(SANS_B, 13), fill=GOLD)
    d.text((150, y0 + 7),
           "Cricket: India 159/1 trail NZ by 209 in Wellington  \u00b7  "
           "EU OKs \u20ac1bn arms aid for Ukraine  \u00b7  US sanctions "
           "4 Iranians",
           font=f(SANS, 13), fill=WHITE)
    d.text((26, y0 + 38),
           "Sources: AP \u00b7 Reuters \u00b7 UN News \u00b7 IMD \u00b7 WSJ "
           "\u00b7 BBC \u00b7 CNN \u00b7 Morningstar \u2014 reported "
           "20\u201321 November 2026",
           font=f(SANS, 12), fill=GREY)
    return y0 + 56


def build(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = masthead(d)
    y = hero(d, y + 8)
    y = markets_climate(d, y + 10)
    y = small_panels(d, y + 10)
    y = brief_strip(d, y + 10)
    y = footer(d, y + 8)
    assert y <= H, f"layout overflow: {y}"
    img.save(out_path, "PNG", optimize=True)


if __name__ == "__main__":
    target = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target, exist_ok=True)
    build(os.path.join(target, "entry.png"))
