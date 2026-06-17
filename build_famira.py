"""
build_famira.py — Remplacements directs UNIQUEMENT, pas de json.loads/dumps.
Opère sur le texte brut du fichier pour ne jamais altérer l'encodage du bundle.
"""
import re, json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    c = f.read()

UNS = "https://images.unsplash.com/photo-"

# ── 1. Titre HTML (hors bundle) ───────────────────────────────────────────────
c = c.replace('<title>Sahel Voyages', '<title>FAMIRA VOYAGES &amp; SERVICES')

# ── 2. Nom agence partout (dans le JSON le nom n'a pas de " donc remplacement direct)
c = c.replace('Sahel Voyages', 'FAMIRA VOYAGES & SERVICES')
print(f"FAMIRA : {c.count('FAMIRA VOYAGES')}x | Sahel restant : {c.count('Sahel Voyages')}x")

# ── 3. Hero : remplacement direct du gradient (pas de " dans la valeur CSS) ──
OLD_HERO = ('background: linear-gradient(162deg, #FF9D4D 0%, #FB6F5C 26%, '
            '#D14B7E 48%, #6B3F96 72%, #042A52 100%);')
NEW_HERO = (f"background: linear-gradient(162deg,rgba(255,157,77,.72) 0%,"
            f"rgba(251,111,92,.72) 26%,rgba(209,75,126,.72) 48%,"
            f"rgba(107,63,150,.72) 72%,rgba(4,42,82,.88) 100%),"
            f"url('{UNS}1436491865332-7a61a109cc05?auto=format&fit=crop&w=1920&q=80')"
            f" center/cover no-repeat;")
n = c.count(OLD_HERO); c = c.replace(OLD_HERO, NEW_HERO)
print(f"Hero      : {n}→{'OK' if NEW_HERO in c else 'ECHEC'}")

# ── 4. Destinations : ajouter photo après grad (le JSON encode " en \") ───────
# Dans le fichier brut : grad:\"linear-gradient(...)\", promo:X
# On ajoute :           grad:\"linear-gradient(...)\", photo:\"url\", promo:X
dests = [
    ('linear-gradient(135deg,#f6c177,#e8893f)', 'true',
     UNS+'1512453979798-5ea266f8880c?auto=format&fit=crop&w=800&q=80'),
    ('linear-gradient(135deg,#5b8def,#9d6ed6)', 'false',
     UNS+'1541432901042-2d8bd64b4a9b?auto=format&fit=crop&w=800&q=80'),
    ('linear-gradient(135deg,#1f8a5b,#0f5c3a)', 'false',
     UNS+'1591178024-4f71b32a3f9a?auto=format&fit=crop&w=800&q=80'),
    ('linear-gradient(135deg,#7b6cd6,#d98bbf)', 'false',
     UNS+'1502602898657-3e91760cbb34?auto=format&fit=crop&w=800&q=80'),
    ('linear-gradient(135deg,#16b89a,#1f9d6b)', 'true',
     UNS+'1508193638397-1c4234db14d8?auto=format&fit=crop&w=800&q=80'),
    ('linear-gradient(135deg,#e06a3b,#c43d2a)', 'true',
     UNS+'1539020140153-e479b8c22e70?auto=format&fit=crop&w=800&q=80'),
    ('linear-gradient(135deg,#d8a55f,#b9794a)', 'false',
     UNS+'1539650116574-75c0f1e23196?auto=format&fit=crop&w=800&q=80'),
    ('linear-gradient(135deg,#23bfe0,#0a72c4)', 'false',
     UNS+'1514282401047-d79a71a590e8?auto=format&fit=crop&w=800&q=80'),
]
for grad, promo, photo in dests:
    old = f'grad:\\"{grad}\\", promo:{promo}'
    new = f'grad:\\"{grad}\\", photo:\\"{photo}\\", promo:{promo}'
    n = c.count(old); c = c.replace(old, new)
    print(f"  dest {grad[:30]}: {n}→{'OK' if n else 'ECHEC'}")

# ── 5. Rendu carte destination (dans JSON : \" pour les guillemets HTML) ───────
OLD_DC = r'<div class=\"photo\" style=\"background:${d.grad}\">'
NEW_DC = (r'<div class=\"photo\" style=\"background:${d.grad};'
          f"background-image:linear-gradient(to bottom,rgba(0,0,0,.08) 0%,rgba(0,0,0,.52) 100%),url('${{d.photo}}');"
          r'background-size:cover;background-position:center\">')
n = c.count(OLD_DC); c = c.replace(OLD_DC, NEW_DC)
print(f"Rendu dest: {n}→{'OK' if 'd.photo' in c else 'ECHEC'}")

# ── 6. Offres : ajouter photo après badge ─────────────────────────────────────
offers = [
    ('best', UNS+'1512453979798-5ea266f8880c?auto=format&fit=crop&w=800&q=80'),
    ('last', UNS+'1591178024-4f71b32a3f9a?auto=format&fit=crop&w=800&q=80'),
    ('new',  UNS+'1514282401047-d79a71a590e8?auto=format&fit=crop&w=800&q=80'),
]
for badge, photo in offers:
    old = f'badge:\\"{badge}\\"'
    new = f'badge:\\"{badge}\\", photo:\\"{photo}\\"'
    n = c.count(old); c = c.replace(old, new)
    print(f"  offre {badge}: {n}→{'OK' if n else 'ECHEC'}")

# ── 7. Rendu carte offre ───────────────────────────────────────────────────────
OLD_OC = r'<div class=\"top\" style=\"background:${o.top}\">'
NEW_OC = (r'<div class=\"top\" style=\"background:${o.top};'
          f"background-image:linear-gradient(to bottom,rgba(0,0,0,.12) 0%,rgba(0,0,0,.55) 100%),url('${{o.photo}}');"
          r'background-size:cover;background-position:center\">')
n = c.count(OLD_OC); c = c.replace(OLD_OC, NEW_OC)
print(f"Rendu offre: {n}→{'OK' if 'o.photo' in c else 'ECHEC'}")

# ── Validation finale du JSON ─────────────────────────────────────────────────
m = re.search(r'<script type="__bundler/template">([\s\S]*?)</script>', c)
try:
    json.loads(m.group(1).strip())
    print("\nJSON final valide : OK")
except json.JSONDecodeError as e:
    print(f"\nERREUR JSON : {e}")
    pos = e.pos; raw = m.group(1)
    print(repr(raw[max(0,pos-60):pos+60]))
    sys.exit(1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print(f"index.html écrit : {len(c)//1024} Ko")
