"""Builds index.html (English), de/index.html and zh/index.html from src/template.html.

Usage: python3 src/build.py   (no dependencies)
"""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import content as C  # noqa: E402

PATHS = {'en': '', 'de': 'de/', 'zh': 'zh/'}


def jsonld(lang):
    t = C.T[lang]
    data = {
        '@context': 'https://schema.org',
        '@type': 'MusicSchool',
        'name': 'Atelier Suflé',
        'description': html.unescape(t['meta.desc']),
        'url': C.SITE_URL + PATHS[lang],
        'image': C.SITE_URL + 'assets/og-image.jpg',
        'logo': C.SITE_URL + 'assets/brand/logo-mark.png',
        'email': C.EMAIL,
        'areaServed': [{'@type': 'City', 'name': 'Bonn'}, {'@type': 'City', 'name': 'Köln'}],
        'availableLanguage': ['en', 'de', 'zh'],
        'sameAs': [C.INSTAGRAM],
        'founder': {
            '@type': 'Person',
            'name': 'Suhsuan Wang',
            'jobTitle': 'Flautist and flute teacher',
            'alumniOf': {'@type': 'CollegeOrUniversity', 'name': 'Hochschule für Musik und Tanz Köln'},
        },
    }
    return json.dumps(data, ensure_ascii=False)


def optional_blocks(lang):
    t = C.T[lang]
    out = {'philosophy': '', 'recordings': '', 'testimonials': ''}
    phil = C.OPTIONAL['philosophy'].get(lang)
    if phil:
        out['philosophy'] = f'<blockquote class="quote">{phil}</blockquote>'
    if C.OPTIONAL['recordings']:
        items = ''.join(
            f'<figure><figcaption>{html.escape(r["title"])}</figcaption>'
            f'<audio controls preload="none" src="{{{{root}}}}{r["src"]}"></audio></figure>'
            for r in C.OPTIONAL['recordings'])
        out['recordings'] = f'<div class="recordings">{items}</div>'
    if C.OPTIONAL['testimonials']:
        items = ''.join(
            f'<figure><blockquote>{q["quote"].get(lang) or q["quote"]["en"]}</blockquote>'
            f'<figcaption>{html.escape(q["name"])}</figcaption></figure>'
            for q in C.OPTIONAL['testimonials'])
        out['testimonials'] = (
            '<section class="block" id="testimonials" aria-labelledby="testi-title"><div class="wrap">'
            f'<div class="section-head"><p class="label">{t["testi.label"]}</p>'
            f'<h2 id="testi-title">{t["testi.title"]}</h2></div>'
            f'<div class="testimonials-list">{items}</div></div></section>')
    return out


def build(lang):
    tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    t = C.T[lang]
    root = '../' if PATHS[lang] else ''
    switch = ''.join(
        f'<a href="{root}{PATHS[l]}index.html" hreflang="{C.HTML_LANG[l]}" lang="{C.HTML_LANG[l]}"'
        f'{" aria-current=" + chr(34) + "true" + chr(34) if l == lang else ""}>{C.LANG_LABEL[l]}</a>'
        for l in C.LANGS)
    alternates = '\n'.join(
        f'<link rel="alternate" hreflang="{C.HTML_LANG[l]}" href="{C.SITE_URL}{PATHS[l]}">' for l in C.LANGS)
    alternates += f'\n<link rel="alternate" hreflang="x-default" href="{C.SITE_URL}">'
    js = {k: html.unescape(re.sub('<[^>]+>', '', t[k])) for k in C.JS_KEYS}
    js['notes'] = C.NOTE_NAMES[lang]
    values = dict(t)
    values.update(optional_blocks(lang))
    values.update({
        'html_lang': C.HTML_LANG[lang], 'og_locale': C.OG_LOCALE[lang], 'lang_name': C.LANG_NAME[lang],
        'canonical': C.SITE_URL + PATHS[lang], 'site_url': C.SITE_URL, 'hreflang': alternates,
        'langswitch': switch, 'home': 'index.html', 'email': C.EMAIL,
        'instagram': C.INSTAGRAM, 'instagram_handle': C.INSTAGRAM_HANDLE,
        'jsonld': jsonld(lang).replace('</', '<\\/'),
        'jsdata': json.dumps(js, ensure_ascii=False).replace('</', '<\\/'),
    })

    def fill(text):
        return re.sub(r'\{\{([\w.]+)\}\}', lambda m: str(values[m.group(1)]) if m.group(1) != 'root' else '{{root}}', text)

    page = fill(fill(tpl)).replace('{{root}}', root)
    page = '\n'.join(line.rstrip() for line in page.split('\n'))
    page = re.sub(r'\n{3,}', '\n\n', page)
    missing = re.findall(r'\{\{[\w.]+\}\}', page)
    assert not missing, f'{lang}: unfilled {missing}'
    out = os.path.join(SITE, PATHS[lang], 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(page)
    return out


def sitemap():
    urls = ''.join(
        f'  <url><loc>{C.SITE_URL}{PATHS[l]}</loc>'
        + ''.join(f'<xhtml:link rel="alternate" hreflang="{C.HTML_LANG[a]}" href="{C.SITE_URL}{PATHS[a]}"/>' for a in C.LANGS)
        + '</url>\n' for l in C.LANGS)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
           f'{urls}</urlset>\n')
    open(os.path.join(SITE, 'sitemap.xml'), 'w', encoding='utf-8').write(xml)
    open(os.path.join(SITE, 'robots.txt'), 'w', encoding='utf-8').write(
        f'User-agent: *\nAllow: /\n\nSitemap: {C.SITE_URL}sitemap.xml\n')


if __name__ == '__main__':
    for lang in C.LANGS:
        print('built', os.path.relpath(build(lang), SITE))
    sitemap()
    print('built sitemap.xml, robots.txt')
