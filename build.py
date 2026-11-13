#!/usr/bin/env python3
"""Builds the static preview of the new CFS Designs US website (GitHub Pages, preview.cfsdesignsus.com).
Run: python3 build.py  -> writes the HTML pages next to this file. Data: data/projects.json."""
import html, json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(ROOT, "data/projects.json")))
E = html.escape

SECTOR = {
    "wardman": "Residential", "225": "Residential", "pike": "Mixed use", "cultural": "Mixed use", "gmu": "Education",
    "south": "Public", "pickersgille": "Senior living", "some1515": "Residential", "255": "Mixed use",
    "toledo": "Residential", "subaru": "Commercial", "embrey": "Healthcare", "drc": "Public", "courtyard": "Hospitality",
    "7607": "Residential", "private": "Residential", "wmata": "Public", "choice": "Residential", "jhu": "Education",
    "lbh": "Healthcare", "accolade": "Residential", "tidewater": "Education", "oven": "Industrial", "fh": "Commercial",
    "gensler": "Commercial", "gsa": "Public", "weta": "Commercial", "20mass": "Residential", "dsu": "Education",
    "kisco": "Senior living", "inovawood": "Healthcare", "citi": "Commercial", "deloitte": "Education",
    "tcat": "Education", "abrc": "Commercial", "tldelockcondos": "Residential", "tidelockrental": "Mixed use",
    "edgewood": "Residential", "400-belgrade": "Residential", "7-eleven-pg-plaza": "Commercial",
    "1265-main-street": "Commercial", "1200-bladensburg": "Mixed use",
}
SECTORS = ["Residential", "Mixed use", "Commercial", "Education", "Healthcare", "Senior living", "Public", "Hospitality", "Industrial"]
FEATURED = ["tidelockrental", "7607", "pike", "deloitte", "edgewood", "gmu"]
for p in P:
    p["sector"] = SECTOR[p["slug"]]
    p["state"] = p["loc"].split(",")[-1].strip()
BY = {p["slug"]: p for p in P}

NAV = [("services.html", "Services"), ("materials.html", "Materials"), ("portfolio.html", "Portfolio"),
       ("tracking.html", "Tracking"), ("about.html", "About"), ("contact.html", "Contact")]


def page(path, title, body, desc="", active=""):
    depth = path.count("/")
    r = "../" * depth
    nav = "".join(f'<li><a href="{r}{h}"{" class=on" if h == active else ""}>{t}</a></li>' for h, t in NAV)
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{E(title)}</title>
<meta name="description" content="{E(desc or 'CFS Designs US, your one-stop shop for rainscreen facades.')}">
<link rel="icon" href="{r}img/site/favicon.png">
<link rel="stylesheet" href="{r}css/site.css">
</head><body>
<nav class="top"><div class="wrap">
  <a href="{r}index.html"><img src="{r}img/site/logo-light.png" alt="CFS Designs US"></a>
  <ul>{nav}</ul>
  <div class="right"><a class="track" href="{r}tracking.html"><b></b>Track a delivery</a><a class="btn btn-blue" href="{r}contact.html">Request a quote</a>
  <button class="burger" aria-label="Menu" onclick="document.body.classList.toggle('menu')"><i></i><i></i></button></div>
</div></nav>
<div class="mnav">{nav}<a class="btn btn-blue" href="{r}contact.html">Request a quote</a></div>
{body}
<footer><div class="wrap">
  <div><img src="{r}img/site/logo-light.png" alt="CFS Designs US"><p>Your one-stop shop for rainscreen facades.<br>5109 Commonwealth Dr<br>Fredericksburg, VA 22407</p><p style="margin-top:14px">Member of MCA &middot; RAINA</p></div>
  <div><h6>Services</h6><ul><li><a href="{r}services.html#drawings">Shop Drawings</a></li><li><a href="{r}services.html#engineering">Engineering &amp; Design</a></li><li><a href="{r}services.html#fabrication">Fabrication</a></li><li><a href="{r}services.html#subconstruction">Subconstruction</a></li><li><a href="{r}services.html#bending">Flashing &amp; Bending</a></li><li><a href="{r}services.html#distribution">Distribution</a></li></ul></div>
  <div><h6>Company</h6><ul><li><a href="{r}about.html">About us</a></li><li><a href="{r}portfolio.html">Portfolio</a></li><li><a href="{r}materials.html">Materials</a></li><li><a href="{r}materials.html#reports">Testing reports</a></li></ul></div>
  <div><h6>Contact</h6><ul><li><a href="tel:+15404248623">(540) 424-8623</a></li><li><a href="mailto:info@cfsdesignsus.com">info@cfsdesignsus.com</a></li><li>Mon&ndash;Fri 7:00 am&ndash;3:30 pm</li><li><a href="{r}tracking.html">Track a delivery</a></li></ul></div>
