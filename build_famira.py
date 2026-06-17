"""
build_famira.py — Construction propre du site FAMIRA VOYAGES & SERVICES.
Règles strictes pour ne pas casser le JSON bundlé :
  - Toujours url('...') avec apostrophes simples dans le JSON
  - Jamais url("...") guillemets doubles (cassent le JSON)
  - Jamais \\'  (escape invalide en JSON)
  - Vérification JSON finale avant écriture
"""
import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    content = f.read()

# ── 1. Titre HTML (hors bundle) ───────────────────────────────────────────────
content = content.replace(
    '<title>Sahel Voyages',
    '<title>FAMIRA VOYAGES &amp; SERVICES'
)

# ── 2. Tout Sahel Voyages → FAMIRA VOYAGES & SERVICES ────────────────────────
content = content.replace('Sahel Voyages', 'FAMIRA VOYAGES & SERVICES')

print(f"FAMIRA VOYAGES : {content.count('FAMIRA VOYAGES')}x")
print(f"Sahel Voyages restant : {content.count('Sahel Voyages')}x")

# ── Extraire le JSON bundlé pour les modifications à l'intérieur ──────────────
OPEN  = '<script type="__bundler/template">'
CLOSE = '</script>'

start = content.find(OPEN) + len(OPEN)
# Fin réelle = le dernier </script> du fichier
end   = content.rfind(CLOSE)
json_raw = content[start:end]

# Décoder pour vérifier que le template est sain
html = json.loads(json_raw.strip())
print(f"JSON valide avant modifs : {len(html):,} chars")

UNS = "https://images.unsplash.com/photo-"

# ── 3. Hero : photo de fond (apostrophes simples — obligatoire dans JSON) ─────
OLD_HERO = (
    'background: linear-gradient(162deg, #FF9D4D 0%, #FB6F5C 26%, #D14B7E 48%, '
    '#6B3F96 72%, #042A52 100%);'
)
NEW_HERO = (
    "background: "
    "linear-gradient(162deg,rgba(255,157,77,.72) 0%,rgba(251,111,92,.72) 26%,"
    "rgba(209,75,126,.72) 48%,rgba(107,63,150,.72) 72%,rgba(4,42,82,.88) 100%),"
    f"url('{UNS}1436491865332-7a61a109cc05?auto=format&fit=crop&w=1920&q=80')"
    " center/cover no-repeat;"
)
html = html.replace(OLD_HERO, NEW_HERO)
print("Hero photo      :", "OK" if NEW_HERO in html else "ECHEC")

# ── 4. Destinations : ajouter champ photo dans le tableau JS ─────────────────
dest_photos = {
    'Dubaï':      UNS + "1512453979798-5ea266f8880c?auto=format&fit=crop&w=800&q=80",
    'Istanbul':   UNS + "1541432901042-2d8bd64b4a9b?auto=format&fit=crop&w=800&q=80",
    'La Mecque':  UNS + "1591178024-4f71b32a3f9a?auto=format&fit=crop&w=800&q=80",
    'Paris':      UNS + "1502602898657-3e91760cbb34?auto=format&fit=crop&w=800&q=80",
    'Bangkok':    UNS + "1508193638397-1c4234db14d8?auto=format&fit=crop&w=800&q=80",
    'Marrakech':  UNS + "1539020140153-e479b8c22e70?auto=format&fit=crop&w=800&q=80",
    'Le Caire':   UNS + "1539650116574-75c0f1e23196?auto=format&fit=crop&w=800&q=80",
    'Maldives':   UNS + "1514282401047-d79a71a590e8?auto=format&fit=crop&w=800&q=80",
}
dest_grads = {
    'Dubaï':     'linear-gradient(135deg,#f6c177,#e8893f)',
    'Istanbul':  'linear-gradient(135deg,#5b8def,#9d6ed6)',
    'La Mecque': 'linear-gradient(135deg,#1f8a5b,#0f5c3a)',
    'Paris':     'linear-gradient(135deg,#7b6cd6,#d98bbf)',
    'Bangkok':   'linear-gradient(135deg,#16b89a,#1f9d6b)',
    'Marrakech': 'linear-gradient(135deg,#e06a3b,#c43d2a)',
    'Le Caire':  'linear-gradient(135deg,#d8a55f,#b9794a)',
    'Maldives':  'linear-gradient(135deg,#23bfe0,#0a72c4)',
}
dest_promos = {'Dubaï':'true','Bangkok':'true','Marrakech':'true'}

