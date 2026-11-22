#!/usr/bin/env python3
"""The Beat District — template v2 T1 site generator (t_36b96016, 2026-11-21).
Record store, 22 N Sycamore St Ste A, Petersburg VA. All copy traces to the card's verified sources:
Google Business Profile (Maps read 2026-11-21), Instagram @thebeatdistrict_pva bio + opening post,
12onyourside.com "What's New in RVA" 2026-11-02 press piece, and the shop's own site thebeatdistrict.co
(og:description, stock/pickup banner, menu + collection names). Unknown facts OMITTED, never invented:
no events, no prices, no trade-in claim, no "we buy", no Richmond geography, no staff roster.
"""
import json, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
ORIGIN = "https://the-beat-district-demo.up.railway.app"
NAME = "The Beat District"
SHOP = "https://thebeatdistrict.co/"
IG = "https://www.instagram.com/thebeatdistrict_pva/"
TEL_D = "(804) 504-2325"
TEL_U = "tel:+18045042325"
MAIL = "info@thebeatdistrict.co"
MAPQ = "22+N+Sycamore+St+Ste+A,+Petersburg,+VA+23803"
MAP_EMBED = "https://www.google.com/maps?q=" + MAPQ + "&output=embed"
MAP_LINK = "https://maps.google.com/maps?q=" + MAPQ
GEO_LAT, GEO_LON = 37.2284303, -77.4039837  # OSM Nominatim geocode of 22 N Sycamore St, 23803 (provenance in evidence.json)

MISSION = ("The Beat District is more than a vinyl record store. It&rsquo;s a place for people who "
"believe music has the power to connect us, inspire us, and tell our stories. We&rsquo;re passionate about "
"creating a welcoming space where casual listeners, longtime collectors, music lovers, and curious newcomers "
"can discover something that moves them. From hip-hop and R&amp;B to soul, jazz, rock, and beyond, our "
"collection celebrates the sounds that have shaped generations and continue to bring people together.")

# ---------------------------------------------------------------- shared art
MARK = ('<svg class="mark" viewBox="0 0 100 100" role="img" aria-label="The Beat District emblem: a vinyl record with a tonearm resting on it">'
'<circle cx="45" cy="55" r="39" fill="#1a140e" stroke="currentColor" stroke-width="3.5"/>'
'<circle cx="45" cy="55" r="31" fill="none" stroke="rgba(245,237,224,.35)" stroke-width="1.6"/>'
'<circle cx="45" cy="55" r="25" fill="none" stroke="rgba(245,237,224,.28)" stroke-width="1.6"/>'
'<circle cx="45" cy="55" r="19" fill="none" stroke="rgba(245,237,224,.22)" stroke-width="1.6"/>'
'<circle cx="45" cy="55" r="12.5" fill="#c8512f"/>'
'<circle cx="45" cy="55" r="12.5" fill="none" stroke="rgba(20,16,9,.5)" stroke-width="1"/>'
'<circle cx="45" cy="55" r="2.6" fill="#f5ede0"/>'
'<circle cx="81" cy="17" r="6" fill="#e9a63e"/>'
'<path d="M81 22 58 46" stroke="#f5ede0" stroke-width="4" stroke-linecap="round"/>'
'<rect x="53" y="41" width="10" height="7" rx="2" fill="#f5ede0" transform="rotate(45 58 44.5)"/>'
'</svg>')

def disc(cx, cy, r, label):
    g = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#17110b"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r*0.78}" fill="none" stroke="rgba(245,237,224,.18)" stroke-width="1.6"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r*0.62}" fill="none" stroke="rgba(245,237,224,.14)" stroke-width="1.6"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r*0.40}" fill="{label}"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{max(2,r*0.07)}" fill="#f5ede0"/>']
    return "".join(g)

