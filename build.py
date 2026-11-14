#!/usr/bin/env python3
"""Builds the static preview of the new CFS Designs US website (GitHub Pages, preview.cfsdesignsus.com).
Run: python3 build.py  -> writes the HTML pages next to this file. Data: data/projects.json."""
import html, json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
# Go-live switch: set PREVIEW = False when the new site replaces www.cfsdesignsus.com (owner, Nov 14 2026: the footer
# then credits the developer). The noindex tags and robots.txt are changed at go-live too.
PREVIEW = True
FOOTER_NOTE = "Preview of the new website &middot; not public" if PREVIEW else "Developed by Sergio Bertholdi"
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
    # Sector and CFS system come from CFS Core (content/projects.json via tools/import_content.py); SECTOR is the
    # original classification, used only when a project has none.
    p["sector"] = p.get("sector") or SECTOR.get(p["slug"], "")
    p["system"] = p.get("system") or ""
    p["state"] = p["loc"].split(",")[-1].strip()
BY = {p["slug"]: p for p in P}

NAV = [("services.html", "Services"), ("systems.html", "Systems"), ("materials.html", "Materials"), ("portfolio.html", "Portfolio"),
       ("tracking.html", "Tracking"), ("about.html", "About"), ("contact.html", "Contact")]


def full(f):
    """Large version used by the lightbox (falls back to the normal file)."""
    d, n = f.rsplit('/', 1)
    big = f'{d}/full/{n}'
    return big if os.path.exists(os.path.join(ROOT, big)) else f


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
  <div><a href="{r}index.html" aria-label="CFS Designs US home"><img src="{r}img/site/logo-light.png" alt="CFS Designs US"></a><p>Your one-stop shop for rainscreen facades.<br>5109 Commonwealth Dr<br>Fredericksburg, VA 22407</p><p style="margin-top:14px">Member of MCA &middot; RAINA</p><a class="social" href="https://www.linkedin.com/company/33312311/" target="_blank" rel="noopener" aria-label="CFS Designs US on LinkedIn"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg>LinkedIn</a></div>
  <div><h6>Services</h6><ul><li><a href="{r}services.html#drawings">Shop Drawings</a></li><li><a href="{r}services.html#engineering">Engineering &amp; Design</a></li><li><a href="{r}services.html#fabrication">Fabrication</a></li><li><a href="{r}services.html#subconstruction">Subconstruction</a></li><li><a href="{r}services.html#bending">Flashing &amp; Bending</a></li><li><a href="{r}services.html#distribution">Distribution</a></li></ul></div>
  <div><h6>Company</h6><ul><li><a href="{r}about.html">About us</a></li><li><a href="{r}portfolio.html">Portfolio</a></li><li><a href="{r}materials.html">Materials</a></li><li><a href="{r}systems.html">CFS Systems</a></li><li><a href="{r}careers.html">Careers</a></li><li><a href="{r}downloads/CFS-Designs-US-Brochure.pdf" download>Brochure (PDF)</a></li></ul></div>
  <div><h6>Contact</h6><ul><li><a href="tel:+15404248623">(540) 424-8623</a></li><li><a href="mailto:info@cfsdesignsus.com">info@cfsdesignsus.com</a></li><li>Mon&ndash;Fri 7:00 am&ndash;3:30 pm</li><li><a href="{r}tracking.html">Track a delivery</a></li></ul></div>
</div>
<div class="wrap legal"><span>&copy; 2026 CFS Designs US</span><span class="prev">{FOOTER_NOTE}</span></div>
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
            + (f'<span class="tag">{E(p["sector"])}</span>' if p["sector"] else '') + f'<div class="cap"><b>{E(p["name"])}</b><span>{E(p["loc"])}</span></div></a>')


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


