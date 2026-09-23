#!/usr/bin/env python3
"""
bruteon README kit — regenerates every SVG in ./assets.
Edit the CONTENT section, run `python3 generate_assets.py`, commit.
"""
import os, textwrap
from xml.sax.saxutils import escape as esc

# ── PALETTE (bruteon) ────────────────────────────────────────────────
CREAM, INK, CINNABAR, MUSTARD, PAPER = "#EDE6DA", "#1A1512", "#C8321E", "#E8B730", "#DDD3C3"
MONO = "'JetBrains Mono','JetBrainsMono Nerd Font','DejaVu Sans Mono',ui-monospace,Menlo,Consolas,monospace"
CJK  = "'Noto Serif CJK JP','Noto Serif JP','Hiragino Mincho ProN','Yu Mincho','Source Han Serif',serif"
OUT  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

# ── CONTENT ──────────────────────────────────────────────────────────
NAME     = "PURSION"
TAGLINE  = "SOC ANALYST (IN TRAINING) · C++ / CLI TOOLING · GAME DEV"
FILE_TAG = "OPERATOR FILE // UP CEBU · BSCS 2028"
MARQUEE  = "BLUE TEAM ■ DETECTION ENGINEERING ■ WAZUH ■ ATOMIC RED TEAM ■ SECURITY+ 2027 ■ COMPETITIVE PROGRAMMING ■ CEBU, PH ■ "

OPERATOR_LEFT = [
    ("CODENAME",    "Pursion (pursion_)"),
    ("CLASS",       "Defender / Blue Team"),
    ("BRANCH",      "SOC Analyst (in training)"),
    ("AFFILIATION", "UP Cebu · BS CompSci"),
    ("BASE",        "Cebu, Philippines"),
]
OPERATOR_RIGHT = [
    ("CERT TARGET", "CompTIA Security+ · mid-2027"),
    ("GRADUATION",  "Class of 2028"),
    ("CURRENT OP",  "Wazuh lab · phishing study"),
    ("ROADMAP",     "22-month SOC plan"),
    ("OPEN TO",     "Collabs · internships"),
]
TRAITS = [("C++ CLI TOOLING", MUSTARD), ("COMPETITIVE PROGRAMMING", CREAM),
          ("DETECTION ENGINEERING", CINNABAR), ("LINUX RICER", CREAM), ("GAME DESIGN", MUSTARD)]

QUOTE = ("At the end of the day, virtue and dignity hold meaning only "
         "for those who live to see the next dawn.")

# (file, status, kanji, title, description, stack)
PROJECTS = [
    ("quest-soclab", "ACTIVE", "盾", "SOC HOME LAB",
     "Wazuh SIEM on an Ubuntu Server VM. Atomic Red Team simulates attacks so I can measure what my detections actually catch.",
     "Wazuh · Ubuntu Server · QEMU/libvirt"),
    ("quest-phishing", "RESEARCH", "釣", "PHISHING CALIBRATION",
     "Do CS students spot phishing as well as they think they do? A self-hosted, randomized quiz with confidence-weighted scoring.",
     "Research · Web instrument · UP Cebu"),
    ("quest-sqlduel", "IN DESIGN", "魔", "WIZARD SQL DUEL",
     "Real-time competitive SQL. Your queries are spells, and your opponent can watch them forming and cast a counter.",
     "Multiplayer · SQL · Steam-bound"),
    ("quest-bruteon", "IN PROGRESS", "剛", "BRUTEON",
     "Quickshell overlay dashboard for my CachyOS desktop. Soft-dark panels, hairline borders, ambient depth.",
     "Quickshell · QML · KDE Plasma"),
    ("archive-bot", "SHIPPED", "機", "PURSION-BOT",
     "Discord bot for the Block C server: slash commands, a role picker, and schedule reminders.",
     "Python · discord.py"),
    ("archive-ordering", "PROTOTYPE", "運", "WHOLESALE ORDERING",
     "Ordering and logistics platform for a ~100-branch Cebu coffee chain. Four roles, locked down with row-level security.",
     "Next.js · React · Supabase"),
    ("archive-celestial", "ARCHIVED", "星", "CELESTIAL SPEEDRUN",
     "2D platformer built as my capstone. My first big game project.",
     "C++ · SFML"),
    ("archive-pvp", "BACKLOG", "闘", "3D PVP FIGHTER",
     "Roguelike 3D fighter. Local Godot prototype first, then LAN netcode, then a server-authoritative build.",
     "Godot · GDScript · Netcode"),
]
STATUS_STYLE = {  # fill, text
    "ACTIVE": (CINNABAR, CREAM), "RESEARCH": (CINNABAR, CREAM), "IN PROGRESS": (CINNABAR, CREAM),
    "IN DESIGN": (MUSTARD, INK), "PROTOTYPE": (MUSTARD, INK), "BACKLOG": (PAPER, INK),
    "SHIPPED": (INK, CREAM), "ARCHIVED": (INK, CREAM),
}

