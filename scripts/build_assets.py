"""Render the terminal / code-editor visuals used in the profile README.

Edit the data below and run:  python scripts/build_assets.py
Writes SVGs into assets/. Palette matches https://atharvanair04.github.io
"""
from pathlib import Path
from html import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

# ---- palette ---------------------------------------------------------------
BG, SIDEBAR, BORDER, GUTTER = "#0F1115", "#0B0D10", "#1E222A", "#4A505C"
TEXT, MUTED, COMMENT = "#D7DAE0", "#8A919E", "#6B7280"
KW, STR, PROP, NUM, ACCENT = "#FF8A65", "#A5D6A7", "#81D4FA", "#FFD54F", "#FF8A65"
FONT = "JetBrains Mono, Cascadia Code, Consolas, Menlo, monospace"

FS, LH, CW = 14, 22, 8.45  # font size, line height, approx monospace char width
W = 820

# A line is a list of (text, colour[, italic]) segments.
T = lambda s, c=TEXT, i=False: (s, c, i)
C = lambda s: (s, COMMENT, True)


def seg_svg(segs):
    out = []
    for s in segs:
        txt, col, ital = (s + (False,))[:3] if len(s) == 2 else s
        style = ' font-style="italic"' if ital else ""
        out.append(f'<tspan fill="{col}"{style}>{escape(txt)}</tspan>')
    return "".join(out)


def window(title, lines, *, numbered=True, tab=None, lang=None, anim=False, cursor_after=None):
    top = 40 + (32 if tab else 0)
    gutter = 48 if numbered else 20
    h = top + 18 + LH * len(lines) + 18
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-label="{escape(title)}">'
    ]
    if anim:
        css = ["@keyframes in{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}",
               "@keyframes blink{50%{opacity:0}}",
               ".l{opacity:0;animation:in .35s ease-out forwards}",
               ".cur{animation:blink 1s steps(1) infinite}",
               "@media (prefers-reduced-motion:reduce){.l{opacity:1;animation:none}.cur{animation:none}}"]
        parts.append(f"<style>{''.join(css)}</style>")
    parts += [
        f'<rect x=".5" y=".5" width="{W-1}" height="{h-1}" rx="10" fill="{BG}" stroke="{BORDER}"/>',
        f'<path d="M.5 10.5a10 10 0 0 1 10-10h{W-21}a10 10 0 0 1 10 10V40H.5z" fill="{SIDEBAR}"/>',
        f'<line x1="0" y1="40" x2="{W}" y2="40" stroke="{BORDER}"/>',
        '<circle cx="22" cy="20" r="6" fill="#FF5F57"/><circle cx="42" cy="20" r="6" fill="#FEBC2E"/><circle cx="62" cy="20" r="6" fill="#28C840"/>',
        f'<text x="{W/2}" y="25" text-anchor="middle" font-family="{FONT}" font-size="12" fill="{MUTED}">{escape(title)}</text>',
    ]
    if tab:
        tw = len(tab) * 7.6 + 34 + (len(lang) * 7.2 + 18 if lang else 0)
        parts += [
            f'<rect x="0" y="40" width="{W}" height="32" fill="{SIDEBAR}"/>',
            f'<rect x="0" y="40" width="{tw}" height="32" fill="{BG}"/>',
            f'<rect x="0" y="40" width="{tw}" height="2" fill="{ACCENT}"/>',
            f'<text x="16" y="61" font-family="{FONT}" font-size="12.5" fill="{TEXT}">{escape(tab)}</text>',
            f'<line x1="0" y1="72" x2="{W}" y2="72" stroke="{BORDER}"/>',
        ]
        if lang:
            parts.append(f'<text x="{16 + len(tab) * 7.6 + 12}" y="61" font-family="{FONT}" font-size="11" fill="{MUTED}">{escape(lang)}</text>')
    y0 = top + 18 + 15
    for i, segs in enumerate(lines):
        y = y0 + i * LH
        cls, st = "", ""
        if anim:
            cls, st = ' class="l"', f' style="animation-delay:{0.25 + i * 0.32:.2f}s"'
        parts.append(f"<g{cls}{st}>")
        if numbered:
            parts.append(f'<text x="{gutter - 14}" y="{y}" text-anchor="end" font-family="{FONT}" font-size="12" fill="{GUTTER}">{i + 1}</text>')
        parts.append(f'<text x="{gutter}" y="{y}" font-family="{FONT}" font-size="{FS}" xml:space="preserve">{seg_svg(segs)}</text>')
        if cursor_after is not None and i == cursor_after:
            x = gutter + sum(len(s[0]) for s in segs) * CW + 2
            parts.append(f'<rect class="cur" x="{x:.1f}" y="{y - 13}" width="9" height="17" fill="{ACCENT}"/>')
        parts.append("</g>")
    parts.append("</svg>\n")
    return "\n".join(parts)


