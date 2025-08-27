from pathlib import Path
import csv, json

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT/'raw'
PROD = ROOT/'products'

def read_csv(p):
    with open(p, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def write_csv(p, rows, fieldnames):
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows: w.writerow(r)

def write(p, text):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')

def write_json(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2), encoding='utf-8')

def cover_svg(title, subtitle):
    return f"""<svg xmlns='http://www.w3.org/2000/svg' width='1400' height='900'>
<rect width='100%' height='100%' fill='#ffffff' />
<rect x='60' y='60' width='1280' height='780' rx='28' ry='28' fill='#f5f5f5' stroke='#ddd'/>
<text x='120' y='240' font-family='Arial' font-size='64' font-weight='700'>{title}</text>
<text x='120' y='320' font-family='Arial' font-size='36'>{subtitle}</text>
<text x='120' y='780' font-family='Arial' font-size='20'>Includes: CSV • TSV • Markdown printable</text>
</svg>"""

PROD.mkdir(exist_ok=True)

# 1) Health: Macro Planner
foods = read_csv(RAW/'usda_foods.csv')
foods_sorted = sorted(foods, key=lambda r: float(r['kcal']))
lane, sku = 'health', 'usda-macro-planner-v1'
out = PROD/lane/sku
out.mkdir(parents=True, exist_ok=True)
write_csv(out/'foods.csv', foods_sorted, ['description','protein','fat','carbs','kcal'])
planner_rows = []
for d in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']:
    for meal in ['Breakfast','Lunch','Dinner']:
        planner_rows.append({'day': d, 'meal': meal, 'item':'', 'kcal':'', 'protein':'', 'fat':'', 'carbs':''})
write_csv(out/'planner_template.csv', planner_rows, list(planner_rows[0].keys()))
write_json(out/'meta.json', {
    'title':'Macro Planner: Foods & Macros (USDA sample)',
    'sku':'H-MACRO-V1','lane':'health',
    'includes':['foods.csv','planner_template.csv','anki.tsv','printable.md','LICENSE.txt'],
    'source':'USDA sample (public domain). Replace with live USDA pulls.',
    'license_note':'Compiled work © YourBrand. Underlying data public domain.'})
write(out/'cover.svg', cover_svg('Macro Planner', 'Foods & Macros (USDA sample)'))
write(out/'README.md', '# Macro Planner\n\nFill `planner_template.csv` using `foods.csv` as reference.')
write(out/'LICENSE.txt', 'Sources: USDA (public domain). Compiled work © YourBrand.')

# 2) Security: NIST SmallBiz
controls = read_csv(RAW/'nist_controls.csv')
lane, sku = 'security', 'nist-smallbiz-checklists-v1'
out = PROD/lane/sku
out.mkdir(parents=True, exist_ok=True)
write_csv(out/'nist_checklist.csv', controls, ['control_id','statement','category'])
vrt = [{'vendor':'','service':'','data_access':'low/med/high','mfa':'yes/no','soc2':'yes/no','last_review':'YYYY-MM-DD','notes':''} for _ in range(5)]
write_csv(out/'vendor_risk_tracker.csv', vrt, list(vrt[0].keys()))
write_json(out/'meta.json', {
    'title':'NIST Small Business Security Checklist + Vendor Tracker',
    'sku':'S-NIST-V1','lane':'security',
    'includes':['nist_checklist.csv','vendor_risk_tracker.csv','printable.md','LICENSE.txt'],
    'source':'NIST-derived small business summary (sample).',
    'license_note':'Maintain required notices. Compiled work © YourBrand.'})
write(out/'cover.svg', cover_svg('NIST Small Biz Security', 'Checklist + Vendor Tracker'))
write(out/'README.md', '# NIST Small Business Security\n\nUse `nist_checklist.csv` then track vendors in `vendor_risk_tracker.csv`.')
write(out/'LICENSE.txt', 'Source: NIST materials (check attribution). Compiled work © YourBrand.')

# 3) Family: Emergency Plan
items = read_csv(RAW/'fema_checklist.csv')
lane, sku = 'family', 'family-emergency-plan-v1'
out = PROD/lane/sku
out.mkdir(parents=True, exist_ok=True)
write_csv(out/'go_bag_checklist.csv', items, ['item','quantity','notes'])
family_plan = [
    {'section':'Contacts','field':'ICE Contact 1','value':''},
    {'section':'Contacts','field':'ICE Contact 2','value':''},
    {'section':'Meeting Point','field':'Neighborhood meeting spot','value':''},
    {'section':'Medical','field':'Allergies/conditions','value':''},
    {'section':'Pets','field':'Vet & microchip info','value':''},
]
write_csv(out/'family_plan_template.csv', family_plan, list(family_plan[0].keys()))
write_json(out/'meta.json', {
    'title':'Family Emergency Plan + Go-Bag Checklist',
    'sku':'F-FEMA-V1','lane':'family',
    'includes':['go_bag_checklist.csv','family_plan_template.csv','printable.md','LICENSE.txt'],
    'source':'FEMA-style checklist (sample).',
    'license_note':'Maintain required notices. Compiled work © YourBrand.'})
write(out/'cover.svg', cover_svg('Family Emergency Plan', '+ Go-Bag Checklist'))
write(out/'README.md', '# Family Emergency Plan\n\nFill `family_plan_template.csv` and pack against `go_bag_checklist.csv`.')
write(out/'LICENSE.txt', 'Source: FEMA-style guidance (check attribution). Compiled work © YourBrand.')

print('build_assets: done.')
