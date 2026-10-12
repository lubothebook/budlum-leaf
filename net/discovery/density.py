#!/usr/bin/env python3
"""density.py: how many validators do Turkey, the EU and the world need?

FINAL/21 Section 21.5.4, "the targets": a validator within 20 km in a
city, within 100 km everywhere covered, the far class elsewhere. Gate SW-24.

Three counts, and the answer is the larger of geometry and capacity:
  1. metro: every city point has k_metro = 3 validator sites within 20 km
     (the probe set of 3 to 5 and a shadow on a separate site);
  2. covered: every habitable point has k_cover = 2 sites within 100 km;
  3. capacity: the concurrent sessions at the peak hour, plus the shadow.

A hexagonal cell of circumradius r has area 3*sqrt(3)/2 * r^2, so one site
covers 1039 km^2 at 20 km and 25 981 km^2 at 100 km [GENERAL].

Output: results/density.json.
    python3 density.py
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")

# ------------------------------------------------------------- the inputs ---
REGIONS = {
    "Turkey": dict(
        pop=86_092_168,      # [PUBLICATION] TUIK ADNKS, 31 Dec 2025, released Feb 2026
        area_km2=783_562,    # [PUBLICATION] TUIK / CIA World Factbook, total area
        habitable=0.95,      # [HYPOTHESIS] share with settlement
        city_share=0.675,    # [PUBLICATION] TUIK 2025 degree of urbanisation: 67.5 % dense
        largest=15_700_000,  # [PUBLICATION] TUIK ADNKS: Istanbul about 15.7 M
    ),
    "EU-27": dict(
        pop=450_400_000,     # [PUBLICATION] Eurostat, 1 Jan 2025: 450.4 M
        area_km2=4_233_262,  # [PUBLICATION] Eurostat, EU-27 total area
        habitable=0.90,      # [HYPOTHESIS]
        city_share=0.39,     # [PUBLICATION] Eurostat DEGURBA: about 39 % in cities
        largest=10_000_000,  # [HYPOTHESIS] Paris functional urban area order
    ),
    "World": dict(
        pop=8_200_000_000,   # [PUBLICATION] UN WPP 2024: 8.2 B in 2025
        area_km2=104_000_000,  # [PUBLICATION] OWID / FAO: 104 M km^2 habitable land
        habitable=1.0,
        city_share=0.45,     # [PUBLICATION] UN WUP 2025: 45 % in cities
        largest=37_000_000,  # [PUBLICATION] UN WUP: Tokyo agglomeration order
    ),
}
WORLD_CITIES = 12_000        # [PUBLICATION] UN WUP 2025: over 12 000 cities of 50 000+
CITY_DENSITY = 4_000.0       # people per km^2 of a city, [HYPOTHESIS] GHSL urban centres are >= 1 500
K_METRO = 3
K_COVER = 2
R_METRO = 20.0
R_COVER = 100.0
HEX = 3 * math.sqrt(3) / 2
SESS_PER_SITE = 256          # [HYPOTHESIS] 32 render GPUs x 8 Leaf sessions at 1600x3200, 240 Hz
PEAK_CONC = 0.15             # [HYPOTHESIS] share of Leaf owners in a session at the peak hour
SHADOW = {"C state-hot": 0.10, "D render-hot": 1.00}   # extra render per session
ADOPTION = (0.01, 0.10, 0.50)


def cities_of(region):
    """City sizes: a Zipf law over the city count, scaled to the city population.

    The count follows the world ratio of cities to city dwellers (UN WUP 2025).
    """
    city_pop = region["pop"] * region["city_share"]
    per_city = WORLD["pop"] * WORLD["city_share"] / WORLD_CITIES
    n = max(1, round(city_pop / per_city))
    # a Zipf law P_r = c / r^a with a fitted so the largest is about `largest`
    best = None
    for a10 in range(50, 151):
        a = a10 / 100.0
        w = [1.0 / (i ** a) for i in range(1, n + 1)]
        c = city_pop / sum(w)
        err = abs(c - region["largest"])
        if best is None or err < best[0]:
            best = (err, a, [c * x for x in w])
    return n, best[1], best[2]


def sites_metro(sizes):
    n = 0
    for p in sizes:
        area = p / CITY_DENSITY
        n += K_METRO * max(1, math.ceil(area / (HEX * R_METRO ** 2)))
    return n


def main():
    global WORLD
    WORLD = REGIONS["World"]
    out = dict(inputs=dict(K_METRO=K_METRO, K_COVER=K_COVER, CITY_DENSITY=CITY_DENSITY,
                           SESS_PER_SITE=SESS_PER_SITE, PEAK_CONC=PEAK_CONC,
                           WORLD_CITIES=WORLD_CITIES), regions={})
    for name, reg in REGIONS.items():
        n_c, a, sizes = cities_of(reg)
        metro = sites_metro(sizes)
        hab = reg["area_km2"] * reg["habitable"]
        hex100 = math.ceil(hab / (HEX * R_COVER ** 2))
        # Lower bound: every 100 km cell already holds a city and its sites.
        # Upper bound: no 100 km cell holds a city, so each needs K_COVER more.
        cover_lo = K_COVER * max(0, hex100 - min(n_c, hex100))
        cover_hi = K_COVER * hex100
        cover_extra = cover_hi
        geo = metro + cover_hi
        cap = {}
        for ad in ADOPTION:
            conc = reg["pop"] * ad * PEAK_CONC
            cap[f"adoption_{int(ad * 100)}pct"] = {
                k: math.ceil(conc * (1 + s) / SESS_PER_SITE) for k, s in SHADOW.items()}
            cap[f"adoption_{int(ad * 100)}pct"]["concurrent_sessions"] = round(conc)
        out["regions"][name] = dict(
            cities=n_c, zipf_exponent=a, largest_city_model=round(sizes[0]),
            metro_sites_20km=metro, hex_cells_100km=hex100,
            cover_extra_sites_100km=dict(low=cover_lo, high=cover_hi),
            geometric_sites=dict(low=metro + cover_lo, high=geo),
            capacity_sites=cap,
            sites_needed={k: max(geo, cap[k]["C state-hot"]) for k in cap},
            fibre_rtt_at_20km_ms=round(2 * 20 * 2.0 / 204.2, 3),
            fibre_rtt_at_100km_ms=round(2 * 100 * 1.5 / 204.2, 3),
        )
        print(name, json.dumps(out["regions"][name], indent=1))
    os.makedirs(RES, exist_ok=True)
    with open(os.path.join(RES, "density.json"), "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
