from pathlib import Path
import shutil, os

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT/'dist'
DIST.mkdir(exist_ok=True)

def zipdir(src: Path, zip_path: Path):
    from zipfile import ZipFile, ZIP_DEFLATED
    with ZipFile(zip_path, 'w', ZIP_DEFLATED) as z:
        for p in src.rglob('*'):
            if p.is_file():
                # avoid including any generated HTML outside product
                arc = p.relative_to(src.parent)
                z.write(p, arcname=str(arc))

for sku_dir in ROOT.joinpath('products').rglob('*'):
    if sku_dir.is_dir() and (sku_dir/'meta.json').exists():
        name = sku_dir.name
        lane = sku_dir.parent.name
        zip_name = f"{lane}-{name}.zip"
        # zip into /dist
        zipdir(sku_dir, DIST/zip_name)
        # also drop a zip next to the SKU dir for convenience
        zipdir(sku_dir, sku_dir/'product.zip')
        print('packaged', zip_name)
