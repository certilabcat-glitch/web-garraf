import os, re

base = r'c:\Users\evam7\certilab\web-garraf'
landings = [
    ('', 'index.html'),
    ('segunda-opinion', 'index.html'),
    ('segunda-opinion-express', 'index.html'),
    ('formulario', 'index.html'),
    ('por-que-no-emite-ce', 'index.html'),
    ('profesionales', 'index.html'),
    ('sobre-nosotros', 'index.html'),
    ('check-up-inmobiliario', 'index.html'),
    ('informe-tecnico-energetico', 'index.html'),
    ('ayudas-eficiencia-energetica', 'index.html'),
    ('calculadoracat', 'index.html'),
]

print(f"{'Landing':<32} {'Title ch':>9} {'Desc ch':>9} {'H1':<35} {'OG?':>5} {'TW?':>5}")
print('-' * 95)

for folder, file in landings:
    path = os.path.join(base, folder, file)
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    name = folder if folder else 'home'
    tm = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    title = tm.group(1).strip() if tm else 'MISSING'
    tlen = len(title)
    dm = re.search(r'<meta name="description" content="(.*?)"', html)
    desc = dm.group(1).strip() if dm else 'MISSING'
    dlen = len(desc) if dm else 0
    hm = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    h1 = re.sub(r'<[^>]+>', '', hm.group(1).strip()[:50]) if hm else 'MISSING'
    og = 'YES' if 'og:title' in html else 'NO'
    tw = 'YES' if 'twitter:title' in html else 'NO'
    flags = []
    if tlen > 60: flags.append('TITLE>60')
    if dlen > 160: flags.append('DESC>160')
    if hm is None: flags.append('NO-H1')
    flag_str = ' '.join(flags) if flags else 'OK'
    print(f"{name:<32} {tlen:>9} {dlen:>9} {h1:<35} {og:>5} {tw:>5}  {flag_str}")