SECTIONS = [  # file, number, title, kanji
    ("h-01-operator", "01", "OPERATOR FILE",      "档案"),
    ("h-02-quests",   "02", "ACTIVE QUESTS",      "任務"),
    ("h-03-archive",  "03", "ARCHIVE & BACKLOG",  "記録"),
    ("h-04-arsenal",  "04", "ARSENAL",            "武器"),
    ("h-05-fieldlog", "05", "FIELD LOG",          "統計"),
    ("h-06-offduty",  "06", "OFF-DUTY",           "休憩"),
]

OFFDUTY = [
    ("PLAYING",     ["Arknights: Endfield", "Skyblade"]),
    ("DREAMING UP", ["A xianxia idle game", "Wizard SQL Duel"]),
    ("RICING",      ["Soft-dark Quickshell", "Wuling (retired)"]),
]

# ── PRIMITIVES ───────────────────────────────────────────────────────
def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>\n'
            f'<defs><pattern id="hatch" width="10" height="10" patternUnits="userSpaceOnUse" '
            f'patternTransform="rotate(45)"><rect width="4" height="10" fill="{INK}" opacity=".12"/></pattern></defs>\n'
            f'{body}\n</svg>\n')

def box(x, y, w, h, fill=CREAM, shadow=CINNABAR, off=10, sw=4):
    # Shadow is cinnabar, not ink, so the offset still reads on GitHub dark mode.
    return (f'<rect x="{x+off}" y="{y+off}" width="{w}" height="{h}" fill="{shadow}" stroke="{INK}" stroke-width="{sw}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{INK}" stroke-width="{sw}"/>')

def text(x, y, s, size, fill=INK, weight=400, anchor="start", font=MONO, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{esc(s)}</text>')

def chip(x, y, label, fill, fg=INK, size=15, pad=12, h=32):
    w = int(len(label) * size * 0.64) + pad * 2
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{INK}" stroke-width="3"/>'
            + text(x + pad, y + h/2 + size*0.36, label, size, fg, 700,
                   extra=f'textLength="{w - pad*2}" lengthAdjust="spacingAndGlyphs"')), w

def write(name, content):
    with open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8") as f:
        f.write(content)

