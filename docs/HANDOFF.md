# New CFS website: handoff (Nov 14 2026)

Read this first in a new session. The owner's working style and golden rules are in
`cfs-core-compass/docs/HANDOFF.md` (summary below).

## How to work with the owner (Sergio Bertholdi)

- Chat in **Portuguese**; everything on the site is in **English**.
- **Numbered questions with lettered options** (last number used: **171**; continue from 172). Answers come as "157=a".
- **One step at a time**, preview before building, **never invent facts** (no fake testimonials, cities, materials,
  systems or AI-made photos presented as CFS work). Be economical; warn before running several agents.
- Commit and push after each change; the site redeploys by itself in about 1 minute.

## What it is

A static preview of the new www.cfsdesignsus.com for the board, live at **https://preview.cfsdesignsus.com**
(GitHub Pages from this public repo, branch `main`, CNAME `preview.cfsdesignsus.com`; DNS CNAME `preview` ->
`slbertholdi1967.github.io` in Squarespace Domains; HTTPS works). The live Squarespace site and the CFS apps are untouched.
Every page is `noindex`, `robots.txt` blocks everything, the footer says "Preview of the new website - not public".

- `python3 build.py` builds all 50 pages from `data/projects.json` (42 projects: name, location, description, photos,
  copied from the current site; sectors are classified in `build.py` `SECTOR`, owner may correct them).
- Pages: Home, Services, **CFS Systems** (3000 ACM wet joint, 4000 ACM dry joint, 5000 FC concealed fastener,
  6000 FC face fastener, with original illustrative section drawings; owner approved, decision 150a), Materials,
  Portfolio (filters + search), one page per project (gallery + lightbox using `img/projects/<slug>/full/`),
  Tracking (DEMO-2026 example data only), About, Contact (quote form demo: nothing is sent).
- Photos: originals downloaded at full size and enhanced with `tools/enhance_photos.py` (Real-ESRGAN general x4v3 ONNX
  upscaling for small photos, vertical/keystone correction, white balance, levels, local contrast, vibrance, highlight
  colour protection). Before/after examples: `docs/CFS_Photos_Before_After.jpg`.
- Video: the facility drone film from the old About page (decrypted from Squarespace HLS), `video/drone-loop.mp4`
  (muted background loop on Home "Our facility" and About header) and `video/cfs-facility.mp4` (full film with sound,
  opened by "Watch the aerial film"). The old site's version shows a leftover "Enter your caption or title here" title
  at the start; ours is cut. Music origin unknown: owner to confirm or replace with royalty-free music.
- Proposal PDF shown earlier: `docs/CFS_Website_Proposal.pdf`.

## Decisions and advice already given

- Competitors reviewed: ceimaterials.com, amdnj.com, ecmsinc.net (they show named "systems", downloads, news; none has delivery tracking).
- Squarespace cannot do the integrations (tracking, quotes into CFS Jobs) and only ~70% of the look: recommend our own site.
- Official hosting recommendation: **Cloudflare Pages free plan** (commercial use allowed, unmetered static bandwidth,
  DDoS protection). GitHub Pages is fine for the preview but GitHub says it is not for business sites.
  Render Pro (owner asked) adds nothing we need; do not recommend it.
- Integration uses the Supabase we already pay for. Customer tracking only through the private customer link or the
  pallet QR code (never by typing a Job number alone). Branded customers never see CFS.
- Integration ideas offered (owner will choose): live tracking, quote request -> CFS Jobs lead + files, portfolio fed
  from finished Jobs (approval by owner/Mark), live totals on the home page, customer portal, testing reports with
  contact capture, news/careers managed in Core, installer videos.
- The biggest real investment is **professional photos and video** (owner agrees).

## Open items

1. Owner is **reviewing the site**; apply his adjustments.
2. **Email to the board with the link** (decision 153): prepare ONLY when he says so, with migration / cost / security
   summary and the integration ideas he keeps. Question **152** (language of the summary) not answered yet.
3. `docs/CFS_Projects_Systems.xlsx`: owner will fill in the CFS system used in each project; then show the system on
   each project page and the projects on each system page.
4. Question **154** (shot list PDF for the photographer: now / after board approval / no) not answered yet.
5. Competitor review done (Nov 14): CEI and ECMS offer free downloads (CSI specs, details, data sheets, warranties,
   color charts; CEI names its tests: ASTM E283/E330/E331, AAMA 501.1/508, NFPA 285, Florida approval). Owner sent Mark an
   email (157) asking for the CFS documents and test standards, which services CFS offers (3D scanning, BIM, estimating,
   PM, installation) and any factory certifications. **Downloads page (158a): build when Mark's files arrive.**
   Done: LinkedIn link in footer (160a, linkedin.com/company/33312311); Careers page with Sales Representatives and
   link to LinkedIn openings (161b, 166b). No News page, no leadership page (162b). 164 = all, done Nov 14: home
   audience paths, project map on Portfolio (data/us-states-albers.json, CITY coords in build.py), Materials
   sustainability + sample request (demo), Contact FAQ, brochure PDF (`python3 tools/make_brochure.py` ->
   downloads/, rerun when content changes). Testimonials NOT built: need real quotes with permission.
   Owner to confirm: CFS supplies EPD/LEED documents, sends samples, FAQ answers.
7. **167a: Mark publishes new portfolio projects from a screen in CFS Core** ("as if everything already worked").
   Proposed: Core page Website > Projects (draft/publish), table + private storage bucket (SQL approved/applied by
   owner), Core server function with a GitHub token (Lovable secret) commits the project to this repo, a GitHub Action
   enhances photos, builds and deploys. Waiting for answers 168-171 and a screen preview before building.
6. Owner may tick **Enforce HTTPS** in GitHub > Settings > Pages (certificate is issued).
