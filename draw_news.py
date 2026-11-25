#!/usr/bin/env python3
"""Draw the "The Wednesday Globe" newspaper front page for 25 November 2026.

Fully deterministic: no randomness, no wall-clock / current-time calls, only a
fixed date string. Uses only Pillow (PIL 10.2.0) and the DejaVu fonts shipped
with the system at /usr/share/fonts/truetype/dejavu/.
"""

import os

from PIL import Image, ImageDraw, ImageFont

# ----------------------------------------------------------------------------
# Fixed constants
# ----------------------------------------------------------------------------
SIZE = 1024
OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

# Palette
PAPER = (247, 242, 229)          # newsprint cream
PANEL = (251, 248, 238)          # story panel fill
PANEL_EDGE = (196, 188, 168)     # story panel border
INK = (23, 23, 23)               # headline ink
BODY = (58, 56, 50)              # caption grey
RULE = (140, 132, 112)           # thin rules
RED = (166, 24, 34)
NAVY = (26, 42, 70)
TEAL = (12, 92, 96)
GREEN = (26, 92, 60)
PURPLE = (88, 46, 108)
BLUE = (30, 80, 160)
GRAY = (82, 82, 88)

# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
img = Image.new("RGB", (SIZE, SIZE), PAPER)
draw = ImageDraw.Draw(img)

_font_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]


def text_w(text, f):
    bbox = draw.textbbox((0, 0), text, font=f)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def fit_font(text, path, max_w, start, minsize):
    """Return the largest font (>= minsize) that fits text on one line."""
    size = start
    while size > minsize:
        f = font(path, size)
        if text_w(text, f)[0] <= max_w:
            return f, size
        size -= 1
    return font(path, minsize), minsize


