#!/usr/bin/env python3
"""Refresh this repository from the public Pastelki library (https://pastelki.club/api/library).

Only pictures that are approved and published on pastelki.club are listed by that API, always in their
current version, so this mirror never contains rejected pictures or older versions. The script:

  * downloads every published SVG into svg/<category>/<slug>.svg (and deletes files that are no longer
    published, e.g. a picture that was moved to another category or withdrawn),
  * checks each SVG (well-formed XML, <svg> root, viewBox 0 0 100 100, no scripts, no event handlers,
    no external references),
  * writes catalog.json and catalog.csv (names in 17 languages, category, tags, colour, version, links),
  * regenerates the gallery pages (gallery/<category>.md) and the gallery section of README.md.

Standard library only (Python 3.9+). No credentials needed: the API is public.

    python3 scripts/sync.py            # update the files
    python3 scripts/sync.py --check    # exit 1 if the repo differs from the live library (changes nothing)

Environment: PASTELKI_URL (default https://pastelki.club), PASTELKI_REPO (default tobob/pastelki-assets).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = os.environ.get("PASTELKI_URL", "https://pastelki.club").rstrip("/")
REPO = os.environ.get("PASTELKI_REPO", "tobob/pastelki-assets")
BRANCH = "main"
RAW = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}"
LANGS = ["pl", "en", "de", "fr", "es", "it", "pt", "nl", "uk", "cs", "sk", "sv", "ro", "hu", "tr", "ja", "zh"]
LICENSE = "MIT"
UA = "pastelki-assets-sync (+https://github.com/" + REPO + ")"
SVG_NS = "{http://www.w3.org/2000/svg}"
GALLERY_START, GALLERY_END = "<!-- gallery:start -->", "<!-- gallery:end -->"
README_PREVIEW = 8  # thumbnails per category in README.md


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as err:
            if err.code < 500 or attempt == 3:
                raise
        except urllib.error.URLError:
            if attempt == 3:
                raise
        time.sleep(2 ** attempt)
    raise AssertionError("unreachable")


# ── validation ──────────────────────────────────────────────────────────────────────────────────

SAFE_SLUG = re.compile(r"^[a-z0-9][a-z0-9-]{0,80}$")


def check_svg(slug: str, data: bytes) -> None:
    text = data.decode("utf-8")
    if re.search(r"<!DOCTYPE|<!ENTITY", text, re.I):
        raise ValueError(f"{slug}: DTD/entities are not allowed")
    root = ET.fromstring(data)
    if root.tag not in ("svg", SVG_NS + "svg"):
        raise ValueError(f"{slug}: root element is <{root.tag}>, expected <svg>")
    if " ".join((root.get("viewBox") or "").replace(",", " ").split()) != "0 0 100 100":
        raise ValueError(f"{slug}: viewBox is {root.get('viewBox')!r}, expected '0 0 100 100'")
    for el in root.iter():
        tag = el.tag.split("}")[-1].lower()
        if tag in ("script", "foreignobject", "iframe", "image", "embed", "object"):
            raise ValueError(f"{slug}: <{tag}> is not allowed")
        for name, value in el.attrib.items():
            attr = name.split("}")[-1].lower()
            if attr.startswith("on"):
                raise ValueError(f"{slug}: event handler {attr}")
            if attr == "href" and not value.startswith("#"):
                raise ValueError(f"{slug}: external reference {value!r}")
            if "url(" in value and re.search(r"url\(\s*['\"]?(?!#)", value):
                raise ValueError(f"{slug}: external url() in {attr}")


# ── generated files ─────────────────────────────────────────────────────────────────────────────

def load_categories() -> dict:
    return json.loads((ROOT / "data" / "categories.json").read_text("utf-8"))["categories"]


def build(library: dict) -> tuple[dict[str, bytes], dict[str, bytes]]:
    """→ (svg files by repo path, metadata files by repo path)."""
    cat_names = load_categories()
    items = library["items"]
    slugs = [it["slug"] for it in items]
    if len(slugs) != len(set(slugs)):
        raise ValueError("duplicate slugs in the library")
    for it in items:
        if not SAFE_SLUG.match(it["slug"]) or not SAFE_SLUG.match(it["category"]):
            raise ValueError(f"unexpected slug/category: {it['slug']!r} / {it['category']!r}")

    with ThreadPoolExecutor(8) as pool:
        blobs = list(pool.map(lambda it: fetch(BASE + it["svg_url"]), items))

    svgs: dict[str, bytes] = {}
    entries = []
    for it, data in zip(items, blobs):
        check_svg(it["slug"], data)
        path = f"svg/{it['category']}/{it['slug']}.svg"
        svgs[path] = data
        names = it.get("names") or {}
        title = {lang: names.get(lang) or (it["name"] if lang == "pl" else it.get("name_en") or it["name"])
                 for lang in LANGS}
        entries.append({
            "slug": it["slug"],
            "title": title,
            "category": it["category"],
            "tags_pl": it.get("tags") or [],
            "color": it.get("color") or "",
            "color_hex": it.get("color_hex") or "",
            "version": it["version"],
            "updated_at": it.get("updated_at") or "",
            "license": LICENSE,
            "file": path,
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "page_url": f"{BASE}/en/image/{it['slug']}",
            "raw_url": f"{RAW}/{path}",
            "site_svg_url": BASE + it["svg_url"],
            "site_png_url": BASE + it["png_url"] if it.get("png_url") else "",
        })
    entries.sort(key=lambda e: (e["category"], e["slug"]))

    order = [c["id"] for c in library["categories"]]
    counts = {c: sum(1 for e in entries if e["category"] == c) for c in order}
    for e in entries:
        if e["category"] not in counts:
            order.append(e["category"])
            counts[e["category"]] = sum(1 for x in entries if x["category"] == e["category"])
    pl_name = {c["id"]: c["name"] for c in library["categories"]}
    missing = [c for c in order if c not in cat_names and counts[c]]
    if missing:
        print(f"warning: no translations for categories {missing} — add them to data/categories.json", file=sys.stderr)
    categories = [{"id": c, "names": {lang: cat_names.get(c, {}).get(lang) or pl_name.get(c, c) for lang in LANGS},
                   "count": counts[c]} for c in order if counts[c]]

    catalog = {
        "name": "Pastelki",
        "description": "Gentle SVG pictures for children aged 2-6. Free, MIT-licensed.",
        "homepage": BASE,
        "source": f"{BASE}/api/library",
        "license": LICENSE,
        "copyright": "Copyright (c) 2026 Pastelki (pastelki.club)",
        "languages": LANGS,
        "count": len(entries),
        "categories": categories,
        "palette": library.get("palette", []),
        "items": entries,
    }
    meta: dict[str, bytes] = {
        "catalog.json": (json.dumps(catalog, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
        "catalog.csv": catalog_csv(entries),
    }
    by_cat = {c["id"]: [e for e in entries if e["category"] == c["id"]] for c in categories}
    for c in categories:
        meta[f"gallery/{c['id']}.md"] = gallery_page(c, by_cat[c["id"]]).encode("utf-8")
    meta["gallery/README.md"] = gallery_index(categories).encode("utf-8")
    meta["README.md"] = readme_with_gallery(categories, by_cat, len(entries)).encode("utf-8")
    return svgs, meta


def catalog_csv(entries: list[dict]) -> bytes:
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["slug", "category", *[f"title_{l}" for l in LANGS], "tags_pl", "color", "color_hex", "version",
                "updated_at", "license", "file", "page_url", "raw_url"])
    for e in entries:
        w.writerow([e["slug"], e["category"], *[e["title"][l] for l in LANGS], ";".join(e["tags_pl"]), e["color"],
                    e["color_hex"], e["version"], e["updated_at"], e["license"], e["file"], e["page_url"],
                    e["raw_url"]])
    return buf.getvalue().encode("utf-8")


def md(s: str) -> str:
    return s.replace("|", "\\|").replace("<", "&lt;").replace('"', "&quot;")


def cap(s: str) -> str:
    """Display form of a name: first letter upper-case (catalog.json keeps the names exactly as on the site)."""
    return s[:1].upper() + s[1:]


def gallery_page(cat: dict, entries: list[dict]) -> str:
    n = cat["names"]
    lines = [f"# {n['en']} · {n['pl']}", "",
             f"{len(entries)} pictures · [all categories](README.md) · [back to the repository](../README.md)", "",
             "<!-- generated by scripts/sync.py — do not edit by hand -->", "",
             "| | | | |", "|:-:|:-:|:-:|:-:|"]
    cells = [f'<a href="../{e["file"]}"><img src="../{e["file"]}" width="110" alt="{md(cap(e["title"]["en"]))}"></a>'
             f'<br>**{md(cap(e["title"]["en"]))}**<br>{md(cap(e["title"]["pl"]))}<br>'
             f'<sub>`{e["slug"]}` · v{e["version"]} · [raw]({e["raw_url"]}) · [site]({e["page_url"]})</sub>'
             for e in entries]
    for i in range(0, len(cells), 4):
        row = cells[i:i + 4] + [""] * (4 - len(cells[i:i + 4]))
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines) + "\n"


def gallery_index(categories: list[dict]) -> str:
    lines = ["# Gallery", "", "<!-- generated by scripts/sync.py — do not edit by hand -->", "",
             "| Category | | Pictures |", "|---|---|--:|"]
    for c in categories:
        lines.append(f"| [{md(c['names']['en'])}]({c['id']}.md) | {md(c['names']['pl'])} | {c['count']} |")
    return "\n".join(lines) + "\n"


def readme_with_gallery(categories: list[dict], by_cat: dict, total: int) -> str:
    readme = (ROOT / "README.md").read_text("utf-8")
    if GALLERY_START not in readme or GALLERY_END not in readme:
        raise ValueError("README.md has no gallery markers")
    parts = [GALLERY_START, "", f"**{total} pictures in {len(categories)} categories.** "
             "Click a category for every picture with its name and download links.", ""]
    for c in categories:
        thumbs = " ".join(f'<img src="{e["file"]}" width="64" alt="{md(cap(e["title"]["en"]))}">'
                          for e in by_cat[c["id"]][:README_PREVIEW])
        parts += [f"**[{md(c['names']['en'])}](gallery/{c['id']}.md)** · {md(c['names']['pl'])} · {c['count']}", "",
                  thumbs, ""]
    parts.append(GALLERY_END)
    head, rest = readme.split(GALLERY_START, 1)
    tail = rest.split(GALLERY_END, 1)[1]
    return head + "\n".join(parts) + tail


# ── main ────────────────────────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--check", action="store_true", help="only report differences; exit 1 if any")
    args = ap.parse_args()

    library = json.loads(fetch(f"{BASE}/api/library"))
    svgs, meta = build(library)
    wanted = {**svgs, **meta}

    existing_svgs = {p.relative_to(ROOT).as_posix() for p in (ROOT / "svg").rglob("*.svg")} if (ROOT / "svg").exists() else set()
    existing_gallery = {p.relative_to(ROOT).as_posix() for p in (ROOT / "gallery").glob("*.md")} if (ROOT / "gallery").exists() else set()
    added = sorted(p for p in svgs if p not in existing_svgs)
    removed = sorted((existing_svgs | existing_gallery) - set(wanted))
    changed = sorted(p for p, data in wanted.items()
                     if p not in added and (not (ROOT / p).exists() or (ROOT / p).read_bytes() != data))
    changed_svgs = [p for p in changed if p.startswith("svg/")]

    summary = (f"{len(svgs)} pictures: {len(added)} new, {len(changed_svgs)} updated, "
               f"{len([p for p in removed if p.startswith('svg/')])} removed")
    print(summary)
    for label, paths in (("new", added), ("updated", changed), ("removed", removed)):
        for p in paths:
            print(f"  {label}: {p}")

    if args.check:
        return 1 if (added or changed or removed) else 0

    for p, data in wanted.items():
        target = ROOT / p
        if not target.exists() or target.read_bytes() != data:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    for p in removed:
        (ROOT / p).unlink()
    for d in sorted((ROOT / "svg").glob("*"), reverse=True):
        if d.is_dir() and not any(d.iterdir()):
            d.rmdir()
    return 0


if __name__ == "__main__":
    sys.exit(main())
