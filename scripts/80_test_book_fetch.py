#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script de prueba para obtener información de un libro desde Open Library"""

import json
from fetch_book_info import enrich_book_info

# Probar con un libro conocido
test_book = {
    "frases_generadas": "✅",
    "clave": "DDD",
    "titulo": "Domain-Driven Design",
    "autor": "Eric Evans",
    "categoria": "Clásicos del Desarrollo",
    "tema": "Diseño centrado en el dominio"
}

print("🧪 Probando búsqueda de libro en Open Library API...\n")
print(f"Libro de prueba: {test_book['titulo']} - {test_book['autor']}\n")

result = enrich_book_info(test_book)

print("\n" + "="*60)
print("RESULTADO:")
print("="*60)
print(json.dumps(result, ensure_ascii=False, indent=2))
