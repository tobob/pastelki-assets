# Contributing

Thank you for wanting to help!

## Pictures are curated on pastelki.club

Every picture is drawn, checked and approved on [pastelki.club](https://pastelki.club/?utm_source=github&utm_medium=contributing&utm_campaign=pastelki-assets) before it is published, and
this repository is an automatic copy of what is published there. **Please don't open pull requests that add or change
SVG files** — the next sync would overwrite them.

- **A picture has a mistake** (wrong detail, odd shape, something that could scare a small child) → tell us at
  [pastelki.club/en/feedback](https://pastelki.club/en/feedback?app=other&utm_source=github&utm_medium=contributing&utm_campaign=pastelki-assets) or open an issue with the slug
  (e.g. `svg/zwierzeta/cat.svg`). The fix is made on the site and arrives here with the next sync.
- **You'd like a new picture** → same place: describe what it should show and for which age.

Everything we publish follows the Pastelki manifest (gentle, nothing scary, loud or flashing; made for children 2–6):
[pastelki.club/en/about#manifest](https://pastelki.club/en/about?utm_source=github&utm_medium=contributing&utm_campaign=pastelki-assets#manifest).

## Pull requests welcome for

- **Translations** of category names in [`data/categories.json`](data/categories.json).
- **Picture names** in any of the 17 languages — `catalog.json` is generated, so open an issue or a PR that lists the
  corrections (slug, language, better name); we apply them on pastelki.club.
- **Scripts and documentation**: `scripts/sync.py`, `scripts/render-png.mjs`, the README.

## Working on the scripts

```bash
python3 scripts/sync.py --check   # does the repo match the live library?
python3 scripts/sync.py           # refresh svg/, catalog.*, gallery/ and the README gallery
npm install && npm run validate   # render every SVG once (must pass)
```

`catalog.json`, `catalog.csv`, `gallery/` and the part of `README.md` between the `gallery` markers are generated —
edit `scripts/sync.py` instead.

By contributing you agree that your contribution is released under the [MIT license](LICENSE) of this repository.
