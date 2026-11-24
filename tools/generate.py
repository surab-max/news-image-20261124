#!/usr/bin/env python3
"""Draw the front page of Tuesday 24 November 2026 as a 1024x1024 PNG.

Design rule learned from the News 23 entry (rank 3,493 of 7,226):
the judge reads the image at ~300 px wide, so headlines must be huge,
stories few, and small print cut. This page carries five stories and
one briefs strip, all verified against reporting read on 24 Nov 2026
(see SOURCES.md). Nothing here is fetched at runtime: the picture is
drawn from fixed text and shapes, so two runs write identical bytes.

Run: python3 tools/generate.py  ->  writes entry.png beside main.py
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 28
INK = (17, 17, 17)
PAPER = (247, 243, 234)
RED = (178, 24, 24)
DARK = (24, 32, 48)
SEA = (16, 42, 66)
SKY_TOP = (38, 48, 74)
SKY_LOW = (214, 96, 44)
FLAME = (255, 122, 26)
FLAME_CORE = (255, 196, 66)
SMOKE = (74, 74, 78)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit `width`."""
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_centered(draw, y, text, fnt, fill=INK, width=W):
    draw.text((width / 2, y), text, font=fnt, fill=fill, anchor="ma")


def draw_lines(draw, x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.08)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def tanker(draw, x, y, scale, flame_h):
    """One burning tanker silhouette: hull, deck blocks, flame, smoke."""
    hull_w, hull_h = int(300 * scale), int(46 * scale)
    # hull
    draw.polygon(
        [(x, y), (x + hull_w, y), (x + hull_w - 18 * scale, y + hull_h),
         (x + 18 * scale, y + hull_h)],
        fill=(10, 10, 12),
    )
    # deck + bridge block
    draw.rectangle([x + 30 * scale, y - 34 * scale,
                    x + 110 * scale, y], fill=(10, 10, 12))
    draw.rectangle([x + 200 * scale, y - 22 * scale,
                    x + 250 * scale, y], fill=(10, 10, 12))
    # funnel
    draw.rectangle([x + 150 * scale, y - 52 * scale,
                    x + 176 * scale, y - 10 * scale], fill=(10, 10, 12))
    # flame above the midship: layered teardrops
    fx = x + hull_w * 0.45
    for r, col in ((flame_h, FLAME), (flame_h * 0.62, FLAME_CORE)):
        draw.ellipse([fx - r * 0.55, y - 52 * scale - r * 1.5,
                      fx + r * 0.55, y - 30 * scale], fill=col)
        draw.polygon([(fx - r * 0.5, y - 40 * scale), (fx, y - 52 * scale - r * 1.6),
                      (fx + r * 0.5, y - 40 * scale)], fill=col)
    # smoke column
    sx = x + hull_w * 0.62
    for i, r in enumerate((26, 34, 44)):
        draw.ellipse([sx - r, y - 150 * scale - i * 46 * scale,
                      sx + r, y - 150 * scale - i * 46 * scale + 2 * r],
                     fill=SMOKE)


def fit_font(draw, text, path, size, width):
    """Largest size at or below `size` that fits `width`."""
    while size > 10 and draw.textlength(text, font=font(path, size)) > width:
        size -= 2
    return font(path, size)


