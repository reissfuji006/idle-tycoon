# Atelier Suflé

Website for **Atelier Suflé**: one-to-one flute lessons with Suhsuan Wang in Bonn, Köln and online, in English, German and Chinese.

Static site, no framework. A small Python script (no dependencies) generates the three language pages from one template.

```
index.html, de/index.html, zh/index.html   Generated pages (do not edit by hand)
impressum.html, datenschutz.html           Legal pages (German law), edited by hand
src/content.py                             All texts in EN / DE / 中文 + optional sections
src/template.html                          Page structure
src/build.py                               Generates the pages, sitemap.xml and robots.txt
assets/css/site.css, assets/js/site.js     Styles and behaviour
assets/photos/                             Photos in WebP + JPEG, two sizes each
assets/audio/                              Flute notes B, A, G and "Mary Had a Little Lamb"
assets/fonts/                              Self-hosted fonts (no requests to Google)
```

## Editing

1. Change texts in `src/content.py` (or structure in `src/template.html`).
2. Run `python3 src/build.py`.
3. Commit and push. GitHub Pages republishes automatically.

### Optional sections (kept off the site until real content exists)

In `src/content.py`, `OPTIONAL`:

- `testimonials`: real, authorised quotes only. Never invent them.
- `philosophy`: Suhsuan's teaching philosophy in her own words, per language.
- `recordings`: her own recordings (MP3 in `assets/audio/`).

Fill one in, rebuild, and the section appears.

## Before going live

1. **Impressum / Datenschutz**: replace every highlighted `[placeholder]` (postal address is required by law, VAT ID if any, photographers, date). These texts are a starting point, not legal advice.
2. **Contact form**: requests go to `hsuan41213@gmail.com` through [FormSubmit](https://formsubmit.co). The first submission sends Suhsuan a one-time confirmation link; she must click it.
3. **Proofreading**: Suhsuan should read the German and Chinese texts, and confirm the "How to start" steps.

## Publish with GitHub Pages (free)

1. Push this folder's contents to the root of a public repository `atelier-sufle`.
2. **Settings → Pages → Deploy from a branch → `main` / `(root)` → Save**.
3. Live at `https://reissfuji006.github.io/atelier-sufle/` (also `/de/` and `/zh/`).
4. Submit `sitemap.xml` in Google Search Console, and add the site link to the Instagram bio.

## Own domain (optional)

Add it in **Settings → Pages → Custom domain**, point the DNS to GitHub Pages, then change `SITE_URL` in `src/content.py` and rebuild.

## Sound

The flute samples are made from a real flute recording (A4) from the [tonejs-instruments](https://github.com/Makefully-Studios/tonejs-instruments) set (npm `tonejs-instrument-flute-mp3`, MIT), pitched to B and G with a light reverb. Recordings of Suhsuan playing the same notes can replace them (same file names).

## Quality checks run before delivery

- html-validate: no errors on all 5 pages.
- axe-core (WCAG 2.0/2.1/2.2 A + AA, best practices): no violations on all pages at 390 px and 1280 px.
- Lighthouse (mobile, local server): Performance 94, Accessibility 100, Best Practices 100, SEO 100.
- Playwright: layout at 390 / 768 / 1280 px in 3 languages, form validation and sending (simulated service), audio, keyboard use, links.
