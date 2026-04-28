# Gap Analysis — Refundación Modelo Sin CE Oficial

**Fecha:** 19/04/2026  
**Rama:** `refundacion-modelo-sin-ce`  
**Autor:** Cline (revisado y validado por Eva González)

---

## Contexto y motivo del cambio

**Decisión estratégica crítica:** Certilab NO va a emitir certificados energéticos oficiales (CE3X).

**Motivo legal:** El Real Decreto 390/2021, art. 5.5, exige visita presencial del técnico al inmueble antes de emitir el certificado. El modelo de Certilab es 100% remoto, por tanto incompatible con emitir CE oficial.

**Riesgos de continuar con el modelo anterior:**
- Sanciones económicas: 300–6.000 €
- Expediente deontológico CAATEB
- Denuncias FACUA
- Pérdida del seguro RC profesional
- Nulidad de los certificados emitidos

**Nuevo posicionamiento:** "La única consultoría energética que no emite certificados — porque los hacemos con rigor técnico, no con prisas."

---

## 1. ELIMINAR (riesgo legal o modelo obsoleto)

| Directorio/Archivo | Problema | Acción |
|---|---|---|
| `certificado-energetico/` | Promueve CE3X oficial 89€ sin visita → **ILEGAL** RD 390/2021 | Redirección 301 → `/por-que-no-emite-ce/` |
| `precio-certificado-energetico/` | Precios modelo antiguo (89€ CE, 299€ auditoría) | Redirección 301 → `/por-que-no-emite-ce/` |
| `obtener-certificado-energetico-gratis/` | Nombre implica emisión de CE | Redirección 301 → `/por-que-no-emite-ce/` |
| `auditoria-energetica-online/` | "Auditoría Energética" = término regulado RD 56/2016 | Redirección 301 → `/informe-tecnico-energetico/` |
| `fondos-next-generation-2026/` | Requiere Agente Rehabilitador inscrito (Certilab no lo es) | Redirección 301 → `/ayudas-eficiencia-energetica/` |
| `certificadoenergeticoinflado/` | Nombre problemático | ✅ Ya redirige → `/segunda-opinion/`, mantener |
| `Tuexpedienteenergético/` | URL con carácter no-ASCII + formulario post-pago modelo antiguo | Migrar contenido → `/expediente/` + 301 desde URL con tilde |
| `index.html` (copy principal) | CE3X, 89€, "registro CCAA", "válido para notarías", Auditoría 299€ | Reescribir completo |
| `BRIEFING-EVA.md` | Basado en modelo antiguo | Reemplazar con nuevo briefing |
| `PROTOCOLO-RESPUESTA-LEADS.md` | Basado en modelo antiguo | Reemplazar con nuevo protocolo |

### Redirecciones 301 — Segmentadas por intención del buscador

| Origen | Destino 301 | Razón de la segmentación |
|---|---|---|
| `/certificado-energetico/` | `/por-que-no-emite-ce/` | Intención: emitir CE → necesita explicación + alternativas |
| `/precio-certificado-energetico/` | `/por-que-no-emite-ce/` | Intención: comparar precios CE → misma razón |
| `/obtener-certificado-energetico-gratis/` | `/por-que-no-emite-ce/` | Intención: CE gratuito → explicación honesta |
| `/auditoria-energetica-online/` | `/informe-tecnico-energetico/` | Intención: análisis profundo → producto equivalente directo |
| `/fondos-next-generation-2026/` | `/ayudas-eficiencia-energetica/` | Intención: info ayudas → contenido informativo SEO útil |
| `/certificadoenergeticoinflado/` | `/segunda-opinion/` | ✅ Ya hecho, mantener |
| `/Tuexpedienteenergético/` | `/expediente/` | Migración técnica URL no-ASCII |

---

## 2. APROVECHAR (con modificaciones)

| Archivo | Estado actual | Modificación necesaria |
|---|---|---|
| `segunda-opinion/index.html` | ✅ Bien estructurado, 39€, sin promesas ilegales | Pulir copy, añadir referencia a variante Express |
| `por-que-no-emite-ce/index.html` | ⚠️ Motivo incorrecto ("especialidad remota") | Reescribir con motivo legal real: RD 390/2021 art. 5.5 + router de intención al final |
| `calculadoracat/index.html` | ✅ Estima ahorro energético (CTE 2019), sin prometer CE oficial | Actualizar menú de navegación + copy hero |
| `formulario/index.html` | ⚠️ Diseñado para CE oficial | Reformular campos para los 5 nuevos servicios. Verificar webhook n8n antes de cambios destructivos |
| `profesionales/index.html` | ⚠️ Catálogo antiguo | Adaptar al nuevo catálogo |
| `style.css` | ✅ CSS unificado, sólido | Sin cambios |
| Estructura HTML/CSS general | ✅ Reutilizable | Base para nuevas páginas |

---

## 3. CREAR DESDE CERO

### Nuevo catálogo de servicios (5 servicios, sin CE oficial)

| URL | Servicio | Precio | Entrega | Rol estratégico |
|---|---|---|---|---|
| `/diagnostico-express/` | Diagnóstico Express | 0€ | Inmediato | Captación |
| `/segunda-opinion/` | Segunda Opinión Estándar | 39€ | 24h lab. | Producto martillo |
| `/segunda-opinion-express/` | Segunda Opinión Express | 79€ | <2h lab. | Upsell urgencia |
| `/check-up-inmobiliario/` | Check-Up Inmobiliario | 199€ | 48h lab. | Producto palanca |
| `/informe-tecnico-energetico/` | Informe Técnico Energético | 399€ | 5-7 días | Premium nicho |

