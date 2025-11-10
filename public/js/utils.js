/**
 * Utilidades
 * Funciones auxiliares reutilizables
 */

/**
 * Escapa caracteres HTML para prevenir XSS
 * @param {string} text - Texto a escapar
 * @returns {string} - Texto escapado
 */
export function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

/**
 * Obtiene un color de la paleta basado en un índice
 * @param {number} index - Índice de la frase
 * @param {string[]} colors - Array de colores disponibles
 * @returns {string} - Nombre del color
 */
export function getColorByIndex(index, colors) {
  return colors[index % colors.length];
}
