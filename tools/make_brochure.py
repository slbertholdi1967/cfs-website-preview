#!/usr/bin/env python3
"""Builds downloads/CFS-Designs-US-Brochure.pdf (5 pages, US Letter) from the same data as the website.
Run: python3 tools/make_brochure.py  (needs Chromium + Playwright, pre-installed in the cloud container)."""
import os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import build as B  # noqa: E402

E = B.E
PROJ = ["tidelockrental", "deloitte", "pike", "edgewood", "7607", "gmu"]
svc = "".join(f'<div class="svc"><b>0{i+1}</b><h4>{E(t)}</h4><p>{E(d.split(". ")[0])}.</p></div>' for i, (k, t, img, d) in enumerate(B.SERVICES))
sysx = "".join(f'<div class="sy"><div class="dr">{B.section_svg(kind)}</div><b>{code}</b><h4>{E(name)}</h4><p>{E(desc)}</p></div>' for k, code, name, kind, img, desc in B.SYSTEMS)
proj = "".join(f'<div class="pj"><div class="ph" style="background-image:url(img/projects/{s}/00.jpg)"></div><h4>{E(B.BY[s]["name"])}</h4><p>{E(B.BY[s]["loc"])}</p></div>' for s in PROJ)
states = len(set(p["state"] for p in B.P))
html = f"""<!doctype html><html><head><meta charset="utf-8"><title>CFS Designs US brochure</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap">
<style>
@page{{size:Letter;margin:0}}*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:Inter,Arial,sans-serif;color:#0b0d10;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.pg{{width:8.5in;height:11in;position:relative;overflow:hidden;page-break-after:always;padding:.6in}}
.dark{{background:#07090c;color:#f4f6f8}}
.cover{{background:#07090c url(img/site/hero.jpg) center/cover;padding:0}}
.cover .sh{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(7,9,12,.35),rgba(7,9,12,.92) 70%)}}
.cover .in{{position:absolute;left:.6in;right:.6in;bottom:.7in;color:#fff}}
.cover img{{height:46px;position:absolute;top:.6in;left:.6in}}
h1{{font-size:46px;line-height:1.05;letter-spacing:-.02em;margin:14px 0}}h1 em{{font-style:normal;color:#5cc0ff}}
h2{{font-size:30px;letter-spacing:-.02em;margin:6px 0 14px}}
.eb{{font-size:10px;letter-spacing:.22em;text-transform:uppercase;color:#0290fa;font-weight:700}}
.lead{{font-size:14px;line-height:1.6;color:#4c5865;max-width:6.2in}}.dark .lead,.cover .lead{{color:#cfd6de}}
.stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:22px 0 26px}}
.stats div{{border-top:3px solid #0290fa;padding-top:8px}}.stats b{{font-size:24px;display:block}}.stats span{{font-size:10px;color:#6b7684}}
.svcs{{display:grid;grid-template-columns:1fr 1fr;gap:14px 26px;margin-top:10px}}
.svc b{{color:#0290fa;font-size:11px}}.svc h4{{font-size:14px;margin:2px 0 4px}}.svc p{{font-size:11px;line-height:1.5;color:#4c5865}}
.sys{{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:8px}}
.sy .dr svg{{width:100%;height:auto;display:block;border-radius:10px}}.sy b{{display:block;color:#5cc0ff;font-size:11px;margin-top:8px;letter-spacing:.1em}}
.sy h4{{font-size:14px;margin:2px 0 4px}}.sy p{{font-size:10.5px;line-height:1.5;color:#b8c1cc}}
.brands{{margin-top:22px;font-size:11px;color:#b8c1cc;line-height:1.7}}.brands b{{color:#fff}}
.pjs{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:10px}}
.ph{{height:2.15in;border-radius:10px;background-size:cover;background-position:center}}.pj h4{{font-size:12.5px;margin-top:7px}}.pj p{{font-size:10.5px;color:#6b7684}}
.fac{{height:3.1in;border-radius:12px;background:url(img/site/factory.jpg) center/cover;margin:12px 0 20px}}
.tr{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:8px 0 26px}}.tr div{{background:#0d1117;border:1px solid #222a33;border-radius:10px;padding:10px;font-size:10.5px;line-height:1.45;color:#cfd6de}}
.ct{{display:grid;grid-template-columns:repeat(2,1fr);gap:10px 30px;font-size:12.5px}}.ct small{{display:block;color:#7d8896;font-size:9.5px;letter-spacing:.15em;text-transform:uppercase}}
.ft{{position:absolute;bottom:.45in;left:.6in;right:.6in;font-size:9px;color:#7d8896;display:flex;justify-content:space-between}}
</style></head><body>
<div class="pg cover"><div class="sh"></div><img src="img/site/logo-light.png" alt="CFS Designs US">
  <div class="in"><div class="eb">Rainscreen facades</div><h1>From drawing <em>to delivery.</em></h1>
  <p class="lead">Shop drawings, engineering, fabrication, subframing, flashing and distribution. One partner, one 100,000 sq ft facility in Fredericksburg, Virginia.</p>
  <p class="lead" style="margin-top:16px">cfsdesignsus.com &middot; (540) 424-8623 &middot; info@cfsdesignsus.com</p></div></div>
<div class="pg"><div class="eb">About us</div><h2>Everything your facade needs, under one roof.</h2>
  <p class="lead">Since 2017, CFS Designs US has been the premier fabricator of ACM, Fiber Cement, and miscellaneous metal facades for the East Coast. With a team of engineers, builders, architects, and draftsmen boasting over 100 years of combined construction expertise, we can tackle any project, from assisting with the design phase to flawless execution.</p>
  <div class="stats"><div><b>2017</b><span>Building facades since</span></div><div><b>100,000</b><span>sq ft factory and warehouse</span></div><div><b>100+</b><span>years of combined expertise</span></div><div><b>{len(B.P)}</b><span>featured projects, {states} states</span></div></div>
  <div class="eb">Services</div><div class="svcs">{svc}</div>
  <div class="fac" style="background-image:url(img/site/drawings.jpg);height:2.6in;margin-top:22px"></div>
  <div class="ft"><span>CFS Designs US</span><span>2</span></div></div>
<div class="pg dark"><div class="eb">CFS Systems</div><h2>Tested systems. Built by us.</h2>
  <p class="lead">Four rainscreen systems for ACM and fiber cement, engineered, tested and fabricated by CFS Designs US. Testing reports are available on request.</p>
  <div class="sys">{sysx}</div>
  <p class="brands"><b>Materials from market leaders:</b> {" &middot; ".join(B.BRANDS)}</p>
  <div class="ft"><span>Illustrative sections, not to scale</span><span>3</span></div></div>
<div class="pg"><div class="eb">Portfolio</div><h2>Buildings we are proud of.</h2>
  <div class="pjs">{proj}</div>
  <div class="ft"><span>See all {len(B.P)} projects at cfsdesignsus.com</span><span>4</span></div></div>
<div class="pg dark"><div class="eb">Our facility</div><h2>100,000 square feet in Fredericksburg, Virginia.</h2>
  <p class="lead">Fabrication, bending, warehouse and loading docks on one campus, so every facade leaves complete and on time.</p>
  <div class="fac"></div>
  <div class="eb">Delivery tracking</div><h2 style="font-size:22px">Know where your facade is. Always.</h2>
  <div class="tr"><div>Live status of every pallet, from the factory floor to your site.</div><div>Proof of Loading and Proof of Delivery by email, with photos.</div><div>Delivery date confirmations before the truck leaves.</div><div>One link for the whole Job. No account, no app to install.</div></div>
  <div class="ct"><div><small>Visit</small>5109 Commonwealth Dr, Fredericksburg, VA 22407</div><div><small>Call</small>(540) 424-8623</div><div><small>Email</small>info@cfsdesignsus.com</div><div><small>Hours</small>Monday to Friday, 7:00 am to 3:30 pm</div></div>
  <div class="ft"><span>&copy; 2026 CFS Designs US</span><span>Member of MCA &middot; RAINA</span></div></div>
</body></html>"""
tmp = os.path.join(ROOT, "_brochure.html")
open(tmp, "w").write(html)
out = os.path.join(ROOT, "downloads", "CFS-Designs-US-Brochure.pdf")
js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{tmp}');await p.waitForLoadState('networkidle');await p.waitForTimeout(500);
await p.pdf({{path:'{out}',format:'Letter',printBackground:true,preferCSSPageSize:true}});await b.close()}})();"""
try:
    subprocess.run(["node", "-e", js], check=True)
finally:
    os.remove(tmp)
print("wrote", out)
