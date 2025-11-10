# Guía para Colaboradores

¡Gracias por tu interés en contribuir a **Frases Chingonas**! 🎉

Este documento te guiará para que puedas colaborar de manera efectiva siguiendo los principios de código limpio y buenas prácticas que promovemos en el proyecto.

## 🚀 Primeros Pasos

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/frases_python.git
cd frases_python
```

### 2. Verificar Requisitos

El proyecto solo requiere **Python 3.6+** (sin dependencias externas):

```bash
python3 --version
```

### 3. Preparar el Entorno

No se requiere instalación de paquetes, pero puedes crear un entorno virtual (opcional):

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 4. Generar los Datos

```bash
# Convertir CSV a JSON
python3 csv_to_json.py
python3 libros_to_json.py

# Generar la página web
python3 generate_index_page.py
```

### 5. Ver el Resultado

```bash
# Iniciar servidor local
python3 server.py

# Abrir en navegador: http://localhost:8000/public/index.html
```

## 📝 Cómo Contribuir

### Agregar Nuevas Frases

1. **Lee las instrucciones** en [`prompt.md`](prompt.md)
2. **Revisa el estilo** de las frases existentes en `frases.csv`
3. **Genera frases originales** inspiradas en el libro (no citas directas)
4. **Agrega las frases** a `frases.csv` con el formato:
   ```csv
   id,frase,autor,fuente
   CLAVE-001,"Tu frase aquí","Autor del Libro","Título del Libro"
   ```

### Agregar Nuevos Libros

1. **Agrega el libro** a `libros.csv`:
   ```csv
   frases_generadas,clave,titulo,autor,categoria,tema
   ❌,NUEVA,Nuevo Libro,Autor del Libro,Categoría,Tema del libro
   ```

2. **Genera las frases** siguiendo [`prompt.md`](prompt.md)

3. **Opcional**: Obtén información enriquecida (portadas, ISBN):
   ```bash
   python3 fetch_book_info.py
   ```

### Mejorar el Código

1. **Sigue los principios de código limpio**:
   - Nombres descriptivos
   - Funciones pequeñas y con una sola responsabilidad
   - Código autodocumentado
   - Sin comentarios innecesarios

2. **Mantén la consistencia**:
   - Usa el mismo estilo de código existente
   - Sigue las convenciones de Python (PEP 8)
   - Documenta funciones complejas

3. **Prueba tus cambios**:
   ```bash
   # Verificar que los scripts funcionen
   python3 csv_to_json.py
   python3 generate_index_page.py
   python3 server.py
   ```

## 📋 Estándares de Código

### Python

- **PEP 8**: Sigue las convenciones de estilo de Python
- **Docstrings**: Documenta funciones y módulos
- **Type hints**: Usa type hints cuando sea útil
- **Nombres descriptivos**: Variables y funciones deben ser autodocumentadas

Ejemplo de código limpio:

```python
def load_frases(csv_file: str) -> List[Dict]:
    """
    Carga frases desde un archivo CSV.

    Args:
        csv_file: Ruta al archivo CSV con frases

    Returns:
        Lista de diccionarios con las frases
    """
    frases = []
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            frases.append({
                "id": row["id"].strip(),
                "frase": row["frase"].strip(),
                "autor": row["autor"].strip(),
                "fuente": row["fuente"].strip(),
            })
    return frases
```

### JavaScript

- **ES6 Modules**: Usa import/export
- **Nombres descriptivos**: Variables y funciones claras
- **Funciones pequeñas**: Una responsabilidad por función
- **Comentarios útiles**: Solo cuando el código no es obvio

Ejemplo:

```javascript
/**
 * Filtra frases por libro
 * @param {Array} frases - Array de frases
 * @param {string} libroClave - Clave del libro
 * @returns {Array} Frases filtradas
 */
export function filterByLibro(frases, libroClave) {
  return frases.filter(frase => frase.libro_clave === libroClave);
}
```

## 🎨 Estilo de Frases

### Principios

1. **Originales inspiradas**: No citas directas del libro
2. **Breves y contundentes**: Una idea clara por frase
3. **Tono profesional**: Reflexivo y técnico
4. **Sentido práctico**: Aplicable al desarrollo de software

### Ejemplos

✅ **Buenas frases**:
- "El código limpio se entiende en minutos, no en reuniones."
- "Una función que hace de todo es una función que no sirve a nadie."
- "El dominio es el lenguaje que da sentido al software."

❌ **Frases a evitar**:
- Citas literales del libro
- Frases demasiado largas o complejas
- Frases vagas sin sentido práctico
- Repetición de estructuras

## 🔄 Flujo de Trabajo

1. **Fork** el repositorio
2. **Crea una rama** para tu contribución:
   ```bash
   git checkout -b mi-contribucion
   ```
3. **Haz tus cambios** siguiendo los estándares
4. **Prueba** que todo funcione correctamente
5. **Commit** con mensajes descriptivos:
   ```bash
   git commit -m "Agregar 100 frases de Clean Code"
   ```
6. **Push** a tu fork:
   ```bash
   git push origin mi-contribucion
   ```
7. **Abre un Pull Request** con descripción clara

## 📚 Estructura de Archivos

### Fuentes de Verdad

- **`libros.csv`**: Lista de libros (fuente de verdad)
- **`frases.csv`**: Colección de frases (fuente de verdad)

### Archivos Generados

- **`public/data/*.json`**: Generados desde CSV
- **`public/index.html`**: Generado por `generate_index_page.py`

**Nota**: Los archivos generados se pueden regenerar, pero es útil versionarlos para GitHub Pages.

## 🐛 Reportar Problemas

Si encuentras un bug o tienes una sugerencia:

1. **Busca** si ya existe un issue similar
2. **Crea un nuevo issue** con:
   - Descripción clara del problema
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Información del entorno (Python, OS)

## ✅ Checklist Antes de Contribuir

- [ ] He leído las instrucciones en `prompt.md`
- [ ] He revisado el estilo de código existente
- [ ] He probado que mis cambios funcionan
- [ ] He seguido los estándares de código
- [ ] He actualizado la documentación si es necesario
- [ ] Mis frases son originales inspiradas (no citas directas)

## 💡 Ideas para Contribuir

- ✨ Agregar nuevas frases a libros existentes
- 📚 Agregar nuevos libros y sus frases
- 🎨 Mejorar el diseño de la interfaz web
- 🐍 Mejorar los scripts de Python
- 📖 Mejorar la documentación
- 🔍 Agregar funcionalidades de búsqueda/filtrado
- 📊 Agregar estadísticas y visualizaciones

## 🙏 Agradecimientos

Gracias por contribuir a este proyecto. Cada contribución, por pequeña que sea, hace que este proyecto sea mejor.

---

**Recuerda**: El objetivo es crear frases **originales inspiradas** que capturen el espíritu de los libros, no citas directas. ¡Mantén el código limpio y las frases chingonas! 🚀
