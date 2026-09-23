#!/usr/bin/env python3
"""
bruteon stats cards — self-generated replacements for github-readme-stats,
the activity graph, and friends. No Vercel, no quotas.

Runs in GitHub Actions (see .github/workflows/profile-cards.yml):
    GH_TOKEN=... python3 scripts/stats_cards.py JecerSE dist
Local preview without a token:
    python3 scripts/stats_cards.py JecerSE dist --mock
"""
import datetime as dt, json, os, random, sys, urllib.request
from xml.sax.saxutils import escape as esc

CREAM, INK, CINNABAR, MUSTARD, PAPER = "#EDE6DA", "#1A1512", "#C8321E", "#E8B730", "#DDD3C3"
LANG_COLORS = [INK, CINNABAR, MUSTARD, "#8A5A3C", "#D9C9B0", "#6E6259"]
MONO = "'JetBrains Mono','JetBrainsMono Nerd Font','DejaVu Sans Mono',ui-monospace,Menlo,Consolas,monospace"
CJK = "'Noto Serif CJK JP','Noto Serif JP','Hiragino Mincho ProN','Yu Mincho',serif"
HIDE_LANGS = {"HTML", "CSS", "SCSS", "Jupyter Notebook", "Makefile", "CMake", "Dockerfile", "Shell"}

QUERY = """
query($login: String!) {
  user(login: $login) {
    repositories(ownerAffiliations: OWNER, isFork: false, first: 100) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name } }
        }
      }
    }
    pullRequests { totalCount }
    issues { totalCount }
    contributionsCollection {
      totalCommitContributions
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}"""

# ── DATA ─────────────────────────────────────────────────────────────
def fetch(login, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "bruteon-stats-cards"})
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if payload.get("errors"):
        sys.exit("GraphQL error: " + json.dumps(payload["errors"]))
    u = payload["data"]["user"]
    cc = u["contributionsCollection"]
    langs = {}
    for repo in u["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    weeks = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in cc["contributionCalendar"]["weeks"]]
    week_starts = [w["contributionDays"][0]["date"] for w in cc["contributionCalendar"]["weeks"]]
    return {
        "stars": sum(r["stargazerCount"] for r in u["repositories"]["nodes"]),
        "repos": u["repositories"]["totalCount"],
        "commits": cc["totalCommitContributions"] + cc["restrictedContributionsCount"],
        "prs": u["pullRequests"]["totalCount"],
        "issues": u["issues"]["totalCount"],
        "contrib": cc["contributionCalendar"]["totalContributions"],
        "langs": langs, "weeks": weeks[-52:], "week_starts": week_starts[-52:],
    }

def mock():
    random.seed(7)
    today = dt.date.today()
    starts = [(today - dt.timedelta(weeks=51 - i, days=today.weekday() + 1)).isoformat() for i in range(52)]
    return {"stars": 14, "repos": 23, "commits": 612, "prs": 9, "issues": 11, "contrib": 734,
            "langs": {"C++": 410000, "Python": 220000, "JavaScript": 160000, "TypeScript": 60000,
                      "QML": 30000, "GDScript": 22000, "HTML": 90000},
            "weeks": [random.choice([0, 2, 5, 9, 14, 21, 30]) for _ in range(52)], "week_starts": starts}

# ── DRAWING ──────────────────────────────────────────────────────────
def T(x, y, s, size, fill=INK, weight=400, anchor="start", font=MONO, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{esc(str(s))}</text>')

def frame(w, h, title, kanji, body, label):
    bw, bh = w - 24, h - 24
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(label)}">'
            f'<title>{esc(label)}</title>'
            f'<rect x="14" y="14" width="{bw}" height="{bh}" fill="{CINNABAR}" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="4" y="4" width="{bw}" height="{bh}" fill="{CREAM}" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="4" y="4" width="{bw}" height="46" fill="{INK}"/>'
            + T(24, 35, title, 19, CREAM, 800) + T(bw - 16, 38, kanji, 26, MUSTARD, 900, "end", CJK)
            + body + "</svg>\n")

def fmt(n):
    return f"{n/1000:.1f}k" if n >= 10000 else f"{n:,}"

def stats_card(d):
    rows = [("STARS EARNED", d["stars"]), ("COMMITS · 1Y", d["commits"]), ("PULL REQUESTS", d["prs"]),
            ("ISSUES", d["issues"]), ("REPOSITORIES", d["repos"])]
    b = []
    for i, (k, v) in enumerate(rows):
        y = 84 + i * 32
        b.append(T(28, y, "▪ " + k, 16, INK, 700))
        b.append(T(356, y, fmt(v), 18, INK, 800, "end"))
        if i < len(rows) - 1:
            b.append(f'<line x1="28" y1="{y+11}" x2="356" y2="{y+11}" stroke="{INK}" stroke-width="1" stroke-dasharray="3 4" opacity=".45"/>')
    b.append(f'<rect x="392" y="70" width="164" height="146" fill="{MUSTARD}" stroke="{INK}" stroke-width="3"/>')
    b.append(T(474, 146, fmt(d["contrib"]), 46, INK, 800, "middle",
               extra=f'textLength="{min(140, 30 * len(fmt(d["contrib"])))}" lengthAdjust="spacingAndGlyphs"'))
    b.append(T(474, 180, "CONTRIBUTIONS", 13, INK, 800, "middle"))
    b.append(T(474, 200, "LAST 12 MONTHS", 13, INK, 700, "middle"))
    return frame(600, 250, "FIELD STATS", "統計", "".join(b),
                 f"GitHub stats: {d['contrib']} contributions in the last year, {d['commits']} commits, {d['stars']} stars")

