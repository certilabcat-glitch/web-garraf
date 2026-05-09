"""
Script de corrección masiva de cookies — Certilab
- Elimina Meta Pixel inline (carga sin consentimiento → ilegal RGPD)
- Elimina banner de cookies viejo hardcodeado (interfiere con cookies.js)
- Añade <script src="/cookies.js" defer> donde falte
Ejecutar desde raíz del repo. Hace backup automático en memoria.
Revisar git diff --stat al terminar.
"""
import re
import os

HTML_FILES = []
for root, dirs, files in os.walk("."):
    # Excluir .git y deploy
    if ".git" in root or "deploy" in root:
        continue
    for f in files:
        if f.endswith(".html"):
            HTML_FILES.append(os.path.join(root, f))

print(f"Archivos HTML encontrados: {len(HTML_FILES)}")

# ── Patrones a buscar/eliminar ──

# 1. Meta Pixel inline (dos variantes: con y sin try/catch)
RE_PIXEL_BLOCK = re.compile(
    r'\s*<!--\s*Meta Pixel( Code)?\s*-->\s*'
    r'<script>\s*'
    r'(?:try\s*\{)?\s*'
    r'!function\(f,b,e,v,n,t,s\)[\s\S]*?'
    r"fbq\('init',\s*'1271893388238243'\);\s*"
    r"fbq\('track',\s*'PageView'\)[\s\S]*?"
    r'</script>\s*'
    r'(?:<!-- End Meta Pixel( Code)? -->\s*)?'
    r'(?:<noscript>[\s\S]*?</noscript>\s*)?',
    re.MULTILINE
)

# 2. Banner viejo hardcodeado
RE_OLD_BANNER = re.compile(
    r'\s*<div id="cookie-banner"[^>]*>[\s\S]*?</div>\s*',
    re.MULTILINE
)
# Función closeCookies inline
RE_CLOSE_COOKIES_FN = re.compile(
    r'\s*<script>\s*function closeCookies\(\)[\s\S]*?</script>\s*',
    re.MULTILINE
)

# 3. Añadir cookies.js antes de </body> si no existe
RE_COOKIES_JS = re.compile(r'<script\s+src="?/cookies\.js"?')
RE_BODY_CLOSE = re.compile(r'(\s*</body>)')

modified = 0

for filepath in HTML_FILES:
    with open(filepath, "r", encoding="utf-8") as fh:
        original = fh.read()

    content = original

    # Paso 1: Eliminar Pixel inline
    if "fbq('init'" in content:
        content = RE_PIXEL_BLOCK.sub("\n", content)
        # Limpiar posibles líneas vacías múltiples
        content = re.sub(r'\n{3,}', '\n\n', content)

    # Paso 2: Eliminar banner viejo
    if 'id="cookie-banner"' in content:
        content = RE_OLD_BANNER.sub("\n", content)
        content = RE_CLOSE_COOKIES_FN.sub("\n", content)
        content = re.sub(r'\n{3,}', '\n\n', content)

    # Paso 3: Añadir cookies.js si no está
    if not RE_COOKIES_JS.search(content):
        content = RE_BODY_CLOSE.sub(
            r'\n    <!-- Banner de cookies con consentimiento RGPD -->\n'
            r'    <script src="/cookies.js" defer></script>\n\1',
            content,
            count=1
        )

    if content != original:
        with open(filepath, "w", encoding="utf-8") as fh:
            fh.write(content)
        modified += 1
        print(f"  [OK] {filepath}")

print(f"\nArchivos modificados: {modified}")
print("Ejecuta: git diff --stat para revisar los cambios.")