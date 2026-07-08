import pandas as pd
import plotly.graph_objects as go
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

    # 1. Horizontales Balkendiagramm: Top 15 Sektoren nach Gesamtanzahl
    top_sectors = df.head(15)
    fig1 = go.Figure(data=[
        go.Bar(
            y=top_sectors['Sector'],
            x=top_sectors['total'],
            orientation='h',
            marker=dict(color=male_color),
            text=top_sectors['total'],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Anzahl: %{x}<extra></extra>'
        )
    ])

    fig1.update_layout(
        title='Top 15 Unicorn-Sektoren nach Anzahl',
        xaxis_title='Anzahl Unicorns',
        yaxis_title='Sektor',
        height=600,
        template='plotly_white',
        hovermode='y unified',
        yaxis=dict(autorange='reversed')
    )

    output_path1 = output_dir / 'rename_und_recolor__ai_sectors_total_bar.html'
    fig1.write_html(str(output_path1), config={'responsive': True, 'displayModeBar': True})

    # 2. Gestapeltes Balkendiagramm: Top 10 Sektoren nach Gender
    top_stacked = df.head(10)
    
    fig2 = go.Figure(data=[
        go.Bar(
            name='Male',
            x=top_stacked['Sector'],
            y=top_stacked['male'],
            marker_color=male_color,
            hovertemplate='<b>%{x}</b><br>Male: %{y}<extra></extra>'
        ),
        go.Bar(
            name='Female',
            x=top_stacked['Sector'],
            y=top_stacked['female'],
            marker_color=female_color,
            hovertemplate='<b>%{x}</b><br>Female: %{y}<extra></extra>'
        ),
        go.Bar(
            name='Unknown',
            x=top_stacked['Sector'],
            y=top_stacked['unknown'],
            marker_color=unknown_color,
            hovertemplate='<b>%{x}</b><br>Unknown: %{y}<extra></extra>'
        )
    ])

    fig2.update_layout(
        title='Top 10 Unicorn-Sektoren: Gestapelte Genderverteilung',
        xaxis_title='Sektor',
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

    output_path2 = output_dir / 'ai_sectors_gender_stacked_bar.html'
    fig2.write_html(str(output_path2), config={'responsive': True, 'displayModeBar': True})

    # 3. Kreisdiagramm: Gender-Verteilung in allen Sektoren
    fig3 = go.Figure(data=[go.Pie(
        labels=['Male', 'Female', 'Unknown'],
        values=overall_totals.values,
        marker=dict(colors=[male_color, female_color, unknown_color], line=dict(color='white', width=2)),
        hovertemplate='<b>%{label}</b><br>Anzahl: %{value}<br>Prozent: %{percent}<extra></extra>',
        textposition='auto',
        textinfo='label+percent'
    )])

    fig3.update_layout(
        title='Gender-Verteilung in allen Unicorn-Sektoren',
        height=600,
        template='plotly_white'
    )

    output_path3 = output_dir / 'rename__ai_sectors_gender_pie_chart.html'
    fig3.write_html(str(output_path3), config={'responsive': True, 'displayModeBar': True})

    print(f'Grafiken gespeichert in: {output_dir}')


if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    csv_path = root.parent / 'processed_data' / 'sectors_gender_counts.csv'
    output_dir = root.parent / 'plots'
    plot_sectors_gender_graphs(csv_path, output_dir)
