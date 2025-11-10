# Guía de Instalación y Configuración

Esta guía te ayudará a configurar el proyecto desde cero, siguiendo los principios de código limpio y simplicidad.

## 📋 Requisitos Previos

### Python

Verifica que tienes Python 3.6 o superior:

```bash
python3 --version
```

Si no tienes Python instalado:
- **Linux/Mac**: Usa el gestor de paquetes de tu distribución
- **Windows**: Descarga desde [python.org](https://www.python.org/downloads/)

### Git (Opcional)

Para clonar el repositorio:

```bash
git --version
```

Si no tienes Git:
- **Linux**: `sudo apt-get install git` (o equivalente)
- **Mac**: `brew install git` o descarga desde [git-scm.com](https://git-scm.com/)
- **Windows**: Descarga desde [git-scm.com](https://git-scm.com/)

## 🚀 Instalación Paso a Paso

### 1. Obtener el Código

#### Opción A: Clonar desde GitHub

```bash
git clone https://github.com/tu-usuario/frases_python.git
cd frases_python
```

#### Opción B: Descargar ZIP

1. Ve a la página del repositorio en GitHub
2. Haz clic en "Code" → "Download ZIP"
3. Extrae el archivo ZIP
4. Abre una terminal en la carpeta extraída

### 2. Verificar la Estructura

Asegúrate de tener estos archivos principales:

```
frases_python/
├── libros.csv          # ✅ Debe existir
├── frases.csv          # ✅ Debe existir
├── generate_index_page.py
├── csv_to_json.py
├── libros_to_json.py
└── public/
```

### 3. Preparar los Datos

El proyecto usa `libros.csv` y `frases.csv` como **fuentes de verdad**. Los archivos JSON se generan automáticamente:

```bash
# Convertir CSV a JSON
python3 csv_to_json.py
python3 libros_to_json.py
```

Esto creará:
- `public/data/frases.json`
- `public/data/libros.json`

### 4. Generar la Página Web

```bash
# Generar página principal con navegación
python3 generate_index_page.py
```

Esto creará `public/index.html` con toda la funcionalidad.

### 5. Verificar que Funciona

#### Opción A: Servidor Local

```bash
# Iniciar servidor
python3 server.py
```

Abre tu navegador en: **http://localhost:8000/public/index.html**

#### Opción B: Abrir Directamente

Si el HTML está generado con datos embebidos, puedes abrir `public/index.html` directamente en tu navegador (algunas funcionalidades pueden no funcionar sin servidor).

## 🔍 Verificación

### Checklist de Instalación

- [ ] Python 3.6+ instalado
- [ ] Archivos `libros.csv` y `frases.csv` presentes
- [ ] Scripts ejecutados sin errores
- [ ] Archivos JSON generados en `public/data/`
- [ ] `public/index.html` generado
- [ ] Servidor local funciona correctamente
- [ ] Página web se muestra en el navegador

### Probar los Scripts

```bash
# Verificar que los scripts funcionan
python3 csv_to_json.py
python3 libros_to_json.py
python3 generate_index_page.py

# Verificar que el servidor inicia
python3 server.py
# (Presiona Ctrl+C para detener)
```

## 🌐 Configuración para GitHub Pages

### 1. Configurar GitHub Pages

1. Ve a tu repositorio en GitHub
2. Settings → Pages
3. Source: `main` (o `master`) branch
4. Folder: `/public`
5. Save

### 2. Actualizar la Página

Cada vez que agregues nuevas frases o libros:

```bash
# Regenerar la página
python3 generate_index_page.py

# Commit y push
git add public/
git commit -m "Actualizar página con nuevas frases"
git push
```

La página se actualizará automáticamente en GitHub Pages.

## 🐛 Solución de Problemas

### Error: "No se encontró el archivo libros.csv"

**Solución**: Asegúrate de estar en el directorio correcto:
```bash
cd frases_python
ls libros.csv  # Debe mostrar el archivo
```

### Error: "python3: command not found"

**Solución**:
- **Linux/Mac**: Usa `python` en lugar de `python3`
- **Windows**: Asegúrate de que Python esté en el PATH

### Error al cargar la página

**Solución**:
1. Verifica que los JSON se generaron:
   ```bash
   ls public/data/*.json
   ```
2. Regenera la página:
   ```bash
   python3 generate_index_page.py
   ```

### Puerto 8000 ya en uso

**Solución**: Usa otro puerto:
```bash
python3 server.py 8080
```

Luego abre: `http://localhost:8080/public/index.html`

## 📚 Próximos Pasos

Una vez instalado:

1. **Lee** [`CONTRIBUTING.md`](CONTRIBUTING.md) para aprender a contribuir
2. **Revisa** [`prompt.md`](prompt.md) para generar nuevas frases
3. **Explora** los scripts para entender cómo funcionan
4. **Contribuye** agregando frases o mejorando el código

## 💡 Tips

- **Mantén los CSV actualizados**: `libros.csv` y `frases.csv` son las fuentes de verdad
- **Regenera después de cambios**: Ejecuta `generate_index_page.py` después de modificar los CSV
- **Usa Git**: Mantén un historial de cambios
- **Prueba localmente**: Siempre prueba en `localhost` antes de hacer push

---

**¿Problemas?** Abre un issue en GitHub o consulta la documentación en [`CONTRIBUTING.md`](CONTRIBUTING.md).
