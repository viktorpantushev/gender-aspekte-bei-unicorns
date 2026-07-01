import re
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go


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
    labels = [f'{float(v):g} Mrd. USD' for v in top_stacked['Exit Valuation']]
    male_color = '#9FB7D8'
    female_color = '#B04C4C'
    unknown_color = '#A9D3A4'

    fig1 = go.Figure(data=[
        go.Bar(
            name='Male',
            x=labels,
            y=top_stacked['male'],
            marker_color=male_color,
            hovertemplate='<b>%{x}</b><br>Male: %{y}<extra></extra>'
        ),
        go.Bar(
            name='Female',
            x=labels,
            y=top_stacked['female'],
            marker_color=female_color,
            hovertemplate='<b>%{x}</b><br>Female: %{y}<extra></extra>'
        ),
        go.Bar(
            name='Unknown',
            x=labels,
            y=top_stacked['unknown'],
            marker_color=unknown_color,
            hovertemplate='<b>%{x}</b><br>Unknown: %{y}<extra></extra>'
        )
    ])

    fig1.update_layout(
        title='Top 12 Unicorn-Exits: Gestapelte Genderverteilung nach Exit-Bewertung',
        xaxis_title='Exit-Bewertung (US$ Milliarden)',
        yaxis_title='Anzahl Unicorns',
        barmode='stack',
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

    output_path1 = output_dir / 'change_x_axis__ai_exit_values_gender_stacked_bar.html'
    fig1.write_html(str(output_path1), config={'responsive': True, 'displayModeBar': True})

    # 2. Kreisdiagramm: Gesamtgender-Verteilung bei Unicorn-Exit-Bewertungen
    fig2 = go.Figure(data=[go.Pie(
        labels=['Male', 'Female', 'Unknown'],
        values=overall_totals.values,
        marker=dict(colors=[male_color, female_color, unknown_color], line=dict(color='white', width=2)),
        hovertemplate='<b>%{label}</b><br>Anzahl: %{value}<br>Prozent: %{percent}<extra></extra>',
        textposition='auto',
        textinfo='label+percent'
    )])

    fig2.update_layout(
        title='Gender-Verteilung bei Unicorn-Exit-Bewertungen',
        height=600,
        template='plotly_white'
    )

    output_path2 = output_dir / 'rename__ai_exit_values_gender_pie_chart.html'
    fig2.write_html(str(output_path2), config={'responsive': True, 'displayModeBar': True})

    print(f'Grafiken gespeichert in: {output_dir}')


if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    csv_path = root.parent / 'processed_data' / 'exitval_gender_counts.csv'
    output_dir = root.parent / 'plots'
    plot_exit_values_gender_graphs(csv_path, output_dir)
