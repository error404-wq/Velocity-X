"""
Render every page in a headless browser and capture screenshots.

Also checks the things a link-checker cannot: that the shared nav/footer actually
mount, that nothing overflows horizontally, and that no console errors fire.
"""
import http.server
import socketserver
import threading

from playwright.sync_api import sync_playwright

PORT = 8042
PAGES = ['index.html', 'simulator.html', 'validation.html',
         'docs.html', 'research.html', 'about.html']


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve():
    with Server(('', PORT), Handler) as httpd:
        httpd.serve_forever()


def main():
    threading.Thread(target=serve, daemon=True).start()
    import time; time.sleep(1.0)

    failures = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for page_name in PAGES:
            page = browser.new_page(viewport={'width': 1280, 'height': 900})
            errors = []
            page.on('console', lambda m: errors.append(m.text)
                    if m.type == 'error' else None)
            page.on('pageerror', lambda e: errors.append(str(e)))

            page.goto(f'http://localhost:{PORT}/{page_name}', wait_until='domcontentloaded')
            page.wait_for_timeout(1200)

            nav = page.locator('.nav-inner').count()
            foot = page.locator('.footer').count()
            overflow = page.evaluate(
                'Math.max(0, document.documentElement.scrollWidth - window.innerWidth)')

            # PyScript failing to reach the network is expected offline; ignore those.
            real_errors = [e for e in errors
                           if 'pyscript' not in e.lower() and 'pyodide' not in e.lower()
                           and 'favicon' not in e.lower()]

            status = 'ok'
            if not nav:
                status = 'NAV MISSING'
            elif not foot:
                status = 'FOOTER MISSING'
            elif overflow > 2:
                status = f'H-OVERFLOW {overflow}px'
            elif real_errors:
                status = f'JS ERROR: {real_errors[0][:70]}'
            if status != 'ok':
                failures.append(f'{page_name}: {status}')

            page.screenshot(path=f'screenshots/{page_name.replace(".html", "")}.png',
                            full_page=True)
            print(f'  {page_name:20s} nav={bool(nav)} footer={bool(foot)} '
                  f'overflow={overflow}px  {status}')
            page.close()

        # mobile pass on the landing page
        page = browser.new_page(viewport={'width': 390, 'height': 844})
        page.goto(f'http://localhost:{PORT}/index.html', wait_until='domcontentloaded')
        page.wait_for_timeout(600)
        mob_overflow = page.evaluate(
            'Math.max(0, document.documentElement.scrollWidth - window.innerWidth)')
        page.screenshot(path='screenshots/index-mobile.png', full_page=True)
        print(f'  {"index.html (390px)":20s} overflow={mob_overflow}px')
        if mob_overflow > 2:
            failures.append(f'index.html mobile: H-OVERFLOW {mob_overflow}px')
        page.close()
        browser.close()

    print()
    if failures:
        print('FAILURES:')
        for f in failures:
            print('  ' + f)
        return 1
    print('All pages render cleanly.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
