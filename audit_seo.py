"""
Auditoría SEO global de Certilab (web-garraf).
Analiza todas las páginas HTML del sitio y genera un reporte con:
- Title, description, H1, OG tags, Twitter tags, Schema, canonical, robots
- Longitudes y warnings
- Estructura de headings (H1-H4)
- Enlaces rotos internos
- Páginas huérfanas (sin enlaces entrantes)
"""

import os
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(r"c:\Users\evam7\certilab\web-garraf")

# Exclusiones razonables
EXCLUDE_DIRS = {".git", "deploy", "docs", ".clinerules", "__pycache__"}

def find_html_files():
    """Encuentra todos los .html en el proyecto (recursivo)."""
    files = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # Filtrar directorios excluidos
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for f in filenames:
            if f.endswith(".html"):
                files.append(Path(dirpath) / f)
    return sorted(files)

def extract_meta(html, name):
    """Extrae <meta name='...' content='...'> o <meta property='...' content='...'>."""
    # Primero property
    m = re.search(rf'<meta\s+property=["\']{name}["\']\s+content=["\']([^"\']*)["\']', html, re.IGNORECASE)
    if m:
        return m.group(1)
    # Luego name
    m = re.search(rf'<meta\s+name=["\']{name}["\']\s+content=["\']([^"\']*)["\']', html, re.IGNORECASE)
    if m:
        return m.group(1)
    return None

def extract_title(html):
    m = re.search(r'<title>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else None

def extract_canonical(html):
    m = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']*)["\']', html, re.IGNORECASE)
    return m.group(1) if m else None

def extract_robots(html):
    m = re.search(r'<meta\s+name=["\']robots["\']\s+content=["\']([^"\']*)["\']', html, re.IGNORECASE)
    return m.group(1) if m else None

def extract_h1(html):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL | re.IGNORECASE)
    if m:
        # Strip tags
        return re.sub(r'<[^>]+>', '', m.group(1)).strip()
    return None

def extract_headings(html):
    """Extrae todos los headings (H1-H4) con su texto."""
    headings = defaultdict(list)
    for level in range(1, 5):
        for m in re.finditer(rf'<h{level}[^>]*>(.*?)</h{level}>', html, re.DOTALL | re.IGNORECASE):
            text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
            headings[f"H{level}"].append(text)
    return dict(headings)

def has_schema(html):
    """Detecta si hay algún Schema.org JSON-LD."""
    return bool(re.search(r'application/ld\+json', html))

def extract_internal_links(html):
    """Extrae todos los enlaces internos (href que empieza con /)."""
    links = set()
    for m in re.finditer(r'href=["\'](/[^"\']*)["\']', html):
        href = m.group(1)
        # Ignorar anchors, tel:, mailto:
        if href.startswith("/#") or href == "/":
            continue
        # Quitar fragment y query string
        href = href.split("#")[0].split("?")[0]
        if href:
            links.add(href)
    return links

def get_relative_path(filepath):
    """Devuelve la ruta relativa desde ROOT."""
    return str(filepath.relative_to(ROOT)).replace("\\", "/")

def url_from_path(rel_path):
    """Convierte ruta relativa a URL del sitio."""
    if rel_path == "index.html":
        return "/"
    if rel_path.endswith("index.html"):
        return "/" + rel_path[:-len("index.html")]
    return "/" + rel_path

def path_from_url(url):
    """Convierte URL interna a ruta de archivo."""
    if url == "/":
        return "index.html"
    url = url.rstrip("/")
    return url[1:] + "/index.html"

def sanitize(text):
    """Reemplaza caracteres no imprimibles en cp1252 (emojis, etc.) por ?."""
    if text is None:
        return None
    return text.encode('cp1252', errors='replace').decode('cp1252')