P = lambda: T("atharva@github", STR)
PROMPT = lambda cmd: [P(), T(":"), T("~", PROP), T("$ "), T(cmd)]

# ---- hero ------------------------------------------------------------------
hero = [
    PROMPT("whoami"),
    [T("Atharva Nair", KW), T(" · frontend engineer")],
    [],
    PROMPT("cat focus.txt"),
    [T("React · TypeScript · Next.js · AI-powered interfaces")],
    [T("prototype → production, with tests that keep it there", MUTED)],
    [],
    PROMPT("./status --short"),
    [T("●", STR), T(" open to remote  "), T("·", MUTED), T(" Thiruvananthapuram, IN  "), T("·", MUTED), T(" B.Tech CSE '27")],
    [],
    [P(), T(":"), T("~", PROP), T("$ ")],
]
(OUT / "hero.svg").write_text(
    window("atharva — zsh — 80×24", hero, numbered=False, anim=True, cursor_after=len(hero) - 1), encoding="utf-8")

# ---- experience as git log -------------------------------------------------
H = lambda h: T(h, NUM)
gitlog = [
    PROMPT("git log --oneline --graph career"),
    [T("* ", KW), H("4e1c9a2"), T(" ("), T("HEAD -> main", PROP), T(") "), T("research: SafeChild, explainable ML, Springer LNCS")],
    [T("* ", KW), H("b73f0d8"), T(" lead: amFOSS web team for amMentor  "), T("dec 2023 – feb 2026", MUTED)],
    [T("* ", KW), H("9a52e17"), T(" chore: anchored Hacktoberfest at college, mentored inductees")],
    [T("* ", KW), H("e08b6c3"), T(" chore: co-coordinated Hack the Future, 36h hackathon @ Vidyut")],
    [T("* ", KW), H("61d4f2a"), T(" feat: Traboda — redesigned 10 core screens in Next.js  "), T("2024–25", MUTED)],
    [T("* ", KW), H("2c9e8b1"), T(" test: 10 Playwright E2E tests, fixed 6 production bugs")],
    [T("* ", KW), H("5f7a0e4"), T(" feat: AWS API integration + end-to-end image upload")],
    [T("* ", KW), H("0000001"), T(" init: B.Tech CSE @ Amrita · CGPA 9.07  "), T("exp. 2027", MUTED)],
]
(OUT / "experience.svg").write_text(window("~/career — git", gitlog, numbered=False), encoding="utf-8")

# ---- project tree ----------------------------------------------------------
D = lambda name: T(name, PROP)
tree = [
    PROMPT("tree ~/projects -L 1"),
    [T("~/projects", KW)],
    [T("├── "), D("colaba-ai/      "), C("# AI collaborative learning · runner-up, OLabs")],
    [T("├── "), D("ammentor/       "), C("# mentorship tracker · web lead @ amFOSS")],
    [T("├── "), D("campus-link/    "), C("# campus platform · Next.js + Flutter")],
    [T("├── "), D("safechild/      "), C("# explainable ML · Springer LNCS co-author")],
    [T("├── "), D("securedrop/     "), C("# anonymous whistleblower portal · archived")],
    [T("└── "), D("pose-estimation/"), C(" # classical CV, revisited · MATLAB + C++")],
    [],
    [T("6 directories", MUTED)],
]
(OUT / "projects.svg").write_text(window("~/projects — zsh", tree, numbered=False), encoding="utf-8")

