#!/usr/bin/env python3
"""Keep data/stats.json (and the CSVs) current using API-Football.

Needs two environment variables: API_FOOTBALL_KEY and PLAYER_ID.
Optional: SEASON (start year of the season, e.g. 2026).

How it works: each run reads Ronaldo's season stats, compares them with the snapshot saved in
data/state.json, and adds only the NEW goals/assists to data/stats.json. The first run just saves
the snapshot, so run it while stats.json is up to date.
"""
import csv, datetime, json, os, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
STATS, STATE = os.path.join(DATA, "stats.json"), os.path.join(DATA, "state.json")
API = "https://v3.football.api-sports.io/players"


def norm(s):
    return "".join(ch for ch in (s or "").lower() if ch.isalnum())


def comp_for(team, league):
    l = (league or "").lower()
    if team == "Al Nassr":
        if "afc" in l: return "AFC Champions League"
        if "king" in l: return "King's Cup"
        if "saudi" in l and "pro" in l: return "Saudi Pro League"
        return "Other cups"
    if "friendl" in l: return "Friendlies"
    if "nations" in l: return "Nations League"
    if "qualif" in l: return "World Cup qualifiers" if "world cup" in l else "Euro qualifiers"
    if "world cup" in l: return "World Cup"
    if "euro" in l: return "UEFA Euro"
    return "Friendlies"


def snapshot(resp):
    teams, comps, assists = {"Al Nassr": 0, "Portugal": 0}, {}, 0
    for item in resp.get("response", []):
        for st in item.get("statistics", []):
            goals = st.get("goals") or {}
            assists += goals.get("assists") or 0
            name = norm((st.get("team") or {}).get("name"))
            team = "Al Nassr" if "nassr" in name else "Portugal" if name == "portugal" else None
            if not team:
                continue
            g = goals.get("total") or 0
            teams[team] += g
            key = team + "|" + comp_for(team, (st.get("league") or {}).get("name"))
            comps[key] = comps.get(key, 0) + g
    return {"teams": teams, "comps": comps, "assists": assists}


def apply(stats, last, now):
    """Return True if stats changed. Raises ValueError if the API went backwards."""
    d_team = {k: v - last["teams"].get(k, 0) for k, v in now["teams"].items()}
    d_comp = {k: v - last["comps"].get(k, 0) for k, v in now["comps"].items()}
    d_ast = now["assists"] - last.get("assists", 0)
    if min(list(d_team.values()) + list(d_comp.values()) + [d_ast]) < 0:
        raise ValueError("API counts went down (a correction?)")
    if not any(d_team.values()) and not d_ast:
        return False
    for t in stats["teams"]:
        t["goals"] += d_team.get(t["name"], 0)
    for key, v in d_comp.items():
        if v:
            next(c for c in stats["comps"] if c["name"] == key.split("|")[1])["goals"] += v
    stats["assists"] += d_ast
    stats["total"] = sum(t["goals"] for t in stats["teams"])
    check(stats)
    today = datetime.date.today()
    stats["asof"] = f"{today.day} {today.strftime('%b %Y')}"
    return True


def check(s):
    club = sum(t["goals"] for t in s["teams"] if t["type"] == "Club")
    assert sum(c["goals"] for c in s["comps"]) == s["total"], "competition goals do not add up"
    assert sum(c["goals"] for c in s["comps"] if c["scope"] == "Club") == club, "club competitions do not add up"


def write_csvs(s):
    def w(name, head, rows):
        with open(os.path.join(DATA, name), "w", newline="", encoding="utf-8") as f:
            c = csv.writer(f); c.writerow(head); c.writerows(rows)
    logos = {}
    p = os.path.join(DATA, "goals_by_team.csv")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            logos = {r["Team"]: r.get("LogoURL", "") for r in csv.DictReader(f)}
    club = sum(t["goals"] for t in s["teams"] if t["type"] == "Club")
    pt = next(t["goals"] for t in s["teams"] if t["type"] == "Country")
    w("goals_by_team.csv", ["Team", "Type", "Years", "Goals", "Abbr", "LogoURL"],
      [(t["name"], t["type"], t["years"], t["goals"], t["abbr"], logos.get(t["name"], "")) for t in s["teams"]])
    w("goals_by_competition.csv", ["Competition", "Scope", "Goals"], [(c["name"], c["scope"], c["goals"]) for c in s["comps"]])
    w("career_summary.csv", ["Metric", "Value", "AsOf"],
      [("Career goals", s["total"], s["asof"]), ("Club goals", club, s["asof"]),
       ("Portugal goals", pt, s["asof"]), ("Career assists", s["assists"], s["asof"])])


def fetch(key, pid, season):
    url = API + "?" + urllib.parse.urlencode({"id": pid, "season": season})
    req = urllib.request.Request(url, headers={"x-apisports-key": key})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if data.get("errors"):
        raise SystemExit(f"API error: {data['errors']}")
    if not data.get("response"):
        raise SystemExit("No data returned. Check PLAYER_ID, SEASON and that your plan includes this season.")
    return data


def main(resp=None):
    today = datetime.date.today()
    season = int(os.environ.get("SEASON") or (today.year if today.month >= 7 else today.year - 1))
    if resp is None:
        resp = fetch(os.environ["API_FOOTBALL_KEY"], os.environ["PLAYER_ID"], season)
    now = snapshot(resp)
    stats = json.load(open(STATS, encoding="utf-8"))
    state = json.load(open(STATE)) if os.path.exists(STATE) else None
    if not state or state.get("season") != season:
        json.dump({"season": season, "snapshot": now}, open(STATE, "w"), indent=1)
        print(f"Saved starting snapshot for season {season}: {now['teams']}. No changes made.")
        return
    try:
        changed = apply(stats, state["snapshot"], now)
    except ValueError as e:
        print("WARNING:", e, "- keeping the previous snapshot; check the numbers by hand.")
        return
    json.dump({"season": season, "snapshot": now}, open(STATE, "w"), indent=1)
    if changed:
        json.dump(stats, open(STATS, "w", encoding="utf-8"), indent=1)
        write_csvs(stats)
        print("Updated: career goals now", stats["total"])
    else:
        print("No new goals.")


if __name__ == "__main__":
    main()
