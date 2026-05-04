import os
import re

def safe(s):
    return s.encode('ascii', errors='replace').decode('ascii')

dirs = ['.'] + sorted([d for d in os.listdir('.') if os.path.isdir(d) and os.path.exists(d+'/index.html')])

for d in dirs:
    filepath = d + '/index.html' if d != '.' else 'index.html'
    label = d if d != '.' else 'HOME'
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    title_match = re.search(r'<title>(.*?)</title>', html)
    desc_match = re.search(r'<meta name="description" content="(.*?)"', html)
    
    title = title_match.group(1) if title_match else 'NO TITLE'
    desc = desc_match.group(1) if desc_match else 'NO DESC'
    
    print(f'=== {label} ===')
    print(f'title ({len(title)} chars): {safe(title)}')
    print(f'desc  ({len(desc)} chars): {safe(desc[:100])}')
    print()