# ── BANNER ───────────────────────────────────────────────────────────
def banner():
    W, H = 1200, 384
    b = [box(4, 4, 1176, 360)]
    b.append(f'<rect x="4" y="4" width="1176" height="360" fill="url(#hatch)" opacity=".35"/>')
    tag_w = int(len(FILE_TAG) * 17 * 0.62) + 28
    b.append(f'<rect x="36" y="34" width="{tag_w}" height="40" fill="{INK}"/>')
    b.append(text(50, 60, FILE_TAG, 17, CREAM, 700, extra=f'textLength="{tag_w - 28}" lengthAdjust="spacingAndGlyphs"'))
    name_w = 88 * len(NAME)  # locked width so every fallback font lines up
    b.append(text(34, 212, NAME, 150, INK, 800, extra=f'textLength="{name_w}" lengthAdjust="spacingAndGlyphs"'))
    cx = 34 + name_w + 14
    b.append(f'<rect x="{cx:.0f}" y="112" width="40" height="104" fill="{CINNABAR}">'
             f'<animate attributeName="opacity" values="1;1;0;0" dur="1.1s" repeatCount="indefinite"/></rect>')
    b.append(text(38, 262, TAGLINE, 21, INK, 700))
    # sticker
    b.append(f'<g transform="rotate(-12 812 104)"><circle cx="812" cy="104" r="54" fill="{MUSTARD}" stroke="{INK}" stroke-width="4"/>'
             + text(812, 98, "3RD", 24, INK, 800, "middle") + text(812, 124, "YEAR", 20, INK, 800, "middle") + '</g>')
    # kanji seal
    b.append(f'<rect x="906" y="42" width="236" height="224" fill="{MUSTARD}" stroke="{INK}" stroke-width="4"/>')
    b.append(f'<rect x="898" y="34" width="236" height="224" fill="{INK}" stroke="{INK}" stroke-width="4"/>')
    b.append(text(1016, 212, "守", 176, CREAM, 900, "middle", CJK))
    b.append(text(1016, 246, "SHU · TO GUARD", 15, MUSTARD, 700, "middle"))
    # marquee strip
    b.append(f'<rect x="4" y="298" width="1176" height="66" fill="{INK}"/>')
    b.append('<clipPath id="strip"><rect x="4" y="298" width="1176" height="66"/></clipPath>')
    seg = len(MARQUEE) * 20 * 0.6
    b.append(f'<g clip-path="url(#strip)"><g>'
             + text(20, 339, MARQUEE * 3, 20, CREAM, 700)
             + f'<animateTransform attributeName="transform" type="translate" from="0 0" to="{-seg:.0f} 0" dur="28s" repeatCount="indefinite"/></g></g>')
    write("banner", svg(W, H, "\n".join(b), f"{NAME} — {TAGLINE}"))

# ── SECTION HEADERS ──────────────────────────────────────────────────
def section(fname, num, title, kanji):
    W, H = 1200, 104
    b = [box(4, 4, 1176, 84, off=8)]
    b.append(f'<rect x="4" y="4" width="96" height="84" fill="{INK}"/>')
    b.append(text(52, 60, num, 40, CREAM, 800, "middle"))
    b.append(text(128, 60, title, 38, INK, 800, extra='letter-spacing="1"'))
    b.append(text(1156, 66, kanji, 50, CINNABAR, 900, "end", CJK))
    write(fname, svg(W, H, "\n".join(b), f"{num} — {title}"))

# ── OPERATOR CARD ────────────────────────────────────────────────────
def operator():
    W, H = 1200, 470
    b = [box(4, 4, 1176, 446)]
    b.append(f'<rect x="4" y="4" width="1176" height="52" fill="{INK}"/>')
    b.append(text(28, 38, "PERSONNEL RECORD", 20, CREAM, 800))
    b.append(text(1156, 38, "CLEARANCE: PUBLIC", 16, MUSTARD, 700, "end"))
    for col, rows in ((0, OPERATOR_LEFT), (1, OPERATOR_RIGHT)):
        x0 = 32 + col * 588
        for i, (k, v) in enumerate(rows):
            y = 84 + i * 56
            b.append(f'<rect x="{x0}" y="{y}" width="176" height="36" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>')
            b.append(text(x0 + 10, y + 24, k, 15, INK, 800))
            b.append(text(x0 + 192, y + 26, v, 21, INK, 500))
    b.append(f'<line x1="592" y1="84" x2="592" y2="344" stroke="{INK}" stroke-width="2" stroke-dasharray="6 6"/>')
    b.append(f'<line x1="4" y1="370" x2="1180" y2="370" stroke="{INK}" stroke-width="3"/>')
    b.append(text(32, 414, "TRAITS", 18, INK, 800))
    x = 120
    for label, fill in TRAITS:
        c, w = chip(x, 390, label, fill, CREAM if fill == CINNABAR else INK)
        b.append(c); x += w + 14
    write("operator", svg(W, H, "\n".join(b), "Operator file: Pursion"))

