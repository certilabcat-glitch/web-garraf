"""
Unifica el <nav> en todas las páginas HTML del proyecto Certilab.
También añade font-display: swap a Google Fonts y el fix del menú móvil.
"""
import os
import re
import glob

# ============================================================
# NAV CANÓNICO (el que irá en TODAS las páginas)
# ============================================================
CANONICAL_NAV = '''<nav class="nav" role="navigation" aria-label="Navegación principal">
    <div class="nav-inner">
        <a href="/" class="nav-logo" aria-label="Certilab — inicio">
            <span>Certilab</span>
        </a>
        <button class="nav-toggle" aria-label="Abrir menú" aria-expanded="false" aria-controls="nav-menu">
            <span></span><span></span><span></span>
        </button>
        <ul class="nav-menu" id="nav-menu" role="list" aria-label="Navegación principal">
            <li><a href="/#servicios">Servicios</a></li>
            <li><a href="/segunda-opinion/">Segunda Opinión</a></li>
            <li><a href="/segunda-opinion-express/">Segunda Opinión Express</a></li>
            <li><a href="/check-up-inmobiliario/">Check-Up</a></li>
            <li><a href="/informe-tecnico-energetico/">Informe Técnico</a></li>
            <li><a href="/formulario/">Diagnóstico Gratis</a></li>
            <li><a href="/calculadoracat/">Calculadora</a></li>
            <li><a href="/blog/">Blog</a></li>
            <li><a href="/profesionales/">Profesionales</a></li>
            <li><a href="/sobre-nosotros/">Sobre nosotros</a></li>
            <li><a href="/por-que-no-emite-ce/" class="nav-cta">Por qué no emitimos CE</a></li>
        </ul>
    </div>
</nav>'''

# ============================================================
# SCRIPT MENÚ MÓVIL UNIFICADO (incluye fix para cerrar al click)
# ============================================================
MOBILE_MENU_JS = '''    <script>
        (function() {
            var toggle = document.querySelector('.nav-toggle');
            var menu = document.querySelector('.nav-menu');
            if (!toggle || !menu) return;
            toggle.addEventListener('click', function() {
                var expanded = toggle.getAttribute('aria-expanded') === 'true';
                toggle.setAttribute('aria-expanded', String(!expanded));
                menu.classList.toggle('is-open');
            });
            // Cerrar menú móvil al hacer clic en cualquier enlace
            document.querySelectorAll('.nav-menu a').forEach(function(link) {
                link.addEventListener('click', function() {
                    menu.classList.remove('is-open');
                    toggle.setAttribute('aria-expanded', 'false');
                });
            });
        })();'''

# ============================================================
# FUNCIONES
# ============================================================

def replace_nav(content):
    """Reemplaza el bloque <nav ...> ... </nav> completo por el canónico."""
    # Patrón: desde <nav hasta </nav> (multilínea, non-greedy en el contenido)
    pattern = r'<nav\b[^>]*>.*?</nav>'
    if re.search(pattern, content, re.DOTALL):
        return re.sub(pattern, CANONICAL_NAV.strip(), content, count=1, flags=re.DOTALL)
    else:
        # Si no encuentra <nav>, intenta buscar solo <nav (por si hay diferencias)
        pattern2 = r'<nav\b.*?</nav>'
        if re.search(pattern2, content, re.DOTALL):
            return re.sub(pattern2, CANONICAL_NAV.strip(), content, count=1, flags=re.DOTALL)
    return content

def replace_mobile_menu_js(content):
    """Reemplaza el bloque del menú móvil JS por la versión unificada con fix."""
    # Buscar el script que contiene nav-toggle y reemplazarlo
    # Patrón: desde (function() { var toggle... hasta })();
    pattern = r'<script>\s*\(function\(\)\s*\{[^}]*var toggle[^<]*?\}\)\(\);\s*</script>'
    if re.search(pattern, content, re.DOTALL):
        return re.sub(pattern, MOBILE_MENU_JS.strip() + '\n    </script>', content, count=1, flags=re.DOTALL)

    # Fallback: buscar cualquier script que contenga nav-toggle
    pattern2 = r'<script>[^<]*nav-toggle[^<]*</script>'
    if re.search(pattern2, content, re.DOTALL):
        return re.sub(pattern2, MOBILE_MENU_JS.strip() + '\n    </script>', content, count=1, flags=re.DOTALL)

    return content

def add_font_display_swap(content):
    """Añade &display=swap a todas las URLs de Google Fonts que no lo tengan."""
    # Busca URLs de Google Fonts sin display=swap
    pattern = r'(https://fonts\.googleapis\.com/css2\?[^"\'\s]+)'
    def replacer(match):
        url = match.group(1)
        if 'display=swap' not in url:
            if '?' in url:
                url += '&display=swap'
            else:
                url += '?display=swap'
        return url
    return re.sub(pattern, replacer, content)

def process_file(filepath):
    """Procesa un archivo HTML aplicando todas las correcciones."""
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    content = original

    # 1. Unificar nav
    content = replace_nav(content)

    # 2. Fix menú móvil
    content = replace_mobile_menu_js(content)

    # 3. font-display: swap
    content = add_font_display_swap(content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Encontrar todos los HTML
    html_files = []
    for root, dirs, files in os.walk(base_dir):
        # Saltar node_modules, .git, deploy
        dirs[:] = [d for d in dirs if d not in ('node_modules', '.git', 'deploy', 'docs')]
        for f in files:
            if f.endswith('.html'):
                html_files.append(os.path.join(root, f))

    print(f"Encontrados {len(html_files)} archivos HTML")
    modified = []
    skipped = []

    for fp in sorted(html_files):
        rel = os.path.relpath(fp, base_dir)
        try:
            changed = process_file(fp)
            if changed:
                modified.append(rel)
                print(f"  [OK] MODIFICADO: {rel}")
            else:
                skipped.append(rel)
        except Exception as e:
                print(f"  [ERROR] en {rel}: {e}")

    print(f"\n--- RESUMEN ---")
    print(f"Modificados: {len(modified)}")
    for m in modified:
        print(f"  • {m}")
    print(f"Sin cambios: {len(skipped)}")

if __name__ == '__main__':
    main()