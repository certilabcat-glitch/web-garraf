# Reglas operativas para Cline — Proyecto Certilab

## Contexto del proyecto
- Repo: web-garraf (sitio Certilab, consultoría energética técnica remota).
- Stack: HTML estático + Caddy + Nixpacks en EasyPanel. Sin framework JS pesado.
- Sistema visual: Aesop premium (Crimson Pro serif + Inter sans, paleta crema/terracota).
- Branch única: main. Deploy automático desde main vía EasyPanel.
- Tracking: Facebook Pixel ID 1271893388238243.
- Pago: PayPal button WURK9UH6WHWRS.
- Webhook n8n: https://n8n-n8n.nfnizn.easypanel.host/webhook/auditoria-pago-certilab.

## Quién decide qué
- El humano (Abdelaziz) es quien decide y quien mergea. Cline propone, nunca dispone.
- Eva María González Gracia (Cateb 9457) firma los informes técnicos. Cualquier wording legal o técnico que la implique requiere validación humana antes de commitear.

## Reglas absolutas (violarlas = parar)
1. **Nunca mergear a main por tu cuenta.** El merge lo hace Abdelaziz manualmente.
2. **Plan Mode siempre antes de Act Mode.** Explica el plan completo, espera confirmación, y solo entonces ejecuta.
3. **Nunca abrir archivos en modo escritura ('w') sin haber leído antes el contenido.** Si necesitas modificar un archivo, primero `read_file`, luego escribe.
4. **Nunca ejecutar scripts Python "autónomos" de auditoría o refactor masivo** que toquen >3 archivos sin aprobación explícita por escrito en el chat.
5. **Nunca commitear sin que el humano haya visto `git diff --stat`.** Si las líneas eliminadas superan masivamente a las insertadas, alarma.
6. **Hash `e69de29` en cualquier diff = archivo vaciado = parar inmediatamente.**

## Reglas técnicas obligatorias
- **PowerShell antiguo no acepta `&&` ni `||`.** Usa `;` o comandos separados. No asumas Bash.
- **Para sustituciones masivas: NO uses scripts.** Recomienda al humano que use Find & Replace global de VSCode. Es más seguro y auditable.
- **Después de cualquier cambio masivo:** ejecuta `git grep` con el término relevante para verificar. No te fíes de tu propio reporte.
- **Antes de cualquier commit:** muestra `git diff --stat` y espera OK explícito.
- **Verificación obligatoria post-cambio:** `git ls-files | ForEach-Object { if ((Get-Item $_).Length -eq 0) { $_ } }` — debe devolver vacío.

## Reglas de contenido y marca
- **Cateb, no CAATEB.** El colegio profesional es "Cateb" (Col·legi d'Aparelladors, Arquitectes Tècnics i Enginyers d'Edificació de Barcelona). Si encuentras "CAATEB" en cualquier archivo, es un error a corregir.
- **NO emitimos certificados energéticos oficiales.** Operamos en remoto. Ofrecemos: segunda opinión, análisis técnicos, consultoría energética. Cualquier wording que sugiera lo contrario es un error grave.
- **NO firmamos dictamen jurídico.** Eva firma solo análisis técnico-energético. El Check-Up Inmobiliario tiene Parte A informativa (sin firma) + Parte B técnica (firmada por Eva).
- **Sistema visual Aesop:** respeta tipografías (Crimson Pro + Inter) y paleta (crema/terracota). No introduzcas Bootstrap, Tailwind ni otros sistemas sin pedir permiso.

## Cómo reportar
- **No digas "todo OK" sin pruebas.** Cita el comando ejecutado y su output.
- **Si algo falla, dilo en la primera frase.** No entierres errores en párrafos largos.
- **Si dudas entre dos enfoques, pregunta antes de actuar.** No asumas.
- **Si una tarea requiere >5 archivos modificados, divídela en fases** y pide validación entre fase y fase.

## Lo que NO debes hacer
- Crear archivos `_headers`, `_redirects` o similares sin pedir permiso (Caddy gestiona headers desde su config).
- Tocar `robots.txt`, `sitemap.xml`, `cookies.html`, `privacidad.html`, `legal.html` sin instrucción explícita.
- Modificar el Facebook Pixel ID, el botón PayPal, ni el webhook n8n.
- Cambiar la branch o crear branches nuevas sin pedirlo.
- Hacer "limpieza" o "refactor estético" sin que se te pida.

## Páginas en producción (Aesop completo, no tocar sin instrucción)
- `/` (index.html)
- `/segunda-opinion/`
- `/segunda-opinion-express/`
- `/por-que-no-emite-ce/`
- `/sobre-nosotros/`

## Páginas pendientes de rediseño Aesop (aquí sí se puede trabajar)
- `/check-up-inmobiliario/` (199 €)
- `/informe-tecnico-energetico/` (399 €)
- `/ayudas-eficiencia-energetica/`
- `/formulario/`, `/calculadoracat/`, `/profesionales/`

## Flujo estándar de trabajo
1. Plan Mode: explica qué vas a hacer, qué archivos tocas, qué riesgos hay.
2. Espera OK del humano.
3. Act Mode: ejecuta paso a paso, mostrando output real de cada comando.
4. Post-cambio: `git diff --stat` + `git grep` del término relevante.
5. Si todo OK: propón el commit con mensaje sugerido. NO commitees solo.
6. El humano commitea y mergea.
