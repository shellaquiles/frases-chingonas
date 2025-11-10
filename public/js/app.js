/**
 * App Module
 * Archivo principal que inicializa la aplicación
 */

import { CONFIG } from './config.js';
import { loadFrases, showError } from './api.js';
import { generateCards } from './card.js';

/**
 * Inicializa la aplicación
 */
async function init() {
  try {
    const frases = await loadFrases();
    generateCards(frases, CONFIG.COLORS);
  } catch (error) {
    showError(error);
  }
}

// Inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  // DOM ya está listo
  init();
}
