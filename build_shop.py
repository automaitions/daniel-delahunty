#!/usr/bin/env python3
# Builds the Shopify-style ebook funnel for the Daniel site:
#  - 7 product pages (ebook-<slug>.html): cover, price, what's-inside, teaser pages, related guides, add-to-cart
#  - bundle.html: all 7 covers, what-you-get, $129 add-to-cart
# Reuses the EXACT nav/drawer/footer from ebooks.html so the chrome is identical.
import os
D = os.path.dirname(os.path.abspath(__file__))

# ---- shared chrome (verbatim from ebooks.html, Shop active) ----
HEAD = lambda title, desc: f'''<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} | Daniel Delahunty</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#16181C">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%2316181C'/%3E%3Ctext x='16' y='23' font-family='Arial,sans-serif' font-size='19' font-weight='bold' fill='%2300DDD6' text-anchor='middle'%3ED%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Anton&family=Archivo:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/daniel.css">
<script>document.documentElement.className='js';</script>
</head>
<body>'''

NAV = '''<nav class="nav" id="nav">
  <a href="index.html" class="nav__brand">Daniel Delahunty</a>
  <div class="nav__links"><a href="index.html" class="nav__link">Home</a><div class="has-drop"><a href="coaching.html" class="nav__link">Coaching ▾</a><div class="drop"><a href="rise-above.html">Rise Above — 8-Week</a><a href="lean-for-life.html">Lean For Life</a><a href="in-person.html">In-Person (Gold Coast)</a></div></div><a href="pricing.html" class="nav__link">Pricing</a><a href="results.html" class="nav__link">Results</a><div class="has-drop"><a href="ebooks.html" class="nav__link is-active">Shop ▾</a><div class="drop"><a href="ebooks.html">E-books</a><a href="bundle.html">Ebook Bundle</a></div></div><a href="macros.html" class="nav__link">Macros</a><a href="faqs.html" class="nav__link">FAQs</a></div>
  <a href="contact.html" class="nav__cta">Free Consult</a>
  <button class="burger" id="burger" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
</nav>
<div class="drawer" id="drawer">
  <a href="index.html" class="drawer__item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M4 11l8-7 8 7M6 10v9h12v-9"/></svg>Home</a>
  <button class="drawer__item" id="coachToggle" aria-expanded="false" aria-controls="coachSub"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 9v6M6 7v10M9 12h6M18 7v10M21 9v6"/></svg>Coaching<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button>
  <div class="drawer__sub" id="coachSub">
    <a href="rise-above.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M4 7h16v13H4zM4 7l2-3h12l2 3M9 11h6"/></svg>Rise Above — 8-Week</a>
    <a href="lean-for-life.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 12a3 3 0 100-.1M17 12a3 3 0 110-.1M7 12c0-3 3-5 5-5s5 2 5 5-3 5-5 5-5-2-5-5z"/></svg>Lean For Life — Online</a>
    <a href="in-person.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M12 21s7-6.5 7-12a7 7 0 10-14 0c0 5.5 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/></svg>In-Person (Gold Coast)</a>
  </div>
  <a href="pricing.html" class="drawer__item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 1v22M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>Pricing</a>
  <a href="results.html" class="drawer__item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M6 4h12v4a6 6 0 01-12 0zM6 6H3v2a3 3 0 003 3M18 6h3v2a3 3 0 01-3 3M9 18h6M10 14h4v4h-4z"/></svg>Client Results</a>
  <button class="drawer__item" id="shopToggle" aria-expanded="false" aria-controls="shopSub"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M6 7h12l1 14H5zM9 7a3 3 0 016 0"/></svg>Shop<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button>
  <div class="drawer__sub" id="shopSub">
    <a href="ebooks.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M3 4h7a3 3 0 013 3v13a2 2 0 00-2-2H3zM21 4h-7a3 3 0 00-3 3v13a2 2 0 012-2h8z"/></svg>E-books</a>
    <a href="bundle.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M6 7h12l1 14H5zM9 7a3 3 0 016 0"/></svg>Ebook Bundle</a>
  </div>
  <a href="macros.html" class="drawer__item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 11h2M12 11h2M16 11h.01M8 15h2M12 15h2M16 15h.01"/></svg>Macro Calculator</a>
  <a href="faqs.html" class="drawer__item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 015 0c0 2-2.5 2-2.5 4M12 17h.01"/></svg>FAQs</a>
  <div class="drawer__foot">
    <a href="contact.html" class="btn btn--primary">Book a Free Consult</a>
    <a href="tel:0402451924" class="btn btn--ghost" style="color:#fff;border-color:rgba(255,255,255,.4)">Call Daniel</a>
  </div>
</div>'''

