# Despliegue en GitHub Pages

Este proyecto está configurado para desplegarse automáticamente en GitHub Pages usando GitHub Actions.

## Configuración Inicial

### 1. Habilitar GitHub Pages en el repositorio

1. Ve a **Settings** > **Pages** en tu repositorio de GitHub
2. En **Source**, selecciona **GitHub Actions** (no "Deploy from a branch")
3. Guarda los cambios

### 2. Verificar la rama principal

El workflow se ejecuta automáticamente cuando haces push a las ramas `main` o `master`. Asegúrate de que tu rama principal tenga uno de estos nombres.

### 3. Estructura del proyecto

El workflow está configurado para desplegar el contenido de la carpeta `public/`. Asegúrate de que todos los archivos estáticos (HTML, CSS, JS, JSON) estén en esta carpeta.

## Cómo funciona

1. **Push automático**: Cada vez que hagas push a `main` o `master`, el workflow se ejecutará automáticamente
2. **Ejecución manual**: También puedes ejecutar el workflow manualmente desde la pestaña **Actions** en GitHub
3. **Despliegue**: El contenido de `public/` se desplegará en `https://[tu-usuario].github.io/[nombre-repo]/`

## Verificar el despliegue

1. Ve a la pestaña **Actions** en GitHub
2. Verifica que el workflow "Deploy to GitHub Pages" se haya ejecutado correctamente
3. Una vez completado, tu sitio estará disponible en la URL de GitHub Pages

## Notas importantes

- El workflow usa las acciones oficiales de GitHub para Pages
- Los archivos se sirven desde la carpeta `public/`
- El despliegue puede tardar unos minutos en completarse
- La URL del sitio aparecerá en la pestaña **Settings** > **Pages** una vez que el primer despliegue se complete

## Solución de problemas

Si el despliegue falla:

1. Verifica que GitHub Pages esté habilitado con **GitHub Actions** como fuente
2. Revisa los logs en la pestaña **Actions** para ver errores específicos
3. Asegúrate de que la carpeta `public/` contenga todos los archivos necesarios
4. Verifica que los permisos del workflow estén configurados correctamente (deberían estar en el archivo `.github/workflows/deploy.yml`)
