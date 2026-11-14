#!/usr/bin/env python3
"""Jobs map for the portfolio (owner decisions 174-177, Mark Nov 14: no Job names for now).

The database sends every Job (name, city, state, ZIP, address code). This turns it into places:
- Jobs at the same address (same code) are one place; scope words are removed from the name ("GMU ACM" -> "GMU").
- A place that is already a portfolio project in the same city ("Wardman Park" / "Wardman Park Redevelopment") is
  left out, because the project is on the map with its photos.
- City spelling typed in CFS Jobs is fixed (CITY_ALIAS).
Only city, state and ZIP are written to data/jobs-map.json; the place name is written only with --names
(GitHub variable SHOW_JOB_NAMES = true), because this repository is public.

Run: python3 tools/jobs_map.py RAW.json [--names]
"""
import json, os, re, sys
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CITY_ALIAS = {
    "Alexanderia, VA": "Alexandria, VA", "Chattnoga, TN": "Chattanooga, TN", "Waltahm, MA": "Waltham, MA",
    "Wasington, DC": "Washington, DC", "Southwest, DC": "Washington, DC", "Mclean, VA": "McLean, VA",
    "SpringField, VA": "Springfield, VA", "Soddy-Daisy, TN": "Soddy Daisy, TN",
    "Huntington, PA": "Huntingdon, PA", "Greenville, VA": "Gainesville, VA",  # by their ZIP codes (16652, 20155)
}

SCOPE = re.compile(r"(?:[\s(\-/]+(?:acm(?: only)?|bending|nichiha|atas|fabrication|sub|panels?|flashings?|hpl|fc|"
                   r"fiber cement|metal|metals)\)?)+\s*$", re.I)


def words(t):
    return re.findall(r"[a-z0-9]+", t.lower())


def place_name(names):
    """One public name for one or more Jobs at the same address: the common start of their names, scope removed."""
    cores = [SCOPE.sub("", n).strip(" -") or n for n in names]
    if len(cores) == 1:
        return cores[0]
    parts = [[w for w in re.split(r"\s+|-", c) if w] for c in cores]
    common = []
    for ws in zip(*parts):
        if len({w.lower() for w in ws}) != 1:
            break
        common.append(ws[0])
    return " ".join(common) if common else min(cores, key=len)


def same_place(a, b):
    wa, wb = words(a), words(b)
    n = min(len(wa), len(wb))
    return n > 0 and wa[:n] == wb[:n]


def places(raw, portfolio):
    groups = OrderedDict()
    for j in raw:
        loc = CITY_ALIAS.get(f'{j["city"]}, {j["state"]}', f'{j["city"]}, {j["state"]}')
        key = (loc, j.get("site") or "name:" + " ".join(words(SCOPE.sub("", j["name"]))))
        g = groups.setdefault(key, {"names": [], "loc": loc, "zip": j.get("zip")})
        g["names"].append(j["name"])
        g["zip"] = g["zip"] or j.get("zip")
    kept = []
    for g in groups.values():
        name = place_name(g["names"])
        if any(p["loc"] == g["loc"] and same_place(name, p["name"]) for p in portfolio):
            continue
        if any(k["loc"] == g["loc"] and same_place(name, k["name"]) for k in kept):
            continue
        kept.append({"name": name, "loc": g["loc"], "zip": g["zip"]})
    return sorted(kept, key=lambda k: (k["loc"].split(", ")[-1], k["loc"], k["name"]))


def main():
    raw = json.load(open(sys.argv[1], encoding="utf-8"))
    show = "--names" in sys.argv
    portfolio = json.load(open(os.path.join(ROOT, "data/projects.json"), encoding="utf-8"))
    out = [{"loc": k["loc"], "zip": k["zip"], **({"name": k["name"]} if show else {})} for k in places(raw, portfolio)]
    with open(os.path.join(ROOT, "data/jobs-map.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"jobs map: {len(out)} places from {len(raw)} Jobs, names {'shown' if show else 'hidden'}")


if __name__ == "__main__":
    main()