</div>
<div class="wrap legal"><span>&copy; 2026 CFS Designs US</span><span class="prev">Preview of the new website &middot; not public</span></div>
</footer>
<script src="{r}js/site.js"></script>
</body></html>"""


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(content)


def pcard(p, r="", big=False):
    return (f'<a class="proj{" big" if big else ""}" href="{r}projects/{p["slug"]}.html" data-sector="{E(p["sector"])}" data-state="{E(p["state"])}" data-q="{E((p["name"] + " " + p["loc"] + " " + p["desc"]).lower())}">'
            f'<div class="ph" style="background-image:url({r}img/thumbs/{p["slug"]}.jpg)"></div>'
            f'<span class="tag">{E(p["sector"])}</span><div class="cap"><b>{E(p["name"])}</b><span>{E(p["loc"])}</span></div></a>')


SERVICES = [
    ("drawings", "Shop Drawings", "img/site/drawings.jpg",
     "We do not just build beautiful facades, we build success from the start. Our in-house team creates meticulous shop drawings, so every detail of your metal panel or fiber cement project is clear, precise and efficient. That means fewer errors, smoother construction, and a project that stays on schedule and on budget."),
    ("engineering", "Engineering & Design Assistance", "img/projects/7607/00.jpg",
     "Engineers, architects and draftsmen with over 100 years of combined construction expertise help you shape the design and make it buildable, from the first concept to the final detail."),
    ("fabrication", "Fabrication", "img/projects/deloitte/00.jpg",
     "We combine technology with craftsmanship to deliver stunning, durable metal panel and fiber cement facades. Our in-house fabrication ensures the highest quality and unmatched lead times, while our team works with you to achieve your design vision."),
    ("subconstruction", "Rainscreen Subconstruction", "img/projects/1265-main-street/00.jpg",
     "The tested subframe systems behind the facade: fabricated and supplied with the panels, so the whole rainscreen comes from one partner."),
    ("bending", "Flashing & Bending", "img/site/factory.jpg",
     "Copings, flashings and trims bent to profile on our own brakes, labeled by Job and packed with the panels they belong to."),
    ("distribution", "Distribution", "img/site/trucks.jpg",
     "High quality interior and exterior products from market leaders around the world, packed by area and delivered on schedule, every pallet tracked."),
]
BRANDS = ["Alucobond", "Alpolic", "Reynobond", "Alfrex", "Equitone", "Nichiha", "Fundermax", "Rockany", "ATAS", "Englert", "Imetco", "Majestic Steel", "SAF", "SFS"]


def home():
    r = ""
    feat = "".join(pcard(BY[s], r, i == 0) for i, s in enumerate(FEATURED[:5]))
    cards = "".join(f'<a class="card" href="services.html#{k}"><div class="vis" style="background-image:url({img})"></div><div class="body"><span class="num">0{i+1}</span><h3>{E(t)}</h3><p>{E(d.split(". ")[0])}.</p></div></a>'
                    for i, (k, t, img, d) in enumerate(SERVICES))
    body = f"""
<header class="hero">
  <div class="heroimg" aria-hidden="true"></div>
  <div class="wrap">
    <span class="dash"><i></i><i></i><i></i></span>
    <h1>Rainscreen facades, <em>from drawing to delivery.</em></h1>
    <p class="lead">Shop drawings, engineering, fabrication, subframing, flashing and distribution. One partner, one 100,000 sq ft facility in Fredericksburg, Virginia, and every pallet tracked to your jobsite.</p>
    <div class="ctas"><a class="btn btn-blue" href="contact.html">Request a quote &rarr;</a><a class="btn btn-ghost" href="portfolio.html">See our projects</a></div>
  </div>
  <a class="live" href="tracking.html">
    <div class="row"><span>Live delivery</span><span class="pill">ON THE WAY</span></div>
    <h4>Pallet #12 &middot; Example project</h4>
    <div class="steps"><span class="on"></span><span class="on"></span><span class="on"></span><span></span></div>
    <div class="lbls"><span>Cut</span><span>Palletized</span><span>Loaded</span><span>Delivered</span></div>
  </a>
