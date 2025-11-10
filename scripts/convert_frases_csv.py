#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convierte frases.csv a frases.json agrupado por libro (clave)
"""

import csv
import json
import sys
from pathlib import Path
from collections import defaultdict


def convert_frases_csv_to_json(csv_path, json_path):
    """Convierte frases.csv a JSON agrupado por clave (libro)"""
    frases_por_libro = defaultdict(list)

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row_num, row in enumerate(reader, 2):  # Empieza en 2 (header en 1)
                clave = (row.get('clave') or '').strip()
                frase_texto = (row.get('frase') or '').strip()

                if not clave or not frase_texto:
                    continue

                # Solo guardar la frase, la info del libro viene de libros.json
                frase = {
                    'frase': frase_texto
                }

                frases_por_libro[clave].append(frase)

        # Convertir defaultdict a dict normal para JSON
        frases_dict = dict(frases_por_libro)

        # Crear directorio si no existe
        json_path.parent.mkdir(parents=True, exist_ok=True)

        # Escribir JSON con formato legible
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(frases_dict, f, ensure_ascii=False, indent=2)

        total_frases = sum(len(frases) for frases in frases_dict.values())
        print(f"✅ Convertidas {total_frases} frases de {len(frases_dict)} libros")
        print(f"📄 Archivo guardado en: {json_path}")
        return True

    except FileNotFoundError:
        msg = f"❌ Error: No se encontró el archivo {csv_path}"
        print(msg, file=sys.stderr)
        return False
    except (IOError, OSError) as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return False


def main():
    """Función principal"""
    # Rutas relativas al directorio del script
    script_dir = Path(__file__).parent.parent
    csv_path = script_dir / "frases.csv"
    json_path = script_dir / "public" / "data" / "frases.json"

    # Permitir rutas personalizadas
    if len(sys.argv) > 1:
        csv_path = Path(sys.argv[1])
    if len(sys.argv) > 2:
        json_path = Path(sys.argv[2])

    success = convert_frases_csv_to_json(csv_path, json_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
