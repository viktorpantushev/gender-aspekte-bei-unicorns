import pandas as pd
import plotly.graph_objects as go
from pathlib import Path


def plot_countries_gender_graphs(csv_path: Path, output_dir: Path) -> None:
    df = pd.read_csv(csv_path)
    df = df.fillna(0)
    df['total'] = df[['male', 'female', 'unknown']].sum(axis=1)
    df = df.sort_values('total', ascending=False)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Gestapeltes Balkendiagramm: Top 12 Länder nach Unicorn-Gründer:innen-Gender
    top_small = df.head(12)

    male_color = '#9FB7D8'
    female_color = '#B04C4C'
    unknown_color = '#A9D3A4'

    fig = go.Figure(data=[
        go.Bar(
            name='Male',
            x=top_small['Country'],
            y=top_small['male'],
            marker_color=male_color,
            hovertemplate='<b>%{x}</b><br>Male: %{y}<extra></extra>'
        ),
        go.Bar(
            name='Female',
            x=top_small['Country'],
            y=top_small['female'],
            marker_color=female_color,
            hovertemplate='<b>%{x}</b><br>Female: %{y}<extra></extra>'
        ),
        go.Bar(
            name='Unknown',
            x=top_small['Country'],
            y=top_small['unknown'],
            marker_color=unknown_color,
            hovertemplate='<b>%{x}</b><br>Unknown: %{y}<extra></extra>'
        )
    ])

    fig.update_layout(
        title='Top 12 Länder: Unicorn-Gründerinnen und -Gründer nach Gender',
        xaxis_title='Land',
        yaxis_title='Anzahl Unicorn-Gründer:innen',
        barmode='group',
        height=600,
        template='plotly_white',
        hovermode='x unified',
        xaxis_tickangle=-45,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        )
    )

    output_path = output_dir / 'ai_countries_gender_grouped_bar.html'
    fig.write_html(str(output_path), config={'responsive': True, 'displayModeBar': True})

    print(f'Grafiken gespeichert in: {output_dir}')


if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    csv_path = root.parent / 'processed_data' / 'countries_gender_counts.csv'
    output_dir = root.parent / 'web_output'
    plot_countries_gender_graphs(csv_path, output_dir)
