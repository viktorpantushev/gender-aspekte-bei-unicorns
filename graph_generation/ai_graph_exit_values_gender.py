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
    df['valuation'] = df['Exit Valuation'].apply(parse_valuation)
    df = df.dropna(subset=['valuation'])
    df['total'] = df[['male', 'female', 'unknown']].sum(axis=1)
    df = df.sort_values('valuation', ascending=False)
    output_dir.mkdir(parents=True, exist_ok=True)

    overall_totals = df[['male', 'female', 'unknown']].sum()

    # 1. Gestapeltes Balkendiagramm: Genderverteilung in Top 12 Exit-Bewertungen
    top_stacked = df.head(12)
    x = range(len(top_stacked))
    labels = [f'{float(v):g} Mrd. USD' for v in top_stacked['Exit Valuation']]
    male_color = '#9FB7D8'
    female_color = '#B04C4C'
    unknown_color = '#A9D3A4'

    plt.figure(figsize=(16, 10))
    plt.bar(x, top_stacked['male'], label='Male', color=male_color)
    plt.bar(x, top_stacked['female'], bottom=top_stacked['male'], label='Female', color=female_color)
    plt.bar(
        x,
        top_stacked['unknown'],
        bottom=top_stacked['male'] + top_stacked['female'],
        label='Unknown',
        color=unknown_color,
    )
    plt.xticks(x, labels, rotation=55, ha='right')
    plt.title('Top 12 Unicorn-Exits: Gestapelte Genderverteilung nach Exit-Bewertung')
    plt.xlabel('Exit-Bewertung (US$ Milliarden)')
    plt.ylabel('Anzahl Unicorns')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.savefig(output_dir / 'change_x_axis__ai_exit_values_gender_stacked_bar.png', dpi=200)
    plt.close()

    # 2. Kreisdiagramm: Gesamtgender-Verteilung bei Unicorn-Exit-Bewertungen
    plt.figure(figsize=(8, 8))
    plt.pie(
        overall_totals,
        labels=['Male', 'Female', 'Unknown'],
        autopct='%1.1f%%',
        startangle=140,
        colors=[male_color, female_color, unknown_color],
        wedgeprops={'edgecolor': 'white'},
    )
    plt.title('Gender-Verteilung bei Unicorn-Exit-Bewertungen')
    plt.savefig(output_dir / 'rename__ai_exit_values_gender_pie_chart.png', dpi=200)
    plt.close()

    print(f'Grafiken gespeichert in: {output_dir}')


if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    csv_path = root.parent / 'processed_data' / 'exitval_gender_counts.csv'
    output_dir = root.parent / 'web_output'
    plot_exit_values_gender_graphs(csv_path, output_dir)
