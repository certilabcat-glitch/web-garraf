"""Unify nav and fix og:image across all HTML pages of Certilab."""
import re
import os
from pathlib import Path

ROOT = Path(r"c:\Users\evam7\certilab\web-garraf")

# Files with the main nav (exclude legal/cookies/privacidad which use minimal layout)
HTML_FILES = [
    "index.html",
    "404.html",
    "sobre-nosotros/index.html",
    "por-que-no-emite-ce/index.html",
    "segunda-opinion/index.html",
    "segunda-opinion-express/index.html",
    "check-up-inmobiliario/index.html",
    "informe-tecnico-energetico/index.html",
    "formulario/index.html",
    "calculadoracat/index.html",
    "ayudas-eficiencia-energetica/index.html",
    "profesionales/index.html",
    "blog/errores-certificado-energetico/index.html",
    "blog/obtener-certificado-energetico-gratis/index.html",
]

NEW_NAV = """<!-- NAV -->
  <nav class="nav" role="navigation" aria-label="Navegaci\u00f3n principal">
    <div class="nav-inner">
        <a href="/" class="nav-logo" aria-label="Certilab \u2014 inicio">
            <span>Certilab</span>
        </a>
        <button class="nav-toggle" aria-label="Abrir men\u00fa" aria-expanded="false" aria-controls="nav-menu">
            <span></span><span></span><span></span>
        </button>
        <ul class="nav-menu" id="nav-menu" role="list" aria-label="Navegaci\u00f3n principal">
            <li><a href="/">Inicio</a></li>
            <li class="nav-dropdown">
                <button class="nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">Servicios <span class="arrow"></span></button>
                <ul class="nav-dropdown-menu">
                    <li><a href="/formulario/">Diagn\u00f3stico Gratuito</a></li>
                    <li><a href="/segunda-opinion/">Segunda Opini\u00f3n (39\u20ac)</a></li>
                    <li><a href="/segunda-opinion-express/">Segunda Opini\u00f3n Express</a></li>
                    <li><a href="/check-up-inmobiliario/">Check-Up Inmobiliario (199\u20ac)</a></li>
                    <li><a href="/informe-tecnico-energetico/">Informe T\u00e9cnico (399\u20ac)</a></li>
                </ul>
            </li>
            <li><a href="/por-que-no-emite-ce/">Por qu\u00e9 no emitimos CE</a></li>
            <li><a href="/blog/">Blog</a></li>
            <li><a href="/sobre-nosotros/">Sobre nosotros</a></li>
            <li><a href="/calculadoracat/">Calculadora</a></li>
            <li><a href="/formulario/" class="nav-cta">Diagn\u00f3stico Gratis</a></li>
            <li><a href="/por-que-no-emite-ce/" class="nav-cta-secondary">Por qu\u00e9 no emitimos CE</a></li>
        </ul>
    </div>
</nav>"""

NEW_SCRIPT = """<script>
    (function() {
        var toggle = document.querySelector('.nav-toggle');
        var menu = document.querySelector('.nav-menu');
        if (!toggle || !menu) return;
        toggle.addEventListener('click', function() {
            var expanded = toggle.getAttribute('aria-expanded') === 'true';
            toggle.setAttribute('aria-expanded', String(!expanded));
            menu.classList.toggle('is-open');
        });
        // Cerrar men\u00fa m\u00f3vil al hacer clic en enlace
        document.querySelectorAll('.nav-menu > li > a, .nav-dropdown-menu a').forEach(function(link) {
            link.addEventListener('click', function() {
                menu.classList.remove('is-open');
                toggle.setAttribute('aria-expanded', 'false');
            });
        });
        // Dropdown toggle en escritorio y m\u00f3vil
        var dropdowns = document.querySelectorAll('.nav-dropdown-toggle');
        dropdowns.forEach(function(btn) {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                var parent = btn.closest('.nav-dropdown');
                if (parent) {
                    parent.classList.toggle('open');
                    btn.setAttribute('aria-expanded', parent.classList.contains('open'));
                }
            });
        });
        // Cerrar dropdown al hacer clic fuera
        document.addEventListener('click', function(e) {
            dropdowns.forEach(function(btn) {
                var parent = btn.closest('.nav-dropdown');
                if (parent && !parent.contains(e.target)) {
                    parent.classList.remove('open');
                    btn.setAttribute('aria-expanded', 'false');
                }
            });
        });
    })();
  </script>"""


