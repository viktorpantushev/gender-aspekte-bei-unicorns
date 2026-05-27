import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def plot_countries_gender_graphs(csv_path: Path, output_dir: Path) -> None:
    df = pd.read_csv(csv_path)
    df = df.fillna(0)
    df['total'] = df[['male', 'female', 'unknown']].sum(axis=1)
    df = df.sort_values('total', ascending=False)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Gestapeltes Balkendiagramm: Top 12 Länder nach Unicorn-Gründer:innen-Gender
    top_small = df.head(12)
    x = range(len(top_small))
    width = 0.25

    male_color = '#9FB7D8'
    female_color = '#B04C4C'
    unknown_color = '#A9D3A4'

    plt.figure(figsize=(14, 8))
    plt.bar([i - width for i in x], top_small['male'], width=width, label='Male', color=male_color)
    plt.bar(x, top_small['female'], width=width, label='Female', color=female_color)
    plt.bar([i + width for i in x], top_small['unknown'], width=width, label='Unknown', color=unknown_color)
    plt.xticks(x, top_small['Country'], rotation=50, ha='right')
    plt.title('Top 12 Länder: Unicorn-Gründerinnen und -Gründer nach Gender')
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
    csv_path = root.parent / 'processed_data' / 'countries_gender_counts.csv'
    output_dir = root.parent / 'web_output'
    plot_countries_gender_graphs(csv_path, output_dir)
