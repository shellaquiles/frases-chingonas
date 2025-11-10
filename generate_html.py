#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera index.html modularizado con CSS y JS externos

El HTML generado usa archivos externos:
- css/main.css: Estilos CSS
- js/app.js: Lógica JavaScript
- data/frases.json: Datos JSON (cargado vía fetch o embebido)

Opciones:
- Sin argumentos: Modo servidor (usa fetch() para cargar frases.json)
- --file o -f: Modo file:// (embebe el JSON directamente en el HTML)
"""

import csv
import json
import sys
from pathlib import Path

# Obtener el directorio base del proyecto (donde está el script)
base_dir = Path(__file__).parent
public_dir = base_dir / "public"
data_dir = public_dir / "data"

# Determinar modo: 'server' (fetch) o 'file' (embebido)
mode = "server"  # Por defecto usa fetch (requiere servidor)
if len(sys.argv) > 1:
    if sys.argv[1] in ["--file", "-f"]:
        mode = "file"
    elif sys.argv[1] in ["--server", "-s"]:
        mode = "server"

# Leer CSV si es modo file://
frases = []
if mode == "file":
    csv_file = base_dir / "frases.csv"
    try:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Filtrar filas que tienen el encabezado como datos
                if (
                    row["id"].lower() == "id"
                    or row["autor"].lower() == "autor"
                    or row["fuente"].lower() == "fuente"
                ):
                    continue
                frases.append(
                    {
                        "id": row["id"],
                        "frase": row["frase"],
                        "autor": row["autor"],
                        "fuente": row["fuente"],
                    }
                )
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {csv_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error al leer el CSV: {e}")
        sys.exit(1)

# Template HTML modularizado
if mode == "file":
    # Modo file:// - embebe el JSON directamente
    frases_json = json.dumps(frases, ensure_ascii=False, indent=2)
    html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Tarjetas PythonCDMX - Paleta Completa</title>
  <link rel="stylesheet" href="css/main.css">
</head>
<body>
  <script type="module">
    // Colores disponibles en orden
    const colores = [
      'verde', 'azul', 'amarillo', 'morado', 'rojo', 'gris',
      'naranja', 'turquesa', 'menta', 'lila', 'mostaza', 'grafito',
      'cian', 'magenta', 'cafe', 'blanco'
    ];

    // Frases embebidas (modo file://)
    const frases = {frases_json};

    // Importar funciones de los módulos
    import {{ escapeHtml }} from './js/utils.js';

    // Función para generar las tarjetas
    function generarTarjetas() {{
      const body = document.body;
      body.innerHTML = ''; // Limpiar el body antes de generar

      frases.forEach((item, index) => {{
        const color = colores[index % colores.length];
        const card = document.createElement('div');
        card.className = `card ${{color}}`;

        const cardPhrase = document.createElement('div');
        cardPhrase.className = 'card-phrase';
        cardPhrase.textContent = item.frase;

        const cardMeta = document.createElement('div');
        cardMeta.className = 'card-meta';
        cardMeta.innerHTML = escapeHtml(item.autor) + (item.fuente ? '<br>' + escapeHtml(item.fuente) : '');

        card.appendChild(cardPhrase);
        card.appendChild(cardMeta);
        body.appendChild(card);
      }});
    }}

    // Generar tarjetas al cargar la página
    generarTarjetas();
  </script>
</body>
</html>"""
else:
    # Modo servidor - usa fetch()
    html_template = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Tarjetas PythonCDMX - Paleta Completa</title>
  <link rel="stylesheet" href="css/main.css">
</head>
<body>
  <script type="module" src="js/app.js"></script>
</body>
</html>"""

# Guardar el HTML
with open(public_dir / "index.html", "w", encoding="utf-8") as f:
    f.write(html_template)

# Mostrar resumen
print(
    f"✅ Generado index.html modularizado ({'modo file://' if mode == 'file' else 'modo servidor'})"
)
print(
    f"   - CSS: css/main.css (importa módulos: reset, variables, layout, components, colors, print)"
)
print(f"   - JS: js/app.js (módulos ES6: config, utils, card, api)")
if mode == "file":
    print(f"   - Datos: JSON embebido en el HTML ({len(frases)} frases)")
    print(f"   - Puedes abrir index.html directamente en el navegador")
else:
    print(f"   - Datos: data/frases.json (cargado vía fetch)")
    print(f"   - Requiere servidor web (ejecuta: python3 server.py)")
    print(f"   - O genera con --file para usar file://")
