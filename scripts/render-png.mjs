#!/usr/bin/env node
// Render every SVG in svg/ to PNG with resvg (the renderer pastelki.club uses for its own PNGs).
//   npm install
//   npm run png                      → png/512/<category>/<slug>.png
//   npm run png -- 256 1024          → png/256/… and png/1024/…
//   npm run png -- 512 --bg=#ffffff  → white background instead of transparent
//   npm run validate                 → render each SVG in memory only and fail on any error (used by CI)
// PNGs are not committed (png/ is in .gitignore) — they are easy to regenerate at any size.
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { Resvg } from '@resvg/resvg-js'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const args = process.argv.slice(2)
const validateOnly = args.includes('--validate')
const bg = args.find((a) => a.startsWith('--bg='))?.slice(5)
const sizes = args.filter((a) => /^\d+$/.test(a)).map(Number)
if (!sizes.length) sizes.push(512)

const files = []
const walk = (dir) => {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name)
    if (e.isDirectory()) walk(p)
    else if (e.name.endsWith('.svg')) files.push(p)
  }
}
walk(path.join(root, 'svg'))
files.sort()

let failed = 0
for (const file of files) {
  const rel = path.relative(path.join(root, 'svg'), file)
  try {
    const svg = fs.readFileSync(file, 'utf8')
    for (const size of validateOnly ? [128] : sizes) {
      const opts = { fitTo: { mode: 'width', value: size } }
      if (bg) opts.background = bg
      const img = new Resvg(svg, opts).render()
      if (img.width !== size || img.height !== size) throw new Error(`rendered ${img.width}×${img.height}`)
      const png = img.asPng()
      if (!validateOnly) {
        const out = path.join(root, 'png', String(size), rel.replace(/\.svg$/, '.png'))
        fs.mkdirSync(path.dirname(out), { recursive: true })
        fs.writeFileSync(out, png)
      }
    }
  } catch (err) {
    failed++
    console.error(`✗ ${rel}: ${err.message}`)
  }
}
console.log(`${validateOnly ? 'validated' : `rendered at ${sizes.join(', ')} px`}: ${files.length - failed}/${files.length} SVGs`)
process.exit(failed ? 1 : 0)