PATHS = [
    ("For architects &amp; engineers", "Specify with confidence.", [("CFS rainscreen systems", "systems.html"), ("Testing reports", "materials.html#reports"), ("Sustainability", "materials.html#sustainability"), ("Request samples", "materials.html#samples")]),
    ("For general contractors", "Clear quotes, on schedule.", [("Request a quote", "contact.html"), ("Projects we have built", "portfolio.html"), ("Live delivery tracking", "tracking.html"), ("Questions and answers", "contact.html#faq")]),
    ("For installers", "Every pallet, accounted for.", [("Track your pallets", "tracking.html"), ("Flashing &amp; bending", "services.html#bending"), ("System details", "systems.html"), ("Talk to our team", "contact.html")]),
]


def paths_block():
    cols = "".join(f'<div class="path rv"><div class="eyebrow">{a}</div><h3>{b}</h3><ul>' + "".join(f'<li><a href="{h}">{t} <span>&rarr;</span></a></li>' for t, h in links) + '</ul></div>'
                   for a, b, links in PATHS)
    return f'<section class="paths-s"><div class="wrap"><h2 class="rv" style="font-size:40px">What are you looking for?</h2><div class="paths">{cols}</div></div></section>'


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
{paths_block()}
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
  <div class="fbox vid">
    <video class="bgv" autoplay muted loop playsinline preload="metadata" poster="{r}video/drone-poster.jpg"><source src="{r}video/drone-loop.mp4" type="video/mp4"></video>
    <div style="position:relative;z-index:2;max-width:540px">
      <div class="eyebrow">Our facility</div>
      <h2>100,000 square feet in Fredericksburg, Virginia.</h2>
      <p class="sub">Fabrication, bending, warehouse and loading docks on one campus, so every facade leaves complete and on time.</p>
      <div style="margin-top:30px;display:flex;gap:12px;flex-wrap:wrap"><button class="btn btn-blue" onclick="openFilm()">&#9654;&nbsp; Watch the aerial film</button><a class="btn btn-ghost" href="{r}about.html">Our story</a><a class="btn btn-ghost" href="{r}downloads/CFS-Designs-US-Brochure.pdf" download>Brochure (PDF)</a></div>
    </div>
  </div>