HEROART = ('<svg class="heroart" viewBox="0 0 560 420" role="img" aria-label="Illustration of an open crate of album sleeves beside a turntable with a spinning record">'
# record lying on the wall behind
'<g transform="translate(415 128)">' + disc(0, 0, 108, "#c8512f") +
'<circle r="108" fill="none" stroke="rgba(245,237,224,.20)" stroke-width="2"/>'
'<circle r="66" fill="none" stroke="rgba(245,237,224,.12)" stroke-width="1.6"/></g>'
# turntable base
'<rect x="318" y="252" width="220" height="122" rx="14" fill="#2c2116" stroke="rgba(245,237,224,.22)" stroke-width="2.5"/>'
'<g transform="translate(408 312)">' + disc(0, 0, 48, "#4f7a63") +
'<circle r="48" fill="none" stroke="rgba(245,237,224,.22)" stroke-width="2"/></g>'
'<circle cx="516" cy="252" r="7" fill="#e9a63e"/>'
'<path d="M516 252 462 322" stroke="#f5ede0" stroke-width="4.5" stroke-linecap="round"/>'
'<rect x="454" y="316" width="15" height="9" rx="2.5" fill="#f5ede0" transform="rotate(56 461 320)"/>'
'<circle cx="517" cy="342" r="4.4" fill="#e9a63e"/>'
# crate
'<rect x="36" y="196" width="262" height="176" rx="8" fill="#3a2a19" stroke="rgba(245,237,224,.28)" stroke-width="3"/>'
'<path d="M36 252h262M36 316h262" stroke="rgba(20,16,9,.55)" stroke-width="4"/>'
'<text x="167" y="294" text-anchor="middle" font-family="Georgia,serif" font-size="30" letter-spacing="7" fill="#f5ede0">RECORDS</text>'
# sleeves in the crate
'<g transform="rotate(-9 112 152)"><rect x="66" y="92" width="92" height="118" rx="4" fill="#c8512f" stroke="rgba(20,16,9,.35)" stroke-width="2"/>' + disc(112, 151, 34, "#f5ede0") + '</g>'
'<g transform="rotate(2 200 146)"><rect x="155" y="86" width="92" height="122" rx="4" fill="#4f7a63" stroke="rgba(20,16,9,.35)" stroke-width="2"/>' + disc(201, 147, 34, "#141009") + '</g>'
'<g transform="rotate(10 285 150)"><rect x="240" y="94" width="92" height="116" rx="4" fill="#e9a63e" stroke="rgba(20,16,9,.35)" stroke-width="2"/>' + disc(286, 152, 33, "#141009") + '</g>'
# floating single + notes
'<g transform="translate(58 84)">' + disc(0, 0, 26, "#e9a63e") + '</g>'
'<path d="M328 96v-34l30-8v34" fill="none" stroke="rgba(245,237,224,.6)" stroke-width="3.5" stroke-linecap="round"/>'
'<circle cx="322" cy="98" r="8" fill="rgba(245,237,224,.6)"/><circle cx="352" cy="90" r="8" fill="rgba(245,237,224,.6)"/>'
'</svg>')

def glyph(color):
    return ('<svg class="glyph" viewBox="0 0 34 34" aria-hidden="true" style="--spine:' + color + '">'
    '<circle cx="17" cy="17" r="14.5" fill="none" stroke="currentColor" stroke-width="2"/>'
    '<circle cx="17" cy="17" r="8.5" fill="' + color + '"/>'
    '<circle cx="17" cy="17" r="1.8" fill="currentColor"/></svg>')

LANES = [
    ("Fresh indie releases", "New pressings from indie labels land here first — many as indie-exclusive editions.", "#c8512f"),
    ("Best sellers", "The records everybody&rsquo;s asking for, kept on the shop&rsquo;s top-sellers list.", "#e9a63e"),
    ("Audiophile-grade pressings", "High-quality pressings for listeners who hear the difference.", "#4f7a63"),
    ("Local artist records", "Records from local artists, stocked in the shop.", "#b98a6a"),
    ("Vintage staples", "Decades-deep staples, new and used.", "#8f5f9e"),
    ("CDs, movies &amp; gifts", "New and used CDs plus movies — and candles, books, toys, and candy for the rest of the crew.", "#c46b3f"),
]

def lanes_cards():
    out = ['<div class="cards">']
    for t, p, c in LANES:
        out.append(f'<article class="card" style="--spine:{c}">' + glyph(c) +
                   f'<h3>{t}</h3><p>{p}</p></article>')
    out.append("</div>")
    return "".join(out)

GENRES = ["Blues &amp; Jazz", "R&amp;B / Soul", "Rock &amp; Pop", "World Music", "Rap &amp; Hip-Hop", "Reggae", "Dance &amp; Electronic"]
def genre_chips():
    return '<div class="chips">' + "".join(f'<a class="chip alt" href="{SHOP}" rel="noopener">{g}</a>' for g in GENRES) + "</div>"

NAP = ('<p class="fbrand">' + NAME + '</p>'
'<address>22 N Sycamore St, Suite A<br>Petersburg, Virginia 23803<br>'
'Wed–Sun 12–6 · <a href="' + TEL_U + '">' + TEL_D + '</a><br><a href="mailto:' + MAIL + '">' + MAIL + '</a></address>')