def langs_card(d, top=6):
    langs = sorted(((k, v) for k, v in d["langs"].items() if k not in HIDE_LANGS), key=lambda kv: -kv[1])[:top]
    total = sum(v for _, v in langs) or 1
    b, x = [], 28.0
    b.append(f'<rect x="28" y="70" width="528" height="30" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>')
    for i, (name, v) in enumerate(langs):
        w = 528 * v / total
        b.append(f'<rect x="{x:.1f}" y="70" width="{w:.1f}" height="30" fill="{LANG_COLORS[i]}" stroke="{INK}" stroke-width="3"/>')
        x += w
    for i, (name, v) in enumerate(langs):
        col, row = i % 2, i // 2
        cx, cy = 28 + col * 270, 138 + row * 34
        b.append(f'<rect x="{cx}" y="{cy-15}" width="18" height="18" fill="{LANG_COLORS[i]}" stroke="{INK}" stroke-width="2"/>')
        b.append(T(cx + 28, cy, name.upper()[:14], 16, INK, 700))
        b.append(T(cx + 248, cy, f"{100*v/total:.1f}%", 16, INK, 500, "end"))
    if not langs:
        b.append(T(300, 150, "NO LANGUAGE DATA YET", 16, INK, 700, "middle"))
    return frame(600, 250, "LANGUAGE LOADOUT", "武器", "".join(b),
                 "Top languages: " + ", ".join(f"{n} {100*v/total:.0f}%" for n, v in langs))

def activity_card(d):
    weeks, starts = d["weeks"], d["week_starts"]
    x0, x1, y0, y1 = 44, 1150, 76, 236
    peak = max(weeks) or 1
    step = (x1 - x0) / max(len(weeks), 1)
    b = [f'<rect x="4" y="50" width="1176" height="226" fill="url(#hatch)"/>']
    for g in (0.5, 1.0):
        gy = y1 - (y1 - y0) * g
        b.append(f'<line x1="{x0}" y1="{gy:.1f}" x2="{x1}" y2="{gy:.1f}" stroke="{INK}" stroke-width="1" stroke-dasharray="4 6" opacity=".35"/>')
        b.append(T(x0 - 8, gy + 5, round(peak * g), 12, INK, 700, "end"))
    last_month, last_x = None, -99
    for i, (n, s) in enumerate(zip(weeks, starts)):
        bx = x0 + i * step + 3
        bw = step - 6
        h = (y1 - y0) * n / peak
        fill = MUSTARD if i == len(weeks) - 1 else CINNABAR
        if n:
            b.append(f'<rect x="{bx:.1f}" y="{y1-h:.1f}" width="{bw:.1f}" height="{h:.1f}" fill="{fill}" stroke="{INK}" stroke-width="2"/>')
        else:
            b.append(f'<rect x="{bx:.1f}" y="{y1-3}" width="{bw:.1f}" height="3" fill="{INK}"/>')
        m = s[5:7]
        if m != last_month:
            if bx - last_x > 44:
                b.append(T(bx, 258, dt.date.fromisoformat(s).strftime("%b").upper(), 12, INK, 700))
                last_x = bx
            last_month = m
    b.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="{INK}" stroke-width="3"/>')
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    b.append(T(1086, 34, f"TOTAL {d['contrib']} · UPDATED {stamp}", 13, CREAM, 700, "end"))
    body = ('<defs><pattern id="hatch" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<rect width="4" height="10" fill="{INK}" opacity=".06"/></pattern></defs>' + "".join(b))
    return frame(1200, 300, "CONTRIBUTION LOG // LAST 52 WEEKS", "記録", body,
                 f"Weekly contributions over the last year, {d['contrib']} total")

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    login = args[0] if args else "JecerSE"
    out = args[1] if len(args) > 1 else "dist"
    if "--mock" in sys.argv:
        d = mock()
    else:
        token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        if not token:
            sys.exit("Set GH_TOKEN (or run with --mock)")
        d = fetch(login, token)
    os.makedirs(out, exist_ok=True)
    for name, svg in (("stats", stats_card(d)), ("langs", langs_card(d)), ("activity", activity_card(d))):
        with open(os.path.join(out, name + ".svg"), "w", encoding="utf-8") as f:
            f.write(svg)
    print(f"wrote stats.svg, langs.svg, activity.svg to {out}/")

if __name__ == "__main__":
    main()
