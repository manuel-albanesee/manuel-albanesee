"""Turn the hands geometry from build_assets.py into ASCII art.

Step 1 (--mask): write hands_mask.html, an SVG of the two hands on black.
Step 2 (--ascii hands_mask.png): convert the screenshot into assets/creation.svg made of text.
Run by hand; reads build_assets.py and the PNG screenshot, writes SVG only.
"""
import sys
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import build_assets as b  # noqa: E402  (regenerates the other assets, harmless)

COLS, ROWS = 150, 31  # character grid
RAMP = " .'`:-~+=*#%@"


def mask():
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="320" viewBox="0 0 1200 320">
<defs>
<linearGradient id="skin" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#777"/></linearGradient>
<linearGradient id="steel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#666"/></linearGradient>
</defs>
<rect width="1200" height="320" fill="#000"/>
<g transform="translate(404,168) rotate(-4)">{b.human_hand()}</g>
<g transform="translate(1200,0) scale(-1,1)"><g transform="translate(404,168) rotate(-4)">{b.robot_hand()}</g></g>
</svg>"""
    (HERE / "hands_mask.html").write_text(
        f"<body style='margin:0;background:#000'>{svg}</body>", encoding="utf-8"
    )


def ascii_svg(png: Path):
    from PIL import Image

    from PIL import ImageChops, ImageFilter

    base = Image.open(png).convert("L").crop((380, 130, 1130, 320)).resize((COLS, ROWS), Image.LANCZOS)
    edges = base.filter(ImageFilter.FIND_EDGES).point(lambda p: min(255, p * 4))
    im = ImageChops.add(base.point(lambda p: int(p * 0.5)), edges)
    px = im.load()
    cw, lh = 7.8, 9.4
    w = int(COLS * cw) + 40
    h = int(ROWS * lh) + 90
    lines = []
    for y in range(ROWS):
        row = ""
        for x in range(COLS):
            v = px[x, y] / 255
            row += RAMP[min(int(v * (len(RAMP) - 1) + 0.5), len(RAMP) - 1)]
        lines.append(row)
    half = COLS // 2
    spans = []
    for i, row in enumerate(lines):
        y = 30 + i * lh
        left, right = escape(row[:half]), escape(row[half:])
        spans.append(
            f'<text x="20" y="{y:.1f}" xml:space="preserve" textLength="{half * cw:.0f}" lengthAdjust="spacing" fill="#f5b87a">{left}</text>'
            f'<text x="{20 + half * cw:.0f}" y="{y:.1f}" xml:space="preserve" textLength="{(COLS - half) * cw:.0f}" lengthAdjust="spacing" fill="#22d3ee">{right}</text>'
        )
    cy = 30 + (ROWS * 0.22) * lh
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="ASCII art: a human hand from the left and a robotic hand from the right reach toward each other, as in The Creation of Adam.">
<rect width="{w}" height="{h}" rx="20" fill="{b.BG}"/>
<g font-family="{b.MONO}" font-size="10.5" font-weight="700">
{''.join(spans)}
</g>
<text x="{w / 2:.0f}" y="{cy:.0f}" text-anchor="middle" font-family="{b.MONO}" font-size="26" font-weight="800" fill="#fde68a">*<animate attributeName="opacity" values="1;.2;1" dur="1.6s" repeatCount="indefinite"/></text>
<text x="{w / 2:.0f}" y="{h - 28}" text-anchor="middle" font-family="{b.MONO}" font-size="13" fill="#8b949e" letter-spacing="4">[ HUMAN INTENT ]  ----&gt;  *  &lt;----  [ MACHINE EXECUTION ]</text>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="19" fill="none" stroke="#ffffff" stroke-opacity=".12"/>
</svg>"""
    (HERE / "assets" / "creation.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    if "--mask" in sys.argv:
        mask()
    else:
        ascii_svg(Path(sys.argv[sys.argv.index("--ascii") + 1]))
