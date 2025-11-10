#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convierte libros.csv a libros.json"""

import csv
import json
import sys
from pathlib import Path


def libros_to_json(csv_file="libros.csv", json_file="libros.json"):
    """Convierte un archivo CSV de libros a JSON"""

    # Leer CSV y convertir a JSON
    libros = []
    try:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                libros.append(
                    {
                        "frases_generadas": row["frases_generadas"],
                        "clave": row["clave"],
                        "titulo": row["titulo"],
                        "autor": row["autor"],
                        "categoria": row["categoria"],
                        "tema": row["tema"],
                    }
                )
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {csv_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error al leer el CSV: {e}")
        sys.exit(1)

    # Guardar como JSON
    try:
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(libros, f, ensure_ascii=False, indent=2)
        print(f"✅ Convertidos {len(libros)} libros de {csv_file} a {json_file}")
    except Exception as e:
        print(f"❌ Error al guardar el JSON: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Obtener el directorio base del proyecto (donde está el script)
    base_dir = Path(__file__).parent
    public_dir = base_dir / "public"
    data_dir = public_dir / "data"

    # Crear directorio data si no existe
    data_dir.mkdir(parents=True, exist_ok=True)

    csv_file = str(base_dir / "libros.csv")
    json_file = str(data_dir / "libros.json")

    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    if len(sys.argv) > 2:
        json_file = sys.argv[2]

    libros_to_json(csv_file, json_file)
