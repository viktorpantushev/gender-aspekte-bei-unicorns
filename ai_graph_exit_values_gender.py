import re
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def parse_valuation(value: str) -> float:
    clean = re.sub(r'\[.*?\]', '', str(value)).strip()
    try:
        return float(clean)
    except ValueError:
        return np.nan


def plot_exit_values_gender_graphs(csv_path: Path, output_dir: Path) -> None:
    df = pd.read_csv(csv_path)
    df = df.fillna(0)
    df['valuation'] = df['Exit valuation(US$billions)'].apply(parse_valuation)
    df = df.dropna(subset=['valuation'])
    df['total'] = df[['male', 'female', 'unknown']].sum(axis=1)
    df = df.sort_values('valuation', ascending=False)
    output_dir.mkdir(parents=True, exist_ok=True)

    overall_totals = df[['male', 'female', 'unknown']].sum()

    # 1. Balkendiagramm: Top 15 Exit-Bewertungen nach Unicorn-Anzahl
    top_vals = df.head(15)
    plt.figure(figsize=(14, 9))
    bars = plt.barh(top_vals['Exit valuation(US$billions)'], top_vals['total'], color='#9467bd')
    plt.title('Top 15 Exit-Bewertungen nach Unicorn-Anzahl')
    plt.xlabel('Anzahl Unicorns')
    plt.ylabel('Exit-Bewertung (US$ Milliarden)')
    plt.gca().invert_yaxis()
    for bar in bars:
        plt.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2, f'{int(bar.get_width())}', va='center')
    plt.tight_layout()
    plt.savefig(output_dir / 'ai_exit_values_total_bar.png', dpi=200)
    plt.close()

    # 2. Gestapeltes Balkendiagramm: Genderverteilung in Top 12 Exit-Bewertungen
    top_stacked = df.head(12)
    x = range(len(top_stacked))
    plt.figure(figsize=(16, 10))
    plt.bar(x, top_stacked['male'], label='male', color='#1f77b4')
    plt.bar(x, top_stacked['female'], bottom=top_stacked['male'], label='female', color='#ff7f0e')
    plt.bar(
        x,
        top_stacked['unknown'],
        bottom=top_stacked['male'] + top_stacked['female'],
        label='unknown',
        color='#2ca02c',
    )
    plt.xticks(x, top_stacked['Exit valuation(US$billions)'], rotation=55, ha='right')
    plt.title('Top 12 Exit-Bewertungen: Gestapelte Genderverteilung')
    plt.xlabel('Exit-Bewertung (US$ Milliarden)')
    plt.ylabel('Anzahl Unicorns')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.savefig(output_dir / 'ai_exit_values_gender_stacked_bar.png', dpi=200)
    plt.close()

    # 3. Kreisdiagramm: Gesamtgender-Anteile bei Exit-Bewertungen
    plt.figure(figsize=(8, 8))
    plt.pie(
        overall_totals,
        labels=['male', 'female', 'unknown'],
        autopct='%1.1f%%',
        startangle=140,
        colors=['#1f77b4', '#ff7f0e', '#2ca02c'],
        wedgeprops={'edgecolor': 'white'},
    )
    plt.title('Gesamtgender-Anteile bei Unicorn-Exit-Bewertungen')
    plt.savefig(output_dir / 'ai_exit_values_gender_pie_chart.png', dpi=200)
    plt.close()

    print(f'Grafiken gespeichert in: {output_dir}')


if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    csv_path = root / 'processed_data' / 'exitval_gender_counts_with_companies.csv'
    output_dir = root / 'processed_data'
    plot_exit_values_gender_graphs(csv_path, output_dir)
