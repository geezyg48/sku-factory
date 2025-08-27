from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PROD = ROOT/'products'
samples = {
    'health/usda-macro-planner-v1/anki.tsv': [
        ('What is a macro?', 'Protein, fat, and carbohydrate.'),
        ('Why track protein?', 'Supports muscle repair and satiety.'),
        ('What is kcal?', 'A unit of energy (kilocalorie).'),
    ],
    'security/nist-smallbiz-checklists-v1/anki.tsv': [
        ('What is MFA?', 'Multi-factor authentication (two or more factors).'),
        ('Why vendor reviews?', 'Manage third-party risk.'),
    ],
    'family/family-emergency-plan-v1/anki.tsv': [
        ('What is an ICE contact?', 'In-Case-of-Emergency contact.'),
        ('Why a meeting point?', 'Reunification if comms fail.'),
    ],
}
for rel, cards in samples.items():
    p = PROD/rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('\n'.join(['\t'.join(x) for x in cards]), encoding='utf-8')
print('make_anki: wrote TSV files.')
