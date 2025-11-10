Genera 100 frases en formato CSV con las columnas:
id,frase,autor,fuente

Usa la siguiente información del libro:
Clave: [CLAVE]
Título: [TÍTULO COMPLETO]
Autor(es): [AUTOR]
Categoría: [CATEGORÍA]
Tema: [TEMA]

Instrucciones de estilo:
- Cada frase debe estar inspirada en los principios, ideas o espíritu del libro.
- Escribe en español con un tono profesional, reflexivo y técnico.
- No repitas estructuras ni frases.
- Mantén la coherencia con el estilo de los bloques anteriores:
  breve, contundente y con sentido conceptual o práctico.
- Si el libro es técnico, usa terminología del área (por ejemplo: arquitectura, testing, DevOps, liderazgo, etc.).
- Si es de desarrollo personal o cultura, usa tono motivacional y de crecimiento profesional.
- No cites directamente ni copies fragmentos del libro; deben ser **frases originales inspiradas**.
- El campo `id` debe tener el formato `[CLAVE]-NNN` (por ejemplo: `DDD-001`, `ACC-045`, `TPP-100`).

Ejemplo de salida esperada:
id,frase,autor,fuente
DDD-001,"El dominio es el lenguaje que da sentido al software.","Eric Evans","Domain-Driven Design"
DDD-002,"Una arquitectura saludable refleja una comprensión profunda del dominio, no solo del código.","Eric Evans","Domain-Driven Design"
...
DDD-100,"La verdadera simplicidad en software nace de la claridad en el modelo mental.","Eric Evans","Domain-Driven Design"

Genera las 100 frases completas en ese formato CSV.
