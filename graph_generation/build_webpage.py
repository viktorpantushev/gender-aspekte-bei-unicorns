from pathlib import Path


def build_webpage(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    images = sorted(
        [p.name for p in output_dir.iterdir() if p.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp'}]
    )

    html_lines = [
        '<!DOCTYPE html>',
        '<html lang="de">',
        '<head>',
        '  <meta charset="UTF-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '  <title>Unicorn Gender Charts</title>',
        '  <style>',
        '    body { font-family: Arial, sans-serif; margin: 0; padding: 0; background: #f6f6f6; color: #222; }',
        '    .page { max-width: 1200px; margin: auto; padding: 24px; }',
        '    h1 { margin-bottom: 0.5em; }',
        '    .chart { margin-bottom: 40px; padding: 18px; background: #fff; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); }',
        '    .chart h2 { margin: 0 0 12px; font-size: 1.2rem; }',
        '    .chart img { width: 100%; height: auto; border-radius: 8px; }',
        '    .footer { margin-top: 32px; font-size: 0.95rem; color: #555; }',
        '  </style>',
        '</head>',
        '<body>',
        '  <div class="page">',
        '    <h1>Unicorn Gender Charts</h1>',
        '    <p>Diese Seite zeigt die generierten Diagramme zur Gender-Verteilung von Unicorns.</p>',
    ]

    title_map = {
        'add_gender__current_unicorns_industry_counts.png': 'Aktuelle Unicorns: Anzahl je Branche',
        'add_gender_current_unicorns_industry_gender_stacked_bar.png': 'Aktuelle Unicorns: Gestapelte Genderverteilung je Branche',
        'ai_countries_gender_grouped_bar.png': 'Top 12 Länder: Unicorn-Gründer:innen nach Gender',
        'ai_sectors_gender_stacked_bar.png': 'Top 10 Unicorn-Sektoren: Gestapelte Genderverteilung',
        'change_x_axis__ai_exit_values_gender_stacked_bar.png': 'Top 12 Unicorn-Exits: Gestapelte Genderverteilung',
        'countries_gender_counts_totals.png': 'Gesamtanzahl der Unicorn-Gründer:innen nach Gender',
        'rename__ai_exit_values_gender_pie_chart.png': 'Gender-Verteilung bei Unicorn-Exit-Bewertungen',
        'rename__ai_sectors_gender_pie_chart.png': 'Gender-Verteilung in allen Unicorn-Sektoren',
        'rename_und_recolor__ai_sectors_total_bar.png': 'Top 15 Unicorn-Sektoren nach Anzahl',
    }

    for image in images:
        title = title_map.get(image, image.replace('_', ' ').replace('.png', '').replace('.jpg', '').replace('.jpeg', '').replace('.webp', ''))
        html_lines.extend([
            '    <div class="chart">',
            f'      <h2>{title}</h2>',
            f'      <img src="{image}" alt="{title}">',
            '    </div>',
        ])

    html_lines.extend([
        '    <div class="footer">',
        '      <p>Generiert aus den Quelldaten im Projekt.</p>',
        '    </div>',
        '  </div>',
        '</body>',
        '</html>',
    ])

    (output_dir / 'index.html').write_text('\n'.join(html_lines), encoding='utf-8')
    print(f'Webseite generiert: {output_dir / "index.html"}')


if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    build_webpage(root.parent / 'web_output')
