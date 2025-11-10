/**
 * Página de frases de un libro
 * Carga las frases desde frases.json y libros.json
 * Muestra las frases en tarjetas con colores rotativos
 */

// ============================================
// Paleta de colores
// ============================================
const COLOR_PALETTE = [
    'verde', 'azul', 'amarillo', 'morado', 'rojo', 'gris',
    'naranja', 'turquesa', 'menta', 'lila', 'mostaza', 'grafito',
    'cian', 'magenta', 'cafe', 'blanco'
];

// ============================================
// Estado de la aplicación
// ============================================
const AppState = {
    clave: null,
    libro: null,
    frases: [],
    allFrases: [] // Todas las frases cuando no se especifica clave
};

// ============================================
// Utilidades
// ============================================
const Utils = {
    /**
     * Obtiene el parámetro de la URL
     */
    getUrlParam(name) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(name);
    },

    /**
     * Mezcla un array de forma aleatoria (Fisher-Yates shuffle)
     */
    shuffleArray(array) {
        const shuffled = [...array];
        for (let i = shuffled.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
        }
        return shuffled;
    },

    /**
     * Escapa HTML para prevenir XSS
     */
    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    /**
     * Obtiene el color de la paleta para un índice
     */
    getColorForIndex(index) {
        return COLOR_PALETTE[index % COLOR_PALETTE.length];
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
     * Renderiza las tarjetas de frases
     */
    renderCards(frases, libro = null) {
        const grid = document.getElementById('cards-grid');
        if (!grid) return;

        if (frases.length === 0) {
            grid.innerHTML = `
                <div style="grid-column: 1 / -1; text-align: center; padding: 2rem; color: #ef4444;">
                    <p>No hay frases disponibles.</p>
                </div>
            `;
            return;
        }

        // Mezclar las frases de forma aleatoria
        const shuffledFrases = Utils.shuffleArray(frases);

        const cardsHtml = shuffledFrases.map((fraseData, index) => {
            const color = Utils.getColorForIndex(index);

            // Si es una frase con información completa (todas las frases)
            if (fraseData.autor && fraseData.titulo) {
                return `
                    <div class="card ${color}" role="listitem">
                        <div class="card-phrase">${this.escapeHtml(fraseData.frase)}</div>
                        <div class="card-meta">${this.escapeHtml(fraseData.autor)}<br>${this.escapeHtml(fraseData.titulo)}</div>
                    </div>
                `;
            }

            // Si es una frase simple (de un libro específico)
            const autor = libro?.autor || 'Autor desconocido';
            const fuente = libro?.titulo || 'Libro desconocido';

            return `
                <div class="card ${color}" role="listitem">
                    <div class="card-phrase">${this.escapeHtml(fraseData.frase)}</div>
                    <div class="card-meta">${this.escapeHtml(autor)}<br>${this.escapeHtml(fuente)}</div>
                </div>
            `;
        }).join('');

        grid.innerHTML = cardsHtml;
    },

    /**
     * Actualiza el header con la información del libro o todas las frases
     */
    updateHeader(libro, frasesCount, isAllFrases = false) {
        const titleEl = document.getElementById('book-title');
        const authorEl = document.getElementById('book-author');
        const countEl = document.getElementById('frases-count');
        const headerBookInfo = document.getElementById('header-book-info');
        const bookCover = document.getElementById('book-cover');
        const bookTitleDetail = document.getElementById('book-title-detail');
        const bookAuthorDetail = document.getElementById('book-author-detail');
        const bookMeta = document.getElementById('book-meta');

        // Si hay un libro específico, mostrar información detallada
        if (libro && !isAllFrases) {
            // Ocultar texto simple y mostrar información del libro
            if (titleEl) titleEl.style.display = 'none';
            if (authorEl) authorEl.style.display = 'none';

            // Mostrar información detallada del libro
            if (headerBookInfo) {
                headerBookInfo.style.display = 'flex';
            }

            if (bookCover && libro.portada) {
                bookCover.src = libro.portada;
                bookCover.style.display = 'block';
            } else if (bookCover) {
                bookCover.style.display = 'none';
            }

            if (bookTitleDetail) {
                bookTitleDetail.textContent = libro.titulo || 'Libro desconocido';
            }

            if (bookAuthorDetail) {
                bookAuthorDetail.textContent = libro.autor || 'Autor desconocido';
            }

            // Mostrar descripción
            const bookDescription = document.getElementById('book-description');
            if (bookDescription) {
                const description = libro.descripcion_es || libro.resumen_ficha || libro.descripcion || '';
                if (description) {
                    bookDescription.textContent = description;
                    bookDescription.style.display = 'block';
                } else {
                    bookDescription.style.display = 'none';
                }
            }

            if (bookMeta) {
                const metaItems = [];

                if (libro.categoria_normalizada) {
                    metaItems.push(`<span>📚 ${this.escapeHtml(libro.categoria_normalizada)}</span>`);
                }

                if (libro.fecha_publicacion) {
                    const year = Math.floor(libro.fecha_publicacion);
                    metaItems.push(`<span>📅 ${year}</span>`);
                }

                if (libro.isbn) {
                    metaItems.push(`<span>🔖 ISBN: ${this.escapeHtml(libro.isbn)}</span>`);
                }

                bookMeta.innerHTML = metaItems.join('');
            }

            // Mostrar tema
            const bookTema = document.getElementById('book-tema');
            if (bookTema && libro.tema) {
                bookTema.textContent = `💡 ${libro.tema}`;
                bookTema.style.display = 'block';
            } else if (bookTema) {
                bookTema.style.display = 'none';
            }

            // Mostrar contador en el header del libro
            const bookCountEl = document.getElementById('book-count');
            if (bookCountEl) {
                bookCountEl.textContent = `${frasesCount} ${frasesCount === 1 ? 'frase' : 'frases'}`;
            }

            // Ocultar contador del texto simple
            if (countEl) {
                countEl.style.display = 'none';
            }
        } else {
            // Mostrar texto simple para todas las frases
            if (titleEl) {
                titleEl.style.display = 'block';
                titleEl.textContent = '🔥 Todas las Frases Chingonas';
            }

            if (authorEl) {
                authorEl.style.display = 'block';
                authorEl.textContent = 'Colección completa de frases inspiradas en libros técnicos';
            }

            if (countEl) {
                countEl.textContent = `${frasesCount} ${frasesCount === 1 ? 'frase' : 'frases'}`;
                countEl.style.display = 'block';
            }

            // Ocultar información detallada del libro
            if (headerBookInfo) {
                headerBookInfo.style.display = 'none';
            }
        }
    },

    /**
     * Muestra/oculta el loading
     */
    toggleLoading(show) {
        const loading = document.getElementById('loading');
        if (loading) {
            if (show) {
                loading.classList.remove('hidden');
            } else {
                loading.classList.add('hidden');
            }
        }
    },

    /**
     * Escapa HTML para prevenir XSS
     */
    escapeHtml(text) {
        return Utils.escapeHtml(text);
    }
};

