#!/usr/bin/env python3
"""
Generator Kartu Statistik GitHub myzert (v2 Perfect Contrast & Dual-Theme).
- Mendukung GitHub Light Mode (#gh-light-mode-only) dan Dark Mode (#gh-dark-mode-only).
- Karakter intip (peek) sudah dihapus sesuai permintaan.
- Statistik di mode terang dan gelap terlihat sangat jelas dengan kontras tinggi.
- Aset Anime PNG HD Transparan & Tajam (Tanpa box kaku, tanpa white halo).
- Ikon Vektor Octicons Resmi (Repo, Star, Commit, Fork, Followers, Following).
- README.md Ultra-Clean: Hanya menampilkan kartu statistik ini sebagai satu-satunya gambar.
"""
import base64
import json
import os
import random
import urllib.request
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
USER = os.getenv("GH_USER", "myzert")
TOKEN = os.getenv("GITHUB_TOKEN", "")

# Fallback Zona Waktu (WIB / UTC+7)
try:
    from zoneinfo import ZoneInfo
    TZ = ZoneInfo(os.getenv("TZ_NAME", "Asia/Jakarta"))
except Exception:
    from datetime import timezone, timedelta as dt_timedelta
    TZ = timezone(dt_timedelta(hours=7))

DEMO = os.getenv("DEMO") == "1"

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"

LANG_COLORS = {
    "JavaScript": "#f1e05a",
    "Python": "#3572A5",
    "Rust": "#dea584",
    "Java": "#b07219",
    "TypeScript": "#3178c6",
    "C++": "#f34b7d",
    "C#": "#178600",
    "C": "#555555",
    "Go": "#00ADD8",
    "PHP": "#4F5D95",
    "Ruby": "#701516",
    "Kotlin": "#A97BFF",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
    "Shell": "#89e051"
}

# Rotasi pose anime (Karakter 'peek' / intip SUDAH DIHAPUS TOTAL)
DAY_ROSTER = {
    0: [("cry", "Senin... kuat ya, semangat!"), ("run", "Senin gaspol ngoding!")],
    1: [("run", "Selasa produktif & fokus!"), ("shy", "Selasa santai tapi beres~")],
    2: [("shy", "Rabu santai tapi tuntas!"), ("kiss", "Rabu manis, keep coding!")],
    3: [("kiss", "Kamis push fitur keren!"), ("shy", "Kamis tenang & optimasi~")],
    4: [("kiss", "Jumat berkah, otw weekend!"), ("run", "Jumat deploy santuy~")],
    5: [("sleep", "Sabtu recharge & nonton anime."), ("kiss", "Sabtu santai bareng waifu!")],
    6: [("shy", "Minggu me-time & ngoding santai."), ("sleep", "Minggu istirahat cukup ya.")]
}

# Vektor Ikon Asli Developer (GitHub Octicons 16x16)
ICONS = {
    "repo": '<path fill-rule="evenodd" d="M3 1.75A1.75 1.75 0 0 1 4.75 0h7.5A1.75 1.75 0 0 1 14 1.75v12.5A1.75 1.75 0 0 1 12.25 16h-7.5A1.75 1.75 0 0 1 3 14.25Zm1.75-.25a.25.25 0 0 0-.25.25v12.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25V1.75a.25.25 0 0 0-.25-.25Z"/>',
    "star": '<path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.75.75 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z"/>',
    "commit": '<path fill-rule="evenodd" d="M10.5 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0Zm1.45 0a3.998 3.998 0 0 0-7.9 0H.75a.75.75 0 0 0 0 1.5h3.3a3.998 3.998 0 0 0 7.9 0h3.3a.75.75 0 0 0 0-1.5h-3.3Z"/>',
    "followers": '<path d="M2 5.5a3 3 0 1 1 6 0 3 3 0 0 1-6 0Zm7 0a2 2 0 1 1 4 0 2 2 0 0 1-4 0Zm-7 8c0-1.87 2.13-3 5-3s5 1.13 5 3v.75H2v-.75Zm9.5-.75v.75H14v-.75c0-1.28-1.07-2.19-2.73-2.54.46.68.73 1.51.73 2.54Z"/>',
    "fork": '<path fill-rule="evenodd" d="M5 3.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm0 2.122a2.25 2.25 0 1 0-1.5 0v.878A2.25 2.25 0 0 0 5.75 8.5h4.5A2.25 2.25 0 0 0 12.5 6.25v-.878a2.25 2.25 0 1 0-1.5 0v.878a.75.75 0 0 1-.75.75h-4.5A.75.75 0 0 1 5 6.25v-.878Zm7.5-2.122a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM8.75 12.75a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm.75-2.122a2.25 2.25 0 1 0-1.5 0V8.5h1.5v2.128Z"/>',
    "following": '<path fill-rule="evenodd" d="M8 1.5a6.5 6.5 0 1 0 0 13 6.5 6.5 0 0 0 0-13ZM0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8Zm11.78-1.72a.75.75 0 0 0-1.06-1.06L7.25 8.69 5.28 6.72a.75.75 0 0 0-1.06 1.06l2.5 2.5a.75.75 0 0 0 1.06 0l4-4Z"/>'
}