# ---- one source file per project, each in its own language ----------------
S = lambda s: T(f'"{s}"', STR)
K = lambda s: T(s, KW)
PR = lambda s: T(s, PROP)
files = {
    "colaba": ("colaba-ai.tsx", "TSX", [
        [C("// COlaba AI: collaborative learning on top of OLabs virtual labs")],
        [C("// runner-up · top 8 of 30 teams · OLabs Hackathon, Mar 2025")],
        [],
        [K("export const "), T("colabaAI"), T(": "), PR("Project"), T(" = {")],
        [T("  "), PR("ships"), T(": ["), S("chrome extension"), T(", "), S("web portal"), T("],")],
        [T("  "), PR("features"), T(": ["), S("shared notes"), T(", "), S("live chat"), T(", "), S("video calls"), T("],")],
        [T("  "), PR("ai"), T(": "), S("Gemini summaries + quiz generation"), T(",")],
        [T("  "), PR("stack"), T(": ["), S("Next.js"), T(", "), S("Firebase"), T(", "), S("Tailwind"), T("],")],
        [T("};")],
    ]),
    "ammentor": ("ammentor.tsx", "TSX", [
        [C("// amMentor: mentorship tracking for amFOSS inductees")],
        [C("// role: web team lead · Mar 2025 – Feb 2026 · 97 commits")],
        [],
        [K("export default function "), PR("MentorDashboard"), T("() {")],
        [T("  "), K("const "), T("{ tasks, submissions, evaluations } = "), PR("useInductees"), T("();")],
        [T("  "), K("return "), T("<"), PR("AppRouterShell"), T(" "), PR("components"), T("="), T("{"), PR("sharedLibrary"), T("}>")],
        [T("    <"), PR("ProgressBoard"), T(" "), PR("for"), T("="), S("mentors"), T(" />")],
        [T("  </"), PR("AppRouterShell"), T(">;")],
        [T("}")],
    ]),
    "campuslink": ("campus_link.dart", "Dart", [
        [C("/// Campus Link: one platform for campus communication")],
        [C("/// Software Engineering course · Aug – Nov 2025")],
        [],
        [K("final "), T("campusLink = "), PR("Platform"), T("(")],
        [T("  "), PR("web"), T(": "), S("Next.js admin portal modules"), T(",")],
        [T("  "), PR("mobile"), T(": "), S("Flutter UI flows for students & faculty"), T(",")],
        [T("  "), PR("backend"), T(": "), S("Supabase"), T(",")],
        [T(");")],
    ]),
    "safechild": ("safechild.py", "Python", [
        [C("# SafeChild: explainable AI for child-safety review")],
        [C("# university research team · Springer LNCS paper (co-author) · 2026")],
        [],
        [T("safechild = "), PR("Classifier"), T("(")],
        [T("    "), PR("labels"), T("="), T("5", NUM), T(",  "), C("# grooming behaviours, multi-label")],
        [T("    "), PR("inputs"), T("=["), S("chat text"), T(", "), S("screenshots via OCR"), T("],")],
        [T("    "), PR("explain"), T("="), S("LIME word-level highlights"), T(",")],
        [T("    "), PR("deploy"), T("="), S("Docker → Cloud Build → Vertex AI"), T(",")],
        [T(")")],
    ]),
    "securedrop": ("main.ts", "NestJS", [
        [C("// SecureDrop: anonymous whistleblower portal (no longer maintained)")],
        [],
        [K("@Module"), T("({")],
        [T("  "), PR("imports"), T(": ["), PR("AuthModule"), T(", "), PR("SubmissionsModule"), T(", "), PR("AttachmentsModule"), T("],")],
        [T("})")],
        [K("export class "), PR("SecureDrop"), T(" {")],
        [T("  "), C("// anonymous submit · JWT + role permissions · file-signature checks")],
        [T("  "), C("// every reviewer access is written to an audit log")],
        [T("}")],
    ]),
    "pose": ("pose_estimation.m", "MATLAB", [
        [C("% Pose estimation: Flexible Mixtures-of-Parts, revisited")],
        [],
        [T("im    = "), PR("adaptive_preprocess"), T("(im);")],
        [T("feat  = "), PR("adaptive_featpyramid"), T("(im, model);")],
        [T("boxes = "), PR("detect_fast"), T("(feat, model);")],
        [T("pose  = "), PR("refine_pose"), T("(boxes);   "), C("% then benchmark vs. baseline")],
    ]),
}
for slug, (fname, lang, lines) in files.items():
    (OUT / f"project-{slug}.svg").write_text(
        window(f"~/projects/{fname}", lines, tab=fname, lang=lang), encoding="utf-8")

# ---- skills.json -----------------------------------------------------------
def arr(key, items, last=False):
    segs = [T("  "), T(f'"{key}"', PROP), T(": [")]
    for j, it in enumerate(items):
        segs.append(S(it))
        if j < len(items) - 1:
            segs.append(T(", "))
    segs.append(T("]" + ("" if last else ",")))
    return segs

skills = [
    [T("{")],
    arr("frontend", ["React", "TypeScript", "Next.js", "Tailwind CSS"]),
    arr("aiProduct", ["Gemini API", "LIME", "Hugging Face", "Vertex AI"]),
    arr("quality", ["Playwright", "production debugging"]),
    arr("backend", ["Python", "Firebase", "Supabase", "Docker", "AWS"]),
    arr("mobile", ["Flutter"]),
    arr("also", ["Java", "Google Cloud", "CI/CD", "Git"], last=True),
    [T("}")],
]
(OUT / "skills.svg").write_text(window("skills.json", skills, tab="skills.json", lang="JSON"), encoding="utf-8")

print("wrote", sorted(p.name for p in OUT.glob("*.svg")))
