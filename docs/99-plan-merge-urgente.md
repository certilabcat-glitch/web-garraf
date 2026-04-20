# Plan de Merge Urgente a Main — Certilab

**Fecha:** 20/04/2026  
**Rama origen:** `refundacion-modelo-sin-ce`  
**Rama destino:** `main`  
**Responsable ejecución:** Abdelaziz Achibane  
**Razón de urgencia:** Producción sirve modelo viejo (CE 89€ sin visita, ilegal según RD 390/2021 art. 6.5)

---

## ⚠️ CONTEXTO CRÍTICO

**Situación actual:** La rama `main` en producción contiene el modelo antiguo que ofrece certificados energéticos sin visita presencial, lo cual es **ilegal según RD 390/2021 art. 6.5**. Cada día que pasa es exposición legal.

**Solución:** Merge urgente de `refundacion-modelo-sin-ce` a `main` en estado actual (con páginas transicionales mínimas para servicios aún no construidos).

**Estado de la rama:**
- ✅ Home nueva con catálogo 5 servicios sin CE oficial
- ✅ Página `/por-que-no-emite-ce/` explicando motivo legal
- ✅ Página `/segunda-opinion/` (39€) completa
- ✅ Página `/segunda-opinion-express/` (79€) completa
- ✅ 3 páginas transicionales mínimas: Check-Up (199€), Informe Técnico (399€), Ayudas
- ✅ Enlaces en home ajustados para evitar 404s
- ✅ Documentación estratégica (keywords, GBP, redirects)

---

## 📋 SECCIÓN 1 — CHECKLIST ANTES DEL MERGE

Verificar estos puntos **ANTES** de ejecutar el merge:

- [ ] **Verificar que todos los commits están pushed a origin**
  ```bash
  git status
  # Debe mostrar: "Your branch is up to date with 'origin/refundacion-modelo-sin-ce'"
  ```

- [ ] **Verificar que no hay cambios sin commitear**
  ```bash
  git status
  # Debe mostrar: "nothing to commit, working tree clean"
  ```

- [ ] **Test manual de la home nueva en local**
  - Abrir `index.html` en navegador
  - Verificar que se ve correctamente
  - Verificar que los enlaces del catálogo funcionan (no dan 404)

- [ ] **Verificar que las 3 páginas transicionales existen**
  ```bash
  ls check-up-inmobiliario/index.html
  ls informe-tecnico-energetico/index.html
  ls ayudas-eficiencia-energetica/index.html
  # Los 3 archivos deben existir
  ```

- [ ] **Backup de la rama main actual (por seguridad)**
  ```bash
  git checkout main
  git branch backup-main-pre-merge
  git checkout refundacion-modelo-sin-ce
  ```

---

## 🔀 SECCIÓN 2 — COMANDOS GIT PARA HACER MERGE

**⚠️ IMPORTANTE:** Ejecutar estos comandos en orden, uno por uno, verificando el resultado de cada paso.

### Paso 1: Estar en la rama de trabajo y verificar estado limpio

```bash
cd c:/Users/evam7/certilab/web-garraf
git checkout refundacion-modelo-sin-ce
git status
```

**Resultado esperado:** `nothing to commit, working tree clean` en la rama `refundacion-modelo-sin-ce`

---

### Paso 2: Cambiar a main

```bash
git checkout main
```

**Resultado esperado:** `Switched to branch 'main'`

---

### Paso 3: Actualizar main con últimos cambios del remoto (por seguridad)

```bash
git pull origin main
```

**Resultado esperado:** `Already up to date.` (o descarga de cambios si los hay)

---

### Paso 4: Hacer el merge desde la rama de trabajo

```bash
git merge refundacion-modelo-sin-ce
```

**Resultado esperado:** 
- Si no hay conflictos: `Merge made by the 'recursive' strategy.` + lista de archivos modificados
- Si hay conflictos: Ver sección "Resolución de conflictos" más abajo

---

### Paso 5: Push a origin main

```bash
git push origin main
```

**Resultado esperado:** `To https://github.com/certilabcat-glitch/web-garraf.git` + confirmación de push

**⚠️ NOTA:** Este push NO dispara deploy automático. El deploy es manual en EasyPanel (ver Sección 4).

---

### 🚨 Resolución de conflictos (si aparecen)

Si el merge genera conflictos, Git mostrará algo como:

```
Auto-merging index.html
CONFLICT (content): Merge conflict in index.html
Automatic merge failed; fix conflicts and then commit the result.
```

**Pasos para resolver:**

1. **Ver qué archivos tienen conflictos:**
   ```bash
   git status
   # Mostrará archivos con "both modified"
   ```