def replace_nav_block(content):
    """Replace <nav class="nav" ...> ... </nav> with the unified nav."""
    # Find opening <nav class="nav"
    pattern_start = re.compile(r'<nav\s+class="nav"[^>]*>')
    m = pattern_start.search(content)
    if not m:
        return content

    start_idx = m.start()
    depth = 1
    i = m.end()
    while i < len(content) and depth > 0:
        # Look for next <nav or </nav>
        next_open = content.find('<nav', i)
        next_close = content.find('</nav>', i)
        if next_close == -1:
            break
        if next_open != -1 and next_open < next_close:
            depth += 1
            i = next_open + 4
        else:
            depth -= 1
            if depth == 0:
                end_idx = next_close + len('</nav>')
                return content[:start_idx] + NEW_NAV + content[end_idx:]
            i = next_close + len('</nav>')
    return content


def replace_script_block(content):
    """Replace the inline nav script with the new one that includes dropdown handler."""
    # Match the script block that starts with (function() { ... nav-toggle
    pattern = re.compile(
        r'<script>\s*\(function\(\)\s*\{.*?nav-toggle.*?\}\s*\)\s*\(\s*\)\s*;\s*</script>',
        re.DOTALL
    )
    m = pattern.search(content)
    if not m:
        # Try looser pattern for older pages
        pattern2 = re.compile(
            r'<script>\s*//\s*Mobile nav toggle.*?</script>',
            re.DOTALL
        )
        m2 = pattern2.search(content)
        if m2:
            return content[:m2.start()] + NEW_SCRIPT + content[m2.end():]
        return content
    return content[:m.start()] + NEW_SCRIPT + content[m.end():]


def fix_og_image(content):
    """Replace favicon.png in og:image with og-image.jpg."""
    # Match og:image with favicon.png
    pattern = re.compile(
        r'<meta\s+property="og:image"\s+content="[^"]*favicon\.png"[^>]*>',
        re.IGNORECASE
    )
    replacement = '<meta property="og:image" content="https://certilab.cat/og-image.jpg">'
    return pattern.sub(replacement, content)


def fix_og_image_twitter(content):
    """Fix twitter:image if it exists with favicon.png."""
    pattern = re.compile(
        r'<meta\s+name="twitter:image"\s+content="[^"]*favicon\.png"[^>]*>',
        re.IGNORECASE
    )
    replacement = '<meta name="twitter:image" content="https://certilab.cat/og-image.jpg">'
    return pattern.sub(replacement, content)


def process_file(filepath):
    path = ROOT / filepath
    if not path.exists():
        print(f"  SKIP (no existe): {filepath}")
        return

    content = path.read_text(encoding='utf-8')
    modified = False

    # Fix og:image
    new_content = fix_og_image(content)
    if new_content != content:
        modified = True
        content = new_content

    # Fix twitter:image if present
    new_content = fix_og_image_twitter(content)
    if new_content != content:
        modified = True
        content = new_content

    # Replace nav
    new_content = replace_nav_block(content)
    if new_content != content:
        modified = True
        content = new_content

    # Replace script
    new_content = replace_script_block(content)
    if new_content != content:
        modified = True
        content = new_content

    if modified:
        path.write_text(content, encoding='utf-8')
        print(f"  MODIFICADO: {filepath}")
    else:
        print(f"  sin cambios: {filepath}")


if __name__ == '__main__':
    print("=== Unificando nav y corrigiendo og:image ===")
    for f in HTML_FILES:
        process_file(f)
    print("=== Completado ===")