FOOTER = ('<footer class="site"><div class="wrap"><div class="nap">' + NAP + '</div>'
'<nav class="site-nav" aria-label="Footer"><ul><li><a href="/records-and-gifts">What We Carry</a></li>'
'<li><a href="/visit">Visit</a></li><li><a href="/preorders">Pre-Orders</a></li><li><a href="/contact">Contact</a></li><li><a href="/privacy">Privacy</a></li></ul></nav>'
'<p class="socials"><a href="' + IG + '" rel="noopener">Instagram</a><a href="' + SHOP + '" rel="noopener">Shop Online</a></p>'
'<p class="footline">© 2026 ' + NAME + ' · new &amp; used vinyl on Sycamore Street · 22 N Sycamore St, Petersburg, VA 23803</p></div></footer>')

NAV = ('<header class="top"><div class="wrap"><a class="brand" href="/">' + MARK +
'<span class="word">' + NAME + '<small>Record store · Petersburg, VA</small></span></a>'
'<nav class="main" aria-label="Main"><ul><li><a href="/records-and-gifts">What We Carry</a></li>'
'<li><a href="/visit">Visit</a></li><li><a href="/preorders">Pre-Orders</a></li><li><a href="' + SHOP + '" rel="noopener">Shop</a></li>'
'<li><a class="btn" href="/contact">Contact</a></li></ul></nav></div></header>')

def head(title, desc, path, og=True):
    h = ['<!DOCTYPE html>\n<html lang="en">\n<head>',
    '<meta charset="utf-8">',
    '<meta name="viewport" content="width=device-width, initial-scale=1">',
    f'<title>{title}</title>',
    f'<meta name="description" content="{desc}">',
    '<meta name="robots" content="noindex, nofollow">',
    f'<link rel="canonical" href="{ORIGIN}{path}">',
    '<link rel="icon" href="/favicon.svg" type="image/svg+xml">']
    if og:
        h += [f'<meta property="og:title" content="{title}">',
        f'<meta property="og:description" content="{desc}">',
        f'<meta property="og:url" content="{ORIGIN}{path}">',
        f'<meta property="og:image" content="{ORIGIN}/og.png">',
        '<meta property="og:type" content="website">',
        '<meta name="twitter:card" content="summary_large_image">']
    h += ['<link rel="stylesheet" href="/style.css">', '</head>', '<body>',
    '<a class="skip" href="#main">Skip to content</a>', '<div class="band" aria-hidden="true"></div>']
    return "\n".join(h)

def ldwrap(graph):
    return '<script type="application/ld+json">\n' + json.dumps(graph, ensure_ascii=False, indent=1) + '\n</script>'

STORE = {
    "@type": "MusicStore",
    "@id": ORIGIN + "/#store",
    "name": NAME,
    "description": ("Independent record store in Petersburg, Virginia — new and used vinyl and CDs, hand-picked by owner Demetrius Frazier: "
                    "fresh indie releases, best sellers, audiophile-grade pressings, local artist records, and vintage staples."),
    "url": ORIGIN + "/",
    "telephone": "+1-804-504-2325",
    "email": MAIL,
    "image": ORIGIN + "/og.png",
    "address": {"@type": "PostalAddress", "streetAddress": "22 N Sycamore St, Suite A",
                "addressLocality": "Petersburg", "addressRegion": "VA", "postalCode": "23803", "addressCountry": "US"},
    "geo": {"@type": "GeoCoordinates", "latitude": GEO_LAT, "longitude": GEO_LON},
    "hasMap": MAP_LINK,
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "12:00", "closes": "18:00"}],
    "founder": {"@type": "Person", "name": "Demetrius Frazier"},
    "sameAs": [IG, SHOP],
    "keywords": "record store, vinyl, new and used vinyl, CDs, pre-orders, Petersburg Virginia",
}
def provider_ref(): return {"@id": ORIGIN + "/#store"}
def breadcrumb(path, label):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": ORIGIN + "/"},
        {"@type": "ListItem", "position": 2, "name": label, "item": ORIGIN + path}]}

# ---------------------------------------------------------------- pages
PAGES = []