2. **Abrir cada archivo conflictivo en VS Code**
   - Buscar marcadores `<<<<<<<`, `=======`, `>>>>>>>`
   - Decidir qué versión mantener (normalmente la de `refundacion-modelo-sin-ce`)
   - Eliminar los marcadores de conflicto

3. **Marcar conflictos como resueltos:**
   ```bash
   git add <archivo-resuelto>
   ```

4. **Completar el merge:**
   ```bash
   git commit -m "Merge refundacion-modelo-sin-ce into main (conflictos resueltos)"
   ```

5. **Push:**
   ```bash
   git push origin main
   ```

---

## 🔄 SECCIÓN 3 — LOS 7 REDIRECTS A CONFIGURAR EN EASYPANEL

**⚠️ IMPORTANTE:** Configurar estos redirects **DESPUÉS** del deploy, cuando la nueva versión esté en producción.

### Tabla de Redirects

| # | Source Path | Destination | Type | Notas |
|---|-------------|-------------|------|-------|
| 1 | `/certificado-energetico/` | `/por-que-no-emite-ce/` | 301 Permanent | Intención: emitir CE → explicación legal |
| 2 | `/precio-certificado-energetico/` | `/por-que-no-emite-ce/` | 301 Permanent | Intención: comparar precios → explicación |
| 3 | `/obtener-certificado-energetico-gratis/` | `/por-que-no-emite-ce/` | 301 Permanent | Intención: CE gratuito → explicación honesta |
| 4 | `/auditoria-energetica-online/` | `/informe-tecnico-energetico/` | 301 Permanent | Intención: análisis profundo → producto equivalente |
| 5 | `/fondos-next-generation-2026/` | `/ayudas-eficiencia-energetica/` | 301 Permanent | Intención: info ayudas → contenido SEO útil |
| 6 | `/certificadoenergeticoinflado/` | `/segunda-opinion/` | 301 Permanent | ✅ Ya configurado, verificar que sigue activo |
| 7 | `/Tuexpedienteenergético/` | `/expediente/` | 301 Permanent | Migración técnica URL no-ASCII (pendiente crear `/expediente/`) |

### Cómo configurar en EasyPanel UI

1. **Acceder a EasyPanel:** https://app.easypanel.io (o URL de tu instancia)
2. **Localizar el proyecto Certilab**
3. **Ir a Settings → Redirects** (o sección equivalente en la UI)
4. **Para cada redirect de la tabla:**
   - Click en "Add Redirect" o botón equivalente
   - **Source Path:** copiar exactamente de la tabla (incluir `/` inicial y final)
   - **Destination:** copiar exactamente de la tabla
   - **Type:** seleccionar "301 Permanent"
   - **Save/Apply**

### Ejemplo de entrada en EasyPanel

```
Source Path: /certificado-energetico/
Destination: /por-que-no-emite-ce/
Type: 301 (Permanent)
```

**⚠️ NOTA sobre redirect #7:** La página `/expediente/` aún no existe. Opciones:
- **Opción A:** No configurar este redirect todavía (dejar para cuando se cree `/expediente/`)
- **Opción B:** Redirigir temporalmente a `/formulario/` hasta que se cree `/expediente/`

---

## 🚀 SECCIÓN 4 — DEPLOY MANUAL EN EASYPANEL

**⚠️ IMPORTANTE:** El push a `main` NO dispara deploy automático. Debes hacerlo manualmente.

### Pasos para deploy:

1. **Acceder a EasyPanel:** https://app.easypanel.io

2. **Localizar el servicio Certilab** en el dashboard

3. **Pulsar botón "Deploy" o "Redeploy"**
   - Puede estar en la página principal del servicio
   - O en Settings → Deployment

4. **Confirmar el deploy**
   - EasyPanel mostrará el progreso del build
   - Esperar a que termine (2-5 minutos normalmente)

5. **Verificar que el servicio está activo**
   - Estado debe cambiar a "Running" o "Active"
   - URL del servicio debe ser accesible

### Logs del deploy

Si el deploy falla:
- Click en "Logs" o "Build Logs"
- Buscar líneas con `ERROR` o `FAILED`
- Copiar el error completo
- Compartir captura al equipo para diagnóstico

---

## ✅ SECCIÓN 5 — VERIFICACIONES POST-DEPLOY

**⚠️ CRÍTICO:** Verificar estos puntos **INMEDIATAMENTE** después del deploy.

### Checklist de verificación:

- [ ] **Home nueva carga correctamente**
  ```
  https://certilab.cat/
  ```
  - ✅ Debe mostrar la home nueva con "La única consultoría energética que no emite certificados"
  - ❌ NO debe mostrar la home vieja con "Certificado Energético 89€"

