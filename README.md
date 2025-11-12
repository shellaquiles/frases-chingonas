# Frases Chingonas

Sistema completo para gestionar, visualizar y compartir frases inspiradas en libros técnicos y de desarrollo profesional.

## 📖 Descripción del Proyecto

Este proyecto es una colección de **frases originales inspiradas** en libros técnicos y de desarrollo profesional. Cada frase está diseñada para ser breve, contundente y con sentido conceptual o práctico, capturando el espíritu y los principios de los libros de referencia en programación, arquitectura de software, liderazgo y desarrollo personal.

### Características Principales

- 📚 **Colección de libros**: Libros técnicos organizados por categorías y temas
- 💬 **Frases inspiradas**: Miles de frases originales basadas en los principios de cada libro
- 🎨 **Interfaz web moderna**: Tres páginas interactivas con diseño responsive
- 🎯 **Navegación intuitiva**: Menú fijo, búsqueda y filtros avanzados
- 🖨️ **Optimizado para impresión**: Estilos de impresión con detección automática de color
- 🚀 **Despliegue automático**: GitHub Actions para despliegue continuo en GitHub Pages

## 🌐 Páginas Web

### 1. **index.html** - Página Principal
- Muestra una frase aleatoria a pantalla completa
- Diseño minimalista con efecto glassmorphism
- Enlaces a biblioteca y otra frase aleatoria
- Frase clickeable que lleva a las frases del libro

### 2. **libros.html** - Catálogo de Libros
- Grid de libros con portadas y metadatos
- Búsqueda en tiempo real por título, autor o tema
- Filtrado por categoría
- Ordenamiento por título, autor o fecha
- Modal con detalles completos del libro
- Botón para ver frases de cada libro

### 3. **frases.html** - Visualización de Frases
- Tarjetas de frases con paleta de 16 colores
- Vista de todas las frases o filtrado por libro específico
- Header dinámico con información del libro (cuando se filtra)
- Navegación fija con menú
- Tarjetas clickeables (cuando se muestran todas las frases)
- Estilos de impresión optimizados (3x3cm, con/sin color según impresora)

## 🏗️ Estructura del Proyecto

```
frases_python/
├── 📄 Datos principales (fuentes de verdad)
│   ├── frases.csv              # Colección de frases (clave, id, frase)
│   └── libros.jsonl            # Lista de libros con metadatos (JSONL)
│
├── 🐍 Scripts de procesamiento
│   └── scripts/
│       ├── convert_frases_csv.py    # Convierte frases.csv → public/data/frases.json
│       └── convert_libros_jsonl.py  # Convierte libros.jsonl → public/data/libros.json
│
├── 🌐 Aplicación web
│   ├── server.py                # Servidor web local (Python)
│   └── public/                   # Archivos estáticos (desplegados en GitHub Pages)
│       ├── index.html           # Página principal - Frase aleatoria
│       ├── libros.html          # Catálogo de libros
│       ├── frases.html          # Visualización de frases
│       │
│       ├── css/                 # Estilos CSS modulares
│       │   ├── variables.css    # Variables CSS compartidas
│       │   ├── base.css         # Reset y estilos base
│       │   ├── utils.css        # Utilidades compartidas
│       │   ├── index.css        # Estilos específicos de index.html
│       │   ├── libros.css       # Estilos específicos de libros.html
│       │   └── frases.css       # Estilos específicos de frases.html
│       │
│       ├── js/                  # JavaScript modular (ES6)
│       │   ├── api.js           # API compartida (loadBooks, loadFrases)
│       │   ├── constants.js     # Constantes compartidas (COLOR_PALETTE)
│       │   ├── utils.js         # Utilidades compartidas
│       │   ├── index.js         # Lógica de index.html
│       │   ├── libros.js        # Lógica de libros.html
│       │   └── frases.js        # Lógica de frases.html
│       │
│       └── data/                # Datos JSON (generados)
│           ├── frases.json      # Frases en formato JSON
│           └── libros.json      # Libros en formato JSON
│
├── 🔧 Configuración
│   ├── .github/
│   │   └── workflows/
│   │       └── deploy.yml       # Workflow de GitHub Actions
│   └── .gitignore
│
└── 📚 Documentación
    ├── README.md                # Este archivo
    ├── DEPLOY.md                # Guía de despliegue
    ├── CONTRIBUTING.md          # Guía para colaboradores
    └── LICENSE
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
# Convertir frases.csv a JSON
python3 scripts/convert_frases_csv.py

# Convertir libros.jsonl a JSON
python3 scripts/convert_libros_jsonl.py
```

#### 3. Iniciar el Servidor Local