home_body = (
'<main id="main">\n'
'<section class="hero"><div class="wrap"><div>'
'<span class="label">New · Independent · Petersburg, Virginia</span>'
'<h1>New &amp; used vinyl, <em>hand-picked</em> in Petersburg.</h1>'
'<p class="lede">For people who believe music has the power to connect us — casual listeners, longtime collectors, '
'and curious newcomers are all welcome on Sycamore Street.</p>'
'<div class="ctas"><a class="btn" href="/visit">Hours &amp; directions</a>'
'<a class="btn ghost" href="' + TEL_U + '">Call ' + TEL_D + '</a></div>'
'<p class="provenance">Pre-orders, restocks, and the full catalog live at <a href="' + SHOP + '" rel="noopener">thebeatdistrict.co</a>.</p>'
'</div>' + HEROART + '</div></section>\n'
'<div class="openstrip"><div class="wrap">'
'<span class="os-item"><span class="os-dot"></span>Wed–Sun · 12–6</span>'
'<span class="os-item"><span class="os-dot"></span>22 N Sycamore St, Petersburg VA 23803</span>'
'<span class="os-item"><span class="os-dot"></span><a href="' + TEL_U + '">' + TEL_D + '</a></span>'
'<span class="os-item"><span class="os-dot"></span><a href="mailto:' + MAIL + '">' + MAIL + '</a></span>'
'<span class="os-item"><span class="os-dot"></span>Black-owned</span>'
'<span class="os-item"><span class="os-dot"></span>LGBTQ+ friendly</span>'
'</div></div>\n'
'<section class="block"><div class="wrap"><div class="sechead"><div>'
'<span class="label">The pick list</span><h2>What you&rsquo;ll <em>find</em> in the crate</h2></div>'
'<a class="more" href="/records-and-gifts">What we carry &rarr;</a></div>'
+ lanes_cards() +
'</div></section>\n'
'<section class="block tight"><div class="wrap"><div class="sechead"><div>'
'<span class="label">On the racks</span><h2>Genres the shop <em>lives</em> for</h2></div></div>'
+ genre_chips() +
'<p class="provenance">The shop&rsquo;s own description: &ldquo;From hip-hop and R&amp;B to soul, jazz, rock, and beyond.&rdquo; — <a href="' + SHOP + '" rel="noopener">thebeatdistrict.co</a></p>'
'</div></section>\n'
'<div class="quotband"><div class="wrap"><span class="qmark" aria-hidden="true">&ldquo;</span>'
'<blockquote>' + MISSION + '<cite>The shop&rsquo;s own words · thebeatdistrict.co</cite></blockquote></div></div>\n'
'<section class="block"><div class="wrap"><div class="mapgrid">'
'<div class="mapcell"><iframe src="' + MAP_EMBED + '" title="Map to The Beat District, 22 N Sycamore St Ste A, Petersburg, VA 23803" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>'
'<div class="mapnote"><h3>Come dig in person</h3>'
'<p><strong>22 N Sycamore St, Suite A</strong><br>Petersburg, Virginia 23803</p>'
'<p>Open Wednesday through Sunday, 12–6.</p>'
'<p>Free local pickup on online orders — order it here, pick it up in Petersburg.</p>'
'<div class="ctas"><a class="btn" href="' + MAP_LINK + '" rel="noopener">Get directions</a><a class="btn ghost" href="/visit">Visit page</a></div>'
'</div></div></div></section>\n'
'<section class="block tight"><div class="wrap"><div class="sechead"><div>'
'<span class="label">Coming soon, first in stock</span><h2>Pre-orders open <em>before</em> release day</h2></div>'
'<a class="more" href="/preorders">How it works &rarr;</a></div>'
'<p class="lede" style="margin-top:0">Indie exclusives, colored pressings, and anniversary editions — order them on the shop site before they ship.</p>'
'<div class="ctas"><a class="btn" href="' + SHOP + '" rel="noopener">Browse pre-orders</a><a class="btn ghost" href="' + TEL_U + '">' + TEL_D + '</a></div>'
'</div></section>\n'
'<section class="callband"><div class="wrap"><h2>Wednesday through Sunday, <em>twelve to six</em>.</h2>'
'<p class="lede">22 N Sycamore Street, Petersburg. The crate is open.</p>'
'<div class="ctas"><a class="btn" href="' + TEL_U + '">Call the shop</a><a class="btn ghost" href="/contact">Send a note</a></div>'
'</div></section>\n</main>\n')
PAGES.append(dict(file="index.html", path="/", title="New & Used Vinyl — The Beat District, Petersburg VA",
    desc="Independent Petersburg VA record store: new and used vinyl and CDs hand-picked daily, plus CDs, movies, and gifts — Wed–Sun 12–6 at 22 N Sycamore St.",
    body=home_body, ld={"@context": "https://schema.org", "@graph": [STORE]}))

