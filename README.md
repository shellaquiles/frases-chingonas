# Frases Python

Sistema completo para gestionar, visualizar y compartir frases inspiradas en libros técnicos y de desarrollo profesional.

## 📖 Descripción del Proyecto

Este proyecto es una colección de **frases originales inspiradas** en libros técnicos y de desarrollo profesional. Cada frase está diseñada para ser breve, contundente y con sentido conceptual o práctico, capturando el espíritu y los principios de los libros de referencia en programación, arquitectura de software, liderazgo y desarrollo personal.

### Características Principales

- 📚 **Colección de libros**: Más de 80 libros técnicos organizados por categorías y temas
- 💬 **Frases inspiradas**: Miles de frases originales basadas en los principios de cada libro
- 🎨 **Visualización web**: Interfaz moderna para navegar y visualizar las frases
- 📊 **Gestión de datos**: Herramientas para convertir, organizar y enriquecer la información
- 🔍 **API de libros**: Integración con Open Library para obtener portadas y metadatos

## 🏗️ Estructura del Proyecto

```
frases_python/
├── 📄 Datos principales (fuentes de verdad)
│   ├── libros.csv              # Lista de libros con metadatos
│   └── frases.csv              # Colección de frases
│
├── 🐍 Scripts de procesamiento (orden de ejecución)
│   └── scripts/
│       ├── 10_split_id_column.py      # Convierte formato de ID (opcional)
│       ├── 20_csv_to_json.py          # Convierte frases.csv a JSON
│       ├── 30_libros_to_json.py       # Convierte libros.csv a JSON
│       ├── 40_fetch_book_info.py      # Obtiene info de Open Library API (opcional)
│       ├── 50_generate_index_page.py  # Genera página principal con navegación ⭐
│       ├── 60_split_by_book.py        # Separa frases por libro
│       ├── 70_generate_html.py        # Genera la interfaz web (versión anterior)
│       └── 80_test_book_fetch.py      # Script de prueba
│
├── 🌐 Aplicación web
│   ├── server.py                # Servidor web local
│   └── public/                  # Archivos estáticos (para GitHub Pages)
│       ├── index.html           # Página principal
│       ├── css/                 # Estilos CSS modulares
│       ├── js/                  # JavaScript modular (ES6)
│       └── data/                 # Datos JSON (generados)
│           ├── frases.json      # Frases en formato JSON
│           ├── libros.json      # Libros en formato JSON
│           └── categorias.json # Categorías organizadas
│
└── 📚 Documentación
    ├── README.md                # Este archivo
    └── docs/
        ├── CONTRIBUTING.md      # Guía para colaboradores
        ├── SETUP.md             # Guía de instalación
        ├── prompt.md            # Instrucciones para generar frases
        ├── FETCH_BOOKS_README.md # Guía de uso de Open Library API
        └── PROYECTO_LISTO.md    # Checklist de preparación
```

## 🚀 Inicio Rápido

### Para Desarrolladores

#### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/frases_python.git
cd frases_python
```

#### 2. Preparar los Datos

```bash
# Convertir CSV a JSON
python3 scripts/20_csv_to_json.py
python3 scripts/30_libros_to_json.py
```

#### 3. Generar la Interfaz Web

```bash
# Generar página principal con navegación
python3 scripts/50_generate_index_page.py
```

Este script lee directamente desde `libros.csv` y `frases.csv` (fuentes de verdad) y genera la página web completa.

#### 4. Iniciar el Servidor Local

```bash
# Iniciar servidor en http://localhost:8000
python3 server.py
```

Abre tu navegador en: **http://localhost:8000/public/index.html**

### Para GitHub Pages

El proyecto está listo para GitHub Pages. Solo necesitas:

1. **Configurar GitHub Pages** en tu repositorio:
   - Settings → Pages
   - Source: `main` branch
   - Folder: `/public`

2. **Los archivos en `public/`** se servirán automáticamente

3. **Actualizar la página** cuando agregues nuevas frases:
   ```bash
   python3 scripts/50_generate_index_page.py
   git add public/
   git commit -m "Actualizar página con nuevas frases"
   git push
   ```

### Convertir Formato de ID (Opcional)

Si tienes un `frases.csv` con el formato antiguo (`id` como `PDS-096`), puedes convertirlo al nuevo formato (`clave,id`):

```bash
# Convertir formato antiguo a nuevo (crea backup automáticamente)
python3 scripts/10_split_id_column.py

