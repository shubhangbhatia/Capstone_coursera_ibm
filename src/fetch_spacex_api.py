"""Fetch SpaceX launch metadata from the public SpaceX API v4.
This script fetches source records; map raw fields and validate labels before modeling.
"""
import argparse, requests, pandas as pd

API = "https://api.spacexdata.com/v4/launches/query"
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", default="data/spacex_launches_api.csv")
    args = p.parse_args()
    query = {"query": {}, "options": {"pagination": False, "sort": {"date_utc": "asc"},
                                      "select": ["name","date_utc","success","flight_number","details",
                                                 "payloads","launchpad","cores","rocket"]}}
    r = requests.post(API, json=query, timeout=60)
    r.raise_for_status()
    docs = r.json().get("docs", [])
    rows = []
    for d in docs:
        cores = d.get("cores") or []
        core = cores[0] if cores else {}
        rows.append({
            "flight_number": d.get("flight_number"),
            "date_utc": d.get("date_utc"),
            "launch_name": d.get("name"),
            "launch_success": d.get("success"),
            "launchpad_id": d.get("launchpad"),
            "rocket_id": d.get("rocket"),
            "core_serial": core.get("core"),
            "landing_attempt": core.get("landing_attempt"),
            "landing_success": core.get("landing_success"),
            "core_reused": core.get("reused"),
            "details": d.get("details")
        })
    pd.DataFrame(rows).to_csv(args.output, index=False)
    print(f"Wrote {len(rows)} API records to {args.output}")
    print("Review and engineer a verified first-stage reuse target before model training.")
if __name__ == "__main__": main()
