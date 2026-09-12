from pathlib import Path


STATIC = Path("/app/static")
INDEX = STATIC / "index.html"
APP_JS = STATIC / "app.js"
BASE_PATH = "/drone-detector/"

index = INDEX.read_text(encoding="utf-8")
required_index_tokens = (
    '<title>Drone Audio Demo</title>',
    'href="/styles.css"',
    'src="/app.js"',
)
for token in required_index_tokens:
    if token not in index:
        raise RuntimeError(f"expected frontend token is missing: {token}")

index = index.replace(
    '<title>Drone Audio Demo</title>',
    f'<base href="{BASE_PATH}"><title>Drone Audio Demo</title>',
    1,
)
index = index.replace('href="/styles.css"', 'href="styles.css"', 1)
index = index.replace('src="/app.js"', 'src="app.js"', 1)
INDEX.write_text(index, encoding="utf-8")

javascript = APP_JS.read_text(encoding="utf-8")
if "'/api/" not in javascript:
    raise RuntimeError("expected absolute API URLs are missing from app.js")
javascript = javascript.replace("'/api/", "'api/")
if "'/api/" in javascript:
    raise RuntimeError("absolute API URLs remain in app.js")
APP_JS.write_text(javascript, encoding="utf-8")
