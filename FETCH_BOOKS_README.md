# Obtener Información de Libros desde Open Library API

Este script permite obtener información completa de libros desde la API pública de Open Library, incluyendo portadas, ISBN, descripción y más.

## Requisitos

- Python 3.6+
- Conexión a Internet
- No se requieren dependencias adicionales (usa solo librerías estándar)

## Uso

### Obtener información de todos los libros

```bash
python3 fetch_book_info.py
```

Esto procesará todos los libros en `libros.csv` y guardará la información enriquecida en `public/data/libros_enriched.json`.

### Opciones disponibles

```bash
python3 fetch_book_info.py --help
```

Opciones:
- `--csv`: Archivo CSV de entrada (por defecto: `libros.csv`)
- `--output`: Archivo JSON de salida (por defecto: `public/data/libros_enriched.json`)
- `--delay`: Delay entre peticiones en segundos (por defecto: 1.0)

### Ejemplo con opciones personalizadas

```bash
python3 fetch_book_info.py --csv libros.csv --output libros_completos.json --delay 2.0
```

## Probar con un solo libro

Para probar el script con un solo libro:

```bash
python3 test_book_fetch.py
```

## Estructura de Datos

El script enriquece cada libro con la siguiente información adicional:

```json
{
  "frases_generadas": "✅",
  "clave": "DDD",
  "titulo": "Domain-Driven Design",
  "autor": "Eric Evans",
  "categoria": "Clásicos del Desarrollo",
  "tema": "Diseño centrado en el dominio",
  "openlibrary": {
    "work_key": "OL4464385W",
    "title": "Domain-Driven Design",
    "author_name": ["Eric Evans"],
    "first_publish_year": 2003,
    "isbn": "0321125215"
  },
  "portada": "https://covers.openlibrary.org/b/id/5548424-L.jpg",
  "isbn": "0321125215",
  "fecha_publicacion": 2003,
  "paginas": null,
  "descripcion": null
}
```

### Campos adicionales

- **openlibrary**: Objeto con información de Open Library
  - `work_key`: Identificador único del trabajo en Open Library
  - `title`: Título del libro
  - `author_name`: Lista de autores
  - `first_publish_year`: Año de primera publicación
  - `isbn`: ISBN del libro
- **portada**: URL de la portada del libro (formato Large)
- **isbn**: ISBN del libro
- **fecha_publicacion**: Año de publicación
- **paginas**: Número de páginas (si está disponible)
- **descripcion**: Descripción del libro (si está disponible)

## API de Open Library

Este script utiliza la API pública de Open Library:
- **Documentación**: https://openlibrary.org/developers/api
- **Búsqueda**: https://openlibrary.org/search.json
- **Portadas**: https://covers.openlibrary.org/

### Límites y Consideraciones

- La API de Open Library es gratuita y de código abierto
- Se recomienda un delay de al menos 1 segundo entre peticiones para no sobrecargar la API
- Algunos libros pueden no estar disponibles en Open Library
- Las portadas pueden no estar disponibles para todos los libros

## Ejemplo de Salida

Al ejecutar el script, verás un progreso similar a:

```
📚 Procesando 89 libros...

[1/89] ACC - Accelerate
  🔍 Buscando: 'Accelerate' por Nicole Forsgren
  ✅ Encontrado: Accelerate
     📷 Portada: https://covers.openlibrary.org/b/id/1234567-L.jpg

[2/89] APP - Apprenticeship Patterns
  🔍 Buscando: 'Apprenticeship Patterns' por Dave Hoover
  ✅ Encontrado: Apprenticeship Patterns
     📷 Portada: https://covers.openlibrary.org/b/id/2345678-L.jpg

...

✅ Información guardada en public/data/libros_enriched.json
📊 Resumen:
   - Total de libros: 89
   - Con portada: 75
   - Con ISBN: 68
   - Con descripción: 45
```

## Solución de Problemas

### Error de conexión

Si obtienes errores de conexión, verifica:
- Tu conexión a Internet
- Que la API de Open Library esté disponible
- Aumenta el delay entre peticiones (`--delay 2.0`)

### Libros no encontrados

Si un libro no se encuentra:
- Verifica que el título y autor estén correctos en el CSV
- Algunos libros técnicos pueden no estar en Open Library
- El script continuará con los demás libros

### Portadas no disponibles

Si no se encuentra portada para un libro:
- El campo `portada` será `null`
- Puedes buscar manualmente la portada en otros servicios
- Algunos libros pueden tener portadas disponibles en otros tamaños

## Integración con el Proyecto

El archivo JSON generado puede ser utilizado por:
- `libros_to_json.py`: Para actualizar el JSON de libros
- `generate_html.py`: Para generar HTML con portadas
- Cualquier otro script que necesite información completa de los libros
