/**
 * Card Component
 * Lógica para crear y manejar tarjetas
 */

import { escapeHtml } from './utils.js';
import { CONFIG } from './config.js';

/**
 * Crea un elemento de tarjeta
 * @param {string} frase - Texto de la frase
 * @param {string} autor - Nombre del autor
 * @param {string} fuente - Fuente/libro de la frase
 * @param {string} color - Clase CSS del color
 * @returns {HTMLElement} - Elemento de tarjeta creado
 */
export function createCard(frase, autor, fuente, color) {
  const card = document.createElement('div');
  card.className = `card ${color}`;

  const cardPhrase = document.createElement('div');
  cardPhrase.className = 'card-phrase';
  cardPhrase.textContent = frase;

  const cardMeta = document.createElement('div');
  cardMeta.className = 'card-meta';
  cardMeta.innerHTML = escapeHtml(autor) + (fuente ? '<br>' + escapeHtml(fuente) : '');

  card.appendChild(cardPhrase);
  card.appendChild(cardMeta);

  return card;
}

/**
 * Genera todas las tarjetas en el DOM
 * @param {Array} frases - Array de objetos con frase, autor y fuente
 * @param {string[]} colors - Array de colores disponibles
 */
export function generateCards(frases, colors) {
  const body = document.body;
  body.innerHTML = ''; // Limpiar el body antes de generar

  frases.forEach((item, index) => {
    const color = colors[index % colors.length];
    const card = createCard(item.frase, item.autor, item.fuente, color);
    body.appendChild(card);
  });
}
