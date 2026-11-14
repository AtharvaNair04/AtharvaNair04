"""Generate the project cover cards used in the profile README.

Edit PROJECTS below and run:  python scripts/build_covers.py
Writes assets/cover-<slug>.svg (one per project).
"""
from pathlib import Path
from html import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

# Each project gets its own accent so the grid doesn't look copy-pasted.
PROJECTS = [
    dict(slug="colaba", title="COlaba AI", kicker="AI · EDTECH", accent="#f59e0b",
         line="Collaborative learning on top of OLabs", glyph="spark"),
    dict(slug="ammentor", title="amMentor", kicker="WEB LEAD · amFOSS", accent="#7aa2f7",
         line="Mentorship tracking for club inductees", glyph="grid"),
    dict(slug="campuslink", title="Campus Link", kicker="WEB + MOBILE", accent="#2dd4bf",
         line="One platform for campus communication", glyph="link"),
    dict(slug="safechild", title="SafeChild", kicker="EXPLAINABLE ML · RESEARCH", accent="#f472b6",
         line="Showing reviewers why the model flagged it", glyph="shield"),
    dict(slug="securedrop", title="SecureDrop", kicker="SECURITY · FULL STACK", accent="#a78bfa",
         line="Anonymous whistleblower portal", glyph="lock"),
    dict(slug="pose", title="Pose Estimation", kicker="COMPUTER VISION", accent="#fb7185",
         line="Classical human pose estimation, revisited", glyph="pose"),
]

W, H = 480, 200

GLYPHS = {
    # Simple line drawings, drawn in the top-right corner (origin at 0,0 of a 90x90 box)
    "spark": '<path d="M45 8 L53 37 L82 45 L53 53 L45 82 L37 53 L8 45 L37 37 Z"/>',
    "grid": '<rect x="8" y="8" width="32" height="40" rx="5"/><rect x="50" y="8" width="32" height="22" rx="5"/>'
            '<rect x="50" y="40" width="32" height="42" rx="5"/><rect x="8" y="58" width="32" height="24" rx="5"/>',
    "link": '<path d="M38 52 a16 16 0 0 1 0-22 l10-10 a16 16 0 0 1 22 22 l-6 6"/>'
            '<path d="M52 38 a16 16 0 0 1 0 22 l-10 10 a16 16 0 0 1-22-22 l6-6"/>',
    "shield": '<path d="M45 8 L78 20 V44 C78 64 64 78 45 84 C26 78 12 64 12 44 V20 Z"/><path d="M31 46 L41 56 L60 36"/>',
    "lock": '<rect x="16" y="38" width="58" height="44" rx="8"/><path d="M28 38 V28 a17 17 0 0 1 34 0 V38"/>'
            '<circle cx="45" cy="58" r="5"/><path d="M45 63 V70"/>',
    "pose": '<circle cx="45" cy="14" r="7"/><path d="M45 21 V52 M45 30 L24 44 M45 30 L66 20 M45 52 L30 82 M45 52 L62 80"/>'
            '<circle cx="24" cy="44" r="3"/><circle cx="66" cy="20" r="3"/><circle cx="30" cy="82" r="3"/><circle cx="62" cy="80" r="3"/>',
}


def cover(p):
    a = p["accent"]
    dots = "".join(
        f'<circle cx="{x}" cy="{y}" r="1.2" fill="{a}" opacity="0.18"/>'
        for x in range(20, W, 20) for y in range(20, H, 20)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(p["title"])}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#16161e"/>
      <stop offset="1" stop-color="#1f2030"/>
    </linearGradient>
    <clipPath id="r"><rect width="{W}" height="{H}" rx="14"/></clipPath>
  </defs>
  <g clip-path="url(#r)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    {dots}
    <circle cx="{W - 40}" cy="40" r="120" fill="{a}" opacity="0.10"/>
    <rect x="0" y="0" width="6" height="{H}" fill="{a}"/>
  </g>
  <g transform="translate({W - 120},26)" fill="none" stroke="{a}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
    {GLYPHS[p["glyph"]]}
  </g>
  <text x="30" y="52" font-family="JetBrains Mono, Consolas, monospace" font-size="12" letter-spacing="2" fill="{a}">{escape(p["kicker"])}</text>
  <text x="30" y="118" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="40" font-weight="800" fill="#e7e9f3">{escape(p["title"])}</text>
  <text x="30" y="152" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="16" fill="#a9b1d6">{escape(p["line"])}</text>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="#2f3349"/>
</svg>
'''


for p in PROJECTS:
    (OUT / f"cover-{p['slug']}.svg").write_text(cover(p), encoding="utf-8")
    print("wrote", f"cover-{p['slug']}.svg")
