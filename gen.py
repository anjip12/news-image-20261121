#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news front page (1024x1024 PNG).

Deterministic PIL renderer, broadsheet theme (tournament winner A).
Usage: python3 gen.py [out.png]  --  no network, no inputs, fixed output.
"""
import math
import sys

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

BG = (247, 242, 231)
INK = (20, 33, 61)
SUB = (84, 92, 110)
ACCENT = (179, 0, 27)
HERO = (20, 33, 61)
HERO_TX = (247, 242, 231)
PANEL = (255, 253, 246)
GOLD = (198, 146, 20)
WHITE = (255, 255, 255)


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, width):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, font, fill, width, leading=1.16):
    for ln in wrap(d, text, font, width):
        d.text((x, y), ln, font=font, fill=fill)
        y += int(font.size * leading)
    return y


def star(d, cx, cy, r, fill, arms=8):
    for i in range(arms):
        a = 2 * math.pi * i / arms
        d.line([cx, cy, cx + r * math.cos(a), cy + r * math.sin(a)],
               fill=fill, width=5)
    d.ellipse([cx - r * 0.32, cy - r * 0.32, cx + r * 0.32, cy + r * 0.32],
              fill=fill)


def dashed_arc(d, p0, p1, p2, fill, width=4, dash=13, gap=9):
    pts = []
    for i in range(91):
        t = i / 90
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pts.append((x, y))
    acc = 0.0
    for i in range(1, len(pts)):
        if (acc % (dash + gap)) < dash:
            d.line([pts[i - 1], pts[i]], fill=fill, width=width)
        acc += math.dist(pts[i - 1], pts[i])


def chip(d, x, y, big, small, wdt):
    d.rounded_rectangle([x, y, x + wdt, y + 72], 10, fill=ACCENT)
    d.text((x + 13, y + 5), big, font=F(SANSB, 29), fill=WHITE)
    d.text((x + 13, y + 42), small, font=F(SANS, 15), fill=WHITE)
    return x + wdt + 12


def hero(d, box):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, 14, fill=HERO)
    d.text((x0 + 26, y0 + 15), "WAR IN EUROPE  ·  NATO", font=F(SANSB, 19),
           fill=GOLD)
    y = text_block(d, x0 + 26, y0 + 42, "RUSSIAN MISSILES LAND IN POLAND",
                   F(SERIF, 40), HERO_TX, 468, 1.08)
    text_block(d, x0 + 26, y + 8,
               "Two missiles and a drone came down on NATO soil during "
               "Russia's huge overnight barrage on Ukraine. PM Tusk called "
               "it \"a deliberate provocation\"; NATO chief Rutte flies to "
               "Warsaw today as Poland seeks more Eastern Sentry forces.",
               F(SANS, 18.5), HERO_TX, 458, 1.22)
    cy = y1 - 84
    nx = chip(d, x0 + 26, cy, "400+", "drones fired at Ukraine", 192)
    nx = chip(d, nx, cy, "110", "missiles in one night", 172)
    chip(d, nx, cy, "8+", "killed in Ukraine", 146)
    mx0, my0, mx1, my1 = x0 + 524, y0 + 40, x1 - 24, y1 - 122
    d.rounded_rectangle([mx0, my0, mx1, my1], 10, outline=HERO_TX, width=2)
    pw = (mx1 - mx0) * 0.42
    mid = my0 + (my1 - my0) / 2
    d.rectangle([mx0 + 7, my0 + 7, mx0 + pw, mid], fill=(238, 240, 244))
    d.rectangle([mx0 + 7, mid, mx0 + pw, my1 - 7], fill=(196, 30, 58))
    d.rectangle([mx0 + pw + 5, my0 + 7, mx1 - 7, mid], fill=(74, 116, 172))
    d.rectangle([mx0 + pw + 5, mid, mx1 - 7, my1 - 7], fill=(240, 198, 60))
    d.text((mx0 + 18, my0 + 14), "POLAND", font=F(SANSB, 20), fill=INK)
    d.text((mx0 + pw + 18, my0 + 14), "UKRAINE", font=F(SANSB, 20), fill=WHITE)
    kyiv = (mx0 + pw + 62, my0 + 88)
    d.ellipse([kyiv[0] - 6, kyiv[1] - 6, kyiv[0] + 6, kyiv[1] + 6], fill=WHITE)
    d.text((kyiv[0] + 10, kyiv[1] - 10), "Kyiv", font=F(SANSB, 15), fill=WHITE)
    hit1 = (mx0 + pw - 40, my0 + 122)
    hit2 = (mx0 + pw - 92, my0 + 62)
    dashed_arc(d, (mx1 - 14, my0 + 40), (mx0 + pw + 88, my0 - 24), hit1, ACCENT)
    dashed_arc(d, (mx1 - 14, my0 + 116), (mx0 + pw + 26, my0 + 2), hit2, ACCENT)
    star(d, hit1[0], hit1[1], 20, (255, 214, 10))
    star(d, hit2[0], hit2[1], 15, (255, 214, 10))
    d.text((hit1[0] - 126, hit1[1] + 22), "Kh-101 down near", font=F(SANS, 14),
           fill=INK)
    d.text((hit1[0] - 126, hit1[1] + 39), "Nowy Lipowiec", font=F(SANSB, 14),
           fill=INK)
    d.text((mx0 + 4, my1 + 10),
           "No one hurt in Poland · two embassies hit in Kyiv",
           font=F(SANS, 15.5), fill=HERO_TX)


def markets(d, box):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, 12, fill=PANEL, outline=INK, width=2)
    d.text((x0 + 20, y0 + 13), "MARKETS  ·  NEW YORK", font=F(SANSB, 16),
           fill=ACCENT)
    d.text((x0 + 20, y0 + 34), "AI TRADE CRASHES:", font=F(SERIF, 26), fill=INK)
    d.text((x0 + 20, y0 + 63), "INTO CORRECTION", font=F(SERIF, 26), fill=INK)
    d.text((x0 + 330, y0 + 32), "-3.7%", font=F(SANSB, 44), fill=ACCENT)
    d.text((x0 + 334, y0 + 80), "S&P 500 Friday", font=F(SANS, 14), fill=SUB)
    gx0, gy0, gx1, gy1 = x0 + 22, y0 + 118, x0 + 240, y1 - 18
    d.line([gx0, gy0, gx0, gy1], fill=SUB, width=2)
    d.line([gx0, gy1, gx1, gy1], fill=SUB, width=2)
    vals = [7430, 7380, 7300, 7176, 6910]
    lo, hi = 6800, 7550
    pts = []
    for i, v in enumerate(vals):
        px = gx0 + 8 + i * (gx1 - gx0 - 16) / (len(vals) - 1)
        py = gy1 - (v - lo) / (hi - lo) * (gy1 - gy0)
        pts.append((px, py))
    d.line(pts, fill=ACCENT, width=5, joint="curve")
    for p in pts:
        d.ellipse([p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4], fill=ACCENT)
    d.text((gx0 + 2, gy1 - 15), "Mon", font=F(SANS, 12), fill=SUB)
    d.text((gx1 - 22, gy1 - 15), "Fri", font=F(SANS, 12), fill=SUB)
    d.text((gx0 + 6, gy0 - 4), "7,430", font=F(SANS, 12), fill=SUB)
    text_block(d, x0 + 262, y0 + 112,
               "Nasdaq -5.3%, negative for the year. Nvidia -14%. Anthropic "
               "-9% a day after its record IPO. Nikkei and Kospi fell 5%.",
               F(SANS, 16), INK, x1 - x0 - 278, 1.2)


def cop31(d, box):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, 12, fill=PANEL, outline=INK, width=2)
    d.text((x0 + 20, y0 + 13), "CLIMATE  ·  ANTALYA", font=F(SANSB, 16),
           fill=ACCENT)
    d.text((x0 + 20, y0 + 34), "COP31 RUNS INTO", font=F(SERIF, 26), fill=INK)
    d.text((x0 + 20, y0 + 63), "OVERTIME", font=F(SERIF, 26), fill=INK)
    cx, cy, r = x0 + 64, y0 + 158, 38
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    d.ellipse([cx - r, cy - 12, cx + r, cy + 12], outline=INK, width=2)
    d.line([cx - r, cy, cx + r, cy], fill=INK, width=2)
    for dx in (-19, 0, 19):
        d.arc([cx + dx - 25, cy - r, cx + dx + 25, cy + r], 90, 270,
              fill=INK, width=2)
    tx = x0 + 122
    d.text((tx, y0 + 106), "1.5°C", font=F(SANSB, 38), fill=ACCENT)
    text_block(d, tx, y0 + 150,
               "Draft deal drops fossil fuels; first COP text to admit the "
               "Paris limit will be overshot. ~200 nations talk on into "
               "the weekend.", F(SANS, 15.5), INK, x1 - tx - 14, 1.2)


def ukeu(d, box):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, 12, fill=PANEL, outline=INK, width=2)
    d.text((x0 + 18, y0 + 11), "BRUSSELS SUMMIT", font=F(SANSB, 15),
           fill=ACCENT)
    d.text((x0 + 18, y0 + 30), "UK-EU RESET:", font=F(SERIF, 23), fill=INK)
    d.text((x0 + 18, y0 + 55), "THREE DEALS SIGNED", font=F(SERIF, 23),
           fill=INK)
    cy = y0 + 106
    d.ellipse([x0 + 20, cy - 24, x0 + 68, cy + 24], fill=(1, 33, 105))
    d.text((x0 + 29, cy - 12), "UK", font=F(SANSB, 18), fill=WHITE)
    d.ellipse([x0 + 88, cy - 24, x0 + 136, cy + 24], fill=(0, 51, 153))
    for i in range(6):
        a = 2 * math.pi * i / 6
        sx, sy = x0 + 112 + 14 * math.cos(a), cy + 14 * math.sin(a)
        d.ellipse([sx - 2.4, sy - 2.4, sx + 2.4, sy + 2.4], fill=(255, 204, 0))
    d.text((x0 + 152, cy - 26), "£5.1bn", font=F(SANSB, 29), fill=INK)
    d.text((x0 + 152, cy + 6), "a year: food deal", font=F(SANS, 14), fill=SUB)
    text_block(d, x0 + 18, y0 + 138,
               "Food checks end, carbon markets link, youth mobility for "
               "100,000 a year.", F(SANS, 15), INK,
               x1 - x0 - 34, 1.2)


def akvan(d, box):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, 12, fill=PANEL, outline=INK, width=2)
    d.text((x0 + 18, y0 + 11), "CYCLONE  ·  INDIA", font=F(SANSB, 15),
           fill=ACCENT)
    d.text((x0 + 18, y0 + 30), "AKVAN SPARES", font=F(SERIF, 23), fill=INK)
    d.text((x0 + 18, y0 + 55), "ODISHA", font=F(SERIF, 23), fill=INK)
    cx, cy = x0 + 54, y0 + 108
    for rr, a0 in ((32, 20), (23, 150), (15, 280)):
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], a0, a0 + 250,
              fill=ACCENT, width=5)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=ACCENT)
    d.text((x0 + 102, y0 + 84), "372,000", font=F(SANSB, 30), fill=INK)
    d.text((x0 + 102, y0 + 118), "evacuated; no deaths", font=F(SANS, 14),
           fill=SUB)
    text_block(d, x0 + 18, y0 + 138,
               "209 mm of rain in a day; 1,450 babies born safe in storm "
               "shelters.", F(SANS, 15), INK, x1 - x0 - 34, 1.2)


def mongolia(d, box):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, 12, fill=PANEL, outline=INK, width=2)
    d.text((x0 + 18, y0 + 11), "ULAANBAATAR", font=F(SANSB, 15), fill=ACCENT)
    d.text((x0 + 18, y0 + 30), "PRESIDENT QUITS", font=F(SERIF, 23), fill=INK)
    d.text((x0 + 18, y0 + 55), "— A FIRST", font=F(SERIF, 23), fill=INK)
    base = y0 + 128
    d.polygon([(x0 + 22, base), (x0 + 74, y0 + 92), (x0 + 120, base)],
              fill=(110, 132, 160))
    d.polygon([(x0 + 92, base), (x0 + 142, y0 + 98), (x0 + 186, base)],
              fill=(84, 104, 128))
    d.text((x0 + 200, y0 + 90), "96 of 104", font=F(SANSB, 21), fill=INK)
    d.text((x0 + 200, y0 + 114), "MPs backed it", font=F(SANS, 13), fill=SUB)
    text_block(d, x0 + 18, y0 + 138,
               "Khurelsukh Ukhnaa steps down amid graft claims; an early "
               "election follows.", F(SANS, 15), INK, x1 - x0 - 34, 1.2)


def build(out):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((28, 18), "THE WORLD IN ONE DAY", font=F(SERIF, 57), fill=INK)
    d.text((W - 28, 28), "No. 21", font=F(SERIF, 30), fill=SUB, anchor="ra")
    d.line([28, 90, W - 28, 90], fill=INK, width=5)
    d.text((28, 100), "SATURDAY 21 NOVEMBER 2026", font=F(SANSB, 31),
           fill=ACCENT)
    d.text((W - 28, 106), "Six stories that shaped the day", font=F(SANS, 19),
           fill=SUB, anchor="ra")
    d.line([28, 144, W - 28, 144], fill=INK, width=2)
    hero(d, (28, 158, W - 28, 520))
    markets(d, (28, 536, 506, 758))
    cop31(d, (522, 536, W - 28, 758))
    ukeu(d, (28, 774, 344, 950))
    akvan(d, (356, 774, 672, 950))
    mongolia(d, (684, 774, W - 28, 950))
    d.rectangle([28, 960, W - 28, 994], fill=INK)
    d.text((42, 968), "ALSO TODAY", font=F(SANSB, 15.5), fill=GOLD)
    d.text((166, 969),
           "Cricket: India 159/1 trail NZ by 209 in Wellington  ·  EU OKs "
           "€1bn arms aid for Ukraine  ·  US sanctions 4 Iranians",
           font=F(SANS, 15), fill=BG)
    d.text((28, 999),
           "Sources: AP · Reuters · UN News · IMD · WSJ · BBC — reported "
           "20-21 November 2026", font=F(SANS, 13.5), fill=SUB)
    img.save(out, optimize=True)
    return out


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    build(out)
    print("wrote", out)
