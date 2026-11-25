# Build notes — The Wednesday Globe (news-image-20261125)

## What was drawn

A 1024x1024 newsprint-style front page, generated deterministically by
`draw_news.py` (Pillow only, DejaVu system fonts, no randomness, no clock):

- **Masthead** — "THE WEDNESDAY GLOBE" in large serif, with the date line
  "Wednesday, 25 November 2026" directly beneath it.
- **Lead story** — "HUAWEI FOUND GUILTY / ON 10 OF 12 COUNTS" with a red
  "GUILTY", a one-line summary (Brooklyn jury, bank fraud, sanctions
  violations) and a simple drawn gavel motif.
- **Seven panel grid (2-3-2)** — NATO sends AWACS to Poland; Houthi drone hits
  Riyadh tower; mines hit Hormuz tankers; AI stocks plunge; Huang comeback
  fades; Putin calls retaliation inevitable; US spy agencies breached. Each
  panel has a region tag, a short headline and a one-line caption.
- **Footer strip** — "25 November 2026 — The day in one image".

## How it was verified

- `entry.png` is a valid PNG, 1024x1024 RGB, ~106 KB (well under 1 MiB).
- Text fitting was checked programmatically: every headline wraps to at most
  two lines and every caption to exactly one line, so nothing is truncated or
  overlapping; the masthead and date both fit the page width.
- Glyph coverage was checked via the DejaVu cmap tables: every character used
  (including ·, — and $) has a real glyph, so there is no tofu/garbled text.
- Pixel-density checks confirm ink is present in the masthead, date, lead,
  all seven panels and the footer, with clean gutters between panels.
- `main.py` was run twice into two different directories (`out-a`, `out-b`);
  both outputs were byte-identical (`sha256sum` equal).
- `python3 main.py` uses only the standard library and needs no network.

## Revisions made

- `draw_news.py` v1: initial layout; three-column panels wrapped to 3 lines and
  the lead summary ran to 3 lines.
- `draw_news.py` v2: shortened captions to one line and set the caption size to
  15px so every panel fits cleanly.
- `draw_news.py` v3: made the lead summary a single line, emphasised "GUILTY"
  in red and widened the headline to "ON 10 OF 12 COUNTS".
