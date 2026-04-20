# Plan de Redirecciones 301 — EasyPanel

**Fecha:** 20/04/2026  
**Rama:** `refundacion-modelo-sin-ce`  
**Objetivo:** Configurar 7 redirecciones 301 para eliminar páginas del modelo antiguo sin perder SEO

---

## 📋 Lista de Redirecciones

| # | Origen | Destino | Razón |
|---|--------|---------|-------|
| 1 | `/certificado-energetico/` | `/por-que-no-emite-ce/` | Intención: emitir CE → explicación legal + alternativas |
| 2 | `/precio-certificado-energetico/` | `/por-que-no-emite-ce/` | Intención: comparar precios CE → misma explicación |
| 3 | `/obtener-certificado-energetico-gratis/` | `/por-que-no-emite-ce/` | Intención: CE gratuito → explicación honesta |
| 4 | `/auditoria-energetica-online/` | `/informe-tecnico-energetico/` | Intención: análisis profundo → producto equivalente |
| 5 | `/fondos-next-generation-2026/` | `/ayudas-eficiencia-energetica/` | Intención: info ayudas → contenido SEO útil |
| 6 | `/certificadoenergeticoinflado/` | `/segunda-opinion/` | ✅ Ya configurado, mantener |
| 7 | `/Tuexpedienteenergético/` | `/expediente/` | Migración técnica URL no-ASCII |

---

## 🔧 Configuración en EasyPanel

EasyPanel utiliza **Nixpacks** como buildpack por defecto, que NO soporta archivos de configuración de servidor web tradicionales (`.htaccess`, `nginx.conf`, `Caddyfile`) directamente en el repositorio.

### Opción recomendada: Redirects en la UI de EasyPanel

1. **Acceder al proyecto** en EasyPanel
2. **Ir a Settings → Redirects** (o equivalente en la UI)
3. **Añadir cada redirección** con estos parámetros:

#### Formato de entrada en EasyPanel UI

```
Source Path: /certificado-energetico/
Destination: /por-que-no-emite-ce/
Type: 301 (Permanent)
```

```
Source Path: /precio-certificado-energetico/
Destination: /por-que-no-emite-ce/
Type: 301 (Permanent)
```

```
Source Path: /obtener-certificado-energetico-gratis/
Destination: /por-que-no-emite-ce/
Type: 301 (Permanent)
```

```
Source Path: /auditoria-energetica-online/
Destination: /informe-tecnico-energetico/
Type: 301 (Permanent)
```

```
Source Path: /fondos-next-generation-2026/
Destination: /ayudas-eficiencia-energetica/
Type: 301 (Permanent)
```

```
Source Path: /certificadoenergeticoinflado/
Destination: /segunda-opinion/
Type: 301 (Permanent)
Status: ✅ Ya configurado
```

```
Source Path: /Tuexpedienteenergético/
Destination: /expediente/
Type: 301 (Permanent)
```

---

## ⚠️ Consideraciones importantes

### 1. Trailing slashes
- EasyPanel puede manejar automáticamente `/path` y `/path/`
- Si no, añadir ambas variantes manualmente

### 2. Orden de ejecución
1. ✅ Primero crear las páginas de destino (ya hecho: `/por-que-no-emite-ce/`)
2. ⏳ Pendiente: crear `/informe-tecnico-energetico/`, `/ayudas-eficiencia-energetica/`, `/expediente/`
3. Configurar redirects en EasyPanel UI
4. Verificar que funcionan correctamente
5. Solo entonces eliminar físicamente los directorios origen

### 3. Verificación post-deploy
Usar `curl -I` para verificar cada redirect:

```bash
curl -I https://certilab.cat/certificado-energetico/
# Debe devolver: HTTP/1.1 301 Moved Permanently
# Location: https://certilab.cat/por-que-no-emite-ce/

curl -I https://certilab.cat/auditoria-energetica-online/
# Debe devolver: HTTP/1.1 301 Moved Permanently
# Location: https://certilab.cat/informe-tecnico-energetico/
```

### 4. Google Search Console
Después de configurar los redirects:
1. Ir a Google Search Console
2. Solicitar re-indexación de las URLs de destino
3. Monitorizar errores 404 en las próximas semanas

---

## 🚫 Lo que NO funciona en EasyPanel/Nixpacks

- ❌ `.htaccess` (Apache)
- ❌ `nginx.conf` en el repo
- ❌ `Caddyfile` en el repo
- ❌ `vercel.json` redirects
- ❌ `netlify.toml` redirects

**Razón:** Nixpacks genera su propia configuración de servidor en tiempo de build. Los archivos de configuración del repo son ignorados.

---

## 📚 Referencias

- [EasyPanel Docs](https://easypanel.io/docs)
- [Nixpacks Documentation](https://nixpacks.com/docs)
- Ver también: `docs/02-investigacion-nixpacks.md` para detalles técnicos

---

*Documento creado: 20/04/2026 | Rama: refundacion-modelo-sin-ce*