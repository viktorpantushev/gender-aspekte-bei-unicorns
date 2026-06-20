import requests
from bs4 import BeautifulSoup
import gender_guesser.detector as gender
import pandas as pd


def scrape_wiki_table(url, table_index=0, output="output.csv"):
    # Step 1: Scrape the HTML
    # Changed User-Agent to comply with Wikipedia's robot policy
    headers = {"User-Agent": "MyWikipediaScraper/1.0 (Colab; contact@example.com)"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    html = resp.text

    # Step 2: Parse and find wikitables
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table", {"class": "wikitable"})
    print(f"Found {len(tables)} wikitable(s)")

    if not tables:
        raise ValueError("No wikitables found on the page")

    table = tables[table_index]

    # Step 3: Extract headers
    # Better: pull headers from the first <tr>
    first_row = table.find("tr")
    headers_row = [th.get_text(strip=True) for th in first_row.find_all(["th", "td"])]

    # Step 4: Extract data rows
    rows = []
    for tr in table.find_all("tr")[1:]:
        cells = tr.find_all(["td", "th"])
        if not cells:
            continue
        row = [cell.get_text(strip=True) for cell in cells]
        rows.append(row)

    # Step 5: Normalize row lengths and build DataFrame
    max_cols = max(len(headers_row), max((len(r) for r in rows), default=0))
    headers_row += [f"col_{i}" for i in range(len(headers_row), max_cols)]
    rows = [r + [""] * (max_cols - len(r)) for r in rows]

    df = pd.DataFrame(rows, columns=headers_row[:max_cols])

    # Step 6: Save to CSV
    df.to_csv(output, index=False)
    print(f"Saved {len(df)} rows to {output}")
    return df

def get_founder_gender(founder_string):
    d = gender.Detector(case_sensitive=False)

    if pd.isna(founder_string) or not founder_string.strip():
        return []

    # Handle common delimiters like ',' and ' and '
    names = []
    if ' and ' in founder_string:
        parts = founder_string.split(' and ')
        for part in parts:
            names.extend([n.strip() for n in part.split(',') if n.strip()])
    else:
        names.extend([n.strip() for n in founder_string.split(',') if n.strip()])

    genders = []
    for name in names:
        # Take the first name to guess gender
        first_name = name.split(' ')[0]
        predicted_gender = d.get_gender(first_name)
        # Treat 'andy' as 'unknown'
        if predicted_gender == 'andy':
            genders.append('unknown')
        else:
            genders.append(predicted_gender)
    return genders
