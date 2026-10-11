"""Builds the language pages from src/template.html and src/content.py.

Outputs index.html (English), de/, zh-hant/ and zh-hans/ (Simplified Chinese is converted
from the Traditional text with OpenCC), plus sitemap.xml and robots.txt.

Usage: python3 src/build.py
Requires: pip install opencc-python-reimplemented   (only for the Simplified Chinese page)
"""
import html
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import content as C  # noqa: E402


def simplified(texts):
    import opencc
    conv = opencc.OpenCC('t2s')
    out = {}
    for k, v in texts.items():
        s = conv.convert(v)
        for a, b in C.SIMPLIFIED_WORDS:
            s = s.replace(a, b)
        out[k] = s
    return out


T = dict(C.T)
T['zh-hans'] = simplified(C.T['zh-hant'])


def plain(s):
    return html.unescape(re.sub('<[^>]+>', '', s))


def jsonld(lang):
    t = T[lang]
    url = C.SITE_URL + C.PATHS[lang]
    graph = [
        {
            '@type': 'MusicSchool',
            '@id': C.SITE_URL + '#school',
            'name': 'Atelier Suflé',
            'description': plain(t['meta.desc']),
            'url': url,
            'image': C.SITE_URL + 'assets/og-image.jpg',
            'logo': C.SITE_URL + 'assets/brand/logo-mark.png',
            'email': C.EMAIL,
            'areaServed': [{'@type': 'City', 'name': 'Bonn'}, {'@type': 'City', 'name': 'Köln'}],
            'availableLanguage': ['en', 'de', 'zh'],
            'sameAs': [C.INSTAGRAM],
            'founder': {'@id': C.SITE_URL + '#suhsuan'},
        },
        {
            '@type': 'Person',
            '@id': C.SITE_URL + '#suhsuan',
            'name': 'Suhsuan Wang',
            'jobTitle': 'Flautist and flute teacher',
            'knowsLanguage': ['en', 'de', 'zh'],
            'alumniOf': {'@type': 'CollegeOrUniversity', 'name': 'Hochschule für Musik und Tanz Köln'},
            'sameAs': [C.INSTAGRAM],
        },
        {
            '@type': 'FAQPage',
            'inLanguage': C.HTML_LANG[lang],
            'mainEntity': [{'@type': 'Question', 'name': plain(t[q]),
                            'acceptedAnswer': {'@type': 'Answer', 'text': plain(t[a])}} for q, a in C.FAQ_KEYS],
        },
    ]
    return json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False)


def blocks(lang, root):
    t = T[lang]
    out = {}
    out['faq_items'] = ''.join(
        f'<details><summary>{t[q]}</summary><p>{t[a]}</p></details>' for q, a in C.FAQ_KEYS)
    out['music_photos'] = ''.join(
        f'<figure><picture><source type="image/webp" srcset="{root}assets/photos/{stem}.webp">'
        f'<img src="{root}assets/photos/{stem}.jpg" alt="{t[alt]}" width="{w}" height="{h}" loading="lazy" decoding="async">'
        f'</picture><figcaption>{t[cap]}</figcaption></figure>'
        for stem, w, h, alt, cap in C.MUSIC_PHOTOS)
    phil = C.OPTIONAL['philosophy'].get(lang) or (C.OPTIONAL['philosophy'].get('zh-hant') if lang == 'zh-hans' else '')
    out['philosophy'] = f'<blockquote class="quote">{phil}</blockquote>' if phil else ''
    out['recordings'] = ''
    if C.OPTIONAL['recordings']:
        out['recordings'] = '<div class="recordings">' + ''.join(
            f'<figure><figcaption>{html.escape(r["title"])}</figcaption>'
            f'<audio controls preload="none" src="{root}{r["src"]}"></audio></figure>'
            for r in C.OPTIONAL['recordings']) + '</div>'
    out['testimonials'] = ''
    if C.OPTIONAL['testimonials']:
        items = ''.join(
            f'<figure><blockquote>{q["quote"].get(lang) or q["quote"].get("en")}</blockquote>'
            f'<figcaption>{html.escape(q["name"])}</figcaption></figure>' for q in C.OPTIONAL['testimonials'])
        more = (f'<a href="{C.OPTIONAL["google_reviews_url"]}" target="_blank" rel="noopener">{t["testi.more"]}</a>'
                if C.OPTIONAL['google_reviews_url'] else '')
        out['testimonials'] = (
            '<section class="block reviews" id="reviews" aria-labelledby="testi-title"><div class="wrap">'
            f'<div class="section-head"><p class="label">{t["testi.label"]}</p>'
            f'<h2 id="testi-title">{t["testi.title"]}</h2></div>'
            f'<div class="testimonials-list">{items}</div>'
            f'<p class="note">{t["testi.source"]} {more}</p></div></section>')
    return out