### Páginas de soporte

| URL | Tipo | Propósito |
|---|---|---|
| `/ayudas-eficiencia-energetica/` | Contenido informativo SEO | Captar tráfico de keywords "ayudas" → CTA a Informe Técnico |
| `/expediente/` | Formulario post-pago | Migración técnica de `/Tuexpedienteenergético/` |

### Notas de producto

**Check-Up Inmobiliario (199€)** — Para DECIDIR una compra (pre-firma):
- Nota Simple del Registro + Certificado Catastral + Consulta de cargas
- Análisis del certificado energético del vendedor si lo aporta (= Segunda Opinión incorporada)
- Análisis técnico con datos del formulario + fotos + facturas
- Detección de reformas no declaradas
- Estimación de coste energético real
- Lista de banderas rojas a verificar presencialmente antes de firmar
- Audio IA personalizado 2-3 minutos
- Informe 10-15 páginas

**Segunda Opinión Express (79€)** — Mismo entregable que Estándar (39€):
- Única diferencia: entrega <2h laborables vs 24h laborables
- Solo válido L-V 9-18h. Fuera de horario → primera hora siguiente día laboral
- Esto debe quedar explícito en el copy. NO es un servicio de contenido distinto.

**`/por-que-no-emite-ce/` — Router de intención al final:**
- "Tengo  y quiero verificarlo" → `/segunda-opinion/`
- "Voy a comprar un piso" → `/check-up-inmobiliario/`
- "Tengo un piso y quiero mejorarlo" → `/informe-tecnico-energetico/`

**`/ayudas-eficiencia-energetica/` — Contenido informativo honesto:**
- Qué ayudas existen (Next Generation, CAE, IRPF, subvenciones autonómicas)
- Requisitos generales de cada una
- Enlaces oficiales a las CCAA
- Disclaimer: "Certilab no gestiona la tramitación de ayudas. Para gestionar la ayuda tras las obras, contacta con un Agente Rehabilitador inscrito en tu CCAA."
- CTA sutil: "Si quieres un plan técnico de mejoras previo a solicitar ayudas, nuestro Informe Técnico Energético (399€) te da la hoja de ruta."

---

## 4. DECISIONES TOMADAS

| Tema | Decisión |
|---|---|
| Idiomas | Solo castellano. Catalán = fase futura. Inglés = descartado. |
| `/ca/` y `/en/` | No están en el directorio actual. Limpiar referencias rotas (header, footer, hreflang) si las hay. |
| Radiografía de Propiedad | No existe como producto visible. Solo componente interno del Check-Up. |
| `/calculadoracat/` | Se mantiene como herramienta de captación gratuita. Solo actualizar menú y copy. |
| `/Tuexpedienteenergético/` | Migrar a `/expediente/` + 301 desde URL con tilde. |
| Formulario | Webhook n8n. Modificable libremente. Verificar antes de cambios destructivos. |
| Redirección `/certificado-energetico/` | → `/por-que-no-emite-ce/` (no a `/segunda-opinion/`) |
| Redirección `/auditoria-energetica-online/` | → `/informe-tecnico-energetico/` (intención equivalente) |
| Redirección `/fondos-next-generation-2026/` | → `/ayudas-eficiencia-energetica/` (nueva página SEO) |

---

## 5. ORDEN DE EJECUCIÓN

### 🔴 Prioridad máxima — Primero preparar el destino
1. ✅ Crear rama `refundacion-modelo-sin-ce`
2. ✅ Escribir este documento `docs/00-gap-analysis.md`
3. ⏸️ **PAUSA — Esperar luz verde de Eva**
4. Reescribir `/por-que-no-emite-ce/` con motivo legal real (RD 390/2021 art. 5.5) + router de intención
5. Reescribir `index.html` eliminando todo CE oficial + nuevo catálogo

*Razón del orden: la redirección 301 sin tener el destino bien preparado es peor que mantener temporalmente las páginas ilegales. Primero preparamos el destino, luego redirigimos.*

### 🟠 Prioridad alta — Inmediatamente después
6. Aplicar redirecciones 301 según tabla corregida
7. Eliminar físicamente los directorios redirigidos (para que no queden huérfanos indexables)

### 🟡 Prioridad media
8. Crear `/diagnostico-express/` (0€)
9. Crear `/segunda-opinion-express/` (79€)
10. Crear `/check-up-inmobiliario/` (199€)
11. Crear `/informe-tecnico-energetico/` (399€)
12. Crear `/ayudas-eficiencia-energetica/` (SEO informativo)
13. Actualizar `formulario/` para nuevos servicios (verificar webhook primero)
14. Actualizar `calculadoracat/` (menú + copy)
15. Actualizar `profesionales/` con nuevo catálogo

### 🟢 Prioridad baja
16. Limpiar referencias rotas a `/ca/`, `/en/`, hreflang
17. Regenerar `sitemap.xml` limpio
18. Actualizar `robots.txt`
19. Merge `refundacion-modelo-sin-ce` → `main`

---

*Documento generado: 19/04/2026 | Validado por Eva González | Rama: refundacion-modelo-sin-ce*