/**
 * Página principal - Muestra una frase aleatoria a pantalla completa
 */

import { escapeHtml, randomElement } from './utils.js';
import { loadBooks, loadFrases } from './api.js';

// ============================================
// Estado de la aplicación
// ============================================
const AppState = {
    allFrases: [], // Array de todas las frases con su información del libro
    currentFrase: null
};

// ============================================
// Utilidades locales
// ============================================
const Utils = {
    escapeHtml,
    randomElement
};

// ============================================
// API de datos
// ============================================
const API = {
    loadBooks,
    loadFrases
};

// ============================================
// Renderizado
// ============================================
const Renderer = {
    /**
     * Renderiza una frase en la página
     */
    renderFrase(fraseData) {
        const fraseTextEl = document.getElementById('frase-text');
        const fraseAuthorEl = document.getElementById('frase-author');
        const fraseBookEl = document.getElementById('frase-book');

        if (!fraseData) {
            if (fraseTextEl) {
                fraseTextEl.textContent = 'No hay frases disponibles.';
            }
            return;
        }

        if (fraseTextEl) {
            fraseTextEl.textContent = fraseData.frase;
        }

        if (fraseAuthorEl) {
            fraseAuthorEl.textContent = fraseData.autor || 'Autor desconocido';
        }

        if (fraseBookEl) {
            fraseBookEl.textContent = fraseData.titulo || 'Libro desconocido';
        }

        // Animación de fade
        const container = document.getElementById('frase-container');
        if (container) {
            container.style.opacity = '0';
            setTimeout(() => {
                container.style.opacity = '1';
            }, 300);
        }
    },

    /**
     * Muestra un mensaje de error
     */
    showError(message) {
        const fraseTextEl = document.getElementById('frase-text');
        if (fraseTextEl) {
            fraseTextEl.textContent = `❌ ${message}`;
            fraseTextEl.style.color = '#ef4444';
        }
    }
};

// ============================================
// Lógica de frases
// ============================================
const FrasesManager = {
    /**
     * Prepara todas las frases con información del libro
     */
    prepareAllFrases(frases, books) {
        const allFrases = [];

        // Crear un mapa de libros por clave para acceso rápido
        const booksMap = {};
        books.forEach(book => {
            if (book.clave) {
                booksMap[book.clave] = book;
            }
        });

        // Combinar frases con información del libro
        Object.keys(frases).forEach(clave => {
            const libro = booksMap[clave];
            const frasesDelLibro = frases[clave] || [];

            frasesDelLibro.forEach(frase => {
                allFrases.push({
                    frase: frase.frase,
                    clave: clave,
                    autor: libro?.autor || 'Autor desconocido',
                    titulo: libro?.titulo || 'Libro desconocido'
                });
            });
        });

        return allFrases;
    },

    /**
     * Obtiene una frase aleatoria
     */
    getRandomFrase() {
        if (AppState.allFrases.length === 0) {
            return null;
        }
        return Utils.randomElement(AppState.allFrases);
    }
};

// ============================================
// Inicialización de la aplicación
// ============================================
const App = {
    /**
     * Inicializa la aplicación
     */
    async init() {
        try {
            // Cargar libros y frases en paralelo
            const [books, frases] = await Promise.all([
                API.loadBooks(),
                API.loadFrases()
            ]);

            // Preparar todas las frases con información del libro
            AppState.allFrases = FrasesManager.prepareAllFrases(frases, books);

            if (AppState.allFrases.length === 0) {
                Renderer.showError('No hay frases disponibles.');
                return;
            }

            // Mostrar una frase aleatoria inicial
            this.showRandomFrase();

            // Configurar el botón de frase aleatoria
            const randomBtn = document.getElementById('random-frase-btn');
            if (randomBtn) {
                randomBtn.addEventListener('click', () => {
                    this.showRandomFrase();
                });
            }

            // El enlace se configurará cuando se muestre la primera frase
        } catch (error) {
            console.error('Error inicializando la aplicación:', error);
            Renderer.showError('Error cargando los datos. Por favor, recarga la página.');
        }
    },

    /**
     * Muestra una frase aleatoria
     */
    showRandomFrase() {
        const frase = FrasesManager.getRandomFrase();
        if (frase) {
            AppState.currentFrase = frase;
            Renderer.renderFrase(frase);
            this.updateFraseLink();
        }
    },

    /**
     * Actualiza el enlace de la frase
     */
    updateFraseLink() {
        const fraseLinkEl = document.getElementById('frase-link');
        const fraseContent = document.getElementById('frase-content');

        console.log('🔍 updateFraseLink llamado');
        console.log('fraseLinkEl:', fraseLinkEl);
        console.log('currentFrase:', AppState.currentFrase);

        if (fraseLinkEl && AppState.currentFrase && AppState.currentFrase.clave) {
            const url = `frases.html?clave=${encodeURIComponent(AppState.currentFrase.clave)}`;
            fraseLinkEl.href = url;
            fraseLinkEl.style.pointerEvents = 'auto';
            fraseLinkEl.style.cursor = 'pointer';

            console.log('✅ Enlace configurado:', url);
            console.log('href actual:', fraseLinkEl.href);
            console.log('pointer-events:', fraseLinkEl.style.pointerEvents);

            // Agregar event listener para debugging
            if (!fraseLinkEl.hasAttribute('data-listener-added')) {
                fraseLinkEl.setAttribute('data-listener-added', 'true');
                fraseLinkEl.addEventListener('click', (e) => {
                    console.log('🖱️ Click detectado en frase-link');
                    console.log('Event:', e);
                    console.log('currentFrase:', AppState.currentFrase);

                    if (AppState.currentFrase && AppState.currentFrase.clave) {
                        const targetUrl = `frases.html?clave=${encodeURIComponent(AppState.currentFrase.clave)}`;
                        console.log('🚀 Navegando a:', targetUrl);
                        window.location.href = targetUrl;
                    } else {
                        console.log('❌ No hay clave, previniendo default');
                        e.preventDefault();
                    }
                }, true);
            }
        } else {
            console.log('⚠️ No se puede configurar enlace:', {
                tieneLinkEl: !!fraseLinkEl,
                tieneFrase: !!AppState.currentFrase,
                tieneClave: !!(AppState.currentFrase && AppState.currentFrase.clave)
            });
            if (fraseLinkEl) {
                fraseLinkEl.href = '#';
                fraseLinkEl.style.pointerEvents = 'none';
                fraseLinkEl.style.cursor = 'default';
            }
        }

        // Agregar hover effect al contenedor
        if (fraseContent && AppState.currentFrase && AppState.currentFrase.clave) {
            fraseContent.style.cursor = 'pointer';
        }
    }
};

// ============================================
// Iniciar aplicación cuando el DOM esté listo
// ============================================
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => App.init());
} else {
    App.init();
}