FOOTER = '''<footer class="footer">
  <div class="wrap">
    <div class="footer__top">
      <div>
        <div class="footer__brand">Daniel Delahunty</div>
        <p style="margin-top:8px;max-width:32ch;font-size:14px">Sustainable coaching for results you keep. Gold Coast &amp; online.</p>
      </div>
      <div class="footer__links">
        <div class="footer__col"><h4>Coaching</h4><a href="coaching.html">Coaching</a><a href="pricing.html">Pricing</a><a href="results.html">Results</a><a href="ebooks.html">Ebooks</a></div>
        <div class="footer__col"><h4>Shop</h4><a href="ebooks.html">All E-books</a><a href="bundle.html">The Bundle</a><a href="macros.html">Macro Calculator</a></div>
        <div class="footer__col"><h4>Connect</h4><a href="mailto:pt@danieldelahunty.com">Email</a><a href="tel:0402451924">0402 451 924</a><a href="https://instagram.com/hardazbodz" target="_blank" rel="noopener">Instagram</a><a href="https://facebook.com/delahuntyfitness" target="_blank" rel="noopener">Facebook</a></div>
      </div>
    </div>
    <div class="footer__bot"><span>© 2026 Daniel Delahunty. All rights reserved.</span><span>Sustainable personal training · Gold Coast, AU</span></div>
  </div>
</footer>
<script src="assets/daniel.js" defer></script>
</body>
</html>'''