def build(lang):
    tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    t = T[lang]
    root = '../' if C.PATHS[lang] else ''
    switch = ''.join(
        f'<a href="{root}{C.PATHS[l]}index.html" hreflang="{C.HTML_LANG[l]}" lang="{C.HTML_LANG[l]}" title="{C.LANG_TITLE[l]}"'
        + (' aria-current="true"' if l == lang else '') + f'>{C.LANG_LABEL[l]}</a>'
        for l in C.LANGS)
    alternates = '\n'.join(
        f'<link rel="alternate" hreflang="{C.HTML_LANG[l]}" href="{C.SITE_URL}{C.PATHS[l]}">' for l in C.LANGS)
    alternates += f'\n<link rel="alternate" hreflang="x-default" href="{C.SITE_URL}">'
    js = {k: plain(t[k]) for k in C.JS_KEYS}
    js['notes'] = C.NOTE_NAMES[lang]
    values = dict(t)
    values.update(blocks(lang, root))
    values.update({
        'html_lang': C.HTML_LANG[lang], 'og_locale': C.OG_LOCALE[lang], 'lang_title': C.LANG_TITLE[lang],
        'canonical': C.SITE_URL + C.PATHS[lang], 'site_url': C.SITE_URL, 'hreflang': alternates,
        'langswitch': switch, 'home': 'index.html', 'email': C.EMAIL,
        'instagram': C.INSTAGRAM, 'instagram_handle': C.INSTAGRAM_HANDLE,
        'jsonld': jsonld(lang).replace('</', '<\\/'),
        'jsdata': json.dumps(js, ensure_ascii=False).replace('</', '<\\/'),
    })

    def fill(text):
        return re.sub(r'\{\{([\w.]+)\}\}', lambda m: '{{root}}' if m.group(1) == 'root' else str(values[m.group(1)]), text)

    page = fill(fill(tpl)).replace('{{root}}', root)
    page = '\n'.join(line.rstrip() for line in page.split('\n'))
    page = re.sub(r'\n{3,}', '\n\n', page)
    missing = re.findall(r'\{\{[\w.]+\}\}', page)
    assert not missing, f'{lang}: unfilled {missing}'
    out = os.path.join(SITE, C.PATHS[lang], 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(page)
    return out


def sitemap():
    urls = ''.join(
        f'  <url><loc>{C.SITE_URL}{C.PATHS[l]}</loc>'
        + ''.join(f'<xhtml:link rel="alternate" hreflang="{C.HTML_LANG[a]}" href="{C.SITE_URL}{C.PATHS[a]}"/>' for a in C.LANGS)
        + '</url>\n' for l in C.LANGS)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
           f'{urls}</urlset>\n')
    open(os.path.join(SITE, 'sitemap.xml'), 'w', encoding='utf-8').write(xml)
    open(os.path.join(SITE, 'robots.txt'), 'w', encoding='utf-8').write(
        f'User-agent: *\nAllow: /\n\nSitemap: {C.SITE_URL}sitemap.xml\n')


if __name__ == '__main__':
    old = os.path.join(SITE, 'zh')  # earlier single Chinese page, replaced by zh-hant/ and zh-hans/
    if os.path.isdir(old):
        shutil.rmtree(old)
    for lang in C.LANGS:
        print('built', os.path.relpath(build(lang), SITE))
    sitemap()
    print('built sitemap.xml, robots.txt')
