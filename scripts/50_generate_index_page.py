#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera index.html con sistema de navegación y clasificación
Lee directamente desde libros.csv y frases.csv (fuentes de verdad)
"""

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path


def normalize_text(text):
    """Normaliza texto para comparación"""
    if not text:
        return ""
    return text.strip().lower()


def load_libros(csv_file):
    """Carga libros desde CSV"""
    libros = []
    libros_map = {}  # clave -> libro
    libros_by_titulo = {}  # titulo normalizado -> libro

    try:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                libro = {
                    "clave": row["clave"].strip(),
                    "titulo": row["titulo"].strip(),
                    "autor": row["autor"].strip(),
                    "categoria": row["categoria"].strip(),
                    "tema": row["tema"].strip(),
                    "frases_generadas": row["frases_generadas"].strip(),
                }
                libros.append(libro)
                libros_map[libro["clave"]] = libro
                libros_by_titulo[normalize_text(libro["titulo"])] = libro
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {csv_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error al leer {csv_file}: {e}")
        sys.exit(1)

    return libros, libros_map, libros_by_titulo


def load_frases(csv_file, libros_map, libros_by_titulo):
    """Carga frases desde CSV y las relaciona con libros"""
    frases = []
    frases_por_libro = defaultdict(list)
    frases_por_categoria = defaultdict(list)
    frases_por_autor = defaultdict(list)

    try:
        with open(csv_file, "r", encoding="utf-8") as f:
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

                frase = {
                    "clave": clave,
                    "id": id_num,
                    "id_completo": (
                        f"{clave}-{id_num}" if clave and id_num else clave or id_num
                    ),
                    "frase": row.get("frase", "").strip(),
                    "autor": row.get("autor", "").strip(),
                    "fuente": row.get("fuente", "").strip(),
                }

                # Relacionar con libro
                libro_clave = None
                libro_info = None

                # Método 1: Usar la clave directamente
                if clave and clave in libros_map:
                    libro_clave = clave
                    libro_info = libros_map[clave]

                # Método 2: Por título en la columna "fuente"
                if not libro_info:
                    fuente_normalizada = normalize_text(frase["fuente"])
                    if fuente_normalizada in libros_by_titulo:
                        libro_info = libros_by_titulo[fuente_normalizada]
                        libro_clave = libro_info["clave"]

                # Agregar información del libro a la frase
                if libro_info:
                    frase["libro_clave"] = libro_clave
                    frase["libro_titulo"] = libro_info["titulo"]
                    frase["libro_autor"] = libro_info["autor"]
                    frase["libro_categoria"] = libro_info["categoria"]
                    frase["libro_tema"] = libro_info["tema"]

                    # Agrupar por libro
                    frases_por_libro[libro_clave].append(frase)
                    # Agrupar por categoría
                    frases_por_categoria[libro_info["categoria"]].append(frase)
                    # Agrupar por autor del libro
                    frases_por_autor[libro_info["autor"]].append(frase)

                frases.append(frase)

    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {csv_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error al leer {csv_file}: {e}")
        sys.exit(1)

    return frases, frases_por_libro, frases_por_categoria, frases_por_autor


def load_enriched_libros(json_file):
    """Carga libros enriquecidos con portadas si existe"""
    enriched = {}
    try:
        if Path(json_file).exists():
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for libro in data:
                    clave = libro.get("clave")
                    if clave:
                        enriched[clave] = {
                            "portada": libro.get("portada"),
                            "isbn": libro.get("isbn"),
                            "descripcion": libro.get("descripcion"),
                            "fecha_publicacion": libro.get("fecha_publicacion"),
                        }
            print(f"✅ Cargados {len(enriched)} libros enriquecidos")
    except Exception as e:
        print(f"⚠️  No se pudo cargar libros enriquecidos: {e}")

    return enriched


def generate_html(
    libros,
    frases,
    frases_por_libro,
    frases_por_categoria,
    frases_por_autor,
    enriched_libros,
):
    """Genera el HTML de la página principal"""

    # Preparar datos para JavaScript
    libros_data = []
    for libro in libros:
        libro_data = {
            "clave": libro["clave"],
            "titulo": libro["titulo"],
            "autor": libro["autor"],
            "categoria": libro["categoria"],
            "tema": libro["tema"],
            "frases_count": len(frases_por_libro.get(libro["clave"], [])),
        }
        # Agregar datos enriquecidos si existen
        if libro["clave"] in enriched_libros:
            libro_data.update(enriched_libros[libro["clave"]])
        libros_data.append(libro_data)

    # Preparar categorías únicas
    categorias = sorted(set(libro["categoria"] for libro in libros))
    categorias_data = [
        {
            "nombre": cat,
            "libros_count": sum(1 for libro in libros if libro["categoria"] == cat),
            "frases_count": len(frases_por_categoria.get(cat, [])),
        }
        for cat in categorias
    ]

    # Preparar autores únicos
    autores = sorted(set(libro["autor"] for libro in libros))
    autores_data = [
        {
            "nombre": autor,
            "libros_count": sum(1 for libro in libros if libro["autor"] == autor),
            "frases_count": len(frases_por_autor.get(autor, [])),
        }
        for autor in autores
    ]

    # Convertir a JSON para JavaScript
    libros_json = json.dumps(libros_data, ensure_ascii=False, indent=2)
    frases_json = json.dumps(frases, ensure_ascii=False, indent=2)
    categorias_json = json.dumps(categorias_data, ensure_ascii=False, indent=2)
    autores_json = json.dumps(autores_data, ensure_ascii=False, indent=2)

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Frases Chingonas - Navegación</title>
  <link rel="stylesheet" href="css/main.css">
  <style>
    /* Estilos adicionales para navegación */
    .navigation {{
      padding: 2rem;
      background: #f5f5f5;
      border-bottom: 2px solid #ddd;
    }}
    .nav-buttons {{
      display: flex;
      gap: 1rem;
      flex-wrap: wrap;
      margin-bottom: 1rem;
    }}
    .nav-button {{
      padding: 0.75rem 1.5rem;
      background: #007bff;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-size: 1rem;
      transition: background 0.3s;
    }}
    .nav-button:hover {{
      background: #0056b3;
    }}
    .nav-button.active {{
      background: #28a745;
    }}
    .index-view {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 1rem;
      padding: 2rem;
    }}
    .index-item {{
      padding: 1rem;
      background: white;
      border: 1px solid #ddd;
      border-radius: 4px;
      cursor: pointer;
      transition: transform 0.2s, box-shadow 0.2s;
    }}
    .index-item:hover {{
      transform: translateY(-2px);
      box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    .index-item.book {{
      text-align: center;
    }}
    .index-item.book img {{
      width: 100%;
      max-width: 150px;
      height: auto;
      margin-bottom: 0.5rem;
    }}
    .index-item h3 {{
      margin: 0.5rem 0;
      font-size: 1rem;
    }}
    .index-item p {{
      margin: 0.25rem 0;
      font-size: 0.875rem;
      color: #666;
    }}
    .breadcrumbs {{
      padding: 1rem 2rem;
      background: #e9ecef;
      border-bottom: 1px solid #ddd;
    }}
    .breadcrumbs a {{
      color: #007bff;
      text-decoration: none;
    }}
    .breadcrumbs a:hover {{
      text-decoration: underline;
    }}
    .content-area {{
      min-height: 400px;
    }}
    .hidden {{
      display: none;
    }}
  </style>
</head>
<body>
  <div class="navigation">
    <h1>Frases Chingonas</h1>
    <div class="nav-buttons">
      <button class="nav-button" data-view="libros">Por Libro</button>
      <button class="nav-button" data-view="categorias">Por Categoría</button>
      <button class="nav-button" data-view="autores">Por Autor</button>
      <button class="nav-button" data-view="todas">Todas las Frases</button>
    </div>
    <div class="breadcrumbs" id="breadcrumbs">
      <a href="#" onclick="showIndex(); return false;">Inicio</a>
    </div>
  </div>

  <div class="content-area" id="content">
    <!-- Contenido dinámico -->
  </div>

  <script type="module">
    // Datos embebidos desde CSV
    const LIBROS = {libros_json};
    const FRASES = {frases_json};
    const CATEGORIAS = {categorias_json};
    const AUTORES = {autores_json};

    // Importar módulos
    import {{ generateCards }} from './js/card.js';
    import {{ CONFIG }} from './js/config.js';

    // Estado de la aplicación
    let currentView = null;
    let currentFilter = null;

    // Función para mostrar índice de libros
    function showLibrosIndex() {{
      const content = document.getElementById('content');
      content.innerHTML = '<div class="index-view" id="index-view"></div>';
      const indexView = document.getElementById('index-view');

      LIBROS.forEach(libro => {{
        const item = document.createElement('div');
        item.className = 'index-item book';
        item.onclick = () => showFrasesByLibro(libro.clave);

        let html = '';
        if (libro.portada) {{
          html += `<img src="${{libro.portada}}" alt="${{libro.titulo}}" />`;
        }} else {{
          html += '<div style="width:100%;height:200px;background:#ddd;display:flex;align-items:center;justify-content:center;font-size:3rem;">📚</div>';
        }}
        html += `<h3>${{libro.titulo}}</h3>`;
        html += `<p>${{libro.autor}}</p>`;
        html += `<p><small>${{libro.frases_count}} frases</small></p>`;

        item.innerHTML = html;
        indexView.appendChild(item);
      }});
    }}

    // Función para mostrar índice de categorías
    function showCategoriasIndex() {{
      const content = document.getElementById('content');
      content.innerHTML = '<div class="index-view" id="index-view"></div>';
      const indexView = document.getElementById('index-view');

      CATEGORIAS.forEach(categoria => {{
        const item = document.createElement('div');
        item.className = 'index-item';
        item.onclick = () => showFrasesByCategoria(categoria.nombre);

        item.innerHTML = `
          <h3>${{categoria.nombre}}</h3>
          <p>${{categoria.libros_count}} libros</p>
          <p><small>${{categoria.frases_count}} frases</small></p>
        `;
        indexView.appendChild(item);
      }});
    }}

    // Función para mostrar índice de autores
    function showAutoresIndex() {{
      const content = document.getElementById('content');
      content.innerHTML = '<div class="index-view" id="index-view"></div>';
      const indexView = document.getElementById('index-view');

      AUTORES.forEach(autor => {{
        const item = document.createElement('div');
        item.className = 'index-item';
        item.onclick = () => showFrasesByAutor(autor.nombre);

        item.innerHTML = `
          <h3>${{autor.nombre}}</h3>
          <p>${{autor.libros_count}} libros</p>
          <p><small>${{autor.frases_count}} frases</small></p>
        `;
        indexView.appendChild(item);
      }});
    }}

    // Función para mostrar frases filtradas
    function showFrases(frasesFiltradas, titulo) {{
      const content = document.getElementById('content');
      content.innerHTML = '';
      generateCards(frasesFiltradas, CONFIG.COLORS);
      updateBreadcrumbs(titulo);
    }}

    // Función para mostrar frases por libro
    function showFrasesByLibro(clave) {{
      const frasesFiltradas = FRASES.filter(f => f.libro_clave === clave);
      const libro = LIBROS.find(l => l.clave === clave);
      const titulo = libro ? libro.titulo : `Libro ${{clave}}`;
      showFrases(frasesFiltradas, titulo);
    }}

    // Función para mostrar frases por categoría
    function showFrasesByCategoria(categoria) {{
      const frasesFiltradas = FRASES.filter(f => f.libro_categoria === categoria);
      showFrases(frasesFiltradas, `Categoría: ${{categoria}}`);
    }}

    // Función para mostrar frases por autor
    function showFrasesByAutor(autor) {{
      const frasesFiltradas = FRASES.filter(f => f.libro_autor === autor);
      showFrases(frasesFiltradas, `Autor: ${{autor}}`);
    }}

    // Función para mostrar todas las frases
    function showTodasFrases() {{
      showFrases(FRASES, 'Todas las Frases');
    }}

    // Función para mostrar índice
    function showIndex() {{
      if (currentView === 'libros') {{
        showLibrosIndex();
      }} else if (currentView === 'categorias') {{
        showCategoriasIndex();
      }} else if (currentView === 'autores') {{
        showAutoresIndex();
      }}
      updateBreadcrumbs('Inicio');
    }}

    // Función para actualizar breadcrumbs
    function updateBreadcrumbs(titulo) {{
      const breadcrumbs = document.getElementById('breadcrumbs');
      breadcrumbs.innerHTML = `<a href="#" onclick="showIndex(); return false;">Inicio</a> > ${{titulo}}`;
    }}

    // Manejar botones de navegación
    document.querySelectorAll('.nav-button').forEach(button => {{
      button.addEventListener('click', () => {{
        const view = button.dataset.view;
        currentView = view;

        // Actualizar botones activos
        document.querySelectorAll('.nav-button').forEach(b => b.classList.remove('active'));
        button.classList.add('active');

        // Mostrar vista correspondiente
        if (view === 'libros') {{
          showLibrosIndex();
        }} else if (view === 'categorias') {{
          showCategoriasIndex();
        }} else if (view === 'autores') {{
          showAutoresIndex();
        }} else if (view === 'todas') {{
          showTodasFrases();
        }}
      }});
    }});

    // Mostrar índice de libros por defecto
    showLibrosIndex();
    document.querySelector('[data-view="libros"]').classList.add('active');
  </script>
</body>
</html>"""

    return html