PRICE = "25.99"
# ---- the 7 guides (order matters for related rotation) ----
BOOKS = [
 dict(slug="muscle-code", title="The Muscle Code", folder="ebook-muscle-code", cover="p-000.jpg",
   tag="Build lean muscle the sustainable way — without living in the gym or guessing your way through every session.",
   teasers=["p-002.jpg","p-003.jpg","p-005.jpg"], life=False,
   bullets=["How much you really need to train to grow","Setting protein &amp; calories for a lean gain","Progressive overload made simple","Why recovery is where muscle is actually built","A weekly structure you can genuinely keep"],
   paras=["Building muscle isn't about training until you break — it's about training and eating with intent. The Muscle Code lays out the few things that actually move the needle: progressive overload, enough protein, and recovery that lets the work pay off.",
          "No fluff, no six-day splits you can't sustain. Just the principles Daniel uses with clients to add lean size without putting the rest of life on hold."],
   bestfor="Anyone who wants to add lean muscle without the guesswork."),
 dict(slug="protein", title="Protein Playbook", folder="ebook-protein", cover="p-000.jpg",
   tag="Hit your protein every day without overthinking it — simple swaps, a go-to food list, and meals that actually fit your life.",
   teasers=["p-016.jpg","p-017.jpg","p-018.jpg"], life=False,
   bullets=["Exactly how much protein you need","A high-protein food list for every budget","Quick meals &amp; snacks that hit your target","Vegetarian &amp; dairy-free options","How to hit protein when you're busy or eating out"],
   paras=["Protein is the one macro almost everyone gets wrong — too little, badly timed, or from sources they don't enjoy. The Protein Playbook makes it effortless: how much you need, where to get it, and how to hit it even on your busiest days.",
          "Packed with simple swaps, high-protein meal ideas and a go-to food list, so you never stare into the fridge wondering what to eat."],
   bestfor="Anyone who struggles to hit their protein day after day."),
 dict(slug="mealprep", title="Meal Prep Made Simple", folder="ebook-mealprep", cover="p-000.jpg",
   tag="Prep once, eat well all week — a repeatable system that takes the daily decision out of eating healthy.",
   teasers=["p-004.jpg","p-005.jpg","p-019.jpg"], life=False,
   bullets=["A simple, repeatable weekly prep system","Batch-cook without burning a whole Sunday","Storage &amp; reheating that keeps food fresh","Balanced meal templates to mix &amp; match","A shopping list that makes prep faster"],
   paras=["Most people quit healthy eating because it's a daily decision. Meal Prep Made Simple removes the decision — one short session sets you up for the week, so the easy choice is also the right one.",
          "It's a repeatable system: pick your meals, batch-cook smart, store it right, and never resort to the drive-through because you're out of options."],
   bestfor="Busy people who want healthy eating to run on autopilot."),
 dict(slug="flexible", title="Flexible Dieting", folder="ebook-flexible", cover="p-000.jpg",
   tag="Eat the foods you love and still hit your goals — work to targets, not rules, so nothing is ever off the table.",
   teasers=["p-003.jpg","p-004.jpg"], life=False,
   bullets=["What flexible dieting actually means","How to fit treats in without the guilt","Building meals around your daily targets","Handling eating out &amp; social events","Why this is the approach you can keep"],
   paras=["Dieting fails when it bans everything you enjoy. Flexible dieting flips that — you work to targets, not rules, so chocolate, pasta and a night out can all fit.",
          "This guide shows you how to track what matters, build meals around your day, and stay on track without the all-or-nothing spiral."],
   bestfor="Anyone tired of restrictive diets that never last."),
 dict(slug="fuel", title="Fuel For Life", folder="ebook-fuel", cover="p-000.jpg",
   tag="Everyday nutrition that keeps you going — the fundamentals done right, built to hold for life, not six weeks.",
   teasers=["p-007.jpg","p-008.jpg","p-009.jpg"], life=False,
   bullets=["The fundamentals of eating well","Balanced plates without counting every gram","Energy &amp; hydration through the day","Habits that outlast any quick fix","How to eat for your lifestyle, not against it"],
   paras=["Fuel For Life is the foundation — not a crash plan, but the eating habits that hold for the long run. It's about energy, health and feeling good in your day-to-day.",
          "Covers the basics done right: balanced plates, hydration, steady energy, and how to eat for the way you actually live."],
   bestfor="Anyone who wants a sustainable foundation, not another fad."),
 dict(slug="inflammation", title="Inflammation Reset", folder="ebook-inflammation", cover="img-003.jpg",
   tag="Eat to recover and feel lighter — the foods that calm the body, and the ones quietly working against you.",
   teasers=["img-006.jpg","img-007.jpg","img-008.jpg"], life=False,
   bullets=["Foods that help fight inflammation","Common triggers to ease off","Simple anti-inflammatory meals","How nutrition speeds your recovery","A gentle reset you can actually stick to"],
   paras=["Persistent bloating, stiffness and low energy often trace back to what's on your plate. The Inflammation Reset shows you the foods that calm the body — and the ones quietly working against you.",
          "It's a practical reset: what to add, what to ease off, and simple meals that help you recover and feel lighter."],
   bestfor="Anyone dealing with bloating, stiffness or low energy."),
 dict(slug="femme-slimdown", title="Femme Body Slimdown", folder="ebook-femme-slimdown", cover="cover.jpg",
   tag="A sustainable slimdown made for women — realistic nutrition, the right training, and recipes you'll look forward to.",
   teasers=["recipe-protein-pancakes.jpg","macro-food-spread.jpg","recipe-chicken-salad.jpg"], life=True,
   bullets=["A nutrition approach built for women","Training that builds shape, not just sweat","Recipes you'll actually look forward to","Fat loss without crash dieting or endless cardio","Habits that keep the results in place"],
   paras=["Built specifically for women who want to lean down without crash diets or hours of cardio. The Femme Body Slimdown blends realistic nutrition, the right training and recipes you'll genuinely look forward to.",
          "It's about working with your body, not punishing it — sustainable fat loss that fits a real life."],
   bestfor="Women who want to lean down and keep it off."),
]
BY = {b["slug"]: b for b in BOOKS}

def cover_path(b): return f'photos/{b["folder"]}/{b["cover"]}'

