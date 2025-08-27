from pathlib import Path
import json as _json

ROOT = Path(__file__).resolve().parents[1]
for meta in ROOT.rglob('meta.json'):
    meta_obj = _json.loads(meta.read_text(encoding='utf-8'))
    sku_dir = meta.parent
    title = meta_obj.get('title', sku_dir.name)
    includes = meta_obj.get('includes', [])
    printable = f"""# {title}

This printable summary accompanies the digital files in this pack.

## What's inside
{chr(10).join(['- ' + x for x in includes])}

## How to use
1. Open CSV files in Excel/Google Sheets or import into Notion.
2. Import TSV into Anki (Basic note type).
3. Print this page to PDF if you want a hard copy.

## Sources & License
- {meta_obj.get('source','')}
- {meta_obj.get('license_note','')}
"""
    (sku_dir/'printable.md').write_text(printable, encoding='utf-8')
print('make_pdfs: wrote printable markdown files.')