# ── DIALOGUE ─────────────────────────────────────────────────────────
def dialogue():
    W, H = 1200, 214
    b = [box(4, 34, 1176, 160)]
    b.append(f'<rect x="36" y="10" width="250" height="46" fill="{INK}" stroke="{INK}" stroke-width="3"/>')
    b.append(text(54, 41, "PURSION // LOG", 20, CREAM, 800))
    for i, line in enumerate(textwrap.wrap(QUOTE, 72)):
        b.append(text(44, 106 + i * 36, ("“" if i == 0 else " ") + line + ("”" if i == len(textwrap.wrap(QUOTE, 72)) - 1 else ""),
                      24, INK, 500, extra='font-style="italic"'))
    b.append(f'<polygon points="1136,162 1160,162 1148,176" fill="{CINNABAR}">'
             f'<animate attributeName="opacity" values="1;0;1" dur="1.2s" repeatCount="indefinite"/></polygon>')
    write("dialogue", svg(W, H, "\n".join(b), QUOTE))

# ── PROJECT CARDS ────────────────────────────────────────────────────
def card(fname, status, kanji, title, desc, stack):
    W, H = 600, 290
    b = [box(4, 4, 576, 272)]
    b.append(text(560, 262, kanji, 190, INK, 900, "end", CJK, 'opacity=".07"'))
    fill, fg = STATUS_STYLE[status]
    c, _ = chip(28, 28, status, fill, fg); b.append(c)
    b.append(f'<rect x="504" y="24" width="52" height="52" fill="{INK}"/>')
    b.append(text(530, 64, kanji, 36, CREAM, 900, "middle", CJK))
    b.append(text(28, 118, title, 30, INK, 800))
    for i, line in enumerate(textwrap.wrap(desc, 50)[:3]):
        b.append(text(28, 152 + i * 25, line, 17, INK, 400))
    b.append(f'<rect x="4" y="226" width="576" height="50" fill="{INK}"/>')
    b.append(text(28, 257, "▸ " + stack, 16, CREAM, 700))
    write(fname, svg(W, H, "\n".join(b), f"{title} — {status}: {desc}"))

# ── OFF-DUTY ─────────────────────────────────────────────────────────
def offduty():
    W, H = 1200, 200
    b = [box(4, 4, 1176, 176)]
    colw = 1176 / len(OFFDUTY)
    for i, (head, items) in enumerate(OFFDUTY):
        x = 4 + i * colw
        if i: b.append(f'<line x1="{x}" y1="4" x2="{x}" y2="180" stroke="{INK}" stroke-width="3"/>')
        b.append(f'<rect x="{x}" y="4" width="{colw}" height="50" fill="{[MUSTARD, CREAM, CINNABAR][i]}" stroke="{INK}" stroke-width="3"/>')
        b.append(text(x + 24, 38, head, 20, CREAM if i == 2 else INK, 800))
        for j, it in enumerate(items):
            b.append(text(x + 24, 102 + j * 44, "▪ " + it, 20, INK, 500))
    write("offduty", svg(W, H, "\n".join(b), "Off-duty: " + "; ".join(h + ": " + ", ".join(i) for h, i in OFFDUTY)))

# ── FOOTER ───────────────────────────────────────────────────────────
def footer():
    W, H = 1200, 132
    b = [box(4, 4, 1176, 108, fill=INK, shadow=MUSTARD)]
    b.append(text(36, 58, "THANKS FOR STOPPING BY", 30, CREAM, 800))
    b.append(text(36, 92, "BUILT NEO-BRUTALIST // CEBU, PH", 16, MUSTARD, 700))
    b.append(text(1152, 84, "またね", 52, CINNABAR, 900, "end", CJK))
    write("footer", svg(W, H, "\n".join(b), "Thanks for stopping by — mata ne"))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    banner(); operator(); dialogue(); offduty(); footer()
    for s in SECTIONS: section(*s)
    for p in PROJECTS: card(*p)
    print("wrote", len(os.listdir(OUT)), "files to", OUT)
