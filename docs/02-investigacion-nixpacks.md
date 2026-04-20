# Investigación Técnica: Nixpacks y Redirecciones

**Fecha:** 20/04/2026  
**Rama:** `refundacion-modelo-sin-ce`  
**Contexto:** Documentación técnica sobre limitaciones de Nixpacks para redirecciones

---

## 🔍 ¿Qué es Nixpacks?

**Nixpacks** es un buildpack moderno desarrollado por Railway (ahora usado también por EasyPanel) que:
- Detecta automáticamente el tipo de proyecto
- Genera una imagen Docker optimizada
- Configura el servidor web automáticamente
- **NO lee archivos de configuración de servidor del repositorio**

### Diferencia clave con otros sistemas

| Sistema | Configuración de redirects |
|---------|---------------------------|
| **Apache** | `.htaccess` en el repo |
| **Nginx tradicional** | `nginx.conf` en el repo |
| **Caddy tradicional** | `Caddyfile` en el repo |
| **Vercel** | `vercel.json` en el repo |
| **Netlify** | `netlify.toml` en el repo |
| **Nixpacks** | ❌ Ignora archivos de config del repo |

---

## 🏗️ Cómo funciona Nixpacks

### 1. Detección automática
Nixpacks analiza el repositorio y detecta:
```
- package.json → Node.js
- requirements.txt → Python
- index.html + sin backend → Static site
```

### 2. Generación de Dockerfile
Crea un Dockerfile temporal con:
- Instalación de dependencias
- Build del proyecto
- **Configuración de servidor web (generada, no leída del repo)**

### 3. Para sitios estáticos
Nixpacks usa internamente:
- **Caddy** o **Nginx** según la configuración de EasyPanel
- La configuración se genera en **tiempo de build**
- Los archivos `Caddyfile` o `nginx.conf` del repo son **ignorados**

---

## 🚫 Por qué no funcionan los archivos de configuración

### Ejemplo: Caddyfile en el repo

```caddy
# Este archivo será IGNORADO por Nixpacks
certilab.cat {
    redir /certificado-energetico/ /por-que-no-emite-ce/ 301
}
```

**Razón:** Nixpacks genera su propio `Caddyfile` en el contenedor, sobrescribiendo cualquier configuración del repo.

### Ejemplo: .htaccess

```apache
# Este archivo será IGNORADO (Nixpacks no usa Apache)
RewriteEngine On
RewriteRule ^certificado-energetico/$ /por-que-no-emite-ce/ [R=301,L]
```

**Razón:** Nixpacks no usa Apache, usa Caddy o Nginx.

---

## ✅ Soluciones viables

### Opción 1: Redirects en la UI de EasyPanel (RECOMENDADO)
- ✅ Funciona de forma nativa
- ✅ No requiere modificar el build
- ✅ Fácil de mantener
- ✅ Se aplica a nivel de proxy inverso (antes de llegar al contenedor)

### Opción 2: Meta refresh HTML
Crear archivos HTML con meta refresh en cada directorio:

```html
<!-- /certificado-energetico/index.html -->
<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="refresh" content="0;url=/por-que-no-emite-ce/">
  <link rel="canonical" href="/por-que-no-emite-ce/">
</head>
<body>
  <p>Redirigiendo...</p>
</body>
</html>
```

**Desventajas:**
- ❌ No es un 301 real (es un 200 con meta refresh)
- ❌ Menos eficiente para SEO
- ❌ Requiere mantener archivos HTML

### Opción 3: JavaScript redirect
```html
<script>window.location.replace('/por-que-no-emite-ce/');</script>
```

**Desventajas:**
- ❌ No funciona sin JavaScript
- ❌ No es un 301 HTTP real
- ❌ Peor para SEO que meta refresh

### Opción 4: Dockerfile personalizado
Crear un `Dockerfile` en el repo para tener control total:

```dockerfile
FROM caddy:2-alpine
COPY Caddyfile /etc/caddy/Caddyfile
COPY . /srv
CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile"]
```

**Desventajas:**
- ❌ Pierdes las optimizaciones automáticas de Nixpacks
- ❌ Más complejo de mantener
- ❌ Requiere conocimientos de Docker

---

## 📊 Comparativa de soluciones

| Solución | SEO | Facilidad | Mantenimiento | Recomendado |
|----------|-----|-----------|---------------|-------------|
| **UI EasyPanel** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ SÍ |
| Meta refresh HTML | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⚠️ Solo si UI no disponible |
| JavaScript redirect | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ NO |
| Dockerfile custom | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ❌ Overkill |

---

## 🎯 Decisión final para Certilab

**Usar la UI de EasyPanel** para configurar los 7 redirects 301.

**Razones:**
1. Es la solución nativa y recomendada
2. Genera 301 HTTP reales (mejor SEO)
3. No requiere modificar el código
4. Fácil de mantener y auditar
5. Se aplica a nivel de infraestructura (más rápido)

---

## 📚 Referencias técnicas

- [Nixpacks GitHub](https://github.com/railwayapp/nixpacks)
- [Nixpacks Docs](https://nixpacks.com/docs)
- [EasyPanel Docs](https://easypanel.io/docs)
- [Caddy Docs - Redirects](https://caddyserver.com/docs/caddyfile/directives/redir)
- [Google: 301 vs Meta Refresh](https://developers.google.com/search/docs/crawling-indexing/301-redirects)

---

## 🔬 Experimentos realizados

### Test 1: Caddyfile en el repo
```bash
# Resultado: IGNORADO
# El archivo existe en el repo pero no se usa en producción
```

### Test 2: .htaccess en el repo
```bash
# Resultado: IGNORADO
# Nixpacks no usa Apache
```

### Test 3: nginx.conf en el repo
```bash
# Resultado: IGNORADO
# Nixpacks genera su propia configuración de Nginx/Caddy
```

### Conclusión
Ningún archivo de configuración de servidor en el repositorio tiene efecto con Nixpacks. La única forma de configurar redirects es a través de la UI de EasyPanel o usando un Dockerfile personalizado (no recomendado).

---

*Documento creado: 20/04/2026 | Rama: refundacion-modelo-sin-ce*