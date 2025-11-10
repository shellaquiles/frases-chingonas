#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Separa frases.csv en múltiples archivos CSV, uno por cada libro
basado en libros.csv
"""

import csv
import sys
from collections import defaultdict
from pathlib import Path


def normalize_text(text):
    """Normaliza texto para comparación"""
    if not text:
        return ""
    return text.strip().lower()


def split_frases_by_book(
    frases_file="frases.csv", libros_file="libros.csv", output_dir="frases_por_libro"
):
    """Separa frases.csv en archivos CSV por libro"""

    # Crear directorio de salida
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Leer libros.csv para crear mapeo de títulos y claves
    libros_map = {}
    libros_info = {}

    print(f"📚 Leyendo {libros_file}...")
    try:
        with open(libros_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                clave = row["clave"].strip()
                titulo = row["titulo"].strip()
                autor = row["autor"].strip()

                # Mapear título normalizado a clave
                titulo_normalizado = normalize_text(titulo)
                libros_map[titulo_normalizado] = clave

                # Guardar información del libro
                libros_info[clave] = {
                    "titulo": titulo,
                    "autor": autor,
                    "categoria": row["categoria"].strip(),
                    "tema": row["tema"].strip(),
                }
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {libros_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error al leer {libros_file}: {e}")
        sys.exit(1)

    print(f"   Encontrados {len(libros_info)} libros")

    # Leer frases.csv y agrupar por libro
    frases_por_libro = defaultdict(list)
    frases_sin_libro = []

    print(f"\n📝 Leyendo {frases_file}...")
    try:
        with open(frases_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Filtrar filas que tienen el encabezado como datos
                if (
                    row.get("clave", "").lower() == "clave"
                    or row.get("id", "").lower() == "id"
                    or row.get("autor", "").lower() == "autor"
                    or row.get("fuente", "").lower() == "fuente"
                ):
                    continue

                # Obtener clave e id (nuevo formato) o id completo (formato antiguo)
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

                id_completo = f"{clave}-{id_num}" if clave and id_num else clave or id_num
                frase = row.get("frase", "").strip()
                autor = row.get("autor", "").strip()
                fuente = row.get("fuente", "").strip()

                # Intentar identificar el libro de dos formas:
                # 1. Por la clave directamente
                # 2. Por el título en la columna "fuente"
                libro_clave = None

                # Método 1: Usar la clave directamente
                if clave and clave in libros_info:
                    libro_clave = clave

                # Método 2: Título en la columna "fuente"
                if not libro_clave:
                    fuente_normalizada = normalize_text(fuente)
                    if fuente_normalizada in libros_map:
                        libro_clave = libros_map[fuente_normalizada]

                # Si encontramos el libro, agregar la frase
                if libro_clave:
                    frases_por_libro[libro_clave].append(
                        {
                            "clave": clave,
                            "id": id_num,
                            "id_completo": id_completo,
                            "frase": frase,
                            "autor": autor,
                            "fuente": fuente,
                        }
                    )
                else:
                    frases_sin_libro.append(
                        {
                            "clave": clave,
                            "id": id_num,
                            "id_completo": id_completo,
                            "frase": frase,
                            "autor": autor,
                            "fuente": fuente,
                        }
                    )
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {frases_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error al leer {frases_file}: {e}")
        sys.exit(1)

    print(
        f"   Total de frases leídas: {sum(len(frases) for frases in frases_por_libro.values()) + len(frases_sin_libro)}"
    )
    print(
        f"   Frases agrupadas por libro: {sum(len(frases) for frases in frases_por_libro.values())}"
    )
    if frases_sin_libro:
        print(f"   ⚠️  Frases sin libro asignado: {len(frases_sin_libro)}")

    # Crear archivo CSV por cada libro
    print(f"\n💾 Creando archivos CSV por libro...")
    archivos_creados = 0

    for clave, frases in frases_por_libro.items():
        if clave in libros_info:
            info = libros_info[clave]
            # Nombre del archivo: clave_titulo.csv (sanitizado)
            titulo_sanitizado = "".join(
                c if c.isalnum() or c in (" ", "-", "_") else "_"
                for c in info["titulo"]
            )
            titulo_sanitizado = titulo_sanitizado.replace(" ", "_")
            nombre_archivo = f"{clave}_{titulo_sanitizado}.csv"
            archivo_path = output_path / nombre_archivo

            # Escribir CSV
            with open(archivo_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(
                    f, fieldnames=["clave", "id", "frase", "autor", "fuente"]
                )
                writer.writeheader()
                writer.writerows(frases)

            archivos_creados += 1
            print(f"   ✅ {nombre_archivo}: {len(frases)} frases")

    # Crear archivo para frases sin libro asignado (si hay)
    if frases_sin_libro:
        archivo_sin_libro = output_path / "sin_libro_asignado.csv"
        with open(archivo_sin_libro, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=["clave", "id", "frase", "autor", "fuente"]
            )
            writer.writeheader()
            writer.writerows(frases_sin_libro)
        print(f"   ⚠️  sin_libro_asignado.csv: {len(frases_sin_libro)} frases")

    # Resumen
    print(f"\n✅ Proceso completado:")
    print(f"   - Archivos creados: {archivos_creados}")
    print(f"   - Directorio de salida: {output_path.absolute()}")

    if frases_sin_libro:
        print(
            f"\n⚠️  Nota: {len(frases_sin_libro)} frases no pudieron ser asignadas a ningún libro."
        )
        print(f"   Revisa sin_libro_asignado.csv para ver cuáles son.")


if __name__ == "__main__":
    frases_file = "frases.csv"
    libros_file = "libros.csv"
    output_dir = "frases_por_libro"

    if len(sys.argv) > 1:
        frases_file = sys.argv[1]
    if len(sys.argv) > 2:
        libros_file = sys.argv[2]
    if len(sys.argv) > 3:
        output_dir = sys.argv[3]

    split_frases_by_book(frases_file, libros_file, output_dir)