hub_body = (
'<main id="main">\n'
'<section class="minihero"><div class="wrap">'
'<span class="label">What we carry</span><h1>Records first — <em>but not only</em>.</h1>'
'<p class="lede">The Beat District sells new and used vinyl and CDs, hand-picked by owner Demetrius Frazier: '
'fresh indie releases, best sellers, audiophile-grade pressings, local artist records, and vintage staples.</p>'
'</div></section>\n'
'<section class="block tight"><div class="wrap"><div class="sechead"><div>'
'<span class="label">The pick list</span><h2>Six lanes, <em>one shop</em></h2></div>'
'<a class="more" href="' + SHOP + '" rel="noopener">Shop the catalog &rarr;</a></div>'
+ lanes_cards() +
'</div></section>\n'
'<section class="block tight"><div class="wrap"><div class="sechead"><div>'
'<span class="label">Genres</span><h2>Sections on the <em>racks</em></h2></div></div>'
+ genre_chips() +
'<p class="provenance">Genre sections listed on the shop&rsquo;s own catalog pages at <a href="' + SHOP + '" rel="noopener">thebeatdistrict.co</a>.</p>'
'</div></section>\n'
'<section class="block tight"><div class="wrap"><div class="sechead"><div>'
'<span class="label">Off the racks, too</span><h2>For the person who has <em>every record</em></h2></div></div>'
'<p class="lede" style="margin-top:0">The shop&rsquo;s own catalog categories cover gifts and goods as well as music:</p>'
'<div class="chips" style="margin-top:18px">'
'<span class="chip">Candles + Incense</span><span class="chip">Housewares</span><span class="chip">Bath + Body</span>'
'<span class="chip">Novelties</span><span class="chip">Books</span><span class="chip">Toys + Games</span>'
'<span class="chip">Music Accessories</span><span class="chip">Clothing</span><span class="chip">Baby/Kids</span>'
'<span class="chip">Wellness</span><span class="chip">Candy</span><span class="chip">Movies</span></div>'
'<p class="provenance">And shop campaigns rotate through: Record Store Day Black Friday, Rhino Rocktober, New Music Friday, and anniversary editions — all listed in the online catalog.</p>'
'</div></section>\n'
'<section class="callband"><div class="wrap"><h2>Not sure what you&rsquo;re <em>after</em>?</h2>'
'<p class="lede">Call the shop and describe it — someone there can point you to the right crate.</p>'
'<div class="ctas"><a class="btn" href="' + TEL_U + '">' + TEL_D + '</a><a class="btn ghost" href="/contact">Send a note</a></div>'
'</div></section>\n</main>\n')
PAGES.append(dict(file="records-and-gifts.html", path="/records-and-gifts",
    title="Vinyl, CDs & Gifts — The Beat District, Petersburg VA",
    desc="New and used vinyl, CDs, movies, and gifts — indie exclusives, best sellers, audiophile pressings, local artists, and vintage staples in Petersburg VA.",
    body=hub_body, ld={"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": "Retail — new and used vinyl, CDs, movies, and gifts",
         "serviceType": "Retail", "url": ORIGIN + "/records-and-gifts",
         "provider": provider_ref(),
         "areaServed": {"@type": "City", "name": "Petersburg", "addressRegion": "VA"}},
        breadcrumb("/records-and-gifts", "What We Carry")]}))

