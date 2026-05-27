import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def plot_sectors_gender_graphs(csv_path: Path, output_dir: Path) -> None:
    df = pd.read_csv(csv_path)
    df = df.fillna(0)
    df['total'] = df[['male', 'female', 'unknown']].sum(axis=1)
    df = df.sort_values('total', ascending=False)
    output_dir.mkdir(parents=True, exist_ok=True)

    overall_totals = df[['male', 'female', 'unknown']].sum()

    male_color = '#9FB7D8'
    female_color = '#B04C4C'
    unknown_color = '#A9D3A4'

    # 1. Balkendiagramm: Top 15 Sektoren nach Gesamtanzahl
    top_sectors = df.head(15)
    plt.figure(figsize=(14, 9))
    bars = plt.barh(top_sectors['Sector'], top_sectors['total'], color=male_color)
    plt.title('Top 15 Unicorn-Sektoren nach Anzahl')
    plt.xlabel('Anzahl Unicorns')
    plt.ylabel('Sektor')
    plt.gca().invert_yaxis()
    for bar in bars:
        plt.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2, f'{int(bar.get_width())}', va='center')
    plt.tight_layout()
    plt.savefig(output_dir / 'rename_und_recolor__ai_sectors_total_bar.png', dpi=200)
    plt.close()

    # 2. Gestapeltes Balkendiagramm: Top 10 Sektoren nach Gender
    top_stacked = df.head(10)
    x = range(len(top_stacked))
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
    plt.xticks(x, top_stacked['Sector'], rotation=55, ha='right')
    plt.title('Top 10 Unicorn-Sektoren: Gestapelte Genderverteilung')
    plt.xlabel('Sektor')
    plt.ylabel('Anzahl Unicorns')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.savefig(output_dir / 'ai_sectors_gender_stacked_bar.png', dpi=200)
    plt.close()

    # 3. Kreisdiagramm: Gender-Verteilung in allen Sektoren
    plt.figure(figsize=(8, 8))
    plt.pie(
        overall_totals,
        labels=['Male', 'Female', 'Unknown'],
        autopct='%1.1f%%',
        startangle=140,
        colors=[male_color, female_color, unknown_color],
        wedgeprops={'edgecolor': 'white'},
    )
    plt.title('Gender-Verteilung in allen Unicorn-Sektoren')
    plt.savefig(output_dir / 'rename__ai_sectors_gender_pie_chart.png', dpi=200)
    plt.close()

    print(f'Grafiken gespeichert in: {output_dir}')


if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    csv_path = root.parent / 'processed_data' / 'sectors_gender_counts.csv'
    output_dir = root.parent / 'web_output'
    plot_sectors_gender_graphs(csv_path, output_dir)
