import re
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


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
    current_path = root / 'raw_data' / 'current_unicorns.csv'
    out_dir = root / 'processed_data'
    out_dir.mkdir(parents=True, exist_ok=True)

    current_counts = load_industry_counts(current_path)
    if current_counts is not None:
        plot_industry_counts(
            current_counts,
            'Current Unicorns: Anzahl nach Industry',
            out_dir / 'current_unicorns_industry_counts.png',
            max_items=20,
        )
        print('Grafik für aktuelle Unicorns gespeichert.')
    else:
        print('Die Datei current_unicorns.csv enthält keine Industry-Spalte.')




if __name__ == '__main__':
    main()
