"""Generate the SVG assets for the GitHub profile README (self-contained, no external requests)."""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)

SANS = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', monospace"
BG = "#0b0f19"


def write(name: str, svg: str) -> None:
    (OUT / name).write_text(svg, encoding="utf-8")


# ---------------------------------------------------------------- banner
def banner() -> str:
    nodes = [(930, 90), (1010, 160), (1090, 70), (1000, 230), (1120, 190), (870, 200), (1150, 120)]
    edges = [(0, 1), (1, 2), (1, 3), (3, 4), (0, 5), (5, 3), (2, 6), (4, 6), (1, 4)]
    lines = "".join(
        f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" '
        f'stroke="url(#g)" stroke-width="1.5" stroke-dasharray="4 6" opacity=".55">'
        f'<animate attributeName="stroke-dashoffset" from="0" to="-40" dur="{3 + i % 3}s" repeatCount="indefinite"/></line>'
        for i, (a, b) in enumerate(edges)
    )
    dots = "".join(
        f'<circle cx="{x}" cy="{y}" r="5" fill="url(#g)">'
        f'<animate attributeName="r" values="4;7;4" dur="{2.5 + i * .4}s" repeatCount="indefinite"/></circle>'
        f'<circle cx="{x}" cy="{y}" r="14" fill="none" stroke="url(#g)" opacity=".25">'
        f'<animate attributeName="r" values="8;22;8" dur="{2.5 + i * .4}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values=".4;0;.4" dur="{2.5 + i * .4}s" repeatCount="indefinite"/></circle>'
        for i, (x, y) in enumerate(nodes)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="320" viewBox="0 0 1200 320" role="img" aria-label="Manuel Albanese. Verifiable AI-assisted engineering.">
<defs>
  <linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8b5cf6"/><stop offset=".55" stop-color="#06b6d4"/><stop offset="1" stop-color="#34d399"/></linearGradient>
  <linearGradient id="t" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#a5b4fc"/></linearGradient>
  <radialGradient id="b1"><stop offset="0" stop-color="#7c3aed" stop-opacity=".55"/><stop offset="1" stop-color="#7c3aed" stop-opacity="0"/></radialGradient>
  <radialGradient id="b2"><stop offset="0" stop-color="#06b6d4" stop-opacity=".45"/><stop offset="1" stop-color="#06b6d4" stop-opacity="0"/></radialGradient>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#ffffff" stroke-opacity=".05"/></pattern>
  <clipPath id="r"><rect width="1200" height="320" rx="24"/></clipPath>
</defs>
<g clip-path="url(#r)">
  <rect width="1200" height="320" fill="{BG}"/>
  <rect width="1200" height="320" fill="url(#grid)"/>
  <circle cx="180" cy="60" r="260" fill="url(#b1)"><animate attributeName="cx" values="180;300;180" dur="14s" repeatCount="indefinite"/></circle>
  <circle cx="980" cy="260" r="280" fill="url(#b2)"><animate attributeName="cx" values="980;860;980" dur="16s" repeatCount="indefinite"/></circle>
  {lines}{dots}
  <text x="70" y="128" font-family="{MONO}" font-size="16" fill="#06b6d4" letter-spacing="3">// HELLO, I'M</text>
  <text x="68" y="196" font-family="{SANS}" font-size="72" font-weight="800" fill="url(#t)">Manuel Albanese</text>
  <text x="70" y="244" font-family="{SANS}" font-size="26" fill="#c4b5fd">Verifiable AI-assisted engineering</text>
  <text x="70" y="282" font-family="{MONO}" font-size="15" fill="#8b949e">orchestration  ·  citable knowledge  ·  enforceable requirements</text>
  <rect x="1" y="1" width="1198" height="318" rx="23" fill="none" stroke="url(#g)" stroke-opacity=".5" stroke-width="1.5"/>
</g></svg>"""


# ---------------------------------------------------------------- cards
CARDS = [
    ("Caronte", "#f59e0b", "#ef4444", "v2.4", ["Delegate to Claude Code with confidence.", "Accept only what the Git diff proves."], ["Claude Code", "Node.js", "Hooks"]),
    ("Teseo", "#22d3ee", "#3b82f6", "MIT", ["Sources in, a wiki you can verify out.", "Citations, graph and local dashboard."], ["Python", "SQLite", "React", "Tauri"]),
    ("Themis", "#a78bfa", "#ec4899", "beta", ["Requirements an agent cannot ignore.", "73 deterministic gates over a spec graph."], ["Python", "MCP", "Nuitka"]),
    ("specdocs-core", "#34d399", "#06b6d4", "WIP", ["Interview in, AFU and ATE documents out.", "Traceable specs, ready for Themis."], ["Python", "Flask", "LaTeX"]),
    ("Radika", "#4ade80", "#a3e635", "MVP", ["Field operations for plant-care businesses.", "Multi-tenant, with an immutable audit trail."], ["TypeScript", "Fastify", "PostgreSQL"]),
    ("SaliceSocialBar", "#fb7185", "#f97316", "prototype", ["Scan the table QR, order, pay at the till.", "A bar's digital menu, client-approved."], ["React 19", "Vite", "Zustand"]),
]


def card(i: int, name: str, c1: str, c2: str, status: str, lines: list[str], chips: list[str]) -> str:
    cx, chip_svg = 28, ""
    for chip in chips:
        w = 14 + len(chip) * 7.4
        chip_svg += (
            f'<rect x="{cx}" y="140" width="{w:.0f}" height="26" rx="13" fill="{c1}" fill-opacity=".12" stroke="{c1}" stroke-opacity=".45"/>'
            f'<text x="{cx + w / 2:.0f}" y="157.5" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{c1}">{escape(chip)}</text>'
        )
        cx += w + 8
    sw = 22 + len(status) * 7.6
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="480" height="190" viewBox="0 0 480 190" role="img" aria-label="{escape(name)}">
<defs>
  <linearGradient id="a{i}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>
  <radialGradient id="o{i}"><stop offset="0" stop-color="{c1}" stop-opacity=".35"/><stop offset="1" stop-color="{c1}" stop-opacity="0"/></radialGradient>
  <clipPath id="c{i}"><rect width="480" height="190" rx="18"/></clipPath>
</defs>
<g clip-path="url(#c{i})">
  <rect width="480" height="190" fill="{BG}"/>
  <circle cx="440" cy="20" r="150" fill="url(#o{i})"><animate attributeName="opacity" values=".6;1;.6" dur="5s" repeatCount="indefinite"/></circle>
  <rect x="0" y="0" width="480" height="4" fill="url(#a{i})"/>
  <rect x="-160" y="0" width="160" height="4" fill="#fff" opacity=".7"><animate attributeName="x" values="-160;480" dur="4.5s" repeatCount="indefinite"/></rect>
  <text x="28" y="62" font-family="{SANS}" font-size="30" font-weight="800" fill="url(#a{i})">{escape(name)}</text>
  <text x="28" y="92" font-family="{SANS}" font-size="14.5" fill="#e6edf3">{escape(lines[0])}</text>
  <text x="28" y="113" font-family="{SANS}" font-size="14.5" fill="#8b949e">{escape(lines[1])}</text>
  {chip_svg}
  <rect x="{452 - sw:.0f}" y="34" width="{sw:.0f}" height="24" rx="12" fill="none" stroke="{c2}" stroke-opacity=".7"/>
  <text x="{452 - sw / 2:.0f}" y="50.5" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{c2}">{escape(status)}</text>
</g>
<rect x=".75" y=".75" width="478.5" height="188.5" rx="17.5" fill="none" stroke="{c1}" stroke-opacity=".35" stroke-width="1.5"/>
</svg>"""


# ---------------------------------------------------------------- flow
def flow() -> str:
    boxes = [
        (40, "specdocs", "interview → AFU + ATE", "#34d399", True),
        (330, "Themis", "spec graph + 73 gates", "#a78bfa", False),
        (620, "Caronte", "delegate + verify the diff", "#f59e0b", False),
        (910, "Your repo", "proven by the diff", "#38bdf8", False),
    ]
    out = []
    for i, (x, t, s, c, wip) in enumerate(boxes):
        dash = ' stroke-dasharray="6 5"' if wip else ""
        out.append(
            f'<rect x="{x}" y="40" width="250" height="96" rx="16" fill="{c}" fill-opacity=".08" stroke="{c}" stroke-width="1.8"{dash}/>'
            f'<text x="{x + 125}" y="82" text-anchor="middle" font-family="{SANS}" font-size="22" font-weight="800" fill="{c}">{t}</text>'
            f'<text x="{x + 125}" y="110" text-anchor="middle" font-family="{MONO}" font-size="12.5" fill="#c9d1d9">{escape(s)}</text>'
        )
        if wip:
            out.append(f'<text x="{x + 125}" y="30" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{c}">work in progress</text>')
        if i < 3:
            ax = x + 250
            out.append(
                f'<line x1="{ax + 6}" y1="88" x2="{ax + 74}" y2="88" stroke="#8b949e" stroke-width="2" stroke-dasharray="6 6">'
                f'<animate attributeName="stroke-dashoffset" from="0" to="-24" dur="1.2s" repeatCount="indefinite"/></line>'
                f'<path d="M{ax + 72} 81 L{ax + 84} 88 L{ax + 72} 95" fill="none" stroke="#8b949e" stroke-width="2"/>'
            )
    teseo = (
        '<rect x="40" y="176" width="1120" height="64" rx="16" fill="#22d3ee" fill-opacity=".08" stroke="#22d3ee" stroke-width="1.8"/>'
        f'<text x="600" y="206" text-anchor="middle" font-family="{SANS}" font-size="20" font-weight="800" fill="#22d3ee">Teseo</text>'
        f'<text x="600" y="228" text-anchor="middle" font-family="{MONO}" font-size="12.5" fill="#c9d1d9">the citable knowledge underneath every step: sources, wiki, graph</text>'
    )
    links = "".join(
        f'<line x1="{x}" y1="140" x2="{x}" y2="172" stroke="#22d3ee" stroke-width="1.6" stroke-dasharray="3 5" opacity=".7">'
        f'<animate attributeName="stroke-dashoffset" from="0" to="16" dur="1.4s" repeatCount="indefinite"/></line>'
        for x in (165, 455, 745, 1035)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="270" viewBox="0 0 1200 270" role="img" aria-label="How the projects fit: specdocs feeds Themis, Themis constrains Caronte, Caronte delivers to your repo, Teseo underpins all of them.">
<rect width="1200" height="270" rx="20" fill="{BG}"/>
{''.join(out)}{links}{teseo}
</svg>"""


# ---------------------------------------------------------------- divider
def divider() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="24" viewBox="0 0 1200 24" role="presentation">
<defs><linearGradient id="d" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8b5cf6" stop-opacity="0"/><stop offset=".3" stop-color="#8b5cf6"/><stop offset=".7" stop-color="#06b6d4"/><stop offset="1" stop-color="#06b6d4" stop-opacity="0"/></linearGradient></defs>
<rect x="0" y="11" width="1200" height="2" fill="url(#d)"/>
<circle cx="600" cy="12" r="5" fill="#06b6d4"><animate attributeName="r" values="4;7;4" dur="3s" repeatCount="indefinite"/></circle>
</svg>"""


# ---------------------------------------------------------------- creation
FINGERS = {
    "index": [(85, -20), (130, -23), (176, -26)],
    "middle": [(92, -4), (125, -2), (150, 10), (158, 28)],
    "ring": [(94, 12), (122, 14), (138, 26), (142, 46)],
    "pinky": [(92, 26), (112, 30), (122, 42), (124, 58)],
    "thumb": [(20, 34), (45, 56), (72, 60), (98, 52)],
}
WIDTHS = {"index": 21, "middle": 20, "ring": 19, "pinky": 17, "thumb": 22}


def poly(pts):
    return "M" + " L".join(f"{x},{y}" for x, y in pts)


def human_hand() -> str:
    parts = [
        '<path d="M-440,-8 L-10,-24 L-10,38 L-440,72 Z" fill="url(#skin)" stroke="#7a4a2b" stroke-width="2"/>',
        '<path d="M-10,-24 C20,-34 60,-38 90,-34 L102,30 C70,46 30,46 -10,38 Z" fill="url(#skin)" stroke="#7a4a2b" stroke-width="2"/>',
    ]
    for name, pts in FINGERS.items():
        w = WIDTHS[name]
        parts.append(f'<path d="{poly(pts)}" fill="none" stroke="#7a4a2b" stroke-width="{w + 3}" stroke-linecap="round" stroke-linejoin="round"/>')
        parts.append(f'<path d="{poly(pts)}" fill="none" stroke="url(#skin)" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')
    parts.append('<path d="M-300,16 C-200,6 -100,2 -20,4" stroke="#fff" stroke-opacity=".18" stroke-width="3" fill="none"/>')
    return "".join(parts)


def robot_hand() -> str:
    parts = [
        '<path d="M-440,-8 L-10,-24 L-10,38 L-440,72 Z" fill="url(#steel)" stroke="#0e7490" stroke-width="2"/>',
        '<path d="M-300,-3 L-300,60 M-200,1 L-200,53 M-110,-7 L-110,47" stroke="#0b0f19" stroke-opacity=".7" stroke-width="3"/>',
        '<path d="M-430,26 L-30,14" stroke="#22d3ee" stroke-width="3" opacity=".9"><animate attributeName="opacity" values=".4;1;.4" dur="2.4s" repeatCount="indefinite"/></path>',
        '<path d="M-10,-24 C20,-34 60,-38 90,-34 L102,30 C70,46 30,46 -10,38 Z" fill="url(#steel)" stroke="#0e7490" stroke-width="2"/>',
        '<rect x="28" y="-12" width="44" height="30" rx="6" fill="#0b0f19" stroke="#22d3ee" stroke-opacity=".7"/>',
        '<circle cx="50" cy="3" r="5" fill="#22d3ee"><animate attributeName="r" values="3.5;6;3.5" dur="2s" repeatCount="indefinite"/></circle>',
    ]
    joints = []
    for name, pts in FINGERS.items():
        w = WIDTHS[name]
        for a, b in zip(pts, pts[1:]):
            parts.append(f'<path d="M{a[0]},{a[1]} L{b[0]},{b[1]}" stroke="#0e7490" stroke-width="{w + 3}" stroke-linecap="round" fill="none"/>')
            parts.append(f'<path d="M{a[0]},{a[1]} L{b[0]},{b[1]}" stroke="url(#steel)" stroke-width="{w - 1}" stroke-linecap="round" fill="none"/>')
        joints += pts[:-1]
    for x, y in joints:
        parts.append(f'<circle cx="{x}" cy="{y}" r="4.5" fill="#0b0f19" stroke="#22d3ee" stroke-width="1.5"/>')
    tx, ty = FINGERS["index"][-1]
    parts.append(f'<circle cx="{tx}" cy="{ty}" r="6" fill="#67e8f9"><animate attributeName="opacity" values=".5;1;.5" dur="1.6s" repeatCount="indefinite"/></circle>')
    return "".join(parts)


def creation() -> str:
    stars = "".join(
        f'<circle cx="{(i * 197) % 1200}" cy="{(i * 61) % 300}" r="{.8 + (i % 3) * .5}" fill="#fff" opacity=".5">'
        f'<animate attributeName="opacity" values=".1;.8;.1" dur="{3 + i % 5}s" begin="{(i % 7) * .4}s" repeatCount="indefinite"/></circle>'
        for i in range(1, 46)
    )
    rays = "".join(f'<line x1="600" y1="150" x2="{600 + 46 * __import__("math").cos(a * 0.5236):.1f}" y2="{150 + 46 * __import__("math").sin(a * 0.5236):.1f}" stroke="#fde68a" stroke-width="2" stroke-linecap="round"/>' for a in range(12))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="320" viewBox="0 0 1200 320" role="img" aria-label="Two hands reaching toward each other, as in The Creation of Adam: a human hand from the left, a robotic hand from the right.">
<defs>
  <linearGradient id="skin" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3c9a0"/><stop offset="1" stop-color="#c98f62"/></linearGradient>
  <linearGradient id="steel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cbd5e1"/><stop offset=".5" stop-color="#64748b"/><stop offset="1" stop-color="#334155"/></linearGradient>
  <radialGradient id="warm"><stop offset="0" stop-color="#f59e0b" stop-opacity=".35"/><stop offset="1" stop-color="#f59e0b" stop-opacity="0"/></radialGradient>
  <radialGradient id="cool"><stop offset="0" stop-color="#06b6d4" stop-opacity=".4"/><stop offset="1" stop-color="#06b6d4" stop-opacity="0"/></radialGradient>
  <radialGradient id="spark"><stop offset="0" stop-color="#fff"/><stop offset=".3" stop-color="#fde68a" stop-opacity=".9"/><stop offset="1" stop-color="#a5f3fc" stop-opacity="0"/></radialGradient>
  <filter id="soft"><feGaussianBlur stdDeviation="1.2"/></filter>
  <clipPath id="cp"><rect width="1200" height="320" rx="24"/></clipPath>
</defs>
<g clip-path="url(#cp)">
  <rect width="1200" height="320" fill="{BG}"/>
  <circle cx="230" cy="170" r="380" fill="url(#warm)"/>
  <circle cx="970" cy="170" r="380" fill="url(#cool)"/>
  {stars}
  <g transform="translate(404,168) rotate(-4)">{human_hand()}</g>
  <g transform="translate(1200,0) scale(-1,1)"><g transform="translate(404,168) rotate(-4)">{robot_hand()}</g></g>
  <g transform="translate(0,0)">
    <g>{rays}<animateTransform attributeName="transform" type="rotate" from="0 600 150" to="360 600 150" dur="18s" repeatCount="indefinite"/><animate attributeName="opacity" values=".3;1;.3" dur="2.4s" repeatCount="indefinite"/></g>
    <circle cx="600" cy="150" r="30" fill="url(#spark)"><animate attributeName="r" values="22;40;22" dur="2.4s" repeatCount="indefinite"/></circle>
  </g>
  <text x="600" y="296" text-anchor="middle" font-family="{MONO}" font-size="14" fill="#8b949e" letter-spacing="4">HUMAN INTENT  ·  MACHINE EXECUTION</text>
  <rect x="1" y="1" width="1198" height="318" rx="23" fill="none" stroke="#ffffff" stroke-opacity=".12" stroke-width="1.5"/>
</g></svg>"""


write("creation.svg", creation())
write("banner.svg", banner())
write("flow.svg", flow())
write("divider.svg", divider())
for n, spec in enumerate(CARDS):
    write(f"card-{spec[0].lower()}.svg", card(n, *spec))
print("ok", sorted(p.name for p in OUT.iterdir()))