def wrap(text, f, max_w):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(trial, f)[0] <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def center_text(y, text, f, fill):
    draw.text((SIZE // 2, y), text, font=f, fill=fill, anchor="ma")


def hrule(y, width, color=RULE, x0=None, x1=None):
    x0 = 28 if x0 is None else x0
    x1 = SIZE - 28 if x1 is None else x1
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


# ----------------------------------------------------------------------------
# Masthead + date line
# ----------------------------------------------------------------------------
M = 28                       # outer side margin
y = 26

mast_font, mast_size = fit_font("THE WEDNESDAY GLOBE", SERIF_BOLD, SIZE - 2 * M, 88, 58)
center_text(y, "THE WEDNESDAY GLOBE", mast_font, INK)
y += mast_size + 4

hrule(y, 4, INK)
y += 8

date_font = font(SERIF_BOLD, 33)
center_text(y, "Wednesday, 25 November 2026", date_font, INK)
y += 33 + 8

hrule(y, 2, RULE)
hrule(y + 4, 1, RULE)
y += 14

# ----------------------------------------------------------------------------
# Lead story panel (largest, full width)
# ----------------------------------------------------------------------------
lead_top = y
lead_bottom = lead_top + 240
lead_x0, lead_x1 = M, SIZE - M

draw.rectangle([lead_x0, lead_top, lead_x1, lead_bottom], fill=PANEL,
               outline=PANEL_EDGE, width=2)

# Tag
draw.rectangle([lead_x0 + 14, lead_top + 12, lead_x0 + 24, lead_top + 22], fill=RED)
draw.text((lead_x0 + 32, lead_top + 9), "NEW YORK  ·  LEAD", font=font(SANS_BOLD, 15),
          fill=RED)

# Headline (two explicit lines; "GUILTY" emphasised in red)
lead_head_font = font(SERIF_BOLD, 42)
hx = lead_x0 + 14
ly = lead_top + 40
draw.text((hx, ly), "HUAWEI FOUND ", font=lead_head_font, fill=INK)
guilty_w = text_w("HUAWEI FOUND ", lead_head_font)[0]
draw.text((hx + guilty_w, ly), "GUILTY", font=lead_head_font, fill=RED)
ly += 46
draw.text((hx, ly), "ON 10 OF 12 COUNTS", font=lead_head_font, fill=INK)
ly += 46

# Summary (single line)
summary = "Brooklyn jury convicts Huawei of bank fraud and sanctions violations."
sum_font = font(SANS, 17)
sum_lines = wrap(summary, sum_font, 600)
ly += 6
for line in sum_lines:
    draw.text((lead_x0 + 14, ly), line, font=sum_font, fill=BODY)
    ly += 22

# Gavel motif (right side of lead panel)
gx0 = lead_x1 - 350
gy0 = lead_top + 14
gw, gh = 322, lead_bottom - lead_top - 28


def draw_gavel(bx, by, bw, bh):
    cx = bx + bw // 2
    block_w = min(240, bw - 40)
    block_h = 34
    block_top = by + bh - block_h - 14
    draw.rounded_rectangle(
        [cx - block_w // 2, block_top, cx + block_w // 2, block_top + block_h],
        radius=8, fill=(94, 64, 38), outline=(52, 34, 20), width=3)
    head_w = min(200, bw - 60)
    head_h = 42
    head_bottom = block_top - 8
    head_top = head_bottom - head_h
    draw.rounded_rectangle(
        [cx - head_w // 2, head_top, cx + head_w // 2, head_bottom],
        radius=11, fill=(150, 100, 58), outline=(52, 34, 20), width=3)
    # handle angled up and right
    draw.line([(cx + 4, head_top + 10), (cx + 60, by + 20)],
              fill=(52, 34, 20), width=22)
    draw.line([(cx + 4, head_top + 10), (cx + 60, by + 20)],
              fill=(150, 100, 58), width=13)


draw_gavel(gx0, gy0, gw, gh)

# ----------------------------------------------------------------------------
# Story grid: 7 smaller panels (2-3-2 layout)
# ----------------------------------------------------------------------------
grid_top = lead_bottom + 16
footer_top = SIZE - 42
grid_bottom = footer_top - 14
gap = 14
row_h = (grid_bottom - grid_top - 2 * gap) // 3

panels = [
    # row 1 (2 columns)
    ("NATO · POLAND", NAVY, "NATO SENDS AWACS TO POLAND",
     "NATO early-warning jets for Poland after missiles landed."),
    ("RIYADH", RED, "HOUTHI DRONE HITS RIYADH TOWER",
     "PIF Tower hit again; at least 11 wounded, officials say."),
    # row 2 (3 columns)
    ("HORMUZ", TEAL, "MINES HIT HORMUZ TANKERS",
     "Tankers mined; shipping fears grow."),
    ("MARKETS", GREEN, "AI STOCKS PLUNGE",
     "Nvidia off 5.9%; Anthropic below $83."),
    ("TECH", PURPLE, "HUANG COMEBACK FADES",
     "Huang apologises; the rally fades."),
    # row 3 (2 columns)
    ("KYIV", BLUE, "PUTIN: RETALIATION 'INEVITABLE'",
     "Ukraine hit the Kerch Bridge; both trade UN accusations."),
    ("WASHINGTON", GRAY, "US SPY AGENCIES BREACHED",
     "CIA and ODNI hit by a cyber intrusion exposing data."),
]


def draw_panel(px, py, pw, ph, tag, tag_color, headline, caption):
    draw.rectangle([px, py, px + pw, py + ph], fill=PANEL,
                   outline=PANEL_EDGE, width=2)
    # region tag with colour bullet
    draw.rectangle([px + 12, py + 10, px + 20, py + 18], fill=tag_color)
    draw.text((px + 26, py + 6), tag, font=font(SANS_BOLD, 14), fill=tag_color)
    # headline
    hf = font(SERIF_BOLD, 25)
    hx = px + 12
    hw = pw - 24
    hy = py + 30
    for line in wrap(headline, hf, hw)[:2]:
        draw.text((hx, hy), line, font=hf, fill=INK)
        hy += 29
    # caption (single line, sized to stay inside the panel)
    cf = font(SANS, 15)
    hy += 5
    for line in wrap(caption, cf, hw)[:2]:
        draw.text((hx, hy), line, font=cf, fill=BODY)
        hy += 20


rows = [2, 3, 2]
idx = 0
ry = grid_top
for ncols in rows:
    total_w = (SIZE - 2 * M) - gap * (ncols - 1)
    col_w = total_w // ncols
    rx = M
    for _ in range(ncols):
        tag, color, headline, caption = panels[idx]
        draw_panel(rx, ry, col_w, row_h, tag, color, headline, caption)
        rx += col_w + gap
        idx += 1
    ry += row_h + gap

# ----------------------------------------------------------------------------
# Footer strip
# ----------------------------------------------------------------------------
draw.rectangle([0, footer_top, SIZE, SIZE], fill=NAVY)
center_text(footer_top + 13, "25 November 2026  —  The day in one image",
            font(SANS_BOLD, 16), (247, 242, 229))

img.save(OUT_PATH)
print("wrote", OUT_PATH, img.size)
