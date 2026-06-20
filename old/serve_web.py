import argparse
import functools
import http.server
import socketserver
import threading
import webbrowser
from pathlib import Path


def serve_web(output_dir: Path, port: int) -> None:
    root = output_dir.resolve()
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))

    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"Starte Webserver unter http://localhost:{port}/")
            print(f"Öffne Browser für {root / 'index.html'}")

            def _serve() -> None:
                try:
                    httpd.serve_forever()
                except KeyboardInterrupt:
                    pass

            thread = threading.Thread(target=_serve, daemon=True)
            thread.start()

            webbrowser.open(f"http://localhost:{port}/index.html")
            try:
                thread.join()
            except KeyboardInterrupt:
                print("Beende Webserver...")
                httpd.shutdown()
    except OSError as exc:
        raise SystemExit(f"Fehler beim Starten des Servers auf Port {port}: {exc}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Starte einen lokalen Webserver für die Unicorn-Gender-Webseite.'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Port für den lokalen Webserver (Standard: 8000)'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('web_output'),
        help='Verzeichnis mit index.html und Diagrammen (Standard: web_output)'
    )
    args = parser.parse_args()

    if not args.output_dir.exists():
        raise SystemExit(f"Fehler: Ausgabeverzeichnis '{args.output_dir}' existiert nicht.")
    if not (args.output_dir / 'index.html').exists():
        raise SystemExit(f"Fehler: '{args.output_dir / 'index.html'}' wurde nicht gefunden.")

    serve_web(args.output_dir, args.port)