# ---------------------------------------------------------------- Data Fetching
def api(path):
    req = urllib.request.Request(
        "https://api.github.com" + path,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-stats-v2"}
    )
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def fmt_num(n):
    if not isinstance(n, int):
        return str(n)
    if n >= 10000:
        return f"{n/1000:.1f}k"
    return f"{n:,}".replace(",", ".")


def get_stats(now):
    s = {
        "repos": 0, "stars": 0, "commits": 0, "followers": 0,
        "forks": 0, "following": 0, "langs": [], "activity": [0] * 30
    }
    if DEMO:
        rnd = random.Random(7)
        s.update(
            repos=12, stars=13, commits=149, followers=10, forks=1, following=20,
            langs=[("JavaScript", 30), ("Python", 20), ("Rust", 10), ("Java", 10)],
            activity=[rnd.randint(0, 5) for _ in range(30)]
        )
        return s

    try:
        u = api(f"/users/{USER}")
        s["repos"] = u.get("public_repos", 0)
        s["followers"] = u.get("followers", 0)
        s["following"] = u.get("following", 0)

        repos = api(f"/users/{USER}/repos?per_page=100&type=owner")
        s["stars"] = sum(r.get("stargazers_count", 0) for r in repos)
        s["forks"] = sum(r.get("forks_count", 0) for r in repos)

        c = Counter(r["language"] for r in repos if r.get("language") and not r.get("fork"))
        tot = sum(c.values()) or 1
        s["langs"] = [(k, round(v * 100 / tot)) for k, v in c.most_common(4)]
    except Exception as e:
        print("Gagal fetch repos/user:", e)

    try:
        s["commits"] = api(f"/search/commits?q=author:{USER}&per_page=1").get("total_count", 0)
    except Exception as e:
        print("Gagal fetch commits:", e)

    try:
        today = now.date()
        counts = Counter()
        for page in (1, 2):
            events = api(f"/users/{USER}/events/public?per_page=100&page={page}")
            for ev in events:
                d = datetime.fromisoformat(ev["created_at"].replace("Z", "+00:00")).astimezone(TZ).date()
                counts[d] += 1
        s["activity"] = [counts.get(today - timedelta(days=29 - i), 0) for i in range(30)]
    except Exception as e:
        print("Gagal fetch aktivitas:", e)

    return s


# ---------------------------------------------------------------- SVG Generation
def get_image_b64(name):
    # Hindari 'peek'
    if name == "peek":
        name = "shy"

    png_path = ASSETS / f"{name}.png"
    if png_path.exists():
        return "data:image/png;base64," + base64.b64encode(png_path.read_bytes()).decode()
    
    jpg_path = ASSETS / f"{name}.jpg"
    if jpg_path.exists():
        return "data:image/jpeg;base64," + base64.b64encode(jpg_path.read_bytes()).decode()
    return ""


def build_activity_chart(values, x, y, w, h, accent_col):
    mx = max(max(values), 1)
    n = len(values)
    pts = [(x + i * w / (n - 1), y + h - (v / mx) * h) for i, v in enumerate(values)]

    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        cx = (x0 + x1) / 2
        d += f" C{cx:.1f},{y0:.1f} {cx:.1f},{y1:.1f} {x1:.1f},{y1:.1f}"

    area = d + f" L{x+w:.1f},{y+h} L{x},{y+h} Z"
    last = pts[-1]

    return f"""
<path class="area" d="{area}" fill="url(#actArea)"/>
<path class="chartLine" pathLength="1" d="{d}" fill="none" stroke="{accent_col}" stroke-width="2.5" stroke-linecap="round"/>
<circle class="pop" cx="{last[0]:.1f}" cy="{last[1]:.1f}" r="4" fill="{accent_col}"/>
<circle class="ping" cx="{last[0]:.1f}" cy="{last[1]:.1f}" r="4" fill="none" stroke="{accent_col}" stroke-width="2"/>"""