# O especificar archivos personalizados
python3 scripts/10_split_id_column.py --input frases.csv --output frases_nuevo.csv
```

## 📋 Scripts Disponibles

### `10_split_id_column.py` ⭐ **Primero (si es necesario)**
Separa la columna `id` en `clave` e `id` en `frases.csv`. Convierte del formato antiguo (`PDS-096`) al nuevo (`PDS,96`).

```bash
# Convertir formato antiguo a nuevo (crea backup automáticamente)
python3 scripts/10_split_id_column.py

# Con opciones personalizadas
python3 scripts/10_split_id_column.py --input frases.csv --output frases_nuevo.csv --no-backup
```

### `20_csv_to_json.py`
Convierte `frases.csv` a `public/data/frases.json`

```bash
python3 scripts/20_csv_to_json.py [archivo_csv] [archivo_json]
```

### `30_libros_to_json.py`
Convierte `libros.csv` a `public/data/libros.json`

```bash
python3 scripts/30_libros_to_json.py [archivo_csv] [archivo_json]
```

### `40_fetch_book_info.py` (Opcional)
Obtiene información completa de libros desde Open Library API (portadas, ISBN, descripción, etc.)

```bash
# Obtener info de todos los libros
python3 scripts/40_fetch_book_info.py

# Con opciones personalizadas
python3 scripts/40_fetch_book_info.py --csv libros.csv --output libros_completos.json --delay 2.0
```

Ver [docs/FETCH_BOOKS_README.md](docs/FETCH_BOOKS_README.md) para más detalles.

### `50_generate_index_page.py` ⭐ **Recomendado - Principal**
Genera `public/index.html` con sistema de navegación completo. Lee directamente desde `libros.csv` y `frases.csv` (fuentes de verdad).

```bash
# Generar página principal con navegación
python3 scripts/50_generate_index_page.py
```

**Características**:
- Navegación por Libro, Categoría y Autor
- Grid de libros con portadas (si están disponibles)
- Filtrado de frases dinámico
- Compatible con GitHub Pages

### `60_split_by_book.py`
Separa `frases.csv` en múltiples archivos CSV, uno por cada libro

```bash
python3 scripts/60_split_by_book.py [frases.csv] [libros.csv] [directorio_salida]
```

### `70_generate_html.py` (Versión anterior)
Genera `public/index.html` con la interfaz web (versión anterior)

```bash
# Modo servidor (usa fetch para cargar JSON)
python3 scripts/70_generate_html.py

# Modo file:// (embebe JSON en el HTML)
python3 scripts/70_generate_html.py --file
```

### `server.py`
Inicia un servidor web local para servir la aplicación

```bash
# Puerto por defecto: 8000
python3 server.py