def book_card(b):
    return (f'<article class="book reveal"><div class="book__img"><a href="ebook-{b["slug"]}.html">'
            f'<img src="{cover_path(b)}" alt="{b["title"]} ebook cover" loading="lazy"></a></div>'
            f'<div class="book__b"><h3><a href="ebook-{b["slug"]}.html">{b["title"]}</a></h3>'
            f'<div class="book__price">${PRICE}</div><p>{b["tag"].split(" — ")[0]}.</p>'
            f'<div class="book__act"><a href="ebook-{b["slug"]}.html" class="btn btn--ghost">Preview</a>'
            f'<button class="btn btn--primary add-cart" data-title="{b["title"]}" data-price="{PRICE}">Add</button></div></div></article>')

def product_page(b, idx):
    related = [BOOKS[(idx+1)%7], BOOKS[(idx+2)%7], BOOKS[(idx+3)%7]]
    teaser_html = "".join(f'<figure class="reveal"><img src="photos/{b["folder"]}/{t}" alt="A page from {b["title"]}" loading="lazy"></figure>' for t in b["teasers"])
    peek_cls = "peek peek--life" if b["life"] else "peek"
    bullets = "".join(f"<li>{x}</li>" for x in b["bullets"])
    paras = "".join(f"<p>{p}</p>" for p in b["paras"])
    related_html = "".join(book_card(r) for r in related)
    return f'''{HEAD(b["title"], b["tag"])}
{NAV}
<main>
<section class="s prodwrap"><div class="wrap">
  <div class="crumb reveal"><a href="ebooks.html">Shop</a><i>/</i><a href="ebooks.html">E-books</a><i>/</i><span>{b["title"]}</span></div>
  <div class="prod">
    <div class="prod__cover reveal"><img src="{cover_path(b)}" alt="{b["title"]} ebook cover"></div>
    <div class="prod__info reveal">
      <div class="eyebrow">Digital guide · E-book</div>
      <h1 class="prod__title">{b["title"]}</h1>
      <div class="prod__stars">★★★★★ <span>Loved by Daniel's clients</span></div>
      <div class="prod__price">${PRICE} <small>AUD · instant download</small></div>
      <p class="prod__tag lead">{b["tag"]}</p>
      <ul class="prod__list">{bullets}</ul>
      <div class="prod__cta">
        <button class="btn btn--primary btn--lg add-cart" data-title="{b["title"]}" data-price="{PRICE}">Add to cart — ${PRICE}</button>
        <a href="bundle.html" class="btn btn--ghost btn--lg">Get all 7 — save $53</a>
      </div>
      <div class="prod__meta"><span>Instant PDF</span><span>Read on any device</span><span>By Daniel Delahunty</span></div>
    </div>
  </div>
</div></section>

<section class="s s--dark"><div class="wrap">
  <div class="s-head center reveal"><div class="eyebrow">A peek inside</div><div class="h-sub">See it before you buy.</div></div>
  <div class="{peek_cls}">{teaser_html}</div>
  <p class="peek__note reveal">A few real pages from inside the guide.</p>
</div></section>

<section class="s"><div class="wrap">
  <div class="inside reveal">
    <div class="eyebrow">Inside this guide</div>
    <h2 class="h-sub" style="margin-top:12px">What you'll learn.</h2>
    {paras}
    <div class="bestfor"><strong>Best for</strong>{b["bestfor"]}</div>
  </div>
</div></section>

<section class="s" style="padding-top:0"><div class="wrap">
  <div class="buystrip reveal">
    <h2>Start reading <em>today.</em></h2>
    <p>Instant download, yours to keep, read on any device. Or get all seven guides together and save $53.</p>
    <div class="buystrip__cta">
      <button class="btn btn--ondark btn--lg add-cart" data-title="{b["title"]}" data-price="{PRICE}">Add {b["title"]} — ${PRICE}</button>
      <a href="bundle.html" class="btn btn--primary btn--lg">Get the bundle — $129</a>
    </div>
  </div>
</div></section>

<section class="s" style="padding-top:0"><div class="wrap">
  <div class="s-head reveal"><div class="eyebrow">Keep going</div><h2 class="h-sub" style="margin-top:10px">More guides you'll like.</h2></div>
  <div class="books">{related_html}</div>
</div></section>
</main>
{FOOTER}'''

