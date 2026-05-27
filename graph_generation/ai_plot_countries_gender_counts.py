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

    # Entfernt: Top 20 Ländervergleich, da im Ordner "not in use".
    # Wenn gewünscht, kann hier eine neue Web-Ausgabe ergänzt werden.


if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    csv_path = root.parent / 'processed_data' / 'countries_gender_counts.csv'
    output_dir = root.parent / 'web_output'
    output_dir.mkdir(parents=True, exist_ok=True)
    plot_gender_counts(csv_path, output_dir)
    print(f'Grafiken gespeichert in: {output_dir}')
