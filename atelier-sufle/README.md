# Atelier Suflé

Website for **Atelier Suflé**: one-to-one flute lessons with Suhsuan Wang in Bonn, Köln and online, in English, German and Chinese.

Static site, no framework. A small Python script generates the four language pages from one template.

```
index.html, de/, zh-hant/, zh-hans/        Generated pages (do not edit by hand)
impressum.html, datenschutz.html           Legal pages (German law), edited by hand
src/content.py                             All texts in EN / DE / 繁體中文 + optional sections
                                           (简体中文 is generated from the Traditional text)
src/make_sound.py                          Generates the soft flute sounds in assets/audio/
src/template.html                          Page structure
src/build.py                               Generates the pages, sitemap.xml and robots.txt
assets/css/site.css, assets/js/site.js     Styles and behaviour
assets/photos/                             Photos in WebP + JPEG, two sizes each
assets/audio/                              Flute notes B, A, G and "Mary Had a Little Lamb"
assets/fonts/                              Self-hosted fonts (no requests to Google)
```

## Editing

1. Change texts in `src/content.py` (or structure in `src/template.html`).
2. Run `python3 src/build.py` (the Simplified Chinese page needs `pip install opencc-python-reimplemented` once).
3. Commit and push. GitHub Pages republishes automatically.

### Optional sections (kept off the site until real content exists)

In `src/content.py`, `OPTIONAL`:

- `testimonials` + `google_reviews_url`: real reviews only (for example from the Google Business Profile), shown with the note "Reviews from Google, shown unedited". Never invent or edit them: fake reviews are illegal in Germany (UWG).
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
3. Live at `https://reissfuji006.github.io/atelier-sufle/` (also `/de/`, `/zh-hant/`, `/zh-hans/`).
4. Submit `sitemap.xml` in Google Search Console, and add the site link to the Instagram bio.

## SEO checklist (in this order)

1. Publish on GitHub Pages, then add the site to **Google Search Console** and submit `sitemap.xml` (also Bing Webmaster Tools).
2. Create a **Google Business Profile** "Atelier Suflé" (category: music teacher / flute teacher, service area Bonn and Köln, no public address needed), link the website, add photos, ask students and parents for reviews.
3. Put the site link in the Instagram bio.
4. Buy the domain (for example `ateliersufle.de`), set it in Pages and in `SITE_URL`, rebuild.
5. Listings: music-teacher directories, local family and expat groups in Bonn / Köln, Chinese community groups.

## Own domain (optional)

Add it in **Settings → Pages → Custom domain**, point the DNS to GitHub Pages, then change `SITE_URL` in `src/content.py` and rebuild.

## Sound

The notes B, A, G and the tune are synthesized by `src/make_sound.py`: a soft soprano-recorder timbre (near-pure tone, gentle attack, light vibrato), one octave up, quiet (peak -6.5 dBFS), very little reverb, 130 bpm. Regenerate with `python3 src/make_sound.py assets/audio 2 0.46` (octave factor, beat in seconds; keep `BEAT` in `assets/js/site.js` equal to the beat). Recordings of Suhsuan playing the same notes can replace the files (same names).

## Quality checks run before delivery

- html-validate: no errors on all 6 pages.
- axe-core (WCAG 2.0/2.1/2.2 A + AA, best practices): no violations on all 6 pages at 390 px and 1280 px.
- Lighthouse (mobile, local server): Performance 96-99, Accessibility 100, Best Practices 100, SEO 100.
- Playwright (29 checks): layout at 390 / 768 / 1280 px in 4 languages, form validation and sending (simulated service), audio, keyboard use, FAQ, active section marker, links.
