#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Separa la columna 'id' en 'clave' e 'id' en frases.csv

Convierte:
  id,frase,autor,fuente
  PDS-096,"frase","autor","libro"

A:
  clave,id,frase,autor,fuente
  PDS,96,"frase","autor","libro"
"""

import csv
import sys
from pathlib import Path


def split_id_column(input_file="frases.csv", output_file=None, backup=True):
    """
    Separa la columna 'id' en 'clave' e 'id'

    Args:
        input_file: Archivo CSV de entrada
        output_file: Archivo CSV de salida (si es None, sobrescribe el original)
        backup: Si True, crea un backup del archivo original
    """
    base_dir = Path(__file__).parent.parent
    input_path = base_dir / input_file

    if output_file:
        output_path = base_dir / output_file
    else:
        output_path = input_path

    # Crear backup si es necesario
    if backup and not output_file:
        backup_path = base_dir / f"{input_file}.backup"
        print(f"📋 Creando backup: {backup_path}")
        with open(input_path, "r", encoding="utf-8") as f_in:
            with open(backup_path, "w", encoding="utf-8") as f_out:
                f_out.write(f_in.read())

    # Leer y transformar
    frases = []
    total = 0
    errores = 0

    print(f"📖 Leyendo {input_path}...")
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                total += 1

                # Filtrar filas que tienen el encabezado como datos
                if (
                    row.get("id", "").lower() == "id"
                    or row.get("autor", "").lower() == "autor"
                    or row.get("fuente", "").lower() == "fuente"
                ):
                    continue

                id_original = row.get("id", "").strip()

                # Separar clave e id
                if "-" in id_original:
                    clave, id_num = id_original.split("-", 1)
                    clave = clave.strip()
                    id_num = id_num.strip()
                else:
                    # Si no tiene guion, intentar separar de otra forma
                    # o usar el id completo como clave
                    clave = id_original
                    id_num = ""
                    errores += 1
                    print(f"  ⚠️  ID sin formato esperado: {id_original}")

                # Crear nueva fila
                nueva_fila = {
                    "clave": clave,
                    "id": id_num,
                    "frase": row.get("frase", "").strip(),
                    "autor": row.get("autor", "").strip(),
                    "fuente": row.get("fuente", "").strip(),
                }

                frases.append(nueva_fila)

    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {input_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error al leer el CSV: {e}")
        sys.exit(1)

    # Escribir nuevo CSV
    print(f"💾 Escribiendo {output_path}...")
    try:
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            fieldnames = ["clave", "id", "frase", "autor", "fuente"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(frases)

        print(f"✅ Archivo transformado exitosamente")
        print(f"   - Total de filas procesadas: {total}")
        print(f"   - Frases transformadas: {len(frases)}")
        if errores > 0:
            print(f"   - ⚠️  Errores encontrados: {errores}")
        print(f"   - Archivo guardado en: {output_path}")
        if backup and not output_file:
            print(f"   - Backup guardado en: {backup_path}")

    except Exception as e:
        print(f"❌ Error al escribir el CSV: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Separa la columna 'id' en 'clave' e 'id' en frases.csv"
    )
    parser.add_argument(
        "--input",
        default="frases.csv",
        help="Archivo CSV de entrada (por defecto: frases.csv)"
    )
    parser.add_argument(
        "--output",
        help="Archivo CSV de salida (si no se especifica, sobrescribe el original)"
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="No crear backup del archivo original"
    )

    args = parser.parse_args()

    split_id_column(
        input_file=args.input,
        output_file=args.output,
        backup=not args.no_backup
    )
