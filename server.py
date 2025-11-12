#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor web simple para servir los archivos HTML y JSON
Útil para desarrollo local sin problemas de CORS
"""

import http.server
import os
import socketserver
import sys
from pathlib import Path

PORT = 8000


class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Handler personalizado para servir archivos con CORS habilitado"""

    def end_headers(self):
        # Agregar headers CORS para permitir fetch()
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def log_message(self, format, *args):
        # Log personalizado
        print(f"[{self.address_string()}] {format % args}")


def main():
    """Inicia el servidor web"""
    # Cambiar al directorio public/ para servir desde ahí
    base_dir = Path(__file__).parent
    public_dir = base_dir / "public"

    if not public_dir.exists():
        print(f"❌ Error: No se encontró el directorio 'public/' en {base_dir}")
        sys.exit(1)

    os.chdir(public_dir)

    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            print("=" * 60)
            print(f"🚀 Servidor web iniciado en http://localhost:{PORT}")
            print("=" * 60)
            print(f"📁 Sirviendo archivos desde: {public_dir}")
            print("🌐 Páginas disponibles:")
            url_base = f"http://localhost:{PORT}"
            print(f"   - {url_base}/index.html (Página principal)")
            print(f"   - {url_base}/libros.html (Catálogo de libros)")
            print(f"   - {url_base}/frases.html (Frases de un libro)")
            print("=" * 60)
            print("Presiona Ctrl+C para detener el servidor")
            print("=" * 60)
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor detenido")
        sys.exit(0)
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"❌ Error: El puerto {PORT} ya está en uso")
            print(f"   Intenta con otro puerto: python3 server.py {PORT + 1}")
        else:
            print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            PORT = int(sys.argv[1])
        except ValueError:
            print("❌ Error: El puerto debe ser un número")
            sys.exit(1)

    main()