</header>
<div class="stats"><div class="wrap">
  <div class="stat"><b data-count="2017">2017</b><span>Building facades since</span></div>
  <div class="stat"><b data-count="100000" data-fmt="1">100,000</b><span>sq ft factory and warehouse</span></div>
  <div class="stat"><b data-count="100" data-suffix="+">100+</b><span>years of combined expertise</span></div>
  <div class="stat"><b data-count="{len(P)}" data-suffix="">{len(P)}</b><span>featured projects, {len(set(p["state"] for p in P))} states</span></div>
</div></div>
<section><div class="wrap">
  <div class="eyebrow rv">One-stop shop</div>
  <h2 class="rv">Everything your facade needs, under one roof.</h2>
  <p class="sub rv">From the first sketch to the last pallet on site, one team owns the details, so your crew installs instead of chasing parts.</p>
  <div class="cards six">{cards}</div>
  <div class="brands"><span class="lbl">Materials from market leaders</span><div class="marquee"><div class="mtrack">{''.join(f'<span>{b}</span>' for b in BRANDS * 2)}</div></div></div>
</div></section>
<section class="process"><div class="wrap">
  <div class="eyebrow rv">How we work</div>
  <h2 class="rv">From shop drawing to signed delivery.</h2>
  <p class="sub rv">Every panel has an ID. Every step is recorded. Nothing is guessed.</p>
  <div class="flow">
    <div class="fstep rv"><div class="n">01</div><h4>Plan</h4><p>Your drawings become a panel list, checked line by line before anything is cut.</p></div>
    <div class="fstep rv"><div class="n">02</div><h4>Fabricate</h4><p>Routing and bending in our own factory, each piece scanned as it is finished.</p></div>
    <div class="fstep rv"><div class="n">03</div><h4>Pack</h4><p>Pallets built by area and elevation, with a QR code and a packing list.</p></div>
    <div class="fstep rv"><div class="n">04</div><h4>Load</h4><p>Photos and the driver's signature at loading, sent to you automatically.</p></div>
    <div class="fstep rv"><div class="n">05</div><h4>Deliver</h4><p>Proof of Delivery with photos, signature and time, the moment it arrives.</p></div>
  </div>
</div></section>
{tracker_block(r)}
<section><div class="wrap">
  <div class="eyebrow rv">Portfolio</div>
  <h2 class="rv">Buildings we are proud of.</h2>
  <div class="pgrid">{feat}</div>
  <div style="margin-top:34px"><a class="btn btn-ghost" href="portfolio.html">See all {len(P)} projects &rarr;</a></div>
</div></section>
{factory_block(r)}
{cta_block(r)}"""
    write("index.html", page("index.html", "CFS Designs US | Rainscreen facades, from drawing to delivery", body))


def tracker_block(r):
    return f"""<section class="tracker"><div class="wrap tgrid">
  <div>
    <div class="eyebrow rv">Only at CFS</div>
    <h2 class="rv">Know where your facade is. Always.</h2>
    <p class="sub rv">Every Job gets its own live page. Your project manager sees what is cut, what is packed, what is on the truck and what was delivered, with photos and signatures.</p>
    <div class="feat">
      <div><i>1</i>Live status of every pallet, from the factory floor to your site.</div>
      <div><i>2</i>Proof of Loading and Proof of Delivery by email, with photos.</div>
      <div><i>3</i>Delivery date confirmations before the truck leaves.</div>
      <div><i>4</i>One link for the whole Job. No account, no app to install.</div>
    </div>
    <div style="margin-top:34px"><a class="btn btn-blue" href="{r}tracking.html">Try the demo &rarr;</a></div>
  </div>
  {phone_mock(r)}
