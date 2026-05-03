import os, sys

count = 0
for root, dirs, files in os.walk('.'):
    for name in files:
        if not name.endswith('.html'):
            continue
        fp = os.path.join(root, name)
        with open(fp, 'r', encoding='utf-8') as fh:
            content = fh.read()
        if 'try { fbq' in content:
            continue  # already fixed

        # Try multiple patterns
        original = content
        # Pattern 1: two separate lines with trailing space on first
        content = content.replace(
            "    fbq('init', '1271893388238243'); \n    fbq('track', 'PageView');",
            "    try { fbq('init', '1271893388238243'); fbq('track', 'PageView'); } catch(e) {}"
        )
        # Pattern 2: no trailing space
        content = content.replace(
            "    fbq('init', '1271893388238243');\n    fbq('track', 'PageView');",
            "    try { fbq('init', '1271893388238243'); fbq('track', 'PageView'); } catch(e) {}"
        )
        # Pattern 3: different indent (6 spaces)
        content = content.replace(
            "      fbq('init', '1271893388238243');\n      fbq('track', 'PageView');",
            "      try { fbq('init', '1271893388238243'); fbq('track', 'PageView'); } catch(e) {}"
        )

        if content != original:
            with open(fp, 'w', encoding='utf-8') as fh:
                fh.write(content)
            print(f'Fixed: {fp}')
            count += 1

print(f'\nTotal fixed: {count}')
if count == 0:
    # Show exact lines from a sample file
    sample = 'index.html'
    with open(sample, 'r', encoding='utf-8') as fh:
        lines = fh.readlines()
    for i, line in enumerate(lines):
        if 'fbq' in line and ('init' in line or 'track' in line):
            print(f'{sample}:{i+1}: {repr(line)}')