def generate_svg(now, s, char_name, quote, mode="dark"):
    W, H = 920, 395
    img_b64 = get_image_b64(char_name)

    # Warna spesifik tema (jaminan 100% kontras tajam)
    if mode == "light":
        bg_card = "#ffffff"
        border_card = "#d0d7de"
        title_col = "#1f2328"
        sub_col = "#57606a"
        sec_col = "#24292f"
        stat_bg = "#f6f8fa"
        stat_border = "#d0d7de"
        stat_val_col = "#1f2328"
        stat_lbl_col = "#57606a"
        icon_col = "#d9363e"
        lang_text_col = "#57606a"
        lang_pct_col = "#1f2328"
        bar_bg = "#eaeef2"
        accent = "#d9363e"
        footer_col = "#8c959f"
        badge_bg = "rgba(255, 255, 255, 0.95)"
        badge_border = "#d0d7de"
        badge_text = "#d9363e"
        act_op = "0.22"
    else:
        bg_card = "#0d1117"
        border_card = "#30363d"
        title_col = "#f0f6fc"
        sub_col = "#8b949e"
        sec_col = "#f0f6fc"
        stat_bg = "#161b22"
        stat_border = "#21262d"
        stat_val_col = "#f0f6fc"
        stat_lbl_col = "#8b949e"
        icon_col = "#ff5376"
        lang_text_col = "#8b949e"
        lang_pct_col = "#f0f6fc"
        bar_bg = "#21262d"
        accent = "#ff5376"
        footer_col = "#484f58"
        badge_bg = "rgba(22, 27, 34, 0.90)"
        badge_border = "#30363d"
        badge_text = "#ff5376"
        act_op = "0.32"

    stat_cards = [
        ("Repositori", fmt_num(s["repos"]), "repo"),
        ("Total Star", fmt_num(s["stars"]), "star"),
        ("Total Commit", fmt_num(s["commits"]), "commit"),
        ("Followers", fmt_num(s["followers"]), "followers"),
        ("Fork", fmt_num(s["forks"]), "fork"),
        ("Following", fmt_num(s["following"]), "following"),
    ]

    elements = []

    # 1. Header Profil & Status Subtitle
    elements.append(f"""
<g class="slide" style="animation-delay:0.1s">
  <text x="35" y="48" font-size="24" font-weight="800" fill="{title_col}">Statistik GitHub</text>
  <text x="35" y="70" font-size="13" font-weight="500" fill="{sub_col}">@{escape(USER)} &#183; Backend Developer &amp; Otaku &#183; {escape(quote)}</text>
</g>""")

    # 2. Grid Kartu Statistik Berkontras Tinggi dengan Vektor Ikon
    for i, (label, val, icon_key) in enumerate(stat_cards):
        col, row = i % 3, i // 3
        cx = 35 + col * 188
        cy = 90 + row * 68
        delay = 0.25 + i * 0.08
        icon_path = ICONS[icon_key]
        elements.append(f"""
<g class="slide" style="animation-delay:{delay:.2f}s">
  <rect x="{cx}" y="{cy}" width="176" height="58" rx="10" fill="{stat_bg}" stroke="{stat_border}" stroke-width="1"/>
  <text x="{cx+14}" y="{cy+28}" font-size="20" font-weight="800" fill="{stat_val_col}">{escape(val)}</text>
  <g transform="translate({cx+14}, {cy+35})">
    <svg width="13" height="13" viewBox="0 0 16 16" fill="{icon_col}">{icon_path}</svg>
  </g>
  <text x="{cx+32}" y="{cy+46}" font-size="11" font-weight="500" fill="{stat_lbl_col}">{escape(label)}</text>
</g>""")

    # 3. Bahasa Teratas
    elements.append(f"""
<g class="slide" style="animation-delay:0.75s">
  <text x="35" y="246" font-size="13" font-weight="700" fill="{sec_col}">Bahasa Teratas</text>
</g>""")

    for i, (lang, pct) in enumerate(s["langs"][:4]):
        lx = 35 + i * 144
        bar_w = max(4, min(pct, 100)) * 1.25
        col = LANG_COLORS.get(lang, accent)
        elements.append(f"""
<g class="slide" style="animation-delay:{0.85 + i*0.1:.2f}s">
  <circle cx="{lx+5}" cy="265" r="4" fill="{col}"/>
  <text x="{lx+14}" y="269" font-size="12" fill="{lang_text_col}">{escape(lang)} <tspan font-weight="700" fill="{lang_pct_col}">{pct}%</tspan></text>
  <rect x="{lx}" y="277" width="128" height="6" rx="3" fill="{bar_bg}"/>
  <rect class="bar" x="{lx}" y="277" width="{bar_w:.0f}" height="6" rx="3" fill="{col}" style="animation-delay:{0.95 + i*0.12:.2f}s"/>
</g>""")

    if not s["langs"]:
        elements.append(f'<text x="35" y="270" font-size="12" fill="{sub_col}">-</text>')

    # 4. Grafik Aktivitas 30 Hari
    total_events = sum(s["activity"])
    elements.append(f"""
<g class="slide" style="animation-delay:1.25s">
  <text x="35" y="318" font-size="13" font-weight="700" fill="{sec_col}">Aktivitas 30 Hari <tspan font-weight="400" fill="{sub_col}">({total_events} event)</tspan></text>
</g>""")
    elements.append(build_activity_chart(s["activity"], 35, 330, 560, 30, accent))

    # Timestamp
    elements.append(f"""
<text x="35" y="380" font-size="10" fill="{footer_col}">Diperbarui {now:%d-%m-%Y %H:%M} WIB &#183; Auto-update tiap jam</text>""")

    # 5. Efek Sparkles Anime
    sparkles = []
    sp_coords = [(635, 55, 8, 0), (895, 75, 7, 0.6), (620, 345, 6, 1.2), (890, 335, 8, 0.4), (615, 200, 5, 1.8)]
    for sx, sy, sr, sd in sp_coords:
        sparkles.append(
            f'<path class="tw" d="M0,-{sr} Q0,0 {sr},0 Q0,0 0,{sr} Q0,0 -{sr},0 Q0,0 0,-{sr}Z" fill="{accent}" '
            f'transform="translate({sx},{sy})" style="animation-delay:{sd}s"/>'
        )
    sparkles_svg = "\n".join(sparkles)

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
  text {{ font-family: {FONT}; }}
  .slide {{ opacity:0; animation: slide .7s cubic-bezier(.2,.8,.2,1) forwards; }}
  .chartLine {{ stroke-dasharray: 1; stroke-dashoffset: 1; animation: draw 1.6s ease 1.3s forwards; }}
  .area {{ opacity: 0; animation: fade 1.2s ease 2.1s forwards; }}
  .bar {{ transform-box: fill-box; transform-origin: left; transform: scaleX(0); animation: grow 1s cubic-bezier(.2,.8,.2,1) forwards; }}
  .pop {{ opacity: 0; animation: fade .4s ease 2.9s forwards; }}
  .ping {{ transform-box: fill-box; transform-origin: center; opacity: 0; animation: ping 2.2s ease-out 2.9s infinite; }}
  .float {{ animation: float 4s ease-in-out infinite; }}
  .tw {{ transform-box: fill-box; transform-origin: center; animation: tw 2.4s ease-in-out infinite; }}

  @keyframes slide {{ from {{ opacity:0; transform:translateX(-18px); }} to {{ opacity:1; transform:none; }} }}
  @keyframes draw {{ to {{ stroke-dashoffset:0; }} }}
  @keyframes grow {{ to {{ transform:scaleX(1); }} }}
  @keyframes fade {{ to {{ opacity:1; }} }}
  @keyframes ping {{ 0% {{ opacity:.75; transform:scale(1); }} 100% {{ opacity:0; transform:scale(3.2); }} }}
  @keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-7px); }} }}
  @keyframes tw {{ 0%, 100% {{ opacity:.2; transform:scale(.6) rotate(0); }} 50% {{ opacity:1; transform:scale(1.15) rotate(25deg); }} }}

  @media (prefers-reduced-motion: reduce) {{
    * {{ animation: none !important; opacity: 1 !important; transform: none !important; stroke-dashoffset: 0 !important; }}
  }}