def main():
    html_files = find_html_files()
    
    print("=" * 110)
    print(" AUDITORIA SEO -- CERTILAB.CAT")
    print("=" * 110)
    print(f"\nArchivos HTML encontrados: {len(html_files)}\n")
    
    # --- PARTE 1: Análisis por página ---
    print("=" * 110)
    print(" 1. METADATOS POR PAGINA")
    print("=" * 110)
    
    page_data = {}
    all_links = set()
    page_urls = {}  # url -> rel_path
    
    for filepath in html_files:
        html = filepath.read_text(encoding='utf-8')
        rel = get_relative_path(filepath)
        url = url_from_path(rel)
        page_urls[url] = rel
        
        title = extract_title(html)
        desc = extract_meta(html, "description")
        og_title = extract_meta(html, "og:title")
        og_desc = extract_meta(html, "og:description")
        og_image = extract_meta(html, "og:image")
        tw_title = extract_meta(html, "twitter:title")
        tw_image = extract_meta(html, "twitter:image")
        canonical = extract_canonical(html)
        robots = extract_robots(html)
        h1 = extract_h1(html)
        headings = extract_headings(html)
        schema = has_schema(html)
        internal_links = extract_internal_links(html)
        
        page_data[rel] = {
            "url": url,
            "title": title,
            "desc": desc,
            "og_title": og_title,
            "og_desc": og_desc,
            "og_image": og_image,
            "tw_title": tw_title,
            "tw_image": tw_image,
            "canonical": canonical,
            "robots": robots,
            "h1": h1,
            "headings": headings,
            "schema": schema,
            "internal_links": internal_links,
        }
        
        # Acumular todos los enlaces internos
        all_links.update(internal_links)
        
        # Build warnings
        warnings = []
        if title is None:
            warnings.append("NO-TITLE")
        elif len(title) < 30:
            warnings.append("TITLE-SHORT")
        elif len(title) > 60:
            warnings.append(f"TITLE-LONG({len(title)})")
        
        if desc is None:
            warnings.append("NO-DESC")
        elif len(desc) < 70:
            warnings.append("DESC-SHORT")
        elif len(desc) > 160:
            warnings.append(f"DESC-LONG({len(desc)})")
        
        if h1 is None:
            warnings.append("NO-H1")
        
        headings_list = []
        for k, v in sorted(headings.items()):
            headings_list.append(f"{k}: {v}")
        
        if not og_title:
            warnings.append("NO-OG:TITLE")
        if not og_desc:
            warnings.append("NO-OG:DESC")
        if not og_image or "favicon" in (og_image or ""):
            warnings.append("OG:IMAGE-FAVICON")
        if not canonical:
            warnings.append("NO-CANONICAL")
        if not schema:
            warnings.append("NO-SCHEMA")
        if not robots:
            warnings.append("NO-ROBOTS")
        
        warn_str = " | ".join(warnings) if warnings else "OK"
        
        print(f"\n  [+] {url}")
        print(f"     Title: {sanitize(title)}")
        print(f"     Desc:  {sanitize(desc)}")
        print(f"     H1:    {sanitize(h1)}")
        print(f"     OG:    title={sanitize(og_title)}, image={sanitize(og_image)}")
        print(f"     TW:    title={sanitize(tw_title)}, image={sanitize(tw_image)}")
        print(f"     Canonical: {sanitize(canonical)}")
        print(f"     Robots: {sanitize(robots)}")
        print(f"     Schema: {'YES' if schema else 'NO'}")
        print(f"     Headings: {sanitize(' | '.join(headings_list) if headings_list else 'NONE')}")
        print(f"     Links salientes: {len(internal_links)}")
        print(f"     [!] {warn_str}")
    
    # --- PARTE 2: Resumen de warnings ---
    print("\n\n" + "=" * 110)
    print(" 2. RESUMEN DE WARNINGS")
    print("=" * 110)
    
    warning_counts = defaultdict(int)
    for rel, data in page_data.items():
        title = data["title"]
        desc = data["desc"]
        
        if title is None:
            warning_counts["NO-TITLE"] += 1
        elif len(title) < 30:
            warning_counts["TITLE-SHORT (<30)"] += 1
        elif len(title) > 60:
            warning_counts[f"TITLE-LONG (>60)"] += 1
        
        if desc is None:
            warning_counts["NO-DESC"] += 1
        elif len(desc) < 70:
            warning_counts["DESC-SHORT (<70)"] += 1
        elif len(desc) > 160:
            warning_counts["DESC-LONG (>160)"] += 1
        
        if data["h1"] is None:
            warning_counts["NO-H1"] += 1
        if not data["og_title"]:
            warning_counts["NO-OG:TITLE"] += 1
        if not data["og_desc"]:
            warning_counts["NO-OG:DESC"] += 1
        if not data["og_image"] or "favicon" in (data["og_image"] or ""):
            warning_counts["OG:IMAGE-FAVICON"] += 1
        if not data["canonical"]:
            warning_counts["NO-CANONICAL"] += 1
        if not data["schema"]:
            warning_counts["NO-SCHEMA"] += 1
        if not data["robots"]:
            warning_counts["NO-ROBOTS"] += 1
    
    for warn, count in sorted(warning_counts.items(), key=lambda x: -x[1]):
        print(f"  {warn:<25} -> {count} paginas")
    
    # --- PARTE 3: Páginas huérfanas ---
    print("\n\n" + "=" * 110)
    print(" 3. PÁGINAS HUÉRFANAS (sin enlaces internos entrantes desde otras páginas)")
    print("=" * 110)
    
    # Construir conjunto de URLs enlazadas
    linked_urls = set()
    for rel, data in page_data.items():
        for link in data["internal_links"]:
            linked_urls.add(link)
    
    orphans = []
    for rel, data in page_data.items():
        url = data["url"]
        if url != "/" and url not in linked_urls:
            orphans.append(url)
    
    if orphans:
        for o in sorted(orphans):
            print(f"  [HUERFANA] {o}")
    else:
        print("  [OK] Ninguna pagina huerfana detectada.")
    
    # --- PARTE 4: Enlaces rotos ---
    print("\n\n" + "=" * 110)
    print(" 4. ENLACES INTERNOS ROTOS (apuntan a páginas que no existen)")
    print("=" * 110)
    
    broken = []
    for link in sorted(all_links):
        expected_path = path_from_url(link)
        if expected_path not in page_data:
            # Verificar si es una URL con subdirectorio que realmente existe
            rel_path = link.lstrip("/")
            if rel_path not in page_data:
                broken.append(link)
    
    if broken:
        for b in sorted(broken):
            # Encontrar qué páginas enlazan a esta URL rota
            sources = []
            for rel, data in page_data.items():
                if b in data["internal_links"]:
                    sources.append(data["url"])
            print(f"  [ROTO] {b} -- enlazado desde: {', '.join(sources)}")
    else:
        print("  [OK] Ningun enlace interno roto detectado.")
    
    # --- PARTE 5: Páginas con más problemas ---
    print("\n\n" + "=" * 110)
    print(" 5. SCORE DE SALUD SEO POR PÁGINA")
    print("=" * 110)
    
    scores = []
    for rel, data in page_data.items():
        score = 0
        issues = []
        
        if data["title"] and 30 <= len(data["title"]) <= 60:
            score += 1
        else:
            issues.append("title")
        
        if data["desc"] and 70 <= len(data["desc"]) <= 160:
            score += 1
        else:
            issues.append("desc")
        
        if data["h1"]:
            score += 1
        else:
            issues.append("h1")
        
        if data["og_title"]:
            score += 1
        else:
            issues.append("og:title")
        
        if data["og_desc"]:
            score += 1
        else:
            issues.append("og:desc")
        
        if data["og_image"] and "favicon" not in (data["og_image"] or ""):
            score += 1
        else:
            issues.append("og:image")
        
        if data["canonical"]:
            score += 1
        else:
            issues.append("canonical")
        
        if data["schema"]:
            score += 1
        else:
            issues.append("schema")
        
        if data["robots"]:
            score += 1
        else:
            issues.append("robots")
        
        scores.append((score, data["url"], issues))
    
    scores.sort()
    for score, url, issues in scores:
        bar = "#" * score + "." * (9 - score)
        issues_str = ", ".join(issues) if issues else "perfecto"
        print(f"  {url:<50} [{bar}] {score}/9 — {issues_str}")
    
    # --- PARTE 6: Stats globales ---
    print("\n\n" + "=" * 110)
    print(" 6. ESTADÍSTICAS GLOBALES")
    print("=" * 110)
    print(f"  Total páginas analizadas: {len(html_files)}")
    print(f"  Total enlaces internos únicos: {len(all_links)}")
    print(f"  Páginas huérfanas: {len(orphans)}")
    print(f"  Enlaces rotos: {len(broken)}")
    avg_score = sum(s[0] for s in scores) / len(scores) if scores else 0
    print(f"  Score promedio: {avg_score:.1f}/9")
    print(f"  Páginas con Schema: {sum(1 for _, d in page_data.items() if d['schema'])}/{len(page_data)}")
    print(f"  Páginas con Canonical: {sum(1 for _, d in page_data.items() if d['canonical'])}/{len(page_data)}")
    print(f"  Páginas con Robots: {sum(1 for _, d in page_data.items() if d['robots'])}/{len(page_data)}")


if __name__ == "__main__":
    main()