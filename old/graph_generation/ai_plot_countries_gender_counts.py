import pandas as pd
import plotly.graph_objects as go
from pathlib import Path


def plot_gender_counts(csv_path: Path, output_dir: Path) -> None:
    df = pd.read_csv(csv_path)
    df = df.fillna(0)

    # Gesamtsummen nach Gender
    totals = df[['male', 'female', 'unknown']].sum()

    # Interaktives Balkendiagramm mit Plotly
    fig = go.Figure(data=[
        go.Bar(
            x=totals.index,
            y=totals.values,
            marker=dict(color=['#9FB7D8', '#B04C4C', '#A9D3A4']),
            text=totals.values,
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Anzahl: %{y}<extra></extra>'
        )
    ])

    fig.update_layout(
        title='Gesamtanzahl der Unicorn-Gründer:innen nach Gender',
        xaxis_title='Gender',
        yaxis_title='Anzahl',
        height=500,
        template='plotly_white',
        hovermode='x unified',
        showlegend=False
    )

    output_path = output_dir / 'countries_gender_counts_totals.html'
    fig.write_html(str(output_path), config={'responsive': True, 'displayModeBar': True})

    # Entfernt: Top 20 Ländervergleich, da im Ordner "not in use".
    # Wenn gewünscht, kann hier eine neue Web-Ausgabe ergänzt werden.


if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    csv_path = root.parent / 'processed_data' / 'countries_gender_counts.csv'
    output_dir = root.parent / 'web_output'
    output_dir.mkdir(parents=True, exist_ok=True)
    plot_gender_counts(csv_path, output_dir)
    print(f'Grafiken gespeichert in: {output_dir}')
