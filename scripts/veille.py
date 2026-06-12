#!/usr/bin/env python3
"""
veille.py — Daily RSS monitoring for FIFA 2026 Watch
-----------------------------------------------------
Reads a list of RSS feeds, filters items from the last 24h that match
FIFA 2026 keywords, and writes a dated candidates file for human review.

Does NOT publish anything. The editor reviews candidates and decides.

Usage:
    python scripts/veille.py
    python scripts/veille.py --days 2        # widen window to 48h
    python scripts/veille.py --out ./drafts  # custom output folder
"""

import argparse
import datetime as dt
import html
import re
import sys
import urllib.request
import urllib.error
from email.utils import parsedate_to_datetime
from pathlib import Path
from xml.etree import ElementTree as ET

# ─────────────────────────────────────────────────────────────
# CONFIG — edit these two lists freely
# ─────────────────────────────────────────────────────────────

FEEDS = [
    # label, RSS url
    ("The Guardian — Football", "https://www.theguardian.com/football/rss"),
    ("The Guardian — World",    "https://www.theguardian.com/world/rss"),
    ("Al Jazeera",              "https://www.aljazeera.com/xml/rss/all.xml"),
    ("BBC Sport — Football",    "https://feeds.bbci.co.uk/sport/football/rss.xml"),
    ("NPR — Sports",            "https://feeds.npr.org/1055/rss.xml"),
    ("France 24 — Sport (EN)",  "https://www.france24.com/en/sport/rss"),
    ("Le Monde — Sport",        "https://www.lemonde.fr/sport/rss_full.xml"),
    ("RFI — Sports",            "https://www.rfi.fr/fr/sports/rss"),
    # Add more freely. Most outlets expose /rss or /feed per section.
]

# An item must contain at least one CORE term AND one CONTEXT term.
CORE_TERMS = [
    "world cup 2026", "fifa 2026", "2026 world cup", "coupe du monde 2026",
    "mondial 2026", "fifa world cup",
]

CONTEXT_TERMS = [
    # English
    "scandal", "controversy", "corruption", "visa", "denied entry", "deport",
    "human rights", "evict", "fraud", "ticket", "heat", "boycott", "protest",
    "discriminat", "detain", "ban", "lawsuit", "subpoena", "referee",
    # French
    "scandale", "polémique", "corruption", "visa", "refus", "expuls",
    "droits", "fraude", "billet", "chaleur", "boycott", "discrimination",
    "enquête", "plainte", "arbitre", "fouille",
]

# ─────────────────────────────────────────────────────────────


def fetch(url: str, timeout: int = 20) -> str | None:
    req = urllib.request.Request(url, headers={"User-Agent": "fifa26watch-veille/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        print(f"  ⚠ skip {url} — {e}", file=sys.stderr)
        return None


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text or "")
    return html.unescape(text).strip()


def parse_date(raw: str):
    if not raw:
        return None
    try:
        return parsedate_to_datetime(raw)
    except (TypeError, ValueError):
        # Try ISO 8601 (Atom feeds)
        try:
            return dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except ValueError:
            return None


def parse_feed(xml_text: str):
    """Yield dicts for both RSS <item> and Atom <entry>."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return

    ns = {"atom": "http://www.w3.org/2005/Atom"}

    # RSS
    for item in root.iter("item"):
        title = item.findtext("title", "")
        link = item.findtext("link", "")
        desc = item.findtext("description", "")
        pub = item.findtext("pubDate", "")
        yield {"title": title, "link": link, "summary": desc, "date": parse_date(pub)}

    # Atom
    for entry in root.iter("{http://www.w3.org/2005/Atom}entry"):
        title = entry.findtext("{http://www.w3.org/2005/Atom}title", "")
        link_el = entry.find("{http://www.w3.org/2005/Atom}link")
        link = link_el.get("href") if link_el is not None else ""
        summary = entry.findtext("{http://www.w3.org/2005/Atom}summary", "") or \
                  entry.findtext("{http://www.w3.org/2005/Atom}content", "")
        updated = entry.findtext("{http://www.w3.org/2005/Atom}updated", "") or \
                  entry.findtext("{http://www.w3.org/2005/Atom}published", "")
        yield {"title": title, "link": link, "summary": summary, "date": parse_date(updated)}


def matches(text: str) -> bool:
    low = text.lower()
    has_core = any(term in low for term in CORE_TERMS)
    has_ctx = any(term in low for term in CONTEXT_TERMS)
    return has_core and has_ctx


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=1, help="look-back window in days")
    ap.add_argument("--out", default="drafts", help="output folder")
    args = ap.parse_args()

    now = dt.datetime.now(dt.timezone.utc)
    cutoff = now - dt.timedelta(days=args.days)

    candidates = []
    seen_links = set()

    print(f"🔎 Scanning {len(FEEDS)} feeds (last {args.days}d)…", file=sys.stderr)
    for label, url in FEEDS:
        xml = fetch(url)
        if not xml:
            continue
        for item in parse_feed(xml):
            link = (item["link"] or "").strip()
            if not link or link in seen_links:
                continue
            title = strip_html(item["title"])
            summary = strip_html(item["summary"])[:300]
            blob = f"{title} {summary}"

            if not matches(blob):
                continue

            # Date filter (keep undated items — better to over-include for review)
            d = item["date"]
            if d is not None and d < cutoff:
                continue

            seen_links.add(link)
            candidates.append({
                "source": label,
                "title": title,
                "link": link,
                "summary": summary,
                "date": d.strftime("%Y-%m-%d %H:%M") if d else "n/a",
            })

    # Sort newest first (undated last)
    candidates.sort(key=lambda c: c["date"], reverse=True)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    today = now.strftime("%Y-%m-%d")
    out_file = out_dir / f"candidats-{today}.md"

    lines = [
        f"# Candidats veille — {today}",
        "",
        f"_{len(candidates)} article(s) correspondant aux critères FIFA 2026 sur les dernières {args.days*24}h._",
        "",
        "> ⚠️ Liste brute non vérifiée. Vérifier la source primaire avant toute publication.",
        "> Garder uniquement les articles journalistiques sérieux et directement liés à FIFA 2026.",
        "",
        "---",
        "",
    ]

    if not candidates:
        lines.append("_Aucun candidat aujourd'hui. Rien à signaler._")
    else:
        for i, c in enumerate(candidates, 1):
            lines += [
                f"## {i}. {c['title']}",
                "",
                f"- **Source :** {c['source']}",
                f"- **Date :** {c['date']}",
                f"- **Lien :** {c['link']}",
                f"- **Extrait :** {c['summary']}",
                "",
                "- [ ] Pertinent — à transformer en JSON",
                "- [ ] Doublon d'un scandale existant",
                "- [ ] Écarté (hors sujet / source insuffisante)",
                "",
                "---",
                "",
            ]

    out_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ {len(candidates)} candidat(s) → {out_file}", file=sys.stderr)

    # Print to stdout too (useful for CI logs / quick read)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