def bundle_page():
    lib = "".join(f'<a href="ebook-{b["slug"]}.html"><div class="lib__img"><img src="{cover_path(b)}" alt="{b["title"]} cover" loading="lazy"></div><div class="lib__t">{b["title"]}</div></a>' for b in BOOKS)
    titles = "".join(f"<li>{b['title']}</li>" for b in BOOKS)
    # teaser strip = one nice page from a few books
    teasers = [("ebook-protein","p-017.jpg",False),("ebook-mealprep","p-005.jpg",False),("ebook-femme-slimdown","macro-food-spread.jpg",True)]
    teaser_html = "".join(f'<figure class="reveal"><img src="photos/{f}/{img}" alt="A page from the bundle" loading="lazy"></figure>' for f,img,_ in teasers)
    return f'''{HEAD("The Complete Library — All 7 Guides", "Get all 7 of Daniel Delahunty's nutrition &amp; training guides in one bundle — save $53.")}
{NAV}
<main>
<section class="s prodwrap"><div class="wrap">
  <div class="crumb reveal"><a href="ebooks.html">Shop</a><i>/</i><span>The Bundle</span></div>
  <div class="prod">
    <div class="prod__cover reveal" style="aspect-ratio:3/4;background:var(--ink);display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:6px">
      <img src="{cover_path(BY["muscle-code"])}" alt="" style="border-radius:8px">
      <img src="{cover_path(BY["protein"])}" alt="" style="border-radius:8px">
      <img src="{cover_path(BY["fuel"])}" alt="" style="border-radius:8px">
      <img src="{cover_path(BY["femme-slimdown"])}" alt="" style="border-radius:8px">
    </div>
    <div class="prod__info reveal">
      <div class="eyebrow">The complete library · 7 e-books</div>
      <h1 class="prod__title">Get All 7 Guides</h1>
      <div class="prod__stars">★★★★★ <span>The full nutrition &amp; training library</span></div>
      <div class="prod__price">$129 <span class="strike">$181.93</span></div>
      <span class="savetag">Save $53 — one click, all seven</span>
      <p class="prod__tag lead">Every guide Daniel has written, together in one bundle — from building muscle and hitting protein to meal prep, flexible dieting and resetting inflammation. The complete toolkit to eat, train and recover the sustainable way.</p>
      <ul class="prod__list">{titles}</ul>
      <div class="prod__cta">
        <button class="btn btn--primary btn--lg add-cart" data-title="All 7 Guides — Bundle" data-price="129">Add the bundle — $129</button>
        <a href="ebooks.html" class="btn btn--ghost btn--lg">Browse single guides</a>
      </div>
      <div class="prod__meta"><span>7 instant PDFs</span><span>Read on any device</span><span>Save $53 vs buying separately</span></div>
    </div>
  </div>
</div></section>

<section class="s s--dark"><div class="wrap">
  <div class="s-head center reveal"><div class="eyebrow">Everything you get</div><div class="h-sub">Seven guides. One price.</div><p class="lead">Tap any guide to see what's inside.</p></div>
  <div class="lib">{lib}</div>
</div></section>

<section class="s"><div class="wrap">
  <div class="s-head center reveal"><div class="eyebrow">A peek inside</div><div class="h-sub">Real pages from the library.</div></div>
  <div class="peek">{teaser_html}</div>
</div></section>

<section class="s" style="padding-top:0"><div class="wrap">
  <div class="buystrip reveal">
    <h2>The whole library for <em>$129.</em></h2>
    <p>That's all seven guides for less than the price of five — and $53 off buying them one by one. Instant download, yours to keep.</p>
    <div class="buystrip__cta">
      <button class="btn btn--ondark btn--lg add-cart" data-title="All 7 Guides — Bundle" data-price="129">Add the bundle — $129</button>
      <a href="contact.html" class="btn btn--primary btn--lg">Or book a free consult</a>
    </div>
  </div>
</div></section>
</main>
{FOOTER}'''

n=0
for i,b in enumerate(BOOKS):
    open(os.path.join(D, f'ebook-{b["slug"]}.html'),"w").write(product_page(b,i)); n+=1
open(os.path.join(D,"bundle.html"),"w").write(bundle_page()); n+=1
print(f"built {n} pages:", ", ".join(f'ebook-{b["slug"]}.html' for b in BOOKS), "+ bundle.html")