</div></section>
<div class="film" onclick="closeFilm(event)"><button class="lbx" aria-label="Close">&times;</button><video controls playsinline preload="none" poster="{r}video/drone-poster.jpg"><source src="{r}video/cfs-facility.mp4" type="video/mp4"></video></div>"""


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


CITY = {  # approximate city centres (lat, lon) for the project map
    "Washington, DC": (38.907, -77.037), "Alexandria, VA": (38.805, -77.047), "Arlington, VA": (38.880, -77.107),
    "Hyattsville, MD": (38.956, -76.946), "Bethesda, MD": (38.985, -77.095), "Rockville, MD": (39.084, -77.153),
    "Lorton, VA": (38.704, -77.228), "Towson, MD": (39.402, -76.602), "West Falls Church, VA": (38.890, -77.188),
    "Manassas, VA": (38.751, -77.475), "Stafford, VA": (38.422, -77.408), "Martinsburg, WV": (39.456, -77.964),
    "Chantilly, VA": (38.894, -77.431), "Great Falls, VA": (39.000, -77.288), "Newport News, VA": (37.087, -76.473),
    "Randallstown, MD": (39.367, -76.795), "Virginia Beach, VA": (36.853, -75.978), "Trenton, GA": (34.872, -85.509),
    "Baltimore, MD": (39.290, -76.612), "Dover, DE": (39.158, -75.524), "Gaithersburg, MD": (39.143, -77.202),
    "Woodbridge, VA": (38.658, -77.250), "Westlake, TX": (32.991, -97.195), "Soddy Daisy, TN": (35.236, -85.191),
    "Oklahoma City, OK": (35.468, -97.516), "West Roxbury, MA": (42.279, -71.149), "Waltham, MA": (42.376, -71.236),
}
_CITIES_FILE = os.path.join(ROOT, "data/cities.json")  # filled by tools/import_content.py for new cities
if os.path.exists(_CITIES_FILE):
    for _k, _v in json.load(open(_CITIES_FILE)).items():
        CITY.setdefault(_k, tuple(_v))
HQ = (38.303, -77.461)  # Fredericksburg, VA


def albers(lat, lon):
    """d3.geoAlbersUsa (lower 48), matching us-atlas states-albers-10m.json."""
    import math
    r = math.radians
    p0, p1 = r(29.5), r(45.5)
    n = (math.sin(p0) + math.sin(p1)) / 2
    c = math.cos(p0) ** 2 + 2 * n * math.sin(p0)
    r0 = math.sqrt(c) / n
    def raw(la, ph):
        rr = math.sqrt(c - 2 * n * math.sin(ph)) / n
        return rr * math.sin(la * n), r0 - rr * math.cos(la * n)
    x, y = raw(r(lon + 96), r(lat))
    xc, yc = raw(r(-0.6), r(38.7))
    return 487.5 + 1300 * (x - xc), 305 - 1300 * (y - yc)


def us_paths():
    t = json.load(open(os.path.join(ROOT, "data/us-states-albers.json")))
    (sx, sy), (tx, ty) = t["transform"]["scale"], t["transform"]["translate"]
    arcs = []
    for a in t["arcs"]:
        x = y = 0; pts = []
        for dx, dy in a:
            x += dx; y += dy; pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)
    def ring(idx):
        pts = []
        for i in idx:
            seg = arcs[i] if i >= 0 else arcs[~i][::-1]
            pts += seg if not pts else seg[1:]
        return "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z"
    states = {p["state"] for p in P}
    out = []
    for g in t["objects"]["states"]["geometries"]:
        polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
        d = "".join(ring(rg) for poly in polys for rg in poly)
        ab = STATE_ABBR.get(g["properties"]["name"], "")
        out.append(f'<path d="{d}" class="{"on" if ab in states else ""}"><title>{E(g["properties"]["name"])}</title></path>')
    return "".join(out)


STATE_ABBR = {"District of Columbia": "DC", "Virginia": "VA", "Maryland": "MD", "West Virginia": "WV", "Delaware": "DE",
              "Georgia": "GA", "Texas": "TX", "Tennessee": "TN", "Oklahoma": "OK", "Massachusetts": "MA"}


def map_block():
    from collections import defaultdict
    by = defaultdict(list)
    for p in P:
        by[p["loc"]].append(p)
    paths = us_paths()
    def dots(scale, labels, fs=1):
        out = []
        for loc, ps in sorted(by.items(), key=lambda kv: -len(kv[1])):
            if loc not in CITY:
                continue  # no coordinates yet: the project is still listed, just not on the map
            x, y = albers(*CITY[loc])
            rad = (2.2 + 1.4 * len(ps) ** .5) * scale
            names = ", ".join(q["name"] for q in ps)
            out.append(f'<g class="dot" data-loc="{E(loc)}" tabindex="0" role="button" aria-label="{E(loc)}: {len(ps)} project(s)"><circle cx="{x:.1f}" cy="{y:.1f}" r="{rad:.2f}"/><title>{E(loc)} ({len(ps)}): {E(names)}</title></g>')
            if labels and len(ps) >= 3:
                out.append(f'<text x="{x + rad + 1.2 * scale:.1f}" y="{y + 1.2 * scale:.1f}" style="font-size:{fs:.2f}px">{E(loc.split(",")[0])} &middot; {len(ps)}</text>')
        hx, hy = albers(*HQ)
        out.append(f'<g class="hq"><rect x="{hx - 2.2 * scale:.1f}" y="{hy - 2.2 * scale:.1f}" width="{4.4 * scale:.1f}" height="{4.4 * scale:.1f}" transform="rotate(45 {hx:.1f} {hy:.1f})"/><title>CFS Designs US factory, Fredericksburg, VA</title></g>')
        if labels:
            out.append(f'<text class="hqt" x="{hx + 4 * scale:.1f}" y="{hy + 1.3 * scale:.1f}" style="font-size:{fs:.2f}px">CFS factory, Fredericksburg</text>')
        return "".join(out)
    # zoom window on the Washington, DC region
    x0, y0 = albers(39.62, -77.85); x1, y1 = albers(38.0, -76.35)
    zx, zy, zw, zh = x0, y0, x1 - x0, y1 - y0
    k = zw / 975
    return f"""<section class="mapsec"><div class="wrap">
  <div class="eyebrow">Where we have built</div>
  <h2 style="font-size:40px">{len(P)} projects in {len(set(p["state"] for p in P))} states.</h2>
  <p class="sub">Tap a city to see its projects.</p>
  <div class="maps">
    <figure class="map"><svg viewBox="0 0 975 610" role="img" aria-label="Map of CFS projects in the United States"><g class="st">{paths}</g><rect class="zoombox" x="{zx:.1f}" y="{zy:.1f}" width="{zw:.1f}" height="{zh:.1f}"/>{dots(1, False)}</svg><figcaption>United States</figcaption></figure>
    <figure class="map"><svg viewBox="{zx:.1f} {zy:.1f} {zw:.1f} {zh:.1f}" role="img" aria-label="Map of CFS projects around Washington, DC"><g class="st" style="stroke-width:{.5 * k * 4:.2f}">{paths}</g>{dots(k * 2.6, True, k * 15)}</svg><figcaption>Washington, DC region</figcaption></figure>
  </div>
