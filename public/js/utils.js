/**
 * Utilidades compartidas
 */

/**
 * Escapa HTML para prevenir XSS
 */
export function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Obtiene el parámetro de la URL
 */
export function getUrlParam(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

/**
 * Mezcla un array de forma aleatoria (Fisher-Yates shuffle)
 */
export function shuffleArray(array) {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
}

/**
 * Obtiene un número aleatorio entre min y max (inclusive)
 */
export function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

/**
 * Selecciona un elemento aleatorio de un array
 */
export function randomElement(array) {
    if (array.length === 0) return null;
    return array[randomInt(0, array.length - 1)];
}

/**
 * Normaliza texto para búsqueda (elimina acentos, convierte a minúsculas)
 */
export function normalizeText(text) {
    return text
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '');
}

/**
 * Formatea el año de publicación
 */
export function formatYear(year) {
    if (!year) return 'N/A';
    return Math.floor(year).toString();
}

/**
 * Trunca texto a una longitud máxima
 */
export function truncate(text, maxLength = 100) {
    if (!text || text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

/**
 * Debounce para optimizar búsquedas
 */
export function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Obtiene el color de la paleta para un índice
 */
export function getColorForIndex(index, colorPalette) {
    return colorPalette[index % colorPalette.length];
}
