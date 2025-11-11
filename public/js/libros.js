/**
 * Aplicación principal para mostrar el catálogo de libros
 * Carga dinámicamente los libros desde libros.json y permite
 * búsqueda, filtrado y visualización detallada
 */

import { normalizeText, formatYear, truncate, debounce } from './utils.js';
import { loadBooks, loadFrases } from './api.js';

// ============================================
// Estado de la aplicación
// ============================================
const AppState = {
    books: [],
    filteredBooks: [],
    categories: new Set(),
    searchTerm: '',
    selectedCategory: '',
    sortBy: 'titulo',
    frases: {} // Frases agrupadas por clave de libro
};

// ============================================
// Utilidades locales
// ============================================
const Utils = {
    normalizeText,
    formatYear,
    truncate,
    debounce
};

// ============================================
// API de datos
// ============================================
const BooksAPI = {
    async loadBooks() {
        return await loadBooks();
    },

    async loadFrases() {
        try {
            return await loadFrases();
        } catch (error) {
            console.error('Error cargando frases:', error);
            // No lanzar error, simplemente retornar objeto vacío
            return {};
        }
    }
};

// ============================================
// Renderizado
// ============================================
const Renderer = {
    /**
     * Renderiza el grid de libros
     */
    renderBooksGrid(books) {
        const grid = document.getElementById('books-grid');
        if (!grid) return;

        if (books.length === 0) {
            grid.innerHTML = '';
            return;
        }

        grid.innerHTML = books.map(book => this.createBookCard(book)).join('');

        // Agregar event listeners a las tarjetas (click en la tarjeta)
        grid.querySelectorAll('.book-card').forEach((card, index) => {
            card.addEventListener('click', (e) => {
                // No abrir modal si se hace click en el botón de frases
                if (!e.target.closest('.book-card__btn-frases')) {
                    this.showBookModal(books[index]);
                }
            });
        });

        // Agregar event listeners a los botones de frases
        grid.querySelectorAll('.book-card__btn-frases').forEach((btn) => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation(); // Evitar que se active el click de la tarjeta
                const clave = btn.getAttribute('data-clave');
                if (clave) {
                    // Abrir nueva página con las frases del libro
                    window.open(`frases.html?clave=${encodeURIComponent(clave)}`, '_blank');
                }
            });
        });
    },

    /**
     * Crea el HTML de una tarjeta de libro
     */
    createBookCard(book) {
        const coverUrl = book.portada || '';
        const coverAlt = `Portada de ${book.titulo}`;
        const year = Utils.formatYear(book.fecha_publicacion);
        const category = book.categoria_normalizada || 'Sin categoría';
        const clave = book.clave || '';
        const hasFrases = clave && AppState.frases[clave] && AppState.frases[clave].length > 0;
        const frasesCount = hasFrases ? AppState.frases[clave].length : 0;

        return `
            <article class="book-card" role="listitem" tabindex="0" aria-label="${book.titulo}">
                <div class="book-card__cover">
                    ${coverUrl
                        ? `<img src="${coverUrl}" alt="${coverAlt}" loading="lazy" onerror="this.parentElement.innerHTML='📚'">`
                        : '📚'
                    }
                </div>
                <div class="book-card__body">
                    <h2 class="book-card__title">${this.escapeHtml(book.titulo)}</h2>
                    <p class="book-card__author">${this.escapeHtml(book.autor || 'Autor desconocido')}</p>
                    <div class="book-card__meta">
                        <span class="book-card__badge">${this.escapeHtml(category)}</span>
                        ${year !== 'N/A' ? `<span class="book-card__year">${year}</span>` : ''}
                    </div>
                    ${hasFrases ? `
                        <button class="book-card__btn-frases" data-clave="${clave}" aria-label="Ver frases de ${book.titulo}">
                            🔥 Ver frases chingonas del libro (${frasesCount})
                        </button>
                    ` : ''}
                </div>
            </article>
        `;
    },

    /**
     * Muestra el modal con los detalles del libro
     */
    showBookModal(book) {
        const modal = document.getElementById('book-modal');
        const modalBody = document.getElementById('modal-body');

        if (!modal || !modalBody) return;

        const coverUrl = book.portada || '';
        const year = Utils.formatYear(book.fecha_publicacion);
        const description = book.descripcion_es || book.descripcion || book.resumen_ficha || 'Sin descripción disponible.';

        modalBody.innerHTML = `
            ${coverUrl ? `<img src="${coverUrl}" alt="Portada de ${book.titulo}" class="modal__cover" onerror="this.style.display='none'">` : ''}
            <h2 class="modal__title">${this.escapeHtml(book.titulo)}</h2>
            <p class="modal__author">${this.escapeHtml(book.autor || 'Autor desconocido')}</p>

            <div class="modal__section">
                <h3 class="modal__section-title">Descripción</h3>
                <p class="modal__section-content">${this.escapeHtml(description)}</p>
            </div>

            ${book.tema ? `
                <div class="modal__section">
                    <h3 class="modal__section-title">Tema</h3>
                    <p class="modal__section-content">${this.escapeHtml(book.tema)}</p>
                </div>
            ` : ''}

            <div class="modal__section">
                <h3 class="modal__section-title">Información</h3>
                <div class="modal__badges">
                    ${book.categoria_normalizada ? `<span class="modal__badge">${this.escapeHtml(book.categoria_normalizada)}</span>` : ''}
                    ${year !== 'N/A' ? `<span class="modal__badge">Año: ${year}</span>` : ''}
                    ${book.isbn ? `<span class="modal__badge">ISBN: ${this.escapeHtml(book.isbn)}</span>` : ''}
                </div>
            </div>
        `;

        modal.hidden = false;
        modal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
    },

    /**
     * Oculta el modal
     */
    hideBookModal() {
        const modal = document.getElementById('book-modal');
        if (modal) {
            modal.hidden = true;
            modal.setAttribute('aria-hidden', 'true');
            document.body.style.overflow = '';
        }
    },


    /**
     * Renderiza las opciones de categorías en el select
     */
    renderCategoryFilter(categories) {
        const select = document.getElementById('category-filter');
        if (!select) return;

        const sortedCategories = Array.from(categories).sort();
        select.innerHTML = '<option value="">Todas las categorías</option>' +
            sortedCategories.map(cat =>
                `<option value="${this.escapeHtml(cat)}">${this.escapeHtml(cat)}</option>`
            ).join('');
    },

    /**
     * Actualiza el contador de libros
     */
    updateBooksCount(count) {
        const countElement = document.getElementById('books-count');
        if (countElement) {
            countElement.textContent = count;
        }
    },

    /**
     * Muestra/oculta el mensaje de "no hay resultados"
     */
    toggleNoResults(show) {
        const noResults = document.getElementById('no-results');
        if (noResults) {
            noResults.hidden = !show;
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
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
};

// ============================================
// Filtrado y búsqueda
// ============================================
const Filter = {
    /**
     * Filtra los libros según los criterios actuales
     */
    filterBooks() {
        let filtered = [...AppState.books];

        // Filtro por búsqueda
        if (AppState.searchTerm) {
            const searchNormalized = Utils.normalizeText(AppState.searchTerm);
            filtered = filtered.filter(book => {
                const title = Utils.normalizeText(book.titulo || '');
                const author = Utils.normalizeText(book.autor || '');
                const theme = Utils.normalizeText(book.tema || '');
                const category = Utils.normalizeText(book.categoria_normalizada || '');

                return title.includes(searchNormalized) ||
                       author.includes(searchNormalized) ||
                       theme.includes(searchNormalized) ||
                       category.includes(searchNormalized);
            });
        }

        // Filtro por categoría
        if (AppState.selectedCategory) {
            filtered = filtered.filter(book =>
                book.categoria_normalizada === AppState.selectedCategory
            );
        }

        // Ordenamiento
        filtered = this.sortBooks(filtered, AppState.sortBy);

        AppState.filteredBooks = filtered;
        return filtered;
    },

    /**
     * Ordena los libros según el criterio seleccionado
     */
    sortBooks(books, sortBy) {
        const sorted = [...books];

        switch (sortBy) {
            case 'titulo':
                sorted.sort((a, b) => {
                    const titleA = (a.titulo || '').toLowerCase();
                    const titleB = (b.titulo || '').toLowerCase();
                    return titleA.localeCompare(titleB, 'es');
                });
                break;

            case 'autor':
                sorted.sort((a, b) => {
                    const authorA = (a.autor || '').toLowerCase();
                    const authorB = (b.autor || '').toLowerCase();
                    return authorA.localeCompare(authorB, 'es');
                });
                break;

            case 'fecha_desc':
                sorted.sort((a, b) => {
                    const yearA = a.fecha_publicacion || 0;
                    const yearB = b.fecha_publicacion || 0;
                    return yearB - yearA;
                });
                break;

            case 'fecha_asc':
                sorted.sort((a, b) => {
                    const yearA = a.fecha_publicacion || 0;
                    const yearB = b.fecha_publicacion || 0;
                    return yearA - yearB;
                });
                break;
        }

        return sorted;
    },

    /**
     * Extrae todas las categorías únicas de los libros
     */
    extractCategories(books) {
        const categories = new Set();
        books.forEach(book => {
            if (book.categoria_normalizada) {
                categories.add(book.categoria_normalizada);
            }
        });
        return categories;
    }
};

// ============================================
// Controladores de eventos
// ============================================
const EventHandlers = {
    /**
     * Inicializa todos los event listeners
     */
    init() {
        // Búsqueda
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            const debouncedSearch = Utils.debounce((e) => {
                AppState.searchTerm = e.target.value;
                this.handleFilterChange();
            }, 300);

            searchInput.addEventListener('input', debouncedSearch);
        }

        // Filtro de categoría
        const categoryFilter = document.getElementById('category-filter');
        if (categoryFilter) {
            categoryFilter.addEventListener('change', (e) => {
                AppState.selectedCategory = e.target.value;
                this.handleFilterChange();
            });
        }

        // Ordenamiento
        const sortSelect = document.getElementById('sort-select');
        if (sortSelect) {
            sortSelect.addEventListener('change', (e) => {
                AppState.sortBy = e.target.value;
                this.handleFilterChange();
            });
        }

        // Botón limpiar filtros
        const clearFiltersBtn = document.getElementById('clear-filters');
        if (clearFiltersBtn) {
            clearFiltersBtn.addEventListener('click', () => {
                this.clearFilters();
            });
        }

        // Modal
        const modal = document.getElementById('book-modal');
        const modalOverlay = document.getElementById('modal-overlay');
        const modalClose = document.getElementById('modal-close');

        if (modalOverlay) {
            modalOverlay.addEventListener('click', () => {
                Renderer.hideBookModal();
            });
        }

        if (modalClose) {
            modalClose.addEventListener('click', () => {
                Renderer.hideBookModal();
            });
        }

        // Cerrar modal con ESC
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal && !modal.hidden) {
                Renderer.hideBookModal();
            }
        });
    },

    /**
     * Maneja cambios en los filtros
     */
    handleFilterChange() {
        const filtered = Filter.filterBooks();
        Renderer.renderBooksGrid(filtered);
        Renderer.updateBooksCount(filtered.length);
        Renderer.toggleNoResults(filtered.length === 0);
    },

    /**
     * Limpia todos los filtros
     */
    clearFilters() {
        AppState.searchTerm = '';
        AppState.selectedCategory = '';
        AppState.sortBy = 'titulo';

        const searchInput = document.getElementById('search-input');
        const categoryFilter = document.getElementById('category-filter');
        const sortSelect = document.getElementById('sort-select');

        if (searchInput) searchInput.value = '';
        if (categoryFilter) categoryFilter.value = '';
        if (sortSelect) sortSelect.value = 'titulo';

        this.handleFilterChange();
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
            // Asegurar que el modal esté oculto inicialmente
            const modal = document.getElementById('book-modal');
            if (modal) {
                modal.hidden = true;
                modal.setAttribute('aria-hidden', 'true');
            }

            Renderer.toggleLoading(true);

            // Cargar libros y frases en paralelo
            const [books, frases] = await Promise.all([
                BooksAPI.loadBooks(),
                BooksAPI.loadFrases()
            ]);

            AppState.books = books;
            AppState.filteredBooks = books;
            AppState.frases = frases;

            // Extraer categorías
            AppState.categories = Filter.extractCategories(books);

            // Renderizar categorías
            Renderer.renderCategoryFilter(AppState.categories);

            // Renderizar libros iniciales
            Renderer.renderBooksGrid(books);
            Renderer.updateBooksCount(books.length);

            // Inicializar event handlers
            EventHandlers.init();

            Renderer.toggleLoading(false);
        } catch (error) {
            console.error('Error inicializando la aplicación:', error);
            Renderer.toggleLoading(false);

            const grid = document.getElementById('books-grid');
            if (grid) {
                grid.innerHTML = `
                    <div style="grid-column: 1 / -1; text-align: center; padding: 2rem; color: #ef4444;">
                        <p>❌ Error cargando los libros. Por favor, recarga la página.</p>
                    </div>
                `;
            }
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