</div></section>"""


def phone_mock(r):
    return f"""<div class="phone rv">
    <div class="top"><img src="{r}img/site/logo-light.png" alt=""><span class="pill">LIVE</span></div>
    <h5>Example Project</h5>
    <div class="muted">Job DEMO-2026 &middot; 14 pallets &middot; 9 delivered</div>
    <div class="pal">
      <div class="h"><span>Pallet #12 &middot; East elevation</span><span style="color:var(--blue2)">On the way</span></div>
      <div class="timeline">
        <div class="ok"><b></b>Cut and checked<small>Mon 8:12</small></div>
        <div class="ok"><b></b>Palletized, 38 panels<small>Tue 14:40</small></div>
        <div class="ok"><b></b>Loaded, driver signed<small>Wed 6:55</small></div>
        <div><b></b>Delivered<small>Today, est. 11:00</small></div>
      </div>
      <div class="photos"><span style="background-image:url({r}img/projects/edgewood/02.jpg)"></span><span style="background-image:url({r}img/site/factory.jpg)"></span><span style="background-image:url({r}img/site/trucks.jpg)"></span></div>
    </div>
  </div>"""


def factory_block(r):
    return f"""<section class="factory" style="padding-top:0"><div class="wrap">
  <div class="fbox">
    <div style="position:relative;z-index:2;max-width:520px">
      <div class="eyebrow">Inside the factory</div>
      <h2>Walk the floor with us.</h2>
      <p class="sub">100,000 square feet of routers, brakes and loading docks. A short film from the first cut to the truck is coming soon.</p>
      <div style="margin-top:30px"><a class="btn btn-ghost" href="{r}about.html">Our story</a></div>
    </div>
    <div class="play" aria-hidden="true"></div>
  </div>
</div></section>"""


def cta_block(r):
    return f"""<section class="cta"><div class="wrap"><div class="ctabox">
  <div>
    <h2>Send us your drawings. Get a clear quote.</h2>
    <p>Upload plans or a panel list and tell us your schedule. A real person from our team answers you, Monday to Friday, 7:00 am to 3:30 pm.</p>
  </div>
  {quote_form()}
</div></div></section>"""


def quote_form():
    return """<form class="form" onsubmit="return demoSubmit(this)">
    <input class="f" required placeholder="Name and company">
    <input class="f" required placeholder="Email or phone">
    <input class="f" placeholder="Project and city">
    <label class="drop"><input type="file" multiple hidden onchange="this.parentNode.querySelector('span').textContent=this.files.length+' file(s) ready'"><span>Drop drawings here or tap to choose<br>PDF, DWG, Excel</span></label>
    <button class="btn" type="submit">Request a quote &rarr;</button>
    <p class="demo-note" hidden>Preview only: nothing was sent. On the live site this request reaches our team and CFS Jobs.</p>
  </form>"""


def portfolio():
    r = ""
    chips = '<span class="chip on" data-f="">All</span>' + "".join(
        f'<span class="chip" data-f="{s}">{s} <small>{sum(1 for p in P if p["sector"] == s)}</small></span>' for s in SECTORS)
    grid = "".join(pcard(p, r) for p in P)
    body = f"""
<header class="phead" style="background-image:url(img/projects/edgewood/00.jpg)"><div class="wrap">
  <div class="eyebrow">Portfolio</div>
  <h1>{len(P)} buildings. One standard.</h1>
  <p class="lead">Residential towers, hospitals, universities, stores and public buildings across the East Coast and beyond.</p>
</div></header>
<section style="padding-top:60px"><div class="wrap">
  <div class="ptools"><div class="filters">{chips}</div><input class="search" placeholder="Search a project or city" oninput="filterProjects()"></div>
  <p class="count"><b id="cnt">{len(P)}</b> projects</p>
  <div class="pall">{grid}</div>
</div></section>
{cta_block(r)}"""
    write("portfolio.html", page("portfolio.html", "Portfolio | CFS Designs US", body, active="portfolio.html"))


def project(i, p):
    r = "../"
    prev, nxt = P[i - 1], P[(i + 1) % len(P)]
    gallery = "".join(f'<a class="g" href="{r}{f}" data-i="{k}"><img loading="lazy" src="{r}{f}" alt="{E(p["name"])}, photo {k+1}"></a>' for k, f in enumerate(p["files"]))
    more = [q for q in P if q["sector"] == p["sector"] and q["slug"] != p["slug"]][:3]
    body = f"""
<header class="phead tall" style="background-image:url({r}{p['files'][0]})"><div class="wrap">
  <a class="back" href="{r}portfolio.html">&larr; All projects</a>
  <div class="eyebrow">{E(p['sector'])}</div>
  <h1>{E(p['name'])}</h1>
  <p class="lead">{E(p['loc'])}</p>