</div></section>"""


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
{map_block()}
<section style="padding-top:60px" id="all"><div class="wrap">
  <div class="ptools"><div class="filters">{chips}</div><input class="search" placeholder="Search a project or city" oninput="filterProjects()"></div>
  <p class="count"><b id="cnt">{len(P)}</b> projects</p>
  <div class="pall">{grid}</div>
</div></section>
{cta_block(r)}"""
    write("portfolio.html", page("portfolio.html", "Portfolio | CFS Designs US", body, active="portfolio.html"))


def project(i, p):
    r = "../"
    prev, nxt = P[i - 1], P[(i + 1) % len(P)]
    gallery = "".join(f'<a class="g" href="{r}{full(f)}" data-i="{k}"><img loading="lazy" src="{r}{f}" alt="{E(p["name"])}, photo {k+1}"></a>' for k, f in enumerate(p["files"]))
    more = [q for q in P if p["sector"] and q["sector"] == p["sector"] and q["slug"] != p["slug"]][:3]
    body = f"""
<header class="phead tall" style="background-image:url({r}{p['files'][0]})"><div class="wrap">
  <a class="back" href="{r}portfolio.html">&larr; All projects</a>
  <div class="eyebrow">{E(p['sector'] or 'Project')}</div>
  <h1>{E(p['name'])}</h1>
  <p class="lead">{E(p['loc'])}</p>
</div></header>
<section style="padding-top:70px"><div class="wrap pdetail">
  <div><p class="story">{E(p['desc'])}</p>
    <div class="facts"><div><small>Location</small><b>{E(p['loc'])}</b></div>{f"<div><small>Sector</small><b>{E(p['sector'])}</b></div>" if p['sector'] else ''}{f"<div><small>System</small><b>{E(p['system'])}</b></div>" if p['system'] else ''}<div><small>Photos</small><b>{len(p['files'])}</b></div></div>
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
<section id="sustainability"><div class="wrap">
  <div class="eyebrow">Sustainability</div><h2>Better walls, less waste.</h2>
  <p class="sub">A rainscreen is one of the most durable ways to clad a building. Here is how we help your project meet its goals.</p>
  <div class="sus">
    <div class="path"><h3>Ventilated, insulated walls</h3><p>A rainscreen keeps the insulation outside the structure and lets the cavity behind the panels drain and dry, which helps the wall manage moisture and energy.</p></div>
    <div class="path"><h3>Recyclable materials</h3><p>Aluminum can be recycled again and again without losing its properties, and the metal in our panels, trims and subframes can be recovered at the end of the building's life.</p></div>
    <div class="path"><h3>Documents for your submittals</h3><p>Ask us for the manufacturer documentation your project needs: Environmental Product Declarations (EPDs), LEED data sheets and recycled content letters.</p></div>
    <div class="path"><h3>Close to your jobsite</h3><p>Fabricated in Fredericksburg, Virginia, a short drive from Washington, DC, Maryland and Northern Virginia, with full pallets packed by area.</p></div>
  </div>
</div></section>
<section class="process" id="samples"><div class="wrap contact">
  <div>
    <div class="eyebrow">Samples</div><h2 style="font-size:40px">See the real finish.</h2>
    <p class="sub">Colors look different on screen. Tell us the material and the color you are considering, and we will send you a sample.</p>
  </div>
  <form class="form" onsubmit="return demoSubmit(this)">
    <input class="f" required placeholder="Name and company">
    <input class="f" required placeholder="Email or phone">
    <select class="f" required><option value="">Material</option><option>ACM</option><option>Fiber cement</option><option>HPL</option><option>Flashing / metal</option></select>
    <input class="f" placeholder="Manufacturer and color, e.g. Alucobond Classic Bronze">
    <input class="f" placeholder="Project name and city">
    <input class="f" required placeholder="Shipping address">
    <button class="btn" type="submit">Request samples &rarr;</button>
    <p class="demo-note" hidden>Preview only: nothing was sent. On the live site this request reaches our team.</p>
  </form>
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
<header class="phead tall" style="background-image:url(video/drone-poster.jpg)"><video class="bgv" autoplay muted loop playsinline preload="metadata" poster="video/drone-poster.jpg"><source src="video/drone-loop.mp4" type="video/mp4"></video><div class="wrap">
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


FAQ = [
    ("What do you need to prepare a quote?", "Architectural drawings, elevations or a panel list, in PDF, DWG or Excel, plus your schedule. If you only have an idea, send it anyway: our team will tell you what is missing."),
    ("Which materials do you work with?", "Aluminum composite (ACM), fiber cement, high pressure laminate (HPL) and break metal flashings, from manufacturers such as Alucobond, Alpolic, Reynobond, Equitone, Nichiha and Fundermax."),
    ("Do you provide shop drawings and engineering?", "Yes. Our in-house team prepares the shop drawings and supports the design and engineering, from the first concept to the final detail."),
    ("Are CFS systems tested?", "Yes. Each CFS system (3000, 4000, 5000 and 6000) has a testing report. Architects and engineers can request it from our team."),
    ("Do you supply the subframe and the flashing too?", "Yes. Panels, rainscreen subframe and flashings can all come from CFS, packed together by area so your crew has everything it needs."),
    ("Where do you work?", "We are based in Fredericksburg, Virginia. Our featured projects are in 10 states, from Massachusetts to Texas, with most of them in Washington, DC, Maryland and Virginia."),
    ("How do I follow my delivery?", "Every Job has its own tracking page. Use the private link we send you or scan the QR code on any CFS pallet to see what is in production, on the truck or delivered."),
    ("When can I reach you?", "Monday to Friday, 7:00 am to 3:30 pm, at (540) 424-8623 or info@cfsdesignsus.com."),
]


def faq_block():
    items = "".join(f'<details class="faq"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in FAQ)
    return f'<section class="process" id="faq"><div class="wrap faqw"><div><div class="eyebrow">FAQ</div><h2 style="font-size:40px">Questions we hear often.</h2></div><div>{items}</div></div></section>'


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
</div></section>
{faq_block()}"""
    write("contact.html", page("contact.html", "Contact | CFS Designs US", body, active="contact.html"))