def main():
    """Función principal"""
    # Script está en scripts/, base_dir es el directorio padre (raíz del proyecto)
    base_dir = Path(__file__).parent.parent
    public_dir = base_dir / "public"
    data_dir = public_dir / "data"

    # Rutas de archivos
    libros_csv = base_dir / "libros.csv"
    frases_csv = base_dir / "frases.csv"
    enriched_json = data_dir / "libros_enriched.json"
    output_html = public_dir / "index.html"

    print("📚 Cargando libros desde libros.csv...")
    libros, libros_map, libros_by_titulo = load_libros(libros_csv)
    print(f"   ✅ Cargados {len(libros)} libros")

    print("\n📝 Cargando frases desde frases.csv...")
    frases, frases_por_libro, frases_por_categoria, frases_por_autor = load_frases(
        frases_csv, libros_map, libros_by_titulo
    )
    print(f"   ✅ Cargadas {len(frases)} frases")
    print(
        f"   📊 Frases relacionadas con libros: {sum(len(fs) for fs in frases_por_libro.values())}"
    )

    print("\n🔍 Cargando libros enriquecidos (portadas)...")
    enriched_libros = load_enriched_libros(enriched_json)

    print("\n🌐 Generando index.html...")
    html = generate_html(
        libros,
        frases,
        frases_por_libro,
        frases_por_categoria,
        frases_por_autor,
        enriched_libros,
    )

    # Guardar HTML
    try:
        with open(output_html, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ Página generada en {output_html}")
        print(f"\n📊 Resumen:")
        print(f"   - Libros: {len(libros)}")
        print(f"   - Frases: {len(frases)}")
        print(f"   - Categorías: {len(set(libro['categoria'] for libro in libros))}")
        print(f"   - Autores: {len(set(libro['autor'] for libro in libros))}")
        print(
            f"   - Libros con portadas: {sum(1 for l in enriched_libros.values() if l.get('portada'))}"
        )
        print(f"\n🚀 Para ver la página:")
        print(f"   python3 server.py")
        print(f"   O abre: http://localhost:8000/public/index.html")
    except Exception as e:
        print(f"❌ Error al guardar HTML: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
