import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def plot_gender_counts(csv_path: Path, output_dir: Path) -> None:
    df = pd.read_csv(csv_path)
    df = df.fillna(0)

    # Gesamtsummen nach Gender
    totals = df[['male', 'female', 'unknown']].sum()

    plt.figure(figsize=(8, 5))
    bars = plt.bar(totals.index, totals.values, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    plt.title('Gesamtanzahl der Unicorn-Gründer:innen nach Gender')
    plt.xlabel('Gender')
    plt.ylabel('Anzahl')
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + max(totals.values) * 0.01, f'{int(height)}', ha='center', va='bottom')
    output_path = output_dir / 'countries_gender_counts_totals.png'
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()

    # Top 20 Länder nach Gesamtanzahl
    df['total'] = df[['male', 'female', 'unknown']].sum(axis=1)
    top_countries = df.sort_values('total', ascending=False).head(20)

    x = range(len(top_countries))
    width = 0.25

    plt.figure(figsize=(14, 8))
    plt.bar([i - width for i in x], top_countries['male'], width=width, label='male', color='#1f77b4')
    plt.bar(x, top_countries['female'], width=width, label='female', color='#ff7f0e')
    plt.bar([i + width for i in x], top_countries['unknown'], width=width, label='unknown', color='#2ca02c')

    plt.xticks(x, top_countries['Country/countries'], rotation=45, ha='right')
    plt.title('Top 20 Länder nach Unicorn-Gründer:innen (male/female/unknown)')
    plt.xlabel('Land')
    plt.ylabel('Anzahl')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    output_path = output_dir / 'countries_gender_counts_top20.png'
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    csv_path = root / 'processed_data' / 'countries_gender_counts.csv'
    output_dir = root / 'processed_data'
    output_dir.mkdir(parents=True, exist_ok=True)
    plot_gender_counts(csv_path, output_dir)
    print(f'Grafiken gespeichert in: {output_dir}')
