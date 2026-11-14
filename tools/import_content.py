#!/usr/bin/env python3
"""Turns what CFS Core publishes (content/projects.json + content/originals/) into the website data.

Run by .github/workflows/publish-content.yml after every publish from CFS Core, then build.py runs.
- New original photos are enhanced (tools/enhance_photos.py) into img/projects/<slug>/<name>.jpg and full/<name>.jpg.
- data/projects.json is rewritten in portfolio order, with sector and CFS system.
- The portfolio card (img/thumbs/<slug>.jpg) is made again when the cover photo changes.
- New cities (portfolio and the Jobs map, data/jobs-map.json) get map coordinates (OpenStreetMap Nominatim,
  cached in data/cities.json).
- Pages of projects taken off the website are removed.
Run: python3 tools/import_content.py
"""
import json, os, sys, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, ROOT)
CONTENT = os.path.join(ROOT, "content/projects.json")
DATA = os.path.join(ROOT, "data/projects.json")
THUMBS = os.path.join(ROOT, "data/thumbs.json")
CITIES = os.path.join(ROOT, "data/cities.json")


def rel(*p):
    return os.path.join(ROOT, *p)


def load(path, default):
    return json.load(open(path, encoding="utf-8")) if os.path.exists(path) else default


def save(path, value):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(value, f, indent=1, ensure_ascii=False)
        f.write("\n")


def enhance(src, slug):
    """Enhanced copies of one uploaded original. Returns the website path of the normal-size photo."""
    stem = os.path.splitext(os.path.basename(src))[0]
    mid = f"img/projects/{slug}/{stem}.jpg"
    full = f"img/projects/{slug}/full/{stem}.jpg"
    if not (os.path.exists(rel(mid)) and os.path.exists(rel(full))):
        import enhance_photos
        print("enhance", src, enhance_photos.process(rel(src), rel(full), rel(mid)), flush=True)
    return mid


def thumb(slug, cover):
    """Portfolio card: 600 x 900 centre crop of the cover photo."""
    from PIL import Image, ImageOps
    src = rel(cover)
    big = rel(os.path.dirname(cover), "full", os.path.basename(cover))
    im = ImageOps.exif_transpose(Image.open(big if os.path.exists(big) else src)).convert("RGB")
    im = ImageOps.fit(im, (600, 900), Image.LANCZOS, centering=(0.5, 0.5))
    os.makedirs(rel("img/thumbs"), exist_ok=True)
    im.save(rel("img/thumbs", f"{slug}.jpg"), quality=82, optimize=True, progressive=True)
    print("thumb", slug, flush=True)


def geocode(loc):
    if loc.startswith("zip:"):
        q = urllib.parse.urlencode({"postalcode": loc[4:], "country": "us", "format": "json", "limit": 1})
    else:
        q = urllib.parse.urlencode({"q": f"{loc}, USA", "format": "json", "limit": 1, "countrycodes": "us"})
    req = urllib.request.Request(f"https://nominatim.openstreetmap.org/search?{q}", headers={"User-Agent": "cfs-website-build/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        res = json.load(r)
    time.sleep(1.1)  # Nominatim usage policy: at most one request per second
    return (round(float(res[0]["lat"]), 3), round(float(res[0]["lon"]), 3)) if res else None


def main():
    if os.path.exists(CONTENT):
        import_projects()
    else:
        print("no content/projects.json: projects unchanged")
    geocode_all()


def import_projects():
    content = load(CONTENT, [])
    old = {p["slug"]: p for p in load(DATA, [])}
    thumbs = load(THUMBS, {s: p["files"][0] for s, p in old.items() if p.get("files")})
    out = []
    for c in content:
        slug = c["slug"]
        files = []
        for ph in c["photos"]:
            if ph["src"] == "site":
                if os.path.exists(rel(ph["path"])):
                    files.append(ph["path"])
                else:
                    print("WARNING missing site photo", ph["path"])
            else:
                try:
                    files.append(enhance(ph["path"], slug))
                except Exception as e:  # one bad photo must not stop the website
                    print("ERROR photo", ph["path"], e)
        if not files:
            print("WARNING no usable photo, project skipped:", slug)
            continue
        out.append({"slug": slug, "name": c["name"], "loc": c["location"], "desc": c["description"], "files": files,
                    "sector": c.get("sector"), "system": c.get("cfs_system")})
        if thumbs.get(slug) != files[0] or not os.path.exists(rel("img/thumbs", f"{slug}.jpg")):
            thumb(slug, files[0])
            thumbs[slug] = files[0]
    save(DATA, out)
    save(THUMBS, {p["slug"]: thumbs[p["slug"]] for p in out if p["slug"] in thumbs})

    keep = {p["slug"] for p in out}
    for f in os.listdir(rel("projects")):
        if f.endswith(".html") and f[:-5] not in keep:
            os.remove(rel("projects", f))
            print("removed page", f)
    print(f"imported {len(out)} projects")


def geocode_all():
    """Map coordinates for every portfolio and Job city that has none yet."""
    import build  # noqa: E402  (reads data/projects.json and data/jobs-map.json at import)
    cities = load(CITIES, {})
    wanted = {p["loc"] for p in build.P} | {j["loc"] for j in build.JOBS} | {f'zip:{j["zip"]}' for j in build.JOBS if j["zip"]}
    for loc in sorted(wanted):
        if loc in cities or (not loc.startswith("zip:") and loc in build._HAND_CITIES):
            continue
        try:
            ll = geocode(loc)
            if ll:
                cities[loc] = ll
                print("geocoded", loc, ll)
        except Exception as e:
            print("WARNING geocode", loc, e)
    save(CITIES, cities)


if __name__ == "__main__":
    main()
