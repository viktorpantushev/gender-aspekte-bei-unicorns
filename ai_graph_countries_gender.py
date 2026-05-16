import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def plot_countries_gender_graphs(csv_path: Path, output_dir: Path) -> None:
    df = pd.read_csv(csv_path)
    df = df.fillna(0)
    df['total'] = df[['male', 'female', 'unknown']].sum(axis=1)
    df = df.sort_values('total', ascending=False)

    overall_totals = df[['male', 'female', 'unknown']].sum()
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Kreisdiagramm: Gesamtgender-Anteile über alle Länder
    plt.figure(figsize=(8, 8))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    plt.pie(
        overall_totals,
        labels=['male', 'female', 'unknown'],
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        wedgeprops={'edgecolor': 'white'},
    )
    plt.title('Gesamtgender-Anteile bei Unicorns nach Ländern')
    plt.savefig(output_dir / 'ai_countries_gender_pie_chart.png', dpi=200)
    plt.close()

    # 2. Gestapeltes Balkendiagramm: Top 20 Länder nach Unicorn-Anzahl
    top_countries = df.head(20)
    x = range(len(top_countries))

    plt.figure(figsize=(16, 9))
    plt.bar(x, top_countries['male'], label='male', color='#1f77b4')
    plt.bar(x, top_countries['female'], bottom=top_countries['male'], label='female', color='#ff7f0e')
    plt.bar(
        x,
        top_countries['unknown'],
        bottom=top_countries['male'] + top_countries['female'],
        label='unknown',
        color='#2ca02c',
    )
    plt.xticks(x, top_countries['Country/countries'], rotation=55, ha='right')
    plt.title('Top 20 Länder: gestapelte Unicorn-Gründer:innen nach Gender')
    plt.xlabel('Land')
    plt.ylabel('Anzahl Unicorn-Gründer:innen')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.savefig(output_dir / 'ai_countries_gender_stacked_bar.png', dpi=200)
    plt.close()

    # 3. Gruppiertes Balkendiagramm: Top 12 Länder nach Gender
    top_small = df.head(12)
    x = range(len(top_small))
    width = 0.25

    plt.figure(figsize=(14, 8))
    plt.bar([i - width for i in x], top_small['male'], width=width, label='male', color='#1f77b4')
    plt.bar(x, top_small['female'], width=width, label='female', color='#ff7f0e')
    plt.bar([i + width for i in x], top_small['unknown'], width=width, label='unknown', color='#2ca02c')
    plt.xticks(x, top_small['Country/countries'], rotation=50, ha='right')
    plt.title('Top 12 Länder: Unicorn-Gründer:innen nach Gender')
    plt.xlabel('Land')
    plt.ylabel('Anzahl Unicorn-Gründer:innen')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.savefig(output_dir / 'ai_countries_gender_grouped_bar.png', dpi=200)
    plt.close()

    print(f'Grafiken gespeichert in: {output_dir}')


if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    csv_path = root / 'processed_data' / 'countries_gender_counts.csv'
    output_dir = root / 'processed_data'
    plot_countries_gender_graphs(csv_path, output_dir)