def section_svg(kind):
    """Original illustrative horizontal section of a CFS system (not to scale)."""
    blue, steel, dark, line = "#0290fa", "#9aa4b2", "#2a313b", "#5c6773"
    parts = [f'<rect x="0" y="0" width="560" height="300" rx="18" fill="#0d1117"/>',
             # substrate + sheathing + WRB
             f'<rect x="40" y="40" width="34" height="220" fill="{dark}"/><text x="57" y="282" fill="{steel}" font-size="11" text-anchor="middle">Wall</text>',
             f'<rect x="74" y="40" width="6" height="220" fill="{blue}" opacity=".7"/>',
             f'<text x="77" y="30" fill="{steel}" font-size="11" text-anchor="middle">WRB</text>']
    # subframe (girts / rails)
    for y in (70, 160):
        parts.append(f'<path d="M80 {y} h60 v40 h-60" fill="none" stroke="{steel}" stroke-width="5"/>')
    parts.append(f'<text x="112" y="282" fill="{steel}" font-size="11" text-anchor="middle">CFS subframe</text>')
    if kind in ("acm_wet", "acm_dry"):
        gap = 14 if kind == "acm_dry" else 10
        for y0, y1 in ((40, 145 - gap / 2), (145 + gap / 2, 260)):
            # tray: face outside (right), returns folded back toward the wall
            parts.append(f'<path d="M150 {y0 + 3} h40 v{y1 - y0 - 6} h-40" fill="none" stroke="{blue}" stroke-width="5" stroke-linejoin="round"/>')
            parts.append(f'<rect x="186" y="{y0}" width="8" height="{y1 - y0}" fill="{blue}"/>')
        if kind == "acm_wet":
            parts.append(f'<rect x="186" y="140" width="8" height="10" fill="#e8edf2"/><circle cx="182" cy="145" r="4" fill="{steel}"/>')
            parts.append(f'<text x="330" y="150" fill="#fff" font-size="15">Sealed joint (wet seal)</text>')
        else:
            parts.append(f'<rect x="150" y="138" width="44" height="14" fill="#0d1117"/><rect x="150" y="141" width="6" height="8" fill="{steel}"/>')
            parts.append(f'<text x="330" y="150" fill="#fff" font-size="15">Open reveal (dry joint)</text>')
        parts.append(f'<path d="M200 145 L320 145" stroke="{line}" stroke-dasharray="4 4"/>')
        for y in (95, 205):
            parts.append(f'<path d="M140 {y} h12" stroke="{steel}" stroke-width="4"/>')
        parts.append(f'<text x="330" y="80" fill="#fff" font-size="15">ACM tray, routed and returned</text><path d="M198 75 L320 75" stroke="{line}" stroke-dasharray="4 4"/>')
        parts.append(f'<text x="330" y="215" fill="#fff" font-size="15">Clip and extrusion on subframe</text><path d="M140 205 L320 210" stroke="{line}" stroke-dasharray="4 4"/>')
    else:
        for y0, y1 in ((40, 140), (150, 260)):
            parts.append(f'<rect x="146" y="{y0}" width="16" height="{y1 - y0}" fill="#8f8a82"/>')
        parts.append(f'<rect x="146" y="140" width="16" height="10" fill="{dark}"/>')
        if kind == "fc_hidden":
            for y in (90, 205):
                parts.append(f'<path d="M140 {y} h14" stroke="{blue}" stroke-width="5"/>')
            parts.append(f'<text x="330" y="100" fill="#fff" font-size="15">Concealed anchors, no visible screws</text><path d="M160 95 L320 95" stroke="{line}" stroke-dasharray="4 4"/>')
        else:
            for y in (90, 205):
                parts.append(f'<circle cx="168" cy="{y}" r="5" fill="{blue}"/><path d="M140 {y} h28" stroke="{blue}" stroke-width="3"/>')
            parts.append(f'<text x="330" y="100" fill="#fff" font-size="15">Colour-matched face fasteners</text><path d="M175 95 L320 95" stroke="{line}" stroke-dasharray="4 4"/>')
        parts.append(f'<text x="330" y="150" fill="#fff" font-size="15">Fiber cement panel</text><path d="M165 150 L320 150" stroke="{line}" stroke-dasharray="4 4"/>')
        parts.append(f'<text x="330" y="215" fill="#fff" font-size="15">Ventilated cavity behind</text><path d="M120 215 L320 215" stroke="{line}" stroke-dasharray="4 4"/>')
    parts.append(f'<text x="530" y="285" fill="#5c6773" font-size="10" text-anchor="end">Illustrative section, not to scale</text>')
    return '<svg viewBox="0 0 560 300" role="img" font-family="Inter,sans-serif">' + "".join(parts) + "</svg>"