</style>
<defs>
  <linearGradient id="actArea" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{accent}" stop-opacity="{act_op}"/>
    <stop offset="100%" stop-color="{accent}" stop-opacity="0.0"/>
  </linearGradient>
</defs>

<!-- Card Canvas: Warna disesuaikan dengan kontras tajam sempurna -->
<rect width="{W}" height="{H}" rx="18" fill="{bg_card}" stroke="{border_card}" stroke-width="1"/>

<!-- Left & Center Stats Content -->
{"".join(elements)}

<!-- Right Anime Character: Pure HD Sharp Transparent PNG, NO Box / Kotak -->
<g class="float">
  <image href="{img_b64}" x="635" y="16" width="265" height="360" preserveAspectRatio="xMidYMid meet"/>
  <!-- Floating Mood Badge -->
  <g transform="translate(645, 342)">
    <rect width="245" height="26" rx="8" fill="{badge_bg}" stroke="{badge_border}" stroke-width="1"/>
    <text x="122" y="17" text-anchor="middle" font-size="11" font-weight="700" fill="{badge_text}">🌸 {escape(quote)}</text>
  </g>
</g>

<!-- Anime Twinkles -->
{sparkles_svg}
</svg>"""
    return svg_content


# ---------------------------------------------------------------- Clean Minimalist README
def generate_readme(now, quote):
    return f"""<div align="center">

  <!-- Statistik GitHub Otomatis Mode Terang & Gelap (Satu-satunya gambar di profil) -->
  <a href="https://github.com/{USER}">
    <img src="assets/stats.svg#gh-dark-mode-only" alt="Statistik GitHub {USER}" width="100%"/>
    <img src="assets/stats-light.svg#gh-light-mode-only" alt="Statistik GitHub {USER}" width="100%"/>
  </a>

  <br>

  <h1>🌸 Zert (myzert)</h1>
  <p><b>Backend Developer &amp; Otaku Enthusiast</b></p>
  <p><i>"はじめまして、私はZertです。バックエンド開発者です。よろしくお願いします。"</i></p>

  <br>

  <p>
    <a href="https://github.com/{USER}">GitHub</a> &bull;
    <a href="https://discord.com/users/1390407633642717305">Discord</a> &bull;
    <a href="mailto:zerttcihuy@gmail.com">Email</a> &bull;
    <a href="https://open.spotify.com/track/4IlGjYs0OWzKSSvSIVonbv?si=Q9n2moViRMS_NJh8vJ7-cA">Spotify</a>
  </p>

  <br>
  <sub><i>Auto-update tiap jam via GitHub Actions &middot; {now:%d-%m-%Y %H:%M} WIB</i></sub>

