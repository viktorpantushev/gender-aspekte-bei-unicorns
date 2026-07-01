from pathlib import Path


def build_webpage(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Suche nach HTML-Dateien mit Diagrammen
    html_files = sorted(
        [p.name for p in output_dir.iterdir() if p.suffix.lower() == '.html' and p.name != 'index.html']
    )

    # Zuordnung von Dateinamen zu Titeln
    title_map = {
        'add_gender__current_unicorns_industry_counts.html': 'Aktuelle Unicorns: Anzahl je Branche',
        'add_gender_current_unicorns_industry_gender_stacked_bar.html': 'Aktuelle Unicorns: Gestapelte Genderverteilung je Branche',
        'ai_countries_gender_grouped_bar.html': 'Top 12 Länder: Unicorn-Gründer:innen nach Gender',
        'ai_sectors_gender_stacked_bar.html': 'Top 10 Unicorn-Sektoren: Gestapelte Genderverteilung',
        'change_x_axis__ai_exit_values_gender_stacked_bar.html': 'Top 12 Unicorn-Exits: Gestapelte Genderverteilung',
        'countries_gender_counts_totals.html': 'Gesamtanzahl der Unicorn-Gründer:innen nach Gender',
        'rename__ai_exit_values_gender_pie_chart.html': 'Gender-Verteilung bei Unicorn-Exit-Bewertungen',
        'rename__ai_sectors_gender_pie_chart.html': 'Gender-Verteilung in allen Unicorn-Sektoren',
        'rename_und_recolor__ai_sectors_total_bar.html': 'Top 15 Unicorn-Sektoren nach Anzahl',
    }

    html_lines = [
        '<!DOCTYPE html>',
        '<html lang="de">',
        '<head>',
        '  <meta charset="UTF-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '  <title>Unicorn Gender Charts</title>',
        '  <style>',
        '    body { font-family: Arial, sans-serif; margin: 0; padding: 0; background: #f6f6f6; color: #222; }',
        '    .page { max-width: 1400px; margin: auto; padding: 24px; }',
        '    h1 { margin-bottom: 0.5em; }',
        '    .chart { margin-bottom: 40px; padding: 18px; background: #fff; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); }',
        '    .chart h2 { margin: 0 0 12px; font-size: 1.2rem; }',
        '    .chart-container { width: 100%; height: auto; }',
        '    iframe { width: 100%; height: 600px; border: none; border-radius: 8px; }',
        '    .footer { margin-top: 32px; font-size: 0.95rem; color: #555; }',
        '  </style>',
        '</head>',
        '<body>',
        '  <div class="page">',
        '    <h1>Unicorn Gender Charts</h1>',
        '    <p>Diese Seite zeigt interaktive Diagramme zur Gender-Verteilung von Unicorns. Hovern Sie über die Diagramme, um Details zu sehen. Nutzen Sie die Toolbar rechts oben zum Zoomen, Verschieben und Speichern.</p>',
    ]

    for html_file in html_files:
        title = title_map.get(html_file, html_file.replace('_', ' ').replace('.html', ''))
        html_lines.extend([
            '    <div class="chart">',
            f'      <h2>{title}</h2>',
            f'      <iframe src="{html_file}"></iframe>',
            '    </div>',
        ])

    html_lines.extend([
        '    <div class="footer">',
        '      <p>Generiert aus den Quelldaten im Projekt. Alle Diagramme sind interaktiv und responsiv.</p>',
        '    </div>',
        '  </div>',
        '</body>',
        '</html>',
    ])

    (output_dir / 'index.html').write_text('\n'.join(html_lines), encoding='utf-8')
    print(f'Webseite generiert: {output_dir / "index.html"}')


if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    build_webpage(root.parent / 'plots')
