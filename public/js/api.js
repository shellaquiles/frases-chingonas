/**
 * API Module
 * Maneja la carga de datos desde el servidor
 */

import { CONFIG } from './config.js';

/**
 * Carga las frases desde el archivo JSON
 * @returns {Promise<Array>} - Promise que resuelve con el array de frases
 * @throws {Error} - Si hay un error al cargar los datos
 */
export async function loadFrases() {
  try {
    const response = await fetch(CONFIG.DATA_URL);

    if (!response.ok) {
      throw new Error(`Error al cargar frases.json: ${response.status}`);
    }

    const frases = await response.json();
    return frases;
  } catch (error) {
    console.error('Error al cargar frases:', error);
    throw error;
  }
}

/**
 * Muestra un mensaje de error en el DOM
 * @param {Error} error - Objeto de error
 */
export function showError(error) {
  document.body.innerHTML = `
    <div style="padding: 20px; text-align: center; color: #c62828;">
      <h2>${CONFIG.ERROR_MESSAGES.LOAD_FAILED}</h2>
      <p>${error.message}</p>
      <p>${CONFIG.ERROR_MESSAGES.FILE_NOT_FOUND}</p>
      <p>${CONFIG.ERROR_MESSAGES.GENERATE_JSON}</p>
    </div>
  `;
}