</div>
"""


def main():
    now = datetime.now(TZ)
    ASSETS.mkdir(exist_ok=True)

    override_char = os.getenv("IMAGE_NAME")
    if override_char and override_char != "peek":
        char_name = override_char
        quote = f"Mood: {char_name.title()}!"
    else:
        day_idx = now.weekday()
        # Roster tanpa karakter peek
        pool = DAY_ROSTER.get(day_idx, [("shy", "Semangat ngoding!")])
        rnd = random.Random(now.strftime("%Y%m%d%H"))
        char_name, quote = rnd.choice(pool)

    stats = get_stats(now)

    # Generate kedua mode agar kontras tajam 100% di mode terang dan gelap
    svg_dark = generate_svg(now, stats, char_name, quote, mode="dark")
    svg_light = generate_svg(now, stats, char_name, quote, mode="light")

    (ASSETS / "stats.svg").write_text(svg_dark, encoding="utf-8")
    (ASSETS / "stats-dark.svg").write_text(svg_dark, encoding="utf-8")
    (ASSETS / "stats-light.svg").write_text(svg_light, encoding="utf-8")
    (ROOT / "README.md").write_text(generate_readme(now, quote), encoding="utf-8")

    print(f"OK {now:%F %H:%M} [v2 Dual-Theme Contrast] char={char_name} quote='{quote}' repos={stats['repos']} stars={stats['stars']}")


if __name__ == "__main__":
    main()