</div></header>
<section style="padding-top:70px"><div class="wrap pdetail">
  <div><p class="story">{E(p['desc'])}</p>
    <div class="facts"><div><small>Location</small><b>{E(p['loc'])}</b></div><div><small>Sector</small><b>{E(p['sector'])}</b></div><div><small>Photos</small><b>{len(p['files'])}</b></div></div>
    <a class="btn btn-blue" href="{r}contact.html" style="margin-top:30px">Start a project like this &rarr;</a>
  </div>
  <div class="gallery">{gallery}</div>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <div class="pn"><a href="{r}projects/{prev['slug']}.html"><small>&larr; Previous</small><b>{E(prev['name'])}</b></a><a href="{r}projects/{nxt['slug']}.html" style="text-align:right"><small>Next &rarr;</small><b>{E(nxt['name'])}</b></a></div>
  {'<h3 class="more">More ' + E(p['sector'].lower()) + ' projects</h3><div class="pall three">' + ''.join(pcard(q, r) for q in more) + '</div>' if more else ''}
</div></section>
<div class="lb" onclick="lbClose(event)"><button class="lbx" aria-label="Close">&times;</button><button class="lbp" aria-label="Previous">&lsaquo;</button><img alt=""><button class="lbn" aria-label="Next">&rsaquo;</button><span class="lbc"></span></div>"""
    write(f"projects/{p['slug']}.html", page(f"projects/{p['slug']}.html", f"{p['name']} | CFS Designs US", body, desc=p["desc"][:150], active="portfolio.html"))


def services():
    r = ""
    blocks = "".join(f"""<div class="svc" id="{k}"><div class="svcimg" style="background-image:url({img})"></div><div class="svctxt"><span class="num">0{i+1}</span><h2>{E(t)}</h2><p class="sub">{E(d)}</p></div></div>"""
                     for i, (k, t, img, d) in enumerate(SERVICES))
    body = f"""
<header class="phead" style="background-image:url(img/site/factory.jpg)"><div class="wrap">
  <div class="eyebrow">Services</div><h1>One partner for the whole rainscreen.</h1>
  <p class="lead">Our one-stop shop model keeps you comfortable and confident through the whole facade installation process.</p>
</div></header>
<section><div class="wrap svcs">{blocks}</div></section>
{cta_block(r)}"""
    write("services.html", page("services.html", "Services | CFS Designs US", body, active="services.html"))


def materials():
    r = ""
    cats = [("ACM", "Aluminum composite material panels in custom finishes and colors, routed and folded in-house.", "img/projects/wardman/00.jpg"),
            ("Fiber Cement", "Fiber cement panels and planks, cut to size and supplied with the right fastening system.", "img/projects/225/00.jpg"),
            ("High Pressure Laminate (HPL)", "Durable, color-stable HPL facade panels for exterior and interior work.", "img/projects/gensler/00.jpg"),
            ("Flashing & Miscellaneous Metals", "Break metal trims, copings and flashings that finish every facade.", "img/site/factory.jpg")]
    c = "".join(f'<div class="card"><div class="vis" style="background-image:url({img})"></div><div class="body"><h3>{E(t)}</h3><p>{E(d)}</p></div></div>' for t, d, img in cats)
    reports = [("CFS 3000", "ACM Wet Joint"), ("CFS 4000", "ACM Dry Joint"), ("CFS 5000", "Fiber Cement Concealed Fastener"), ("CFS 6000", "Fiber Cement Face Fastener")]
    rp = "".join(f'<div class="rep"><b>{a}</b><span>{b} Testing Report</span><a class="btn btn-ghost" href="contact.html">Request PDF</a></div>' for a, b in reports)
    body = f"""
<header class="phead" style="background-image:url(img/projects/wmata/00.jpg)"><div class="wrap">
  <div class="eyebrow">Materials</div><h1>Top quality products from market leaders.</h1>
  <p class="lead">From break metal trims to complete facade systems, our suppliers give you the best materials for every rainscreen.</p>
</div></header>
<section><div class="wrap">
  <div class="cards four">{c}</div>
  <div class="brands" style="margin-top:80px"><span class="lbl">Brands we carry</span><div class="marquee"><div class="mtrack">{''.join(f'<span>{b}</span>' for b in BRANDS * 2)}</div></div></div>
</div></section>
<section class="process" id="reports"><div class="wrap">
  <div class="eyebrow">Tested systems</div><h2>Our testing reports.</h2>
  <p class="sub">CFS systems are tested. Architects and engineers can request each report.</p>
  <div class="reps">{rp}</div>
</div></section>
{cta_block(r)}"""
    write("materials.html", page("materials.html", "Materials | CFS Designs US", body, active="materials.html"))


def tracking():
    r = ""
    body = f"""
