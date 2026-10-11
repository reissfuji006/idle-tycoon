# Atelier Suflé

Website for **Atelier Suflé**: one-to-one flute lessons with Suhsuan Wang in Bonn, Köln and online, in English, German and Chinese.

A static site: plain HTML, CSS and JavaScript, no build step.

```
index.html          Home page (EN / DE / 中文, switched in the page)
impressum.html      Legal notice (required in Germany)
datenschutz.html    Privacy policy (required in Germany)
assets/brand/       Logo and flute drawings
assets/photos/      Photos of Suhsuan
assets/fonts/       Self-hosted fonts (no requests to Google, GDPR-friendly)
assets/og-image.jpg Preview image for WhatsApp, Instagram, etc.
favicon.png, apple-touch-icon.png
```

## Before going live

1. **Impressum and Datenschutz**: replace every highlighted `[placeholder]` (postal address, optional phone, VAT ID if any, photographers, date). German law requires a real postal address in the Impressum. These texts are a starting point, not legal advice; a check with a generator such as eRecht24 is recommended.
2. **Contact form**: it sends requests to `hsuan41213@gmail.com` through [FormSubmit](https://formsubmit.co). The very first time someone sends the form, FormSubmit emails Suhsuan a confirmation link. She clicks it once, and from then on every request arrives in her inbox.
3. **Translations**: have Suhsuan proofread the German and Chinese texts (in `index.html`, inside the `T = { de: {...}, zh: {...} }` block).

## Publish with GitHub Pages (free)

1. Push these files to the root of a GitHub repository named `atelier-sufle`.
2. On GitHub: **Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: `main`, folder `/ (root)` → Save**.
3. After about a minute the site is live at `https://reissfuji006.github.io/atelier-sufle/`.

## Own domain (optional)

If you buy a domain (for example `ateliersufle.com`):

1. In **Settings → Pages → Custom domain**, enter the domain and save; tick **Enforce HTTPS** once it is available.
2. At the domain registrar, point the domain to GitHub Pages ([GitHub's guide](https://docs.github.com/pages/configuring-a-custom-domain-for-your-github-pages-site)).
3. In `index.html`, replace `https://reissfuji006.github.io/atelier-sufle/` with the new address (in the `og:` tags and the JSON-LD block).

## Editing the content

- **Text**: the English text is in the HTML. German and Chinese translations are in the `T` object near the bottom of `index.html`, keyed by the same `data-i18n` names.
- **Language links**: `?lang=de` or `?lang=zh` at the end of the address opens the site directly in that language (handy for sharing). Without it, the site follows the visitor's last choice, then their browser language.
- **Photos**: replace the files in `assets/photos/`, keeping the same names (or update the `src` in `index.html`).

## Sound

`assets/audio/` holds the flute notes B4, A4, G4 and the tune *Mary Had a Little Lamb* (B A G A B B B) used by the music staff at the top of the page. They are made from a real flute recording (A4) from the [tonejs-instruments](https://github.com/Makefully-Studios/tonejs-instruments) sample set (npm package `tonejs-instrument-flute-mp3`, MIT license), pitched to B and G with a light room reverb. For an even more personal touch, these four files can be replaced by recordings of Suhsuan playing the same notes (same file names, MP3).