// ============================================
// Inicialización de la aplicación
// ============================================
const App = {
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
     * Inicializa la aplicación
     */
    async init() {
        try {
            // Obtener la clave del libro desde la URL
            const clave = Utils.getUrlParam('clave');

            Renderer.toggleLoading(true);

            // Cargar libros y frases en paralelo
            const [books, frases] = await Promise.all([
                API.loadBooks(),
                API.loadFrases()
            ]);

            // Si no hay clave, mostrar todas las frases
            if (!clave) {
                // Preparar todas las frases con información del libro
                const allFrases = this.prepareAllFrases(frases, books);

                if (allFrases.length === 0) {
                    this.showError('No hay frases disponibles.');
                    Renderer.toggleLoading(false);
                    return;
                }

                AppState.allFrases = allFrases;

                // Actualizar el header para todas las frases
                Renderer.updateHeader(null, allFrases.length, true);

                // Renderizar las tarjetas (ya mezcladas aleatoriamente en renderCards)
                Renderer.renderCards(allFrases);

                Renderer.toggleLoading(false);

                // Actualizar título de la página
                document.title = 'Todas las Frases - Frases Python';
                return;
            }

            // Si hay clave, mostrar frases de un libro específico
            AppState.clave = clave;

            // Buscar el libro por clave
            const libro = books.find(book => book.clave === clave);

            if (!libro) {
                this.showError(`No se encontró el libro con clave "${clave}".`);
                Renderer.toggleLoading(false);
                return;
            }

            AppState.libro = libro;

            // Obtener las frases del libro
            const frasesDelLibro = frases[clave] || [];

            if (frasesDelLibro.length === 0) {
                this.showError(`No hay frases disponibles para el libro "${libro.titulo}".`);
                Renderer.toggleLoading(false);
                return;
            }

            AppState.frases = frasesDelLibro;

            // Actualizar el header
            Renderer.updateHeader(libro, frasesDelLibro.length, false);

            // Renderizar las tarjetas (ya mezcladas aleatoriamente en renderCards)
            Renderer.renderCards(frasesDelLibro, libro);

            Renderer.toggleLoading(false);

            // Actualizar título de la página
            if (libro.titulo) {
                document.title = `Frases de ${libro.titulo} - Frases Python`;
            }
        } catch (error) {
            console.error('Error inicializando la aplicación:', error);
            this.showError('Error cargando los datos. Por favor, recarga la página.');
            Renderer.toggleLoading(false);
        }
    },

    /**
     * Muestra un mensaje de error
     */
    showError(message) {
        const grid = document.getElementById('cards-grid');
        if (grid) {
            grid.innerHTML = `
                <div style="grid-column: 1 / -1; text-align: center; padding: 2rem; color: #ef4444;">
                    <p>❌ ${message}</p>
                    <a href="libros.html" style="color: #2563eb; text-decoration: none; margin-top: 1rem; display: inline-block;">
                        ← Volver al catálogo
                    </a>
                </div>
            `;
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
