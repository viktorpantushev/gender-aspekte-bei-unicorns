import re
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from gender_guesser.detector import Detector


def normalize_industry(value):
    if pd.isna(value):
        return []

    text = str(value).strip()
    if not text:
        return []

    text = re.sub(r'[;/]', '|', text)
    text = text.replace(' and ', '|')
    text = text.replace(' & ', '|')

    parts = [part.strip() for part in text.split('|') if part.strip()]
    return parts


def load_industry_counts(csv_path: Path) -> pd.Series | None:
    df = pd.read_csv(csv_path)
    if 'Industry' not in df.columns:
        return None

    industries = df['Industry'].fillna('').apply(normalize_industry).explode()
    industries = industries.dropna().astype(str)
    if industries.empty:
        return pd.Series(dtype=int)

    return industries.value_counts().sort_values(ascending=False)


def guess_gender(name: str, detector: Detector) -> str:
    if not isinstance(name, str) or not name.strip():
        return 'unknown'

    parts = name.strip().split()
    if not parts:
        return 'unknown'

    first_name = parts[0]
    prediction = detector.get_gender(first_name)
    if prediction in ('female', 'mostly_female'):
        return 'female'
    if prediction in ('male', 'mostly_male'):
        return 'male'
    return 'unknown'


def normalize_founder_names(founder_string: str) -> list[str]:
    if pd.isna(founder_string):
        return []

    text = str(founder_string)
    for sep in (' and ', ' & ', ','):
        text = text.replace(sep, '|')
    parts = [part.strip() for part in text.split('|') if part.strip()]
    return parts


def load_gender_counts_by_industry(csv_path: Path) -> pd.DataFrame | None:
    df = pd.read_csv(csv_path)
    if 'Industry' not in df.columns or 'Founder(s)' not in df.columns:
        return None

    detector = Detector(case_sensitive=False)
    industry_gender = {}

    for _, row in df.iterrows():
        industries = normalize_industry(row['Industry'])
        founders = normalize_founder_names(row['Founder(s)'])
        if not industries or not founders:
            continue

        for founder_name in founders:
            gender = guess_gender(founder_name, detector)
            for industry in industries:
                entry = industry_gender.setdefault(industry, {'male': 0, 'female': 0, 'unknown': 0})
                entry[gender] += 1

    if not industry_gender:
        return None

    result = pd.DataFrame.from_dict(industry_gender, orient='index').fillna(0).astype(int)
    result['total'] = result[['male', 'female', 'unknown']].sum(axis=1)
    return result.sort_values('total', ascending=False)


def plot_industry_gender_stacked(counts: pd.DataFrame, title: str, output_path: Path, max_items: int = 15) -> None:
    if counts is None or counts.empty:
        return

    counts = counts.head(max_items)
    x = range(len(counts))

    male_color = '#9FB7D8'
    female_color = '#B04C4C'
    unknown_color = '#A9D3A4'

    plt.figure(figsize=(16, 10))
    plt.bar(x, counts['male'], label='Male', color=male_color)
    plt.bar(x, counts['female'], bottom=counts['male'], label='Female', color=female_color)
    plt.bar(
        x,
        counts['unknown'],
        bottom=counts['male'] + counts['female'],
        label='Unknown',
        color=unknown_color,
    )
    plt.xticks(x, counts.index, rotation=55, ha='right')
    plt.title(title)
    plt.xlabel('Industry')
    plt.ylabel('Anzahl Gründer:innen')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def plot_industry_counts(counts: pd.Series, title: str, output_path: Path, max_items: int = 20) -> None:
    if counts is None:
        return

    counts = counts.head(max_items)
    plt.figure(figsize=(12, 8))
    bars = plt.barh(counts.index[::-1], counts.values[::-1], color='#4C72B0')
    plt.title(title)
    plt.xlabel('Anzahl der Unicorns')
    plt.tight_layout()

    for bar in bars:
        width = bar.get_width()
        plt.text(width + max(counts.values) * 0.01, bar.get_y() + bar.get_height() / 2, f'{int(width)}', va='center')

    plt.savefig(output_path, dpi=200)
    plt.close()


def main() -> None:
    root = Path(__file__).resolve().parent
    current_path = root.parent / 'raw_data' / 'current_unicorns.csv'
    out_dir = root.parent / 'web_output'
    out_dir.mkdir(parents=True, exist_ok=True)

    current_counts = load_industry_counts(current_path)
    if current_counts is not None:
        plot_industry_counts(
            current_counts,
            'Aktuelle Unicorns: Anzahl je Branche',
            out_dir / 'add_gender__current_unicorns_industry_counts.png',
            max_items=20,
        )
        print('Grafik für aktuelle Unicorns gespeichert.')
    else:
        print('Die Datei current_unicorns.csv enthält keine Industry-Spalte.')

    industry_gender_counts = load_gender_counts_by_industry(current_path)
    if industry_gender_counts is not None:
        plot_industry_gender_stacked(
            industry_gender_counts,
            'Aktuelle Unicorns: Gestapelte Genderverteilung je Branche',
            out_dir / 'add_gender_current_unicorns_industry_gender_stacked_bar.png',
            max_items=15,
        )
        print('Gestapeltes Gender-Diagramm für aktuelle Unicorns gespeichert.')
    else:
        print('Unable to generate stacked gender chart because gender or Industry data is unavailable.')




if __name__ == '__main__':
    main()