def lead_scene(w, h):
    """Burning tankers in the Strait of Hormuz at dusk, on its own layer."""
    layer = Image.new("RGB", (w, h), SKY_TOP)
    draw = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = 0, 0, w, h
    # sky: horizontal gradient bands
    bands = 48
    for i in range(bands):
        t = i / (bands - 1)
        col = tuple(int(SKY_TOP[c] + (SKY_LOW[c] - SKY_TOP[c]) * t)
                    for c in range(3))
        yy0 = y0 + (y1 - y0) * 0.62 * i / bands
        yy1 = y0 + (y1 - y0) * 0.62 * (i + 1) / bands + 1
        draw.rectangle([x0, yy0, x1, yy1], fill=col)
    horizon = y0 + int((y1 - y0) * 0.62)
    # low sun
    draw.ellipse([x0 + 700, horizon - 52, x0 + 790, horizon + 38],
                 fill=(255, 214, 120))
    # sea
    draw.rectangle([x0, horizon, x1, y1], fill=SEA)
    for i in range(9):
        yy = horizon + 14 + i * 16
        draw.line([x0 + 20 + (i % 3) * 90, yy, x1 - 40 - (i % 2) * 120, yy],
                  fill=(52, 96, 130), width=3)
    # sun reflection
    for i in range(6):
        draw.line([x0 + 716, horizon + 8 + i * 14,
                   x0 + 774, horizon + 8 + i * 14],
                  fill=(255, 170, 80), width=4)
    # three tankers, near to far
    tanker(draw, x0 + 560, horizon - 30, 0.62, 34)
    tanker(draw, x0 + 60, horizon - 8, 0.9, 52)
    tanker(draw, x0 + 330, horizon + 26, 1.05, 62)
    return layer


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    inner = W - 2 * MARGIN

    # ---- masthead -------------------------------------------------
    d.rectangle([MARGIN, 16, W - MARGIN, 20], fill=INK)
    draw_centered(d, 28, "THE WORLD", font(SERIF_B, 92))
    draw_centered(d, 132, "TUESDAY 24 NOVEMBER 2026",
                  font(SANS_B, 40))
    d.rectangle([MARGIN, 182, W - MARGIN, 186], fill=INK)
    d.rectangle([MARGIN, 190, W - MARGIN, 194], fill=INK)

    # ---- lead picture ---------------------------------------------
    scene = lead_scene(inner, 228)
    img.paste(scene, (MARGIN, 202))
    d.rectangle([MARGIN, 202, W - MARGIN, 430], outline=INK, width=3)

    # ---- lead headline --------------------------------------------
    draw_centered(d, 442, "THREE TANKERS ABLAZE",
                  fit_font(d, "THREE TANKERS ABLAZE", SANS_B, 72, inner),
                  fill=RED)
    draw_centered(d, 520, "IN THE STRAIT OF HORMUZ",
                  fit_font(d, "IN THE STRAIT OF HORMUZ", SANS_B, 62, inner))
    draw_centered(
        d, 586,
        "Ships hit naval mines, Iran's Guard says",
        font(SANS_B, 28))
    d.rectangle([MARGIN, 628, W - MARGIN, 632], fill=INK)

    # ---- story rows ------------------------------------------------
    f_head = font(SANS_B, 36)
    f_sub = font(SANS, 21)

    def story(x, y, w, kicker, headline, sub):
        d.text((x, y), kicker, font=font(SANS_B, 20), fill=RED)
        y += 28
        y = draw_lines(d, x, y, wrap(d, headline, f_head, w), f_head,
                       leading=40)
        y = draw_lines(d, x, y + 4, wrap(d, sub, f_sub, w), f_sub,
                       leading=26)
        return y

    col_w = (inner - 36) // 2
    y1 = story(MARGIN, 648, col_w, "UNITED NATIONS",
               "NO DEAL ON KILLER ROBOTS",
               "Robot-weapons talks end with no pact.")
    y2 = story(MARGIN + col_w + 36, 648, col_w, "UNITED STATES",
               "TRUMP HALTS IOWA BLAST",
               "Army: no detonation without a court.")
    d.line([MARGIN + col_w + 18, 648, MARGIN + col_w + 18,
            max(y1, y2)], fill=INK, width=2)

    d.rectangle([MARGIN, 800, W - MARGIN, 804], fill=INK)
    y3 = story(MARGIN, 812, col_w, "WASHINGTON",
               "US SANCTIONS IRAN EXCHANGES",
               "Two dozen-plus exchange houses hit.")
    y4 = story(MARGIN + col_w + 36, 812, col_w, "UNITED NATIONS",
               "RUSSIA: NO NEW GRAIN DEAL",
               "Moscow tells the UN: no new grain deal.")
    d.line([MARGIN + col_w + 18, 812, MARGIN + col_w + 18,
            max(y3, y4)], fill=INK, width=2)

    # ---- briefs strip ----------------------------------------------
    d.rectangle([MARGIN, 958, W - MARGIN, 962], fill=INK)
    draw_centered(
        d, 970,
        "ALSO TODAY:  School bomb threats in Germany & Denmark  ·  "
        "India pledges €1.4bn to Nepal",
        font(SANS_B, 17), fill=INK)
    draw_centered(
        d, 994,
        "China sets 2030 care targets  ·  Colombia violence surges  ·  "
        "Erdoğan visits Libya",
        font(SANS_B, 17), fill=INK)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