<header class="phead" style="background-image:url(img/site/trucks.jpg)"><div class="wrap">
  <div class="eyebrow">Tracking</div><h1>Follow your delivery, live.</h1>
  <p class="lead">Type your Job number or scan the QR code on any CFS pallet.</p>
  <form class="tform" onsubmit="return demoTrack(this)"><input placeholder="Job number, e.g. DEMO-2026" required><button class="btn btn-blue">Track</button></form>
  <p class="demo-hint">Preview: type <b>DEMO-2026</b> to see an example. On the live site this shows your real Job.</p>
</div></header>
<section class="tracker" id="result" hidden><div class="wrap">
  <div class="tres">
    <div class="trh"><div><div class="eyebrow">Job DEMO-2026</div><h2 style="margin:8px 0 4px">Example Project</h2><p class="sub">14 pallets &middot; 9 delivered &middot; 1 on the way &middot; 4 in production</p></div><span class="pill big">EXAMPLE DATA</span></div>
    <div class="tlist" id="tlist"></div>
  </div>
</div></section>
{tracker_block(r).replace('Try the demo &rarr;', 'How it works').replace('href="tracking.html"', 'href="#top"')}
"""
    write("tracking.html", page("tracking.html", "Track a delivery | CFS Designs US", body, active="tracking.html"))


def about():
    r = ""
    body = f"""
<header class="phead" style="background-image:url(img/site/hero.jpg)"><div class="wrap">
  <div class="eyebrow">About us</div><h1>Since 2017, building the East Coast's facades.</h1>
</div></header>
<section><div class="wrap about">
  <div>
    <p class="story">Since 2017, CFS Designs US has been the premier fabricator of ACM, Fiber Cement, and miscellaneous metal facades for the East Coast. Our 100,000 square foot facility allows us to handle all aspects of fabrication and distribution, ensuring a smooth and efficient experience for our clients.</p>
    <p class="sub" style="margin-top:22px">With a team of engineers, builders, architects, and draftsmen boasting over 100 years of combined construction expertise, we can tackle any project, from assisting with the design phase to flawless execution.</p>
    <p class="sub" style="margin-top:22px">Our vision is to provide design solutions to our clients: high quality interior and exterior products from market leaders around the world, plus shop drawing, engineering and design assistance services. This full spectrum approach brings value that results in lasting relationships.</p>
  </div>
  <div class="aimg" style="background-image:url(img/site/factory.jpg)"></div>
</div></section>
<div class="stats"><div class="wrap">
  <div class="stat"><b>2017</b><span>Founded</span></div><div class="stat"><b>100,000</b><span>sq ft facility</span></div>
  <div class="stat"><b>100+</b><span>years of combined expertise</span></div><div class="stat"><b>MCA &middot; RAINA</b><span>Industry memberships</span></div>
</div></div>
{factory_block(r)}
{cta_block(r)}"""
    write("about.html", page("about.html", "About | CFS Designs US", body, active="about.html"))


def contact():
    r = ""
    body = f"""
<header class="phead short" style="background-image:url(img/projects/gmu/00.jpg)"><div class="wrap">
  <div class="eyebrow">Contact</div><h1>Let's build your facade.</h1>
</div></header>
<section><div class="wrap contact">
  <div>
    <h2 style="font-size:40px">Request a quote</h2>
    <p class="sub">Send drawings, a panel list or just an idea. We answer Monday to Friday, 7:00 am to 3:30 pm.</p>
    <div class="cinfo">
      <div><small>Visit</small><b>5109 Commonwealth Dr<br>Fredericksburg, VA 22407</b></div>
      <div><small>Call</small><b><a href="tel:+15404248623">(540) 424-8623</a></b></div>
      <div><small>Email</small><b><a href="mailto:info@cfsdesignsus.com">info@cfsdesignsus.com</a></b></div>
      <div><small>Hours</small><b>Monday to Friday<br>7:00 am to 3:30 pm</b></div>
    </div>
  </div>
  <div class="ctabox solo">{quote_form()}</div>
</div></section>"""
    write("contact.html", page("contact.html", "Contact | CFS Designs US", body, active="contact.html"))


if __name__ == "__main__":
    home(); portfolio(); services(); materials(); tracking(); about(); contact()
    for i, p in enumerate(P):
        project(i, p)
    print("built", 7 + len(P), "pages")