```bash
# Iniciar servidor en http://localhost:8000
python3 server.py

# O en un puerto personalizado
python3 server.py 8001
```

Abre tu navegador en:
- **http://localhost:8000/index.html** - Página principal
- **http://localhost:8000/libros.html** - Catálogo de libros
- **http://localhost:8000/frases.html** - Todas las frases

### Para GitHub Pages (Despliegue Automático)

El proyecto está configurado con **GitHub Actions** para desplegarse automáticamente en GitHub Pages.

#### Configuración Inicial (Solo una vez)

1. **Habilitar GitHub Pages** en tu repositorio:
   - Ve a **Settings** > **Pages** en tu repositorio de GitHub
   - En **Source**, selecciona **GitHub Actions** (no "Deploy from a branch")
   - Guarda los cambios

2. **Verificar la rama principal**:
   - El workflow se ejecuta automáticamente cuando haces push a `main` o `master`
   - Asegúrate de que tu rama principal tenga uno de estos nombres

#### Despliegue Automático

Una vez configurado, cada vez que hagas push a `main` o `master`, el sitio se desplegará automáticamente:

```bash
# Actualizar datos y desplegar
python3 scripts/convert_frases_csv.py  # Si actualizaste frases.csv
python3 scripts/convert_libros_jsonl.py  # Si actualizaste libros.jsonl
git add public/
git commit -m "Actualizar sitio con nuevas frases"
git push
```

El workflow se ejecutará automáticamente y desplegará el contenido de `public/` a GitHub Pages.

#### Verificar el Despliegue

1. Ve a la pestaña **Actions** en GitHub
2. Verifica que el workflow "Deploy to GitHub Pages" se haya ejecutado correctamente
3. Tu sitio estará disponible en: `https://[tu-usuario].github.io/[nombre-repo]/`

> 📖 **Documentación completa**: Ver [DEPLOY.md](DEPLOY.md) para más detalles sobre el despliegue.

## 📋 Scripts Disponibles

### `convert_frases_csv.py`
Convierte `frases.csv` a `public/data/frases.json`

**Formato de entrada (frases.csv)**:
```csv
clave,id,frase
CC,001,"El código limpio se entiende en minutos, no en reuniones."
CC,002,"Si necesitas explicar tu función con un párrafo, en realidad necesitas una mejor función."
```

**Uso**:
```bash
python3 scripts/convert_frases_csv.py
```

### `convert_libros_jsonl.py`
Convierte `libros.jsonl` a `public/data/libros.json`

**Formato de entrada (libros.jsonl)**:
```jsonl
{"clave": "CC", "titulo": "Clean Code", "autor": "Robert C. Martin", "categoria": "Serie Clean", "tema": "Código Limpio", "portada": "https://...", ...}
```

**Uso**:
```bash
python3 scripts/convert_libros_jsonl.py
```

### `server.py`
Inicia un servidor web local para servir la aplicación

```bash
# Puerto por defecto: 8000
python3 server.py

# Puerto personalizado
python3 server.py 8080
```

## 🎨 Arquitectura Frontend

### CSS Modular

El proyecto utiliza una arquitectura CSS modular:

- **`variables.css`**: Variables CSS compartidas (colores, espaciado, tipografía, sombras, transiciones)
- **`base.css`**: Reset y estilos base
- **`utils.css`**: Utilidades compartidas (container, sr-only, hidden)
- **Estilos específicos**: `index.css`, `libros.css`, `frases.css`

### JavaScript Modular (ES6)

El proyecto utiliza módulos ES6 para compartir código:

- **`api.js`**: Funciones para cargar datos (loadBooks, loadFrases)
- **`constants.js`**: Constantes compartidas (COLOR_PALETTE)
- **`utils.js`**: Utilidades compartidas (escapeHtml, getUrlParam, shuffleArray, etc.)
- **Scripts específicos**: `index.js`, `libros.js`, `frases.js`

### Características de la UI

- **Paleta de 16 colores** para las tarjetas de frases
- **Diseño responsive** (móvil, tablet, desktop)
- **Estilos de impresión optimizados**:
  - Detección automática de impresora a color
  - Tarjetas de 3x3cm con bordes
  - Sin separación entre tarjetas
  - Márgenes: 1cm superior/inferior, 1.5cm laterales
- **Navegación fija** con menú glassmorphism
- **Carga dinámica de datos** (fetch API)

## 📊 Formato de Datos

### Frases (frases.csv)

```csv
clave,id,frase
CC,001,"El código limpio se entiende en minutos, no en reuniones."
CC,002,"Si necesitas explicar tu función con un párrafo, en realidad necesitas una mejor función."
DDD,001,"El dominio es el lenguaje que da sentido al software."
```

