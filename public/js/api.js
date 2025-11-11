/**
 * API compartida para cargar datos
 */

/**
 * Carga los libros desde el archivo JSON
 */
export async function loadBooks() {
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
}

/**
 * Carga las frases desde el archivo JSON
 */
export async function loadFrases() {
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
