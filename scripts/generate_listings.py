# scripts/generate_listings.py
from pathlib import Path
import json, datetime, html

ROOT = Path(__file__).resolve().parents[1]
PROD = ROOT / "products"
SITE = ROOT / "seo_site"
TPL = SITE / "templates" / "sku_page.html"
SITE.mkdir(exist_ok=True, parents=True)
(SITE / "products").mkdir(exist_ok=True, parents=True)
(SITE / "templates").mkdir(exist_ok=True, parents=True)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang=\"en\">
<head>
<meta charset=\"utf-8\" />
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
<title>{{title}}</title>
<meta name=\"description\" content=\"{{desc}}\" />
</head>
<body>
  <main>
    <h1>{{title}}</h1>
    <p><em>SKU:</em> {{sku}} | <em>Lane:</em> {{lane}}</p>
    <img alt=\"cover\" src=\"../../{{cover_rel}}\" style=\"max-width:640px;display:block;margin:1rem 0;\" />
    <h2>What you get</h2>
    <ul>
      {{includes_list}}
    </ul>
    <h2>How to use</h2>
    <ol>
      <li>Open CSV files in Excel/Google Sheets or import into Notion.</li>
      <li>Import TSV into Anki as Basic flashcards.</li>
      <li>Print the printable markdown to PDF if needed.</li>
    </ol>
    <h2>Sources & License</h2>
    <p>{{source}}</p>
    <p>{{license}}</p>
    <hr />
    <p>(c) {{year}} YourBrand - This is a compiled product built from public resources.</p>
    <p><a href=\"../index.html\">&larr; Back to all products</a></p>
  </main>
</body>
</html>"""

if not TPL.exists():
    TPL.write_text(HTML_TEMPLATE, encoding="utf-8")

# Build listing.md and HTML pages + index
all_pages = []
for meta_path in PROD.rglob("meta.json"):
    sku_dir = meta_path.parent
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    title = meta.get("title", sku_dir.name)
    desc = f"{title} — structured digital asset pack (CSV/TSV/printable)."
    includes = meta.get("includes", [])
    includes_list = "\n      ".join([f"<li>{html.escape(x)}</li>" for x in includes])
    sku = meta.get("sku", sku_dir.name)
    lane = meta.get("lane", sku_dir.parent.name)
    cover_rel = str((sku_dir / "cover.svg").relative_to(ROOT).as_posix())
    year = datetime.datetime.utcnow().year

    # listing.md (for marketplaces)
    listing_md = (
        f"# {title}\n\n"
        f"**What's inside**\n"
        + "".join([f"- {x}\n" for x in includes])
        + "\n**Why it helps**\n"
        "- Structured, editable CSVs and TSV (Anki) for quick onboarding.\n"
        "- Printable quickstart (markdown -> PDF).\n"
        "- Built from public-domain/permissive sources with clear licensing notes.\n\n"
        "**How to use**\n"
        "1) Open CSVs in Sheets/Excel/Notion.\n"
        "2) Import TSV into Anki.\n"
        "3) Print the markdown if you need a hard copy.\n\n"
        "**Sources & License**\n"
        f"- {meta.get('source','')}\n"
        f"- {meta.get('license_note','')}\n"
    )
    (sku_dir/"listing.md").write_text(listing_md, encoding="utf-8")

    # product page HTML
    html_tpl = TPL.read_text(encoding="utf-8")
    page_html = (html_tpl
                 .replace("{{title}}", html.escape(title))
                 .replace("{{desc}}", html.escape(desc))
                 .replace("{{sku}}", html.escape(sku))
                 .replace("{{lane}}", html.escape(lane))
                 .replace("{{includes_list}}", includes_list)
                 .replace("{{source}}", html.escape(meta.get("source","")))
                 .replace("{{license}}", html.escape(meta.get("license_note","")))
                 .replace("{{cover_rel}}", cover_rel)
                 .replace("{{year}}", str(year))
                 )
    rel = f"products/{sku}.html"
    (SITE/rel).write_text(page_html, encoding="utf-8")
    all_pages.append(rel)

# index.html (simple)
index_links = "\n".join([f'<li><a href="{p}">{p.split("/")[-1].replace(".html","")}</a></li>' for p in sorted(all_pages)])
index_html = f"""<!DOCTYPE html>
<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
<title>SKU Factory Index</title></head>
<body>
<main>
  <h1>SKU Factory — Products</h1>
  <ul>
    {index_links}
  </ul>
</main>
</body></html>"""
(SITE/"index.html").write_text(index_html, encoding="utf-8")

# sitemap.xml
base = "https://YOUR_USERNAME.github.io/YOUR_REPO"
urls = "\n".join([f"  <url><loc>{base}/{p}</loc></url>" for p in sorted(all_pages)])
sitemap = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">
{urls}
</urlset>
"""
(SITE/"sitemap.xml").write_text(sitemap, encoding="utf-8")

print("generate_listings: site and listings built.")