SYSTEMS = [
    ("cfs-3000", "CFS 3000", "ACM Wet Joint System", "acm_wet", ("img/projects/wardman/00.jpg", "ACM facade by CFS: Wardman Park, Washington, DC"),
     "Aluminum composite panels routed and returned into trays, with sealed joints for a crisp, continuous facade line."),
    ("cfs-4000", "CFS 4000", "ACM Dry Joint System", "acm_dry", ("img/projects/edgewood/00.jpg", "ACM facade by CFS: Edgewood, Washington, DC"),
     "Aluminum composite panels with open reveals: a rainscreen that drains and ventilates, with clean shadow lines."),
    ("cfs-5000", "CFS 5000", "Fiber Cement Concealed Fastener System", "fc_hidden", ("img/projects/225/00.jpg", "Fiber cement facade by CFS: 225 Vine Street, Washington, DC"),
     "Fiber cement panels held by concealed anchors on the CFS subframe, for a smooth face with no visible screws."),
    ("cfs-6000", "CFS 6000", "Fiber Cement Face Fastener System", "fc_face", ("img/projects/pickersgille/00.jpg", "Fiber cement facade by CFS: Pickersgill, Towson, MD"),
     "Fiber cement panels fixed with colour-matched face fasteners on the CFS subframe: fast, economical and proven."),
]