**Campos**:
- `clave`: Identificador del libro (ej: CC, DDD)
- `id`: Identificador único de la frase dentro del libro
- `frase`: Texto de la frase

### Libros (libros.jsonl)

```jsonl
{"clave": "CC", "titulo": "Clean Code", "autor": "Robert C. Martin", "categoria": "Serie Clean", "tema": "Código Limpio", "portada": "https://...", "descripcion": "...", "anio": 2008, "isbn": "978-0132350884"}
```

**Campos principales**:
- `clave`: Identificador único del libro
- `titulo`: Título del libro
- `autor`: Autor del libro
- `categoria`: Categoría del libro
- `tema`: Tema principal
- `portada`: URL de la portada del libro
- `descripcion`: Descripción del libro
- `anio`: Año de publicación
- `isbn`: ISBN del libro

## 🔧 Requisitos

- **Python 3.6+** (solo librerías estándar, sin dependencias externas)
- **Navegador web moderno** (Chrome, Firefox, Safari, Edge)
- **Git** (para despliegue en GitHub Pages)

### Sin Dependencias Externas

El proyecto usa solo librerías estándar de Python:
- `csv` - Para leer CSV
- `json` - Para generar JSON
- `pathlib` - Para manejo de rutas
- `http.server` - Para servidor web local

**No requiere** `pip install` ni `requirements.txt`. ¡Listo para usar!

## 🖨️ Impresión

El proyecto incluye estilos de impresión optimizados:

- **Detección automática**: Detecta si la impresora es a color o monocromo
- **Con color**: Mantiene gradientes y colores de las tarjetas
- **Sin color**: Fondo blanco con bordes negros
- **Tamaño**: Tarjetas de 3x3cm
- **Sin separación**: Tarjetas pegadas entre sí
- **Márgenes**: 1cm superior/inferior, 1.5cm laterales
- **Hoja carta**: Optimizado para formato letter

Para imprimir, simplemente presiona `Ctrl+P` (o `Cmd+P` en Mac) en cualquier página.

## 📝 Agregar Nuevas Frases

1. Edita `frases.csv` y agrega nuevas frases con el formato:
   ```csv
   clave,id,frase
   CC,003,"Nueva frase aquí"
   ```

2. Regenera el JSON:
   ```bash
   python3 scripts/convert_frases_csv.py
   ```

3. Haz commit y push:
   ```bash
   git add frases.csv public/data/frases.json
   git commit -m "Agregar nuevas frases"
   git push
   ```

## 📝 Agregar Nuevos Libros

1. Edita `libros.jsonl` y agrega un nuevo libro (una línea por libro):
   ```jsonl
   {"clave": "NUEVO", "titulo": "Nuevo Libro", "autor": "Autor", "categoria": "Categoría", "tema": "Tema", ...}
   ```

2. Regenera el JSON:
   ```bash
   python3 scripts/convert_libros_jsonl.py
   ```

3. Haz commit y push:
   ```bash
   git add libros.jsonl public/data/libros.json
   git commit -m "Agregar nuevo libro"
   git push
   ```

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Este proyecto sigue los principios de código limpio y buenas prácticas que promovemos en las frases.

### Guía Completa para Colaboradores

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para la guía completa que incluye:

- ✅ Cómo clonar y configurar el proyecto
- ✅ Cómo agregar nuevas frases
- ✅ Cómo agregar nuevos libros
- ✅ Estándares de código (Python y JavaScript)
- ✅ Flujo de trabajo con Git
- ✅ Checklist antes de contribuir

### Contribución Rápida

1. **Fork** el repositorio
2. **Crea una rama** para tu contribución
3. **Agrega frases o libros** siguiendo los formatos establecidos
4. **Regenera los JSON**:
   ```bash
   python3 scripts/convert_frases_csv.py
   python3 scripts/convert_libros_jsonl.py
   ```
5. **Prueba** que todo funcione:
   ```bash
   python3 server.py
   ```
6. **Commit** y **Push** a tu fork
7. **Abre un Pull Request**

### Fuentes de Verdad

- **`frases.csv`**: Colección de frases (fuente de verdad)
- **`libros.jsonl`**: Lista de libros (fuente de verdad)

Todos los scripts leen directamente desde estos archivos. Los archivos JSON se generan automáticamente.

## 📄 Licencia

Ver archivo [LICENSE](LICENSE) para más detalles.

## 🔗 Enlaces Útiles

- [GitHub Pages](https://pages.github.com/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [ES6 Modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules)

---

**Nota**: Este proyecto es una colección educativa de frases inspiradas en libros técnicos. Las frases son originales y están diseñadas para capturar el espíritu y los principios de los libros de referencia.
