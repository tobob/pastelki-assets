# Pastelki — free SVG pictures for little kids

**[pastelki.club](https://pastelki.club)** is a library of gentle, colourful SVG illustrations for children aged 2–6:
animals, food, vehicles, toys, the sea, space, feelings and more. Every picture is free for personal and commercial
use under the MIT license — for picture books, worksheets, colouring pages, apps, games and videos.

This repository is the downloadable copy of the whole library: every **approved, current** picture from pastelki.club
as an SVG file, plus a catalog with names in 17 languages. It is refreshed automatically from the site.

- Simple shapes, thick soft outlines, a calm pastel palette — nothing scary, loud or busy.
- Every picture is a square `viewBox="0 0 100 100"`: scale it to any size without losing quality.
- Small, clean SVG (no scripts, no external references, no embedded images) — a few kilobytes each.
- Moving parts carry stable ids (`pk-head`, `pk-eye-l`, `pk-leg-r`, `pk-tail`, …) so you can animate them.

## Download

| How | |
|---|---|
| **Everything as a ZIP** | Green **Code → Download ZIP** button on GitHub, or [download the ZIP from pastelki.club](https://pastelki.club/api/download/pastelki.zip) (SVGs only, same files) |
| **With git** | `git clone https://github.com/tobob/pastelki-assets.git` — then `git pull` for new pictures |
| **One picture** | Open it in the [gallery](gallery/README.md) and click *raw*, or use a link like `https://raw.githubusercontent.com/tobob/pastelki-assets/main/svg/zwierzeta/cat.svg` |
| **From a CDN** | `https://cdn.jsdelivr.net/gh/tobob/pastelki-assets@main/svg/<category>/<slug>.svg` |
| **On the website** | Browse, search, recolour and download single SVG/PNG files at [pastelki.club](https://pastelki.club) |

### What's inside

```
svg/<category>/<slug>.svg   the pictures (current approved version only)
catalog.json                every picture: names in 17 languages, category, tags, colour, version, links, sha256
catalog.csv                 the same as a spreadsheet
data/categories.json        category names in 17 languages
gallery/                    preview pages, one per category
scripts/sync.py             refreshes the repository from the public pastelki.club API
scripts/render-png.mjs      renders PNGs at any size
```

Languages in the catalog: `pl en de fr es it pt nl uk cs sk sv ro hu tr ja zh`. Tags (`tags_pl`) are in Polish.

<details>
<summary>An entry in <code>catalog.json</code></summary>

```json
{
  "slug": "buzka-psa",
  "title": { "pl": "buźka psa", "en": "Dog face", "de": "Hundegesicht", "…": "…" },
  "category": "buzki",
  "tags_pl": ["pies", "buźka", "zwierzę", "szczeniak", "oklapnięte uszy"],
  "color": "brown",
  "color_hex": "#9A6B4A",
  "version": 1,
  "updated_at": "2026-11-20T09:10:31.149740",
  "license": "MIT",
  "file": "svg/buzki/buzka-psa.svg",
  "bytes": 2187,
  "sha256": "…",
  "page_url": "https://pastelki.club/en/image/buzka-psa",
  "raw_url": "https://raw.githubusercontent.com/tobob/pastelki-assets/main/svg/buzki/buzka-psa.svg",
  "site_svg_url": "https://pastelki.club/files/buzka-psa/buzka-psa-v1.svg",
  "site_png_url": "https://pastelki.club/files/buzka-psa/buzka-psa-v1.png"
}
```

`version` grows when a picture is redrawn; the repository always holds the newest approved version.
`site_png_url` is a ready 512 × 512 PNG on pastelki.club.
</details>

## Using the pictures

- **Apps and websites:** use the SVG directly (`<img src="cat.svg">`, `react-native-svg`, Android Vector Drawable
  import, Flutter `flutter_svg`, …). Read `catalog.json` to show the names in the child's language.
- **Print:** SVG is vector — it stays sharp at any size. Open it in Inkscape, Illustrator, Affinity, Figma, Canva or a
  browser and print, or render a large PNG (below).
- **Colouring pages:** the outlines are thick and closed. Remove the `fill` colours (or set them to white) in any
  vector editor, or use the colouring app [Kolorowanki](https://github.com/tobob/kolorowanki), which is built on these pictures.
- **Animation:** groups such as `pk-head`, `pk-arm-l`, `pk-leg-r`, `pk-tail` pivot naturally; `pk-shine-*` and
  `pk-shade-*` mark highlights and shading.
- **Recolouring and editing:** pastelki.club has an editor in the browser (open a picture → *Edit*).

### PNG files

PNGs are not stored in the repository (it stays small and diffs stay readable), but they are easy to make:

```bash
npm install
npm run png                  # png/512/<category>/<slug>.png
npm run png -- 256 1024      # several sizes
npm run png -- 1024 --bg=#ffffff
```

This uses [resvg](https://github.com/RazrFalcon/resvg) — the same renderer pastelki.club uses. Any SVG tool works too,
e.g. `rsvg-convert -w 512 cat.svg -o cat.png` or `inkscape cat.svg -w 512 -o cat.png`.

## License and attribution

The pictures are released under the [MIT license](LICENSE) — © 2026 Pastelki ([pastelki.club](https://pastelki.club)) —
with an **additional permission**:

- **Using a picture inside your own work** (a picture book, print, poster, worksheet, app, game, website, video,
  classroom material…), personal or commercial: you **don't** need to show the license or credit anyone.
- **Redistributing the files themselves** (for example as a downloadable asset pack, or on a stock site): include the
  [LICENSE](LICENSE) file, and please link back to the source, [pastelki.club](https://pastelki.club).
  Don't present the pictures as your own stock collection or claim exclusive rights to them.

You may edit, crop, combine and recolour them as much as you like. The pictures are provided "as is", without any
warranty. The name and logo "Pastelki" are not covered by the license. More in plain words:
[pastelki.club/en/license](https://pastelki.club/en/license).

The pictures are Pastelki's own work: they are written as SVG with the help of AI (the Claude model) following a strict
style guide, and a person checks and approves every picture before it is published. No third-party artwork is included.

## Made with these pictures

- **Kolorowanki** — a gentle colouring app for children 2–6: [github.com/tobob/kolorowanki](https://github.com/tobob/kolorowanki) · [pastelki.club/en/apps/kolorowanki](https://pastelki.club/en/apps/kolorowanki)
- **Pasujki** — a calm, offline matching game for children 2–5: [github.com/tobob/pasujki](https://github.com/tobob/pasujki) · [pastelki.club/en/apps/pasujki](https://pastelki.club/en/apps/pasujki)

## Feedback, problems, ideas for pictures

Found a mistake in a picture or a name, or would you like a picture that's missing?
Tell us at **[pastelki.club/en/feedback](https://pastelki.club/en/feedback?app=other)**, or
[open an issue](https://github.com/tobob/pastelki-assets/issues). Pictures are fixed on pastelki.club and reach this
repository with the next sync — see [CONTRIBUTING.md](CONTRIBUTING.md).

## How this repository is updated

[`scripts/sync.py`](scripts/sync.py) (Python standard library only) reads the public API
`https://pastelki.club/api/library`, which lists only approved pictures in their current version. It downloads the
SVGs, checks each one (valid XML, `viewBox 0 0 100 100`, no scripts or external references), removes pictures that are
no longer published, and regenerates `catalog.json`, `catalog.csv` and the gallery. A
[GitHub Action](.github/workflows/sync.yml) runs it every day and commits the changes after `npm run validate` has
rendered every SVG.

```bash
python3 scripts/sync.py           # refresh
python3 scripts/sync.py --check   # only report differences
```

## Gallery

<!-- gallery:start -->

**302 pictures in 18 categories.** Click a category for every picture with its name and download links.

**[Animals](gallery/zwierzeta.md)** · Zwierzęta · 57

<img src="svg/zwierzeta/alpaka.svg" width="64" alt="Alpaca"> <img src="svg/zwierzeta/bazant.svg" width="64" alt="Pheasant"> <img src="svg/zwierzeta/bear.svg" width="64" alt="Bear"> <img src="svg/zwierzeta/bee.svg" width="64" alt="Bee"> <img src="svg/zwierzeta/bird.svg" width="64" alt="Bird"> <img src="svg/zwierzeta/bobr.svg" width="64" alt="Beaver"> <img src="svg/zwierzeta/butterfly.svg" width="64" alt="Butterfly"> <img src="svg/zwierzeta/buzka-psa-2.svg" width="64" alt="Puppy">

**[Baby animals](gallery/maluchy.md)** · Zwierzęce maluchy · 14

<img src="svg/maluchy/chick.svg" width="64" alt="Chick"> <img src="svg/maluchy/cielatko.svg" width="64" alt="Little calf"> <img src="svg/maluchy/duckling.svg" width="64" alt="Duckling"> <img src="svg/maluchy/dzik.svg" width="64" alt="Baby wild boar"> <img src="svg/maluchy/foka-maluch.svg" width="64" alt="Baby seal"> <img src="svg/maluchy/jezyk.svg" width="64" alt="Baby hedgehog"> <img src="svg/maluchy/kaczuszka-z-mama.svg" width="64" alt="Duckling with mama"> <img src="svg/maluchy/kitten.svg" width="64" alt="Kitten">

**[Animal faces](gallery/buzki.md)** · Zwierzęce buźki · 11

<img src="svg/buzki/buzka-psa.svg" width="64" alt="Dog face"> <img src="svg/buzki/calf.svg" width="64" alt="Calf"> <img src="svg/buzki/cow.svg" width="64" alt="Cow"> <img src="svg/buzki/elephant.svg" width="64" alt="Elephant"> <img src="svg/buzki/kapibara.svg" width="64" alt="Capybara"> <img src="svg/buzki/lion.svg" width="64" alt="Lion"> <img src="svg/buzki/monkey.svg" width="64" alt="Monkey"> <img src="svg/buzki/mors.svg" width="64" alt="Walrus">

**[Food](gallery/jedzenie.md)** · Jedzenie · 33

<img src="svg/jedzenie/ananas.svg" width="64" alt="Pineapple"> <img src="svg/jedzenie/apple.svg" width="64" alt="Apple"> <img src="svg/jedzenie/banana.svg" width="64" alt="Banana"> <img src="svg/jedzenie/blueberries.svg" width="64" alt="Blueberries"> <img src="svg/jedzenie/bone.svg" width="64" alt="Bone"> <img src="svg/jedzenie/bread.svg" width="64" alt="Bread"> <img src="svg/jedzenie/brokul.svg" width="64" alt="Broccoli"> <img src="svg/jedzenie/cake.svg" width="64" alt="Cake">

**[Nature & weather](gallery/natura.md)** · Natura i pogoda · 20

<img src="svg/natura/acorn.svg" width="64" alt="Acorn"> <img src="svg/natura/cloud.svg" width="64" alt="Cloud"> <img src="svg/natura/flower.svg" width="64" alt="Flower"> <img src="svg/natura/iceberg.svg" width="64" alt="Iceberg"> <img src="svg/natura/kaktus.svg" width="64" alt="Cactus in a pot"> <img src="svg/natura/leaf.svg" width="64" alt="Leaf"> <img src="svg/natura/moon.svg" width="64" alt="Moon"> <img src="svg/natura/mushroom.svg" width="64" alt="Mushroom">

**[Houses & places](gallery/domki.md)** · Domki i miejsca · 12

<img src="svg/domki/barn.svg" width="64" alt="Barn"> <img src="svg/domki/beehive.svg" width="64" alt="Beehive"> <img src="svg/domki/doghouse.svg" width="64" alt="Doghouse"> <img src="svg/domki/domek-na-drzewie.svg" width="64" alt="Treehouse"> <img src="svg/domki/house.svg" width="64" alt="House"> <img src="svg/domki/hutch.svg" width="64" alt="Rabbit hutch"> <img src="svg/domki/kennel-bowl.svg" width="64" alt="Pet bowl"> <img src="svg/domki/kominek.svg" width="64" alt="Fireplace">

**[Vehicles](gallery/pojazdy.md)** · Pojazdy · 14

<img src="svg/pojazdy/airplane.svg" width="64" alt="Airplane"> <img src="svg/pojazdy/autobus.svg" width="64" alt="Bus"> <img src="svg/pojazdy/bicycle.svg" width="64" alt="Bicycle"> <img src="svg/pojazdy/boat.svg" width="64" alt="Boat"> <img src="svg/pojazdy/car.svg" width="64" alt="Car"> <img src="svg/pojazdy/helikopter.svg" width="64" alt="Helicopter"> <img src="svg/pojazdy/koparka.svg" width="64" alt="Excavator"> <img src="svg/pojazdy/rakieta.svg" width="64" alt="Rocket">

**[Clothes](gallery/ubrania.md)** · Ubranka · 14

<img src="svg/ubrania/boot.svg" width="64" alt="Rain boot"> <img src="svg/ubrania/hat.svg" width="64" alt="Hat"> <img src="svg/ubrania/kapcie.svg" width="64" alt="Slipper"> <img src="svg/ubrania/kapelusz-slomkowy.svg" width="64" alt="Straw hat"> <img src="svg/ubrania/kombinezon.svg" width="64" alt="Romper"> <img src="svg/ubrania/koszulka.svg" width="64" alt="T-shirt"> <img src="svg/ubrania/mitten.svg" width="64" alt="Mitten"> <img src="svg/ubrania/plaszczyk-przeciwdeszczowy.svg" width="64" alt="Raincoat">

**[At home](gallery/dom.md)** · W domu · 18

<img src="svg/dom/bed.svg" width="64" alt="Bed"> <img src="svg/dom/book.svg" width="64" alt="Book"> <img src="svg/dom/clock.svg" width="64" alt="Clock"> <img src="svg/dom/crayon.svg" width="64" alt="Crayon"> <img src="svg/dom/cup.svg" width="64" alt="Cup"> <img src="svg/dom/kapibara-w-kapieli.svg" width="64" alt="Capybara in the bath"> <img src="svg/dom/key.svg" width="64" alt="Key"> <img src="svg/dom/kropla-miodu-na-lyzeczce.svg" width="64" alt="Honey dipper">

**[Toys](gallery/zabawki.md)** · Zabawki · 19

<img src="svg/zabawki/baczek.svg" width="64" alt="Spinning top"> <img src="svg/zabawki/ball.svg" width="64" alt="Ball"> <img src="svg/zabawki/balloon.svg" width="64" alt="Balloon"> <img src="svg/zabawki/block.svg" width="64" alt="Toy block"> <img src="svg/zabawki/bucket.svg" width="64" alt="Bucket"> <img src="svg/zabawki/drum.svg" width="64" alt="Drum"> <img src="svg/zabawki/gift.svg" width="64" alt="Gift"> <img src="svg/zabawki/grzechotka.svg" width="64" alt="Rattle">

**[Sea creatures](gallery/morze.md)** · Morskie stworzenia · 12

<img src="svg/morze/kalamarnica.svg" width="64" alt="Squid"> <img src="svg/morze/konik-morski.svg" width="64" alt="Seahorse"> <img src="svg/morze/krewetka.svg" width="64" alt="Shrimp"> <img src="svg/morze/meduza.svg" width="64" alt="Jellyfish"> <img src="svg/morze/mewa.svg" width="64" alt="Seagull"> <img src="svg/morze/mors-2.svg" width="64" alt="Walrus"> <img src="svg/morze/narwal.svg" width="64" alt="Narwhal"> <img src="svg/morze/rak-pustelnik.svg" width="64" alt="Hermit crab">

**[Bugs & insects](gallery/owady.md)** · Owady i robaczki · 12

<img src="svg/owady/biedronka-na-lisciu.svg" width="64" alt="Ladybug on a leaf"> <img src="svg/owady/gasienica.svg" width="64" alt="Caterpillar"> <img src="svg/owady/konik-polny.svg" width="64" alt="Grasshopper"> <img src="svg/owady/motyl-na-kwiatku.svg" width="64" alt="Butterfly on a flower"> <img src="svg/owady/mrowka.svg" width="64" alt="Ant"> <img src="svg/owady/osa.svg" width="64" alt="Wasp"> <img src="svg/owady/pajak.svg" width="64" alt="Spider"> <img src="svg/owady/pszczolka-na-kwiatku.svg" width="64" alt="Bee on a flower">

**[Dinosaurs](gallery/dinozaury.md)** · Dinozaury · 7

<img src="svg/dinozaury/dinozaur-z-dluga-szyja.svg" width="64" alt="Long-neck dinosaur"> <img src="svg/dinozaury/jajko-dinozaura.svg" width="64" alt="Dinosaur egg"> <img src="svg/dinozaury/maly-pterodaktyl.svg" width="64" alt="Little pterodactyl"> <img src="svg/dinozaury/smok.svg" width="64" alt="Dragon"> <img src="svg/dinozaury/smok-latawiec.svg" width="64" alt="Stegosaurus"> <img src="svg/dinozaury/triceratops.svg" width="64" alt="Triceratops"> <img src="svg/dinozaury/tyranozaur.svg" width="64" alt="Friendly T-rex">

**[Space](gallery/kosmos.md)** · Kosmos · 13

<img src="svg/kosmos/astronauta-mis.svg" width="64" alt="Astronaut teddy bear"> <img src="svg/kosmos/gwiazda-polarna.svg" width="64" alt="Bright star"> <img src="svg/kosmos/gwiazda-spadajaca.svg" width="64" alt="Shooting star"> <img src="svg/kosmos/gwiazdozbior-wielkiego-wozu.svg" width="64" alt="Big Dipper"> <img src="svg/kosmos/helm-astronauty.svg" width="64" alt="Space helmet"> <img src="svg/kosmos/kometa.svg" width="64" alt="Comet"> <img src="svg/kosmos/ksiezycowy-lazik.svg" width="64" alt="Moon rover"> <img src="svg/kosmos/maly-kosmita.svg" width="64" alt="Little alien">

**[Music](gallery/muzyka.md)** · Muzyka · 12

<img src="svg/muzyka/bebenek-marszowy.svg" width="64" alt="Drum"> <img src="svg/muzyka/bebenek-tamburyn.svg" width="64" alt="Tambourine"> <img src="svg/muzyka/cymbalki.svg" width="64" alt="Xylophone"> <img src="svg/muzyka/flet.svg" width="64" alt="Flute"> <img src="svg/muzyka/gitara.svg" width="64" alt="Guitar"> <img src="svg/muzyka/marakasy.svg" width="64" alt="Maracas"> <img src="svg/muzyka/mikrofon.svg" width="64" alt="Microphone"> <img src="svg/muzyka/pianino.svg" width="64" alt="Piano">

**[Faces & feelings](gallery/emocje.md)** · Buzie i emocje · 11

<img src="svg/emocje/buzia-ze-lza-ze-szczescia.svg" width="64" alt="Happy tears face"> <img src="svg/emocje/pingwinek-na-lodzie.svg" width="64" alt="Penguin on the ice"> <img src="svg/emocje/pingwinek-z-kokardka.svg" width="64" alt="Penguin with a bow"> <img src="svg/emocje/smutna-buzia.svg" width="64" alt="Sad face"> <img src="svg/emocje/spiaca-buzia.svg" width="64" alt="Sleepy face"> <img src="svg/emocje/usmiechnieta-buzia.svg" width="64" alt="Smiley face"> <img src="svg/emocje/usmiechnieta-chmurka.svg" width="64" alt="Happy cloud"> <img src="svg/emocje/wesola-buzia-ze-smiechem.svg" width="64" alt="Laughing face">

**[Celebrations](gallery/swieta.md)** · Święta i przyjęcia · 10

<img src="svg/swieta/balony.svg" width="64" alt="Balloons"> <img src="svg/swieta/choinka.svg" width="64" alt="Christmas tree"> <img src="svg/swieta/choinkowa-bombka.svg" width="64" alt="Christmas bauble"> <img src="svg/swieta/dzwonek.svg" width="64" alt="Bell"> <img src="svg/swieta/fajerwerk.svg" width="64" alt="Firework"> <img src="svg/swieta/kapelusz-czarodzieja.svg" width="64" alt="Wizard hat"> <img src="svg/swieta/krasnoludek.svg" width="64" alt="Garden gnome"> <img src="svg/swieta/mikolaj.svg" width="64" alt="Santa Claus">

**[Sports & play](gallery/sport.md)** · Sport i ruch · 13

<img src="svg/sport/banki-mydlane.svg" width="64" alt="Soap bubbles"> <img src="svg/sport/dzwonek-rowerowy.svg" width="64" alt="Bicycle bell"> <img src="svg/sport/hulajnoga.svg" width="64" alt="Scooter"> <img src="svg/sport/hustawka.svg" width="64" alt="Swing"> <img src="svg/sport/koparka-piaskowa.svg" width="64" alt="Toy digger"> <img src="svg/sport/lopata-do-sniegu.svg" width="64" alt="Snow shovel"> <img src="svg/sport/piaskownica.svg" width="64" alt="Sandbox"> <img src="svg/sport/pilka-nozna.svg" width="64" alt="Football">

<!-- gallery:end -->
