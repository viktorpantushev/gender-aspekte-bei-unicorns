import requests
from bs4 import BeautifulSoup
import gender_guesser.detector as gender
import pandas as pd

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

        print(predicted_gender)

        # Map 'mostly_*' to full genders; treat 'andy' and 'unknown' as 'unknown'
        if predicted_gender in ('andy', 'unknown'):
            genders.append('unknown')
        elif predicted_gender in ('mostly_male'):
            genders.append('male')
        elif predicted_gender == 'mostly_female':
            genders.append('female')
        else:
            genders.append(predicted_gender)

    return genders