faq_items = [
    ("Is online stock the same as in-store stock?",
     "No — the shop&rsquo;s own note is plain: &ldquo;In Stock&rdquo; online means quick order fulfillment, generally 2–3 business days, and online prices can differ from the shop floor."),
    ("Can I pick up online orders in Petersburg?",
     "Yes — free local pickup in Petersburg is offered on online orders."),
    ("Do you stock local artists?",
     "Yes — records from local artists are part of the shop&rsquo;s pick list."),
]
visit_faq = "".join('<details><summary>' + q + '</summary><p>' + a + '</p></details>' for q, a in faq_items)
visit_body = (
'<main id="main">\n'
'<section class="minihero"><div class="wrap">'
'<span class="label">Visit</span><h1>Find us on <em>Sycamore Street</em>.</h1>'
'<p class="lede">Open Wednesday through Sunday, 12–6 — Suite A at 22 N Sycamore Street, Petersburg, Virginia 23803.</p>'
'</div></section>\n'
'<section class="block tight"><div class="wrap"><div class="mapgrid">'
'<div class="mapcell"><iframe src="' + MAP_EMBED + '" title="Map to The Beat District, 22 N Sycamore St Ste A, Petersburg, VA 23803" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>'
'<div class="mapnote"><h3>The details</h3>'
'<p><strong>Address</strong><br>22 N Sycamore St, Suite A<br>Petersburg, VA 23803</p>'
'<p><strong>Hours</strong><br>Wednesday–Sunday, 12:00–18:00</p>'
'<p><strong>Phone</strong> <a href="' + TEL_U + '">' + TEL_D + '</a><br><strong>Email</strong> <a href="mailto:' + MAIL + '">' + MAIL + '</a></p>'
'<div class="ctas"><a class="btn" href="' + MAP_LINK + '" rel="noopener">Get directions</a></div>'
'</div></div>'
'<p class="provenance">Black-owned · LGBTQ+ friendly — from the shop&rsquo;s Google Business Profile.</p>'
'</div></section>\n'
'<section class="block tight"><div class="wrap"><div class="sechead"><div>'
'<span class="label">Good to know</span><h2>Before you <em>dig</em></h2></div></div>'
'<div class="faq">' + visit_faq + '</div></div></section>\n'
'<section class="block tight"><div class="wrap">'
'<span class="label">Who&rsquo;s behind the counter</span>'
'<h2>A new shop, run by the <em>person picking the records</em></h2>'
'<p class="lede">The Beat District opened in fall 2026 and is run by Demetrius Frazier, who also runs Resist Booksellers just down the street. '
'Coverage of the opening notes that he hand-picks the vinyl himself — from fresh indie releases to best sellers, '
'audiophile-grade pressings, local artist records, and vintage staples.</p>'
'<p class="provenance">Source: 12onyourside.com, &ldquo;What&rsquo;s New in RVA&rdquo;, November 2, 2026.</p>'
'</div></section>\n'
'<section class="callband"><div class="wrap"><h2>Twelve to six, <em>Wednesday through Sunday</em>.</h2>'
'<p class="lede">22 N Sycamore Street, Petersburg — email works too: <a href="mailto:' + MAIL + '">' + MAIL + '</a>.</p>'
'<div class="ctas"><a class="btn" href="' + TEL_U + '">Call the shop</a><a class="btn ghost" href="/preorders">Pre-orders</a></div>'
'</div></section>\n</main>\n')
PAGES.append(dict(file="visit.html", path="/visit",
    title="Hours, Directions & In-Store Digging — The Beat District, Petersburg VA",
    desc="Visit The Beat District: Wed–Sun 12–6 at 22 N Sycamore St Ste A, Petersburg VA 23803. Call (804) 504-2325. Black-owned, LGBTQ+ friendly record shop.",
    body=visit_body, ld={"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": "In-store vinyl and CD shopping", "serviceType": "Record store",
         "url": ORIGIN + "/visit", "provider": provider_ref(),
         "areaServed": {"@type": "City", "name": "Petersburg", "addressRegion": "VA"}},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q.replace("&rsquo;", "'").replace("&ldquo;", '"').replace("&rdquo;", '"'),
             "acceptedAnswer": {"@type": "Answer", "text": a.replace("&rsquo;", "'").replace("&ldquo;", '"').replace("&rdquo;", '"')}}
            for q, a in faq_items]},
        breadcrumb("/visit", "Visit")]}))

