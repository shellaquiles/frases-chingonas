#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convierte libros.jsonl a libros.json para consumo en la web
"""

import json
import sys
from pathlib import Path


def convert_jsonl_to_json(jsonl_path, json_path):
    """Convierte un archivo JSONL a JSON"""
    libros = []

    try:
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    libro = json.loads(line)
                    libros.append(libro)
                except json.JSONDecodeError as e:
                    msg = f"⚠️  Error en línea {line_num}: {e}"
                    print(msg, file=sys.stderr)
                    continue

        # Crear directorio si no existe
        json_path.parent.mkdir(parents=True, exist_ok=True)

        # Escribir JSON con formato legible
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(libros, f, ensure_ascii=False, indent=2)

        print(f"✅ Convertidos {len(libros)} libros")
        print(f"📄 Archivo guardado en: {json_path}")
        return True

    except FileNotFoundError:
        msg = f"❌ Error: No se encontró el archivo {jsonl_path}"
        print(msg, file=sys.stderr)
        return False
    except (IOError, OSError) as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return False


def main():
    """Función principal"""
    # Rutas relativas al directorio del script
    script_dir = Path(__file__).parent.parent
    jsonl_path = script_dir / "libros.jsonl"
    json_path = script_dir / "public" / "data" / "libros.json"

    # Permitir rutas personalizadas
    if len(sys.argv) > 1:
        jsonl_path = Path(sys.argv[1])
    if len(sys.argv) > 2:
        json_path = Path(sys.argv[2])

    success = convert_jsonl_to_json(jsonl_path, json_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