def systems():
    r = ""
    cards = "".join(f'<a class="syscard" href="#{k}"><b>{code}</b><span>{E(name)}</span></a>' for k, code, name, *_ in SYSTEMS)
    blocks = "".join(f"""<div class="sys" id="{k}">
      <div class="systxt"><div class="eyebrow">{code}</div><h2>{E(name)}</h2><p class="sub">{E(desc)}</p>
        <ul class="syslist"><li>Shop drawings and engineering support</li><li>Fabricated in our Fredericksburg factory</li><li>Subframe, panels and flashing from one partner</li><li>Testing report available</li></ul>
        <a class="btn btn-ghost" href="contact.html">Request the {code} report</a></div>
      <div class="sysvis"><figure class="sysphoto" style="background-image:url({img[0]})"><figcaption>{E(img[1])}</figcaption></figure><div class="sysdraw">{section_svg(kind)}</div></div>
    </div>""" for k, code, name, kind, img, desc in SYSTEMS)
    body = f"""
<header class="phead" style="background-image:url(img/projects/gmu/00.jpg)"><div class="wrap">
  <div class="eyebrow">CFS Systems</div><h1>Tested systems. Built by us.</h1>
  <p class="lead">Four rainscreen systems for ACM and fiber cement, engineered, tested and fabricated by CFS Designs US.</p>
</div></header>
<section style="padding-top:60px"><div class="wrap">
  <div class="syscards">{cards}</div>
  <div class="syss">{blocks}</div>
</div></section>
{cta_block(r)}"""
    write("systems.html", page("systems.html", "CFS Systems | CFS Designs US", body, active="systems.html"))


def careers():
    r = ""
    jobs = "https://www.linkedin.com/company/33312311/jobs/"
    body = f"""
<header class="phead" style="background-image:url(img/site/factory.jpg)"><div class="wrap">
  <div class="eyebrow">Careers</div><h1>Join the team.</h1>
  <p class="lead">We are growing. Help us build the East Coast's facades, from drawing to delivery.</p>
</div></header>
<section><div class="wrap about">
  <div>
    <div class="eyebrow">Now hiring</div>
    <h2 style="margin:10px 0 18px">Sales Representatives</h2>
    <p class="story">We are looking for new sales professionals to bring CFS rainscreen facades to architects, general contractors and installers.</p>
    <p class="sub" style="margin-top:22px">You will work with a team of engineers, architects and draftsmen with over 100 years of combined construction expertise, backed by our 100,000 square foot facility in Fredericksburg, Virginia.</p>
    <p style="margin-top:30px"><a class="btn btn-blue" href="{jobs}" target="_blank" rel="noopener">See our openings on LinkedIn &rarr;</a></p>
  </div>
  <div class="aimg" style="background-image:url(img/site/drawings.jpg)"></div>
</div></section>
"""
    write("careers.html", page("careers.html", "Careers | CFS Designs US", body, active="careers.html"))


if __name__ == "__main__":
    home(); portfolio(); services(); systems(); materials(); tracking(); about(); contact(); careers()
    for i, p in enumerate(P):
        project(i, p)
    print("built", 9 + len(P), "pages")