pre_body = (
'<main id="main">\n'
'<section class="minihero"><div class="wrap">'
'<span class="label">Pre-orders &amp; online shop</span><h1>Order it <em>before</em> release day.</h1>'
'<p class="lede">The shop&rsquo;s online catalog carries pre-orders, indie exclusives, new releases, and recent restocks — '
'with free local pickup in Petersburg.</p>'
'<div class="ctas"><a class="btn" href="' + SHOP + '" rel="noopener">Browse the shop</a><a class="btn ghost" href="' + TEL_U + '">' + TEL_D + '</a></div>'
'</div></section>\n'
'<section class="block tight"><div class="wrap"><div class="sechead"><div>'
'<span class="label">How pre-orders work</span><h2>Release date, label, <em>pressing color</em></h2></div></div>'
'<div class="prose"><p>Upcoming releases open for pre-order on the shop site with the release date, the label, '
'and the pressing called out — indie-exclusive orange, midnight purple, stoney orange, neon pink. '
'Anniversary editions and Record Store Day releases ride the same list.</p>'
'<p><strong>Quick order fulfillment, generally 2–3 business days.</strong> The shop&rsquo;s own note: &ldquo;In Stock&rdquo; online '
'means quick order fulfillment — online prices and stock can differ from the shop floor.</p>'
'<p><strong>Free local pickup in Petersburg.</strong> Order online, pick it up in Petersburg.</p></div>'
'</div></section>\n'
'<section class="block tight"><div class="wrap"><div class="sechead"><div>'
'<span class="label">Lists worth following</span><h2>Where the <em>news</em> lives</h2></div></div>'
'<div class="chips"><a class="chip alt" href="' + SHOP + '" rel="noopener">New Releases</a>'
'<a class="chip alt" href="' + SHOP + '" rel="noopener">Pre-Orders</a>'
'<a class="chip alt" href="' + SHOP + '" rel="noopener">Recent Online Restocks</a>'
'<a class="chip alt" href="' + SHOP + '" rel="noopener">Music Top Sellers</a>'
'<a class="chip alt" href="' + SHOP + '" rel="noopener">New Music Friday</a>'
'<a class="chip alt" href="' + SHOP + '" rel="noopener">Record Store Day Black Friday</a>'
'<a class="chip alt" href="' + SHOP + '" rel="noopener">Movies</a></div>'
'<p class="provenance">Arrival and event posts land on the shop&rsquo;s News page and its Instagram, <a href="' + IG + '" rel="noopener">@thebeatdistrict_pva</a>.</p>'
'</div></section>\n'
'<section class="callband"><div class="wrap"><h2>Want something that isn&rsquo;t <em>listed</em>?</h2>'
'<p class="lede">Call or email the shop with the artist and pressing — that reaches Petersburg directly.</p>'
'<div class="ctas"><a class="btn" href="' + TEL_U + '">' + TEL_D + '</a><a class="btn ghost" href="mailto:' + MAIL + '">' + MAIL + '</a></div>'
'</div></section>\n</main>\n')
PAGES.append(dict(file="preorders.html", path="/preorders",
    title="Pre-Orders & Online Shop — The Beat District, Petersburg VA",
    desc="Pre-order vinyl releases, indie exclusives, and anniversary editions before release day. Quick fulfillment 2–3 business days; free local pickup in Petersburg.",
    body=pre_body, ld={"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": "Online record store with pre-orders and free local pickup",
         "serviceType": "Retail", "url": ORIGIN + "/preorders", "provider": provider_ref(),
         "areaServed": {"@type": "City", "name": "Petersburg", "addressRegion": "VA"}},
        breadcrumb("/preorders", "Pre-Orders")]}))

contact_body = (
'<main id="main">\n'
'<section class="minihero"><div class="wrap">'
'<span class="label">Contact</span><h1>Talk to the <em>shop</em>.</h1>'
'<p class="lede">Email always works: <a href="mailto:' + MAIL + '">' + MAIL + '</a>. Phone between twelve and six, '
'Wednesday through Sunday: <a href="' + TEL_U + '">' + TEL_D + '</a>. Or leave a note below and it gets read and answered.</p>'
'</div></section>\n'
'<section class="block tight"><div class="wrap"><div class="mapgrid">'
'<div class="mapnote" style="grid-column:1"><h3>Send a note</h3>'
'<form class="cform" method="post" action="/contact">'
'<div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" required autocomplete="name"></div>'
'<div class="field"><label for="f-phone">Phone (optional)</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>'
'<div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email"></div>'
'<div class="field"><label for="f-msg">What are you looking for?</label><textarea id="f-msg" name="message" required placeholder="Artist, pressing, color — whatever you&rsquo;re hunting for."></textarea></div>'
'<p class="cform-note">Name and message are enough. The form is the slow door — email and phone are the fast ones.</p>'
'<div class="ctas"><button class="btn" type="submit">Send</button></div>'
'</form></div>'
'<div class="mapnote"><h3>Or come by</h3>'
'<p><strong>Address</strong><br>22 N Sycamore St, Suite A<br>Petersburg, VA 23803</p>'
'<p><strong>Hours</strong><br>Wednesday–Sunday, 12:00–18:00</p>'
'<p><strong>Direct lines</strong><br><a href="' + TEL_U + '">' + TEL_D + '</a><br><a href="mailto:' + MAIL + '">' + MAIL + '</a></p>'
'<p><strong>Full catalog</strong><br><a href="' + SHOP + '" rel="noopener">thebeatdistrict.co</a></p>'
'</div></div></div></section>\n</main>\n')
PAGES.append(dict(file="contact.html", path="/contact",
    title="Contact — The Beat District, Petersburg VA",
    desc="Contact The Beat District record store in Petersburg VA: email info@thebeatdistrict.co, call (804) 504-2325, or send a note — Wed–Sun 12–6.",
    body=contact_body, ld={"@context": "https://schema.org", "@graph": [
        {"@type": "ContactPage", "name": "Contact " + NAME, "url": ORIGIN + "/contact"},
        breadcrumb("/contact", "Contact")]}))