- [ ] **Página por-que-no-emite-ce carga**
  ```
  https://certilab.cat/por-que-no-emite-ce/
  ```
  - ✅ Debe cargar sin errores
  - ✅ Debe explicar RD 390/2021 art. 6.5

- [ ] **Redirect 1: certificado-energetico → por-que-no-emite-ce**
  ```bash
  curl -I https://certilab.cat/certificado-energetico/
  ```
  - ✅ Debe devolver: `HTTP/1.1 301 Moved Permanently`
  - ✅ Header `Location:` debe apuntar a `/por-que-no-emite-ce/`

- [ ] **Redirect 2: precio-certificado-energetico → por-que-no-emite-ce**
  ```bash
  curl -I https://certilab.cat/precio-certificado-energetico/
  ```
  - ✅ Debe devolver: `HTTP/1.1 301 Moved Permanently`

- [ ] **Redirect 3: obtener-certificado-energetico-gratis → por-que-no-emite-ce**
  ```bash
  curl -I https://certilab.cat/obtener-certificado-energetico-gratis/
  ```
  - ✅ Debe devolver: `HTTP/1.1 301 Moved Permanently`

- [ ] **Redirect 4: auditoria-energetica-online → informe-tecnico-energetico**
  ```bash
  curl -I https://certilab.cat/auditoria-energetica-online/
  ```
  - ✅ Debe devolver: `HTTP/1.1 301 Moved Permanently`
  - ✅ Header `Location:` debe apuntar a `/informe-tecnico-energetico/`

- [ ] **Redirect 5: fondos-next-generation-2026 → ayudas-eficiencia-energetica**
  ```bash
  curl -I https://certilab.cat/fondos-next-generation-2026/
  ```
  - ✅ Debe devolver: `HTTP/1.1 301 Moved Permanently`

- [ ] **Redirect 6: certificadoenergeticoinflado → segunda-opinion (ya existente)**
  ```bash
  curl -I https://certilab.cat/certificadoenergeticoinflado/
  ```
  - ✅ Debe devolver: `HTTP/1.1 301 Moved Permanently`

- [ ] **Redirect 7: Tuexpedienteenergético → expediente**
  ```bash
  curl -I https://certilab.cat/Tuexpedienteenergético/
  ```
  - ⚠️ Solo si configuraste este redirect (ver nota en Sección 3)

- [ ] **Enlaces del catálogo en home funcionan (no dan 404)**
  - https://certilab.cat/formulario/ (Diagnóstico Express)
  - https://certilab.cat/segunda-opinion/ (Segunda Opinión 39€)
  - https://certilab.cat/segunda-opinion-express/ (Segunda Opinión Express 79€)
  - https://certilab.cat/check-up-inmobiliario/ (Check-Up 199€)
  - https://certilab.cat/informe-tecnico-energetico/ (Informe Técnico 399€)
  - https://certilab.cat/ayudas-eficiencia-energetica/ (Ayudas)

- [ ] **Las 3 páginas transicionales cargan correctamente**
  - https://certilab.cat/check-up-inmobiliario/
  - https://certilab.cat/informe-tecnico-energetico/
  - https://certilab.cat/ayudas-eficiencia-energetica/
  - ✅ Deben mostrar mensaje "Servicio en fase de lanzamiento"

- [ ] **CSS carga correctamente (la home se ve bien visualmente)**
  - Colores correctos (terra, crema, verde)
  - Tipografías correctas (Crimson Pro + Inter)
  - Layout responsive funciona

### Verificación en diferentes dispositivos:

- [ ] **Desktop (Chrome/Firefox)**
- [ ] **Mobile (Chrome Android o Safari iOS)**
- [ ] **Modo incógnito** (para evitar caché)

---

## 🚨 SECCIÓN 6 — QUÉ HACER SI ALGO FALLA

### Problema 1: El deploy falla en EasyPanel

**Síntomas:**
- Build logs muestran errores
- El servicio no arranca
- Estado "Failed" o "Error"

**Solución:**
1. Ir a Build Logs en EasyPanel
2. Buscar la línea con `ERROR` o `FAILED`
3. Copiar el error completo
4. Compartir captura al equipo (Eva + Abdelaziz)
5. **NO intentar arreglar solo** — esperar diagnóstico

**Rollback de emergencia:**
```bash
git checkout main
git reset --hard backup-main-pre-merge
git push origin main --force
```
⚠️ Solo usar si el deploy falla completamente y no hay otra opción.

---

### Problema 2: Un redirect no funciona

**Síntomas:**
- `curl -I` devuelve `404 Not Found` en lugar de `301`
- O devuelve `200 OK` (carga la página vieja en lugar de redirigir)

