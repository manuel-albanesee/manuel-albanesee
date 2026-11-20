"""Colorize ascii_hero.txt into assets/ascii-hero.svg (per-glyph positioned text, no external requests).

Run by hand: python ascii_color.py. Reads ascii_hero.txt (plain text), writes assets/ascii-hero.svg.
"""
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).parent
BG = (11, 15, 25)
STOPS = [(0.0, (139, 92, 246)), (0.5, (6, 182, 212)), (1.0, (52, 211, 153))]
AMBER = (251, 191, 36)
CW, LH, FS = 4.2, 8.6, 7.2
HEAVY = set("@#%XA2")
DIM = set(",.:;'`-")
STRUCT = set("\\/|)(")


def grad(t):
    for (a, ca), (b, cb) in zip(STOPS, STOPS[1:]):
        if t <= b:
            k = (t - a) / (b - a)
            return tuple(ca[i] + (cb[i] - ca[i]) * k for i in range(3))
    return STOPS[-1][1]


def mix(c, d, k):
    return tuple(c[i] + (d[i] - c[i]) * k for i in range(3))


def hexq(c):
    return "#%02x%02x%02x" % tuple(min(255, int(round(v / 16) * 16)) for v in c)


lines = (HERE / "ascii_hero.txt").read_text(encoding="utf-8").rstrip("\n").split("\n")
cols = max(len(l) for l in lines)
w, h = int(cols * CW) + 40, int(len(lines) * LH) + 40

rows = []
for r, line in enumerate(lines):
    y = 24 + r * LH
    runs = []  # (color, [(x, ch)])
    for c, ch in enumerate(line):
        if ch == " ":
            continue
        col = grad(c / cols)
        # amber accents: eyes and sensors "(o)", "(@)", "(O)"
        near = line[max(0, c - 2): c + 3]
        if ch in "o@O" and ("(" in near and ")" in near):
            col = AMBER
        elif ch in HEAVY:
            col = mix(col, (255, 255, 255), 0.35)
        elif ch in DIM:
            col = mix(col, BG, 0.45)
        elif ch in STRUCT:
            col = mix(col, (255, 255, 255), 0.1)
        key = hexq(col)
        if runs and runs[-1][0] == key:
            runs[-1][1].append((c, ch))
        else:
            runs.append((key, [(c, ch)]))
    for key, items in runs:
        xs = " ".join(f"{20 + c * CW:.1f}" for c, _ in items)
        txt = escape("".join(ch for _, ch in items))
        rows.append(f'<text x="{xs}" y="{y:.1f}" fill="{key}">{txt}</text>')

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="ASCII art of a robotic figure in violet, cyan and green.">
<rect width="{w}" height="{h}" rx="20" fill="#0b0f19"/>
<g font-family="'SFMono-Regular', Consolas, 'Liberation Mono', monospace" font-size="{FS}" font-weight="700">
{chr(10).join(rows)}
</g>
<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="19.5" fill="none" stroke="#ffffff" stroke-opacity=".12"/>
</svg>"""
(HERE / "assets" / "ascii-hero.svg").write_text(svg, encoding="utf-8")
print(w, h, len(svg))
