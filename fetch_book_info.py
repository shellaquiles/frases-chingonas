#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Obtiene información completa de libros desde Open Library API"""

import csv
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, Optional


def fetch_json(url: str, timeout: int = 10) -> Optional[Dict]:
    """Obtiene y parsea JSON desde una URL"""
    try:
        req = urllib.request.Request(url)
        user_agent = "Mozilla/5.0 (compatible; BookInfoBot/1.0)"
        req.add_header("User-Agent", user_agent)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"  ⚠️  Error al obtener {url}: {e}")
        return None


def search_book(title: str, author: str) -> Optional[Dict]:
    """Busca un libro en Open Library por título y autor"""
    # Limpiar título y autor para la búsqueda
    title_clean = title.strip()
    if "," in author:
        author_clean = author.split(",")[0].strip()
    else:
        author_clean = author.strip()
    if "&" in author_clean:
        author_clean = author_clean.split("&")[0].strip()

    # Construir URL de búsqueda
    params = {
        "title": title_clean,
        "author": author_clean,
        "limit": 1,
        "fields": (
            "key,title,author_name,first_publish_year,"
            "isbn,cover_i,cover_edition_key,edition_key"
        ),
    }
    query_string = urllib.parse.urlencode(params)
    search_url = f"https://openlibrary.org/search.json?{query_string}"

    print(f"  🔍 Buscando: '{title_clean}' por {author_clean}")
    data = fetch_json(search_url)

    if not data or "docs" not in data or len(data["docs"]) == 0:
        return None

    # Obtener el primer resultado
    book_data = data["docs"][0]

    # Obtener información detallada del work
    work_key = book_data.get("key", "")
    if work_key:
        work_url = f"https://openlibrary.org{work_key}.json"
        work_data = fetch_json(work_url)
        if work_data:
            book_data["work_details"] = work_data

    return book_data


def get_cover_url(book_data: Dict) -> Optional[str]:
    """Obtiene la URL de la portada del libro"""
    # Intentar diferentes métodos para obtener la portada

    # Método 1: cover_i (ID de portada)
    cover_i = book_data.get("cover_i")
    if cover_i:
        return f"https://covers.openlibrary.org/b/id/{cover_i}-L.jpg"

    # Método 2: cover_edition_key
    cover_edition_key = book_data.get("cover_edition_key")
    if cover_edition_key:
        base_url = "https://covers.openlibrary.org/b/olid"
        return f"{base_url}/{cover_edition_key}-L.jpg"

    # Método 3: edition_key
    edition_keys = book_data.get("edition_key", [])
    if edition_keys:
        base_url = "https://covers.openlibrary.org/b/olid"
        return f"{base_url}/{edition_keys[0]}-L.jpg"

    # Método 4: work_details
    work_details = book_data.get("work_details", {})
    covers = work_details.get("covers", [])
    if covers:
        return f"https://covers.openlibrary.org/b/id/{covers[0]}-L.jpg"

    return None


def enrich_book_info(book_row: Dict) -> Dict:
    """Enriquece la información de un libro con datos de Open Library"""
    title = book_row["titulo"]
    author = book_row["autor"]

    # Buscar el libro
    book_data = search_book(title, author)

    if not book_data:
        print(f"  ❌ No se encontró información para '{title}'")
        return {
            **book_row,
            "openlibrary": None,
            "portada": None,
            "isbn": None,
            "descripcion": None,
            "fecha_publicacion": None,
            "paginas": None,
        }

    # Extraer información relevante
    enriched = {
        **book_row,
        "openlibrary": {
            "work_key": book_data.get("key", "").replace("/works/", ""),
            "title": book_data.get("title", title),
            "author_name": book_data.get("author_name", [author]),
            "first_publish_year": book_data.get("first_publish_year"),
            "isbn": (
                book_data.get("isbn", [None])[0] if book_data.get("isbn") else None
            ),
        },
        "portada": get_cover_url(book_data),
        "isbn": (book_data.get("isbn", [None])[0] if book_data.get("isbn") else None),
        "fecha_publicacion": book_data.get("first_publish_year"),
        "paginas": None,
        "descripcion": None,
    }

    # Intentar obtener descripción del work_details
    work_details = book_data.get("work_details", {})
    if work_details:
        description = work_details.get("description")
        if description:
            if isinstance(description, dict):
                enriched["descripcion"] = description.get("value", "")
            else:
                enriched["descripcion"] = str(description)

    print(f"  ✅ Encontrado: {enriched['openlibrary']['title']}")
    if enriched["portada"]:
        print(f"     📷 Portada: {enriched['portada']}")

    return enriched


def fetch_all_books(
    csv_file: str = "libros.csv", output_file: Optional[str] = None, delay: float = 1.0
):
    """Obtiene información de todos los libros desde Open Library"""

    base_dir = Path(__file__).parent
    public_dir = base_dir / "public"
    data_dir = public_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    csv_path = base_dir / csv_file
    if output_file:
        json_path = Path(output_file)
    else:
        json_path = data_dir / "libros_enriched.json"

    # Leer libros desde CSV
    libros = []
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                libros.append(row)
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {csv_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error al leer el CSV: {e}")
        sys.exit(1)

    print(f"📚 Procesando {len(libros)} libros...\n")

    # Enriquecer cada libro
    libros_enriched = []
    for i, libro in enumerate(libros, 1):
        print(f"[{i}/{len(libros)}] {libro['clave']} - {libro['titulo']}")
        enriched = enrich_book_info(libro)
        libros_enriched.append(enriched)

        # Delay para no sobrecargar la API
        if i < len(libros):
            time.sleep(delay)
        print()

    # Guardar resultados
    try:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(libros_enriched, f, ensure_ascii=False, indent=2)
        print(f"✅ Información guardada en {json_path}")
        print("📊 Resumen:")
        total = len(libros_enriched)
        con_portada = sum(1 for libro in libros_enriched if libro.get("portada"))
        con_isbn = sum(1 for libro in libros_enriched if libro.get("isbn"))
        con_desc = sum(1 for libro in libros_enriched if libro.get("descripcion"))
        print(f"   - Total de libros: {total}")
        print(f"   - Con portada: {con_portada}")
        print(f"   - Con ISBN: {con_isbn}")
        print(f"   - Con descripción: {con_desc}")
    except Exception as e:
        print(f"❌ Error al guardar el JSON: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse

    desc = "Obtiene información de libros desde Open Library API"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("--csv", default="libros.csv", help="Archivo CSV de entrada")
    parser.add_argument("--output", help="Archivo JSON de salida")
    parser.add_argument(
        "--delay", type=float, default=1.0, help="Delay entre peticiones (segundos)"
    )

    args = parser.parse_args()

    fetch_all_books(args.csv, args.output, args.delay)
