import logging
import time
from urllib.parse import quote

import gender_guesser.detector as gender
import pandas as pd
import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
_DEFAULT_HEADERS = {
    "User-Agent": (
        "GenderResearchBot/1.0 "
        "(academic research; github.com/example/gender-aspekte-bei-unicorns)"
    )
}

# Confidence thresholds
_HIGH_CONFIDENCE = 1.0    # 'male' / 'female'
_MID_CONFIDENCE = 0.5     # 'mostly_male' / 'mostly_female'
_LOW_CONFIDENCE = 0.0     # 'andy' / 'unknown'
_FALLBACK_THRESHOLD = 0.8  # use middle name when first-name confidence < this

# Pronoun detection: require at least this many pronouns to avoid noise
# Reduced from 2 to 1 if it's the ONLY indicator found
_MIN_PRONOUN_COUNT = 1

# Titles to strip from names
_TITLES = frozenset([
    "Dr.", "Dr", "Prof.", "Prof", "Mr.", "Ms.", "Mrs.", "Miss", "Sir", "Dame",
])

# Retry settings
_MAX_RETRIES = 3
_BACKOFF_BASE = 1.5  # seconds; wait = _BACKOFF_BASE ** attempt


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_founder_gender(founder_string, use_web_search: bool = True) -> list[str]:
    """Detect founder genders using gender_guesser and optionally web search.

    Args:
        founder_string: Comma- or 'and'-separated founder names.
        use_web_search: If True, attempts Wikipedia / Wikidata / Google lookup.

    Returns:
        List of gender predictions per founder: 'male', 'female', or 'unknown'.
    """
    d = gender.Detector(case_sensitive=False)

    if founder_string is None or (isinstance(founder_string, float) and pd.isna(founder_string)):
        return []

    founder_string = str(founder_string).strip()
    if not founder_string:
        return []

    names = _parse_names(founder_string)
    results: list[str] = []

    for name in names:
        try:
            if use_web_search:
                prediction = _predict_with_web_search(name, d)
            else:
                prediction = _predict_single_gender(name, d)
        except Exception:
            logger.exception("Unexpected error predicting gender for %r", name)
            prediction = "unknown"

        results.append(prediction)
        # Small delay to avoid aggressive scraping; Wikidata/Wiki are fast, Google is sensitive
        time.sleep(0.3)

    return results


# ---------------------------------------------------------------------------
# Name parsing
# ---------------------------------------------------------------------------

def _parse_names(founder_string: str) -> list[str]:
    """Parse a founder string into individual names, handling various formats."""
    # Handle common delimiters
    for sep in (" and ", " & ", "&"):
        founder_string = founder_string.replace(sep, ",")

    # Handle "NameandName" case (often seen in scraped data)
    if "and" in founder_string:
        import re
        # Split "NameandName" into "Name,Name"
        founder_string = re.sub(r'([a-z])and([A-Z])', r'\1,\2', founder_string)

    raw_names = [n.strip() for n in founder_string.split(",") if n.strip()]

    cleaned: list[str] = []
    for name in raw_names:
        words = [w for w in name.split() if w not in _TITLES]
        joined = " ".join(words).strip()
        if joined:
            cleaned.append(joined)

    return cleaned


# ---------------------------------------------------------------------------
# Gender prediction helpers
# ---------------------------------------------------------------------------

def _predict_with_web_search(name: str, detector) -> str:
    """Predict gender via web search; fall back to name-heuristic."""
    bio_gender = _scrape_biography(name)
    if bio_gender != "unknown":
        logger.debug("Web search resolved %r → %s", name, bio_gender)
        return bio_gender
    return _predict_single_gender(name, detector)


def _predict_single_gender(name: str, detector) -> str:
    """Predict gender from first (and optionally middle) name via gender_guesser."""
    parts = name.split()
    if not parts:
        return "unknown"

    first_name = parts[0]
    # Simple middle name logic: if 3+ parts, 2nd is often middle name
    middle_name = parts[1] if len(parts) > 2 else None

    prediction = detector.get_gender(first_name)
    confidence = _get_confidence(prediction)

    if confidence < _FALLBACK_THRESHOLD and middle_name:
        middle_prediction = detector.get_gender(middle_name)
        middle_confidence = _get_confidence(middle_prediction)
        if middle_confidence > confidence:
            logger.debug(
                "Switching from first-name prediction %r (%.1f) to middle-name %r (%.1f) for %r",
                prediction, confidence, middle_prediction, middle_confidence, name,
            )
            prediction = middle_prediction

    return _normalize_gender(prediction)


def _get_confidence(prediction: str) -> float:
    """Map a gender_guesser prediction to a confidence score."""
    if prediction in ("andy", "unknown"):
        return _LOW_CONFIDENCE
    if prediction.startswith("mostly_"):
        return _MID_CONFIDENCE
    return _HIGH_CONFIDENCE


def _normalize_gender(prediction: str) -> str:
    """Normalize gender_guesser output to 'male', 'female', or 'unknown'."""
    if prediction in ("male", "mostly_male"):
        return "male"
    if prediction in ("female", "mostly_female"):
        return "female"
    return "unknown"


# ---------------------------------------------------------------------------
# Web scraping helpers
# ---------------------------------------------------------------------------

def _scrape_biography(name: str) -> str:
    """Search Wikidata, then Wikipedia, then Google to infer gender."""
    # 1. Wikidata (Very precise)
    wikidata_gender = _search_wikidata(name)
    if wikidata_gender != "unknown":
        return wikidata_gender

    # 2. Wikipedia (Biographical text)
    wiki_gender = _search_wikipedia(name)
    if wiki_gender != "unknown":
        return wiki_gender

    # 3. Google Snippets (General search)
    return _search_google_knowledge(name)