priv_body = (
'<main id="main">\n'
'<section class="minihero"><div class="wrap">'
'<span class="label">Privacy</span><h1>Small shop site, <em>small print</em>.</h1>'
'</div></section>\n'
'<section class="block tight"><div class="wrap"><div class="prose">'
'<p>This website sets <strong>no cookies</strong> and carries <strong>no third-party trackers or scripts</strong> — '
'there is nothing running in the background while you read.</p>'
'<p>The only third-party content is the <strong>Google Maps embed</strong> on the visit page. When a map loads, '
'Google receives standard request data (such as an IP address) the same way it does for any embedded map.</p>'
'<p>The contact form collects what you type into it — your name, phone, email, and message — so the note can be '
'read and answered. It is not sold, and it is not used for anything else.</p>'
'<p>The full record catalog lives on the shop&rsquo;s own store site, <a href="' + SHOP + '" rel="noopener">thebeatdistrict.co</a>, '
'which keeps its own cookie and privacy practices.</p>'
'<p>Questions about anything on this page: <a href="mailto:' + MAIL + '">' + MAIL + '</a>.</p>'
'</div></div></section>\n</main>\n')
PAGES.append(dict(file="privacy.html", path="/privacy",
    title="Privacy — The Beat District",
    desc="This record-store website sets no cookies and runs no trackers. The contact form stores what you submit so the shop can answer.",
    body=priv_body, ld={"@context": "https://schema.org", "@graph": [
        {"@type": "PrivacyPolicy", "name": "Privacy — " + NAME, "url": ORIGIN + "/privacy"},
        breadcrumb("/privacy", "Privacy")]}))

nf_body = (
'<main id="main"><section class="block util"><div class="wrap">'
'<span class="label">404</span><h1>That sleeve isn&rsquo;t in <em>this crate</em>.</h1>'
'<p class="lede">Try the record lanes, the visit page, or the shop&rsquo;s own catalog.</p>'
'<div class="ctas" style="margin-top:26px"><a class="btn" href="/records-and-gifts">What we carry</a>'
'<a class="btn ghost" href="/visit">Visit</a><a class="btn ghost" href="' + SHOP + '" rel="noopener">Shop online</a></div>'
'</div></section></main>\n')
PAGES.append(dict(file="404.html", path="/404", title="Page Not Found — The Beat District",
    desc="That page isn't at The Beat District site. Jump to the record lanes, the visit page, or the shop's own online catalog.",
    body=nf_body, ld=None, og=False))

th_body = (
'<main id="main"><section class="block util"><div class="wrap">'
'<span class="label">Received</span><h1>Your note is <em>in</em></h1>'
'<p class="lede">It gets read and answered. For anything urgent, email or phone reach the shop directly — '
'and arrival news lands on the shop&rsquo;s News page and Instagram first.</p>'
'<div class="ctas" style="margin-top:24px"><a class="btn" href="' + IG + '" rel="noopener">Instagram</a>'
'<a class="btn ghost" href="/">Back to home</a></div>'
'</div></section></main>\n')
PAGES.append(dict(file="thanks.html", path="/thanks", title="Thanks — The Beat District",
    desc="Your note reached the shop site. For anything urgent, email or phone reach The Beat District in Petersburg directly.",
    body=th_body, ld=None, og=False))

# ---------------------------------------------------------------- emit
def render(p):
    doc = [head(p["title"], p["desc"], p["path"], og=p.get("og", True))]
    doc.append(NAV)
    doc.append(p["body"])
    doc.append(FOOTER)
    doc.append("<!-- BUILT-2026-11-21 -->")
    if p.get("ld"):
        doc.append(ldwrap(p["ld"]))
    doc.append("</body>\n</html>")
    return "\n".join(doc)

for p in PAGES:
    with open(os.path.join(OUT, p["file"]), "w", encoding="utf-8") as f:
        f.write(render(p))
    print("wrote", p["file"])

SITEMAP_PATHS = ["/", "/records-and-gifts", "/visit", "/preorders", "/contact", "/privacy"]
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for path in SITEMAP_PATHS:
    sm.append(f"<url><loc>{ORIGIN}{path}</loc><lastmod>2026-11-21</lastmod></url>")
sm.append("</urlset>")
open(os.path.join(OUT, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
open(os.path.join(OUT, "robots.txt"), "w").write(
    "User-agent: *\nAllow: /\n\nSitemap: " + ORIGIN + "/sitemap.xml\n")
print("wrote sitemap.xml robots.txt")