# Puerto personalizado
python3 server.py 8080
```

## 📊 Formato de Datos

### Frases (frases.csv)

**Formato actual (recomendado)**:
```csv
clave,id,frase,autor,fuente
DDD,001,"El dominio es el lenguaje que da sentido al software.","Eric Evans","Domain-Driven Design"
DDD,002,"Una arquitectura saludable refleja una comprensión profunda del dominio, no solo del código.","Eric Evans","Domain-Driven Design"
```

**Formato antiguo (soportado para compatibilidad)**:
```csv
id,frase,autor,fuente
DDD-001,"El dominio es el lenguaje que da sentido al software.","Eric Evans","Domain-Driven Design"
```

> **Nota**: Para convertir del formato antiguo al nuevo, usa:
> ```bash
> python3 scripts/10_split_id_column.py
> ```

### Libros (libros.csv)

```csv
frases_generadas,clave,titulo,autor,categoria,tema
✅,DDD,Domain-Driven Design,Eric Evans,Clásicos del Desarrollo,Diseño centrado en el dominio
```

## 🎨 Interfaz Web

La aplicación web incluye:

- **Visualización de frases**: Tarjetas con colores rotativos
- **Navegación fluida**: Diseño responsive y moderno
- **Estilos modulares**: CSS organizado por componentes
- **JavaScript ES6**: Código modular y mantenible

### Características de la UI

- Paleta de 16 colores para las tarjetas
- Diseño responsive (móvil, tablet, desktop)
- Estilos de impresión optimizados
- Carga dinámica de datos (fetch API)

## 📚 Categorías de Libros

Los libros están organizados en las siguientes categorías:

- **Clásicos del Desarrollo**: Fundamentos y principios atemporales
- **Serie Clean**: Libros de Robert C. Martin sobre código limpio
- **DevOps y SRE**: Operaciones y confiabilidad de sistemas
- **Testing y Calidad**: Pruebas y aseguramiento de calidad
- **Cloud, Data & Arquitectura Moderna**: Arquitectura moderna y datos
- **Liderazgo y Cultura**: Gestión de equipos y cultura organizacional
- **Desarrollo Personal**: Crecimiento profesional y personal
- **Seguridad y Resiliencia**: Seguridad y sistemas resilientes
- **Ciencia de Datos e IA**: Análisis de datos e inteligencia artificial

## 🔧 Requisitos

- **Python 3.6+** (solo librerías estándar, sin dependencias externas)
- **Navegador web moderno** (Chrome, Firefox, Safari, Edge)
- **Conexión a Internet** (solo para `fetch_book_info.py` - opcional)

### Sin Dependencias Externas

El proyecto usa solo librerías estándar de Python:
- `csv` - Para leer CSV
- `json` - Para generar JSON
- `pathlib` - Para manejo de rutas
- `urllib` - Para API de Open Library (opcional)

**No requiere** `pip install` ni `requirements.txt`. ¡Listo para usar!

## 📝 Generar Nuevas Frases

Para generar frases inspiradas en un libro, sigue las instrucciones en [docs/prompt.md](docs/prompt.md):

1. Usa la información del libro desde `libros.csv`
2. Sigue las instrucciones de estilo en `prompt.md`
3. Genera 100 frases en formato CSV
4. Agrega las frases a `frases.csv`

### Instrucciones de Estilo

- Cada frase debe estar inspirada en los principios del libro
- Tono profesional, reflexivo y técnico
- Breve, contundente y con sentido conceptual o práctico
- **Frases originales inspiradas**, no citas directas
- Formato de ID: `[CLAVE]-NNN` (ejemplo: `DDD-001`)

## 🌐 API de Open Library

El proyecto integra la API pública de Open Library para enriquecer la información de los libros:

- **Portadas**: URLs de portadas en alta resolución
- **ISBN**: Números de identificación
- **Descripción**: Resúmenes y descripciones
- **Metadatos**: Año de publicación, autores, etc.

Ver [docs/FETCH_BOOKS_README.md](docs/FETCH_BOOKS_README.md) para más información.

## 📄 Licencia

Ver archivo [LICENSE](LICENSE) para más detalles.

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Este proyecto sigue los principios de código limpio y buenas prácticas que promovemos en las frases.

### Guía Completa para Colaboradores

Ver [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) para la guía completa que incluye:

- ✅ Cómo clonar y configurar el proyecto
- ✅ Cómo agregar nuevas frases
- ✅ Cómo agregar nuevos libros
- ✅ Estándares de código (Python y JavaScript)
- ✅ Estilo de frases y ejemplos
- ✅ Flujo de trabajo con Git
- ✅ Checklist antes de contribuir

### Contribución Rápida

1. **Fork** el repositorio
2. **Crea una rama** para tu contribución
3. **Agrega frases** siguiendo [`docs/prompt.md`](docs/prompt.md)
4. **Prueba** que todo funcione:
   ```bash
   python3 scripts/50_generate_index_page.py
   python3 server.py
   ```
5. **Commit** y **Push** a tu fork
6. **Abre un Pull Request**

### Fuentes de Verdad

- **`libros.csv`**: Lista de libros (fuente de verdad)
- **`frases.csv`**: Colección de frases (fuente de verdad)

Todos los scripts leen directamente desde estos CSV. Los archivos JSON se generan automáticamente.

## 📊 Estadísticas

- **Libros en la colección**: 89
- **Frases generadas**: 6,900+
- **Categorías**: 9
- **Temas**: 80+

## 🔗 Enlaces Útiles

- [Open Library API](https://openlibrary.org/developers/api)
- [Documentación de la API](https://openlibrary.org/developers/api)

---

**Nota**: Este proyecto es una colección educativa de frases inspiradas en libros técnicos. Las frases son originales y están diseñadas para capturar el espíritu y los principios de los libros de referencia.