def _robust_get(url: str, params: dict | None = None, timeout: int = 10) -> requests.Response:
    """GET with exponential-backoff retry on transient errors."""
    for attempt in range(_MAX_RETRIES):
        try:
            resp = requests.get(
                url, params=params, headers=_DEFAULT_HEADERS, timeout=timeout
            )
            if resp.status_code == 429:
                wait = _BACKOFF_BASE ** (attempt + 2)
                logger.warning("Rate-limited (429) on %s; sleeping %.1fs", url, wait)
                time.sleep(wait)
                continue
            if resp.status_code >= 500:
                wait = _BACKOFF_BASE ** (attempt + 1)
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp
        except (requests.exceptions.RequestException, requests.exceptions.Timeout) as exc:
            wait = _BACKOFF_BASE ** (attempt + 1)
            logger.warning("Request error on %s (%s); retry %d/%d", url, exc, attempt + 1, _MAX_RETRIES)
            time.sleep(wait)

    raise requests.exceptions.RetryError(f"All {_MAX_RETRIES} retries failed for {url}")


def _infer_gender_from_text(text: str) -> str:
    """Infer gender from pronoun and indicator counts in *text*."""
    text = text.lower()
    
    # Core pronouns
    female_indicators = ["she ", " her ", " hers ", " herself ", " businesswoman ", " woman ", " daughter ", " wife "]
    male_indicators = ["he ", " him ", " his ", " himself ", " businessman ", " man ", " son ", " husband "]

    female_count = sum(text.count(i) for i in female_indicators)
    male_count = sum(text.count(i) for i in male_indicators)

    if female_count == 0 and male_count == 0:
        return "unknown"
    
    # If one is significantly more frequent, or the only one present
    if female_count > male_count:
        return "female"
    if male_count > female_count:
        return "male"
    
    return "unknown"


def _search_wikidata(name: str) -> str:
    """Search Wikidata for gender (P21)."""
    try:
        search_resp = _robust_get(
            "https://www.wikidata.org/w/api.php",
            params={
                "action": "wbsearchentities",
                "search": name,
                "language": "en",
                "format": "json",
                "limit": 1
            }
        )
        data = search_resp.json()
        search_results = data.get("search", [])
        if not search_results:
            return "unknown"
        
        entity_id = search_results[0]["id"]
        
        claims_resp = _robust_get(
            "https://www.wikidata.org/w/api.php",
            params={
                "action": "wbgetclaims",
                "entity": entity_id,
                "property": "P21",
                "format": "json"
            }
        )
        claims_data = claims_resp.json()
        claims = claims_data.get("claims", {}).get("P21", [])
        
        for claim in claims:
            val = claim.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id")
            if val == "Q6581097": # male
                return "male"
            if val == "Q6581072": # female
                return "female"
            
        return "unknown"
    except Exception as e:
        logger.debug("Wikidata lookup failed for %r: %s", name, e)
        return "unknown"


def _search_wikipedia(name: str) -> str:
    """Search Wikipedia and analyze intro text."""
    try:
        search_resp = _robust_get(
            "https://en.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": name,
                "srnamespace": 0,
                "srlimit": 1,
            },
        )
        search_data = search_resp.json()
        results = search_data.get("query", {}).get("search", [])
        if not results:
            return "unknown"

        page_title = results[0]["title"]
        extract_resp = _robust_get(
            "https://en.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "format": "json",
                "titles": page_title,
                "prop": "extracts",
                "exintro": True,
                "explaintext": True,
            },
        )
        extract_data = extract_resp.json()
        pages = extract_data.get("query", {}).get("pages", {})
        text = "".join(p.get_extract("") for p in pages.values() if hasattr(p, "get_extract") or "extract" in p)
        # Handle dict values if necessary (extract API is weird sometimes)
        if not text:
            for p_id in pages:
                text = pages[p_id].get("extract", "")
                if text: break

        return _infer_gender_from_text(text)
    except Exception as e:
        logger.debug("Wikipedia lookup failed for %r: %s", name, e)
        return "unknown"


def _search_google_knowledge(name: str) -> str:
    """Scrape Google snippets for gender clues."""
    try:
        # Search for biography to get better snippets
        search_url = f"https://www.google.com/search?q={quote(name + ' biography founder')}"
        resp = _robust_get(search_url)
        soup = BeautifulSoup(resp.content, "html.parser")
        
        # Look for honorifics first in the text (Mr., Ms.)
        full_text = soup.get_text()
        if " Mr. " in full_text or " Mr " in full_text:
            return "male"
        if " Ms. " in full_text or " Mrs. " in full_text or " Ms " in full_text:
            return "female"

        # Analyze snippets
        snippet_divs = soup.select("div.BNeawe, div.VwiC3b, span.st")
        text = " ".join(d.get_text() for d in snippet_divs)
        
        return _infer_gender_from_text(text)
    except Exception as e:
        logger.debug("Google lookup failed for %r: %s", name, e)
        return "unknown"


# ---------------------------------------------------------------------------
# Manual testing
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_cases = [
        "Elon Musk",
        "Zhang Yiming",
        "Whitney Wolfe Herd",
        "Melanie Perkins",
        "Arvid Lunnemark",
    ]

    for founder_str in test_cases:
        result = get_founder_gender(founder_str, use_web_search=True)
        print(f"{founder_str!r} → {result}")
