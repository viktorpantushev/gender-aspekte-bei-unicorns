#!/usr/bin/env python3
"""
company_founders.py

Look up the founder(s) of a list of companies using Wikidata's public API.

Why Wikidata instead of scraping arbitrary company websites?
  - It exposes STRUCTURED data (the "founded by" property, P112), so you get
    clean names instead of guessing which line on an /about page is a founder.
  - It's free, needs no API key, and explicitly permits programmatic access.
  - Coverage is strong for established / notable companies. Very small startups
    may not be on Wikidata yet; those come back with a "not found" note.

Setup:
    pip install requests

Usage:
    python company_founders.py "OpenAI" "Stripe" "Patagonia"
    python company_founders.py --input companies.txt --output founders.csv
"""

import argparse
import csv
import time
from typing import Optional

import requests

WIKIDATA_API = "https://www.wikidata.org/w/api.php"

# Wikimedia asks scripts to identify themselves. Put a real contact here.
HEADERS = {"User-Agent": "company-founder-lookup/1.0 (your-email@example.com)"}

# Be polite: pause between companies so you don't hammer the API.
REQUEST_DELAY_SECONDS = 0.5


def search_entity(company: str, session: requests.Session) -> Optional[str]:
    """Return the Wikidata Q-id for the best match of `company`, or None.

    Note: this takes the top search hit. For ambiguous names (e.g. "Apple")
    it may match the wrong entity. See the README notes for disambiguation.
    """
    params = {
        "action": "wbsearchentities",
        "search": company,
        "language": "en",
        "type": "item",
        "limit": 1,
        "format": "json",
    }
    resp = session.get(WIKIDATA_API, params=params, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    hits = resp.json().get("search", [])
    return hits[0]["id"] if hits else None


def get_founders(qid: str, session: requests.Session) -> list:
    """Return a list of founder names for a Wikidata entity (property P112)."""
    params = {
        "action": "wbgetentities",
        "ids": qid,
        "props": "claims",
        "format": "json",
    }
    resp = session.get(WIKIDATA_API, params=params, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    claims = resp.json()["entities"][qid].get("claims", {})

    founder_qids = []
    for claim in claims.get("P112", []):  # P112 = "founded by"
        try:
            founder_qids.append(claim["mainsnak"]["datavalue"]["value"]["id"])
        except (KeyError, TypeError):
            continue  # claim with no usable value (e.g. marked "unknown")

    return resolve_labels(founder_qids, session)


def resolve_labels(qids: list, session: requests.Session) -> list:
    """Turn a list of Q-ids into English labels in a single batched request."""
    if not qids:
        return []
    params = {
        "action": "wbgetentities",
        "ids": "|".join(qids),
        "props": "labels",
        "languages": "en",
        "format": "json",
    }
    resp = session.get(WIKIDATA_API, params=params, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    entities = resp.json().get("entities", {})
    # Preserve the original founder order.
    return [
        entities.get(q, {}).get("labels", {}).get("en", {}).get("value", q)
        for q in qids
    ]


def lookup(company: str, session: requests.Session) -> dict:
    """Resolve a single company name to its founder(s)."""
    try:
        qid = search_entity(company, session)
        if qid is None:
            return {"company": company, "qid": "", "founders": "", "note": "not found"}
        founders = get_founders(qid, session)
        return {
            "company": company,
            "qid": qid,
            "founders": "; ".join(founders),
            "note": "" if founders else "no founder listed",
        }
    except requests.RequestException as exc:
        return {"company": company, "qid": "", "founders": "", "note": f"error: {exc}"}


def company_founders_main(companies) -> None:

    # parser = argparse.ArgumentParser(description="Look up company founders via Wikidata.")
    # parser.add_argument("companies", nargs="*", help="Company names to look up.")
    # parser.add_argument("--input", help="Text file with one company name per line.")
    # parser.add_argument("--output", help="Write results to this CSV file.")
    # args = parser.parse_args()

    # companies = list(args.companies)

    session = requests.Session()
    results = []
    for name in companies:
        row = lookup(name, session)
        results.append(row)
        print(f"{row['company']:<30} {row['founders'] or '—'}  {row['note']}".rstrip())
        time.sleep(REQUEST_DELAY_SECONDS)