**Solución:**
1. Verificar que el redirect está configurado en EasyPanel UI
2. Verificar que el Source Path es exacto (incluir `/` inicial y final)
3. Verificar que el Destination es exacto
4. Verificar que Type es "301 Permanent"
5. Probar en modo incógnito (para evitar caché del navegador)
6. Si sigue sin funcionar, probar añadiendo variante sin trailing slash:
   - Ejemplo: si `/certificado-energetico/` no funciona, añadir también `/certificado-energetico`

---

### Problema 3: La home se ve rota (CSS no carga)

**Síntomas:**
- La home carga pero sin estilos
- Texto negro sobre fondo blanco
- Layout desorganizado

**Solución:**
1. Verificar que el archivo `style.css` existe en el repositorio
2. Abrir DevTools del navegador (F12)
3. Ir a pestaña "Network"
4. Recargar la página
5. Buscar `style.css` en la lista de recursos
6. Si aparece en rojo (404), el problema es que el archivo no se deployó
7. Si aparece en verde pero la página sigue sin estilos, el problema es de caché:
   - Hacer hard refresh: Ctrl+Shift+R (Windows) o Cmd+Shift+R (Mac)
   - O abrir en modo incógnito

---

### Problema 4: Un enlace da 404

**Síntomas:**
- Click en un enlace del catálogo → página "Not Found"

**Solución:**
1. Verificar que el archivo existe en el repositorio:
   ```bash
   ls segunda-opinion/index.html
   ls check-up-inmobiliario/index.html
   # etc.
   ```
2. Si el archivo existe pero da 404, el problema es del deploy:
   - Verificar logs de EasyPanel
   - Puede que el archivo no se haya copiado correctamente
3. Si el archivo NO existe, es un error de la rama:
   - Contactar al equipo
   - Mientras tanto, el enlace mostrará la página transicional o 404

---

## 📊 SECCIÓN 7 — MONITORIZACIÓN POST-MERGE

### Primeras 24 horas:

- [ ] **Revisar Google Search Console**
  - Ir a https://search.google.com/search-console
  - Verificar que no hay pico de errores 404
  - Solicitar re-indexación de `/` y `/por-que-no-emite-ce/`

- [ ] **Revisar Google Analytics** (si está configurado)
  - Verificar que el tráfico sigue llegando
  - Verificar que no hay caída brusca de visitas

- [ ] **Revisar Meta Pixel** (si está configurado)
  - Verificar que los eventos se siguen registrando

### Primera semana:

- [ ] **Monitorizar errores 404 en Google Search Console**
  - Si aparecen URLs no contempladas, añadir redirects adicionales

- [ ] **Revisar posicionamiento de keywords principales**
  - "certificado energético" (debería redirigir a por-que-no-emite-ce)
  - "segunda opinión certificado energético" (debería llevar a /segunda-opinion/)

- [ ] **Revisar feedback de usuarios**
  - ¿Alguien reporta enlaces rotos?
  - ¿Alguien se queja de no encontrar el servicio de CE?

---

## 📝 SECCIÓN 8 — NOTAS FINALES

### Archivos modificados en el merge (resumen):

**Archivos AÑADIDOS:**
- `deploy/Caddyfile.backup`
- `docs/00-gap-analysis.md`
- `docs/01-plan-redirects-easypanel.md`
- `docs/02-investigacion-nixpacks.md`
- `docs/10-mapa-keywords.md`
- `docs/11-estrategia-gbp.md`
- `segunda-opinion-express/index.html`
- `check-up-inmobiliario/index.html`
- `informe-tecnico-energetico/index.html`
- `ayudas-eficiencia-energetica/index.html`

**Archivos MODIFICADOS:**
- `index.html` (home nueva)
- `por-que-no-emite-ce/index.html` (explicación legal)

**Total:** 10 commits desde la creación de la rama `refundacion-modelo-sin-ce`.

### Próximos pasos después del merge:

1. ✅ Merge completado y verificado
2. ⏳ Construir páginas completas de los 3 servicios transicionales:
   - `/check-up-inmobiliario/` (actualmente mínima)
   - `/informe-tecnico-energetico/` (actualmente mínima)
   - `/ayudas-eficiencia-energetica/` (actualmente mínima)
3. ⏳ Crear página `/diagnostico-express/` (actualmente redirige a `/formulario/`)
4. ⏳ Migrar `/Tuexpedienteenergético/` → `/expediente/`
5. ⏳ Actualizar `/formulario/`, `/calculadoracat/`, `/profesionales/`
6. ⏳ Actualizar `sitemap.xml` y `robots.txt`

### Contacto en caso de emergencia:

- **Eva María González Gracia:** [teléfono/email]
- **Abdelaziz Achibane:** [teléfono/email]

---

**Documento creado:** 20/04/2026  
**Última actualización:** 20/04/2026  
**Versión:** 1.0  
**Estado:** Listo para ejecución