for name, photo in dest_photos.items():
    promo = dest_promos.get(name, 'false')
    grad  = dest_grads[name]
    old = f'grad:"{grad}", promo:{promo}'
    new = f'grad:"{grad}", photo:"{photo}", promo:{promo}'
    found = old in html
    html = html.replace(old, new)
    print(f"  dest {name:<12}: {'OK' if found else 'ECHEC'}")

# ── 5. Rendu cartes destinations (apostrophes simples) ────────────────────────
OLD_DCARD = '    <div class="photo" style="background:${d.grad}">'
NEW_DCARD = (
    '    <div class="photo" style="background:${d.grad};'
    "background-image:linear-gradient(to bottom,rgba(0,0,0,.08) 0%,rgba(0,0,0,.52) 100%),url('${d.photo}');"
    'background-size:cover;background-position:center">'
)
html = html.replace(OLD_DCARD, NEW_DCARD)
print("Rendu dest      :", "OK" if "d.photo" in html else "ECHEC")

# ── 6. Offres spéciales : ajouter champ photo ────────────────────────────────
offer_photos = {
    'best': UNS + "1512453979798-5ea266f8880c?auto=format&fit=crop&w=800&q=80",
    'last': UNS + "1591178024-4f71b32a3f9a?auto=format&fit=crop&w=800&q=80",
    'new':  UNS + "1514282401047-d79a71a590e8?auto=format&fit=crop&w=800&q=80",
}
for badge, photo in offer_photos.items():
    old = f'badge:"{badge}"'
    new = f'badge:"{badge}", photo:"{photo}"'
    found = old in html
    html = html.replace(old, new)
    print(f"  offre {badge:<6}: {'OK' if found else 'ECHEC'}")

# ── 7. Rendu cartes offres (apostrophes simples) ──────────────────────────────
OLD_OCARD = '    <div class="top" style="background:${o.top}">'
NEW_OCARD = (
    '    <div class="top" style="background:${o.top};'
    "background-image:linear-gradient(to bottom,rgba(0,0,0,.12) 0%,rgba(0,0,0,.55) 100%),url('${o.photo}');"
    'background-size:cover;background-position:center">'
)
html = html.replace(OLD_OCARD, NEW_OCARD)
print("Rendu offres    :", "OK" if "o.photo" in html else "ECHEC")

# ── Vérifications de sécurité ─────────────────────────────────────────────────
assert 'url("' + UNS not in html, "ERREUR : url() avec guillemets doubles trouvé !"
assert "\\'}" not in html and "\\'" not in html, "ERREUR : backslash-apostrophe trouvé !"
print("\nVérifications sécurité : OK")

# ── Re-encoder et ré-injecter dans le fichier ─────────────────────────────────
# json.dumps produit un JSON valide ; on échappe </script> → <\/script>
# pour que le parser HTML ne ferme pas le tag prématurément.
new_json = json.dumps(html, ensure_ascii=False)
new_json = new_json.replace('</', '<\\/')   # </tag> → <\/tag>  (standard bundler trick)

# Validation finale
try:
    json.loads(new_json)
    print("JSON final valide : OK")
except json.JSONDecodeError as e:
    print(f"ERREUR JSON final : {e}")
    sys.exit(1)

new_content = content[:start] + '\n' + new_json + '\n' + content[end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"\nindex.html écrit : {len(new_content)//1024} Ko")
