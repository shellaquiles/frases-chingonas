/**
 * Página principal - Muestra una frase aleatoria a pantalla completa
 */

// ============================================
// Estado de la aplicación
// ============================================
const AppState = {
    allFrases: [], // Array de todas las frases con su información del libro
    currentFrase: null
};

// ============================================
// Utilidades
// ============================================
const Utils = {
    /**
     * Obtiene un número aleatorio entre min y max (inclusive)
     */
    randomInt(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    },

    /**
     * Selecciona un elemento aleatorio de un array
     */
    randomElement(array) {
        if (array.length === 0) return null;
        return array[this.randomInt(0, array.length - 1)];
    },

    /**
     * Escapa HTML para prevenir XSS
     */
    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
};

// ============================================
// API de datos
// ============================================
const API = {
    /**
     * Carga los libros desde el archivo JSON
     */
    async loadBooks() {
        try {
            const response = await fetch('data/libros.json');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error cargando libros:', error);
            throw error;
        }
    },

    /**
     * Carga las frases desde el archivo JSON
     */
    async loadFrases() {
        try {
            const response = await fetch('data/frases.json');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error cargando frases:', error);
            throw error;
        }
    }
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

        if (fraseLinkEl && AppState.currentFrase && AppState.currentFrase.clave) {
            fraseLinkEl.href = `frases.html?clave=${encodeURIComponent(AppState.currentFrase.clave)}`;
            fraseLinkEl.style.pointerEvents = 'auto';
            fraseLinkEl.style.cursor = 'pointer';

            // Agregar event listener si no existe
            if (!fraseLinkEl.hasAttribute('data-listener-added')) {
                fraseLinkEl.setAttribute('data-listener-added', 'true');
                fraseLinkEl.addEventListener('click', (e) => {
                    if (AppState.currentFrase && AppState.currentFrase.clave) {
                        // Permitir navegación normal
                        return true;
                    }
                    e.preventDefault();
                    return false;
                });
            }
        } else if (fraseLinkEl) {
            fraseLinkEl.href = '#';
            fraseLinkEl.style.pointerEvents = 'none';
            fraseLinkEl.style.cursor = 'default';
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
