"""Verify internal links resolve and every page has the shared scaffolding."""
import os
import re

SEP = os.sep


def norm(path):
    return os.path.normpath(path).replace(SEP, '/').lstrip('./')


def main():
    pages = sorted(p for p in os.listdir('.') if p.endswith('.html'))
    assets = set()
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__')]
        for f in files:
            assets.add(norm(os.path.join(root, f)))

    print('PAGES:', pages)
    print()

    problems = []
    required = [
        ('id="site-nav"', 'nav mount'),
        ('id="site-footer"', 'footer mount'),
        ('assets/site.js', 'site.js'),
        ('assets/style.css', 'style.css'),
        ('id="main"', 'main landmark'),
        ('<title>', 'title'),
        ('name="description"', 'meta description'),
    ]

    for page in pages:
        html = open(page, encoding='utf-8').read()
        for ref in re.findall(r'(?:href|src)="([^"#][^"]*)"', html):
            if ref.startswith(('http', '//', 'mailto:', 'data:')):
                continue
            if norm(ref) not in assets:
                problems.append(f'  {page}: broken link -> {ref}')
        for needle, label in required:
            if needle not in html:
                problems.append(f'  {page}: MISSING {label}')

    print('LINK / STRUCTURE CHECK')
    print('\n'.join(problems) if problems
          else '  OK - all internal links resolve, all pages have nav/footer/main/title/meta')
    print()

    nav = open('assets/site.js', encoding='utf-8').read()
    targets = re.findall(r"href: '([^']+)'", nav)
    missing = [t for t in targets if t not in assets]
    print('NAV TARGETS:', targets)
    print('  missing:', missing if missing else 'none')

    return 1 if problems or missing else 0


if __name__ == '__main__':
    raise SystemExit(main())
