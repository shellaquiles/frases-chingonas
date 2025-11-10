#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convierte frases.csv a frases.json"""

import csv
import json
import sys


def csv_to_json(csv_file="frases.csv", json_file="frases.json"):
    """Convierte un archivo CSV a JSON"""

    # Leer CSV y convertir a JSON
    frases = []
    try:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Soporte para formato nuevo (clave,id) y antiguo (id)
                clave = row.get("clave", "").strip()
                id_num = row.get("id", "").strip()

                # Si no hay clave separada, intentar extraer del id (formato antiguo)
                if not clave and "id" in row:
                    id_original = row["id"].strip()
                    if "-" in id_original:
                        clave, id_num = id_original.split("-", 1)
                        clave = clave.strip()
                        id_num = id_num.strip()
                    else:
                        clave = id_original
                        id_num = ""

                # Crear id completo para compatibilidad
                id_completo = f"{clave}-{id_num}" if clave and id_num else clave or id_num

                frases.append(
                    {
                        "clave": clave,
                        "id": id_num,
                        "id_completo": id_completo,
                        "frase": row.get("frase", "").strip(),
                        "autor": row.get("autor", "").strip(),
                        "fuente": row.get("fuente", "").strip(),
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
            json.dump(frases, f, ensure_ascii=False, indent=2)
        print(f"✅ Convertidas {len(frases)} frases de {csv_file} a {json_file}")
    except Exception as e:
        print(f"❌ Error al guardar el JSON: {e}")
        sys.exit(1)


if __name__ == "__main__":
    from pathlib import Path

    # Script está en scripts/, base_dir es el directorio padre (raíz del proyecto)
    base_dir = Path(__file__).parent.parent
    public_dir = base_dir / "public"
    data_dir = public_dir / "data"

    # Crear directorio data si no existe
    data_dir.mkdir(parents=True, exist_ok=True)

    csv_file = str(base_dir / "frases.csv")
    json_file = str(data_dir / "frases.json")

    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    if len(sys.argv) > 2:
        json_file = sys.argv[2]

    csv_to_json(csv_file, json_file)
