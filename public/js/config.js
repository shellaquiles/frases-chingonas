/**
 * Configuración
 * Define constantes y configuración de la aplicación
 */

export const CONFIG = {
  // Colores disponibles en orden
  COLORS: [
    'verde', 'azul', 'amarillo', 'morado', 'rojo', 'gris',
    'naranja', 'turquesa', 'menta', 'lila', 'mostaza', 'grafito',
    'cian', 'magenta', 'cafe', 'blanco'
  ],

  // Rutas de datos
  DATA_URL: 'data/frases.json',

  // Mensajes de error
  ERROR_MESSAGES: {
    LOAD_FAILED: 'Error al cargar las frases',
    FILE_NOT_FOUND: 'Asegúrate de que el archivo data/frases.json existe.',
    GENERATE_JSON: 'Ejecuta: python3 scripts/20_csv_to_json.py para generar el archivo JSON.'
  }
};
