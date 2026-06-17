"""
Fix voyage card rendering — remplacements directs dans le JSON bundlé.
Règle impérative : dans un JSON string, utiliser url('...') avec apostrophes simples,
JAMAIS url(\"...\") avec guillemets doubles (casserait le JSON) ni url(\'...\') avec
backslash-quote (escape invalide en JSON).
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

UNS = "https://images.unsplash.com/photo-"

with open('index.html', encoding='utf-8') as f:
    c = f.read()

# ── Corriger d'abord les \' invalides déjà insérés ───────────────────────────
# (insérés par erreur lors d'un run précédent avec raw strings Python)
c = c.replace(r"url(\'${d.photo}\')", "url('${d.photo}')")
c = c.replace(r"url(\'${o.photo}\')", "url('${o.photo}')")
print("Nettoyage backslash-quote :", "OK" if r"\'" not in c else "encore présent")

# ── 1. Rendu carte destination ────────────────────────────────────────────────
OLD_DCARD = r'<div class=\"photo\" style=\"background:${d.grad}\">'
NEW_DCARD = (
    r'<div class=\"photo\" style=\"background:${d.grad};'
    "background-image:linear-gradient(to bottom,rgba(0,0,0,.08) 0%,rgba(0,0,0,.52) 100%),url('${d.photo}');"
    r'background-size:cover;background-position:center\">'
)
already_done = "d.photo" in c and OLD_DCARD not in c
if not already_done:
    c = c.replace(OLD_DCARD, NEW_DCARD)
print("Rendu dcard :", "OK" if "d.photo" in c else "ECHEC")

# ── 2. Photos dans le tableau offers ─────────────────────────────────────────
offers = [
    ('badge:\\"best\\"', UNS + "1512453979798-5ea266f8880c?auto=format&fit=crop&w=800&q=80"),
    ('badge:\\"last\\"', UNS + "1591178024-4f71b32a3f9a?auto=format&fit=crop&w=800&q=80"),
    ('badge:\\"new\\"',  UNS + "1514282401047-d79a71a590e8?auto=format&fit=crop&w=800&q=80"),
]
for badge_str, photo_url in offers:
    new_badge = badge_str + ', photo:\\"' + photo_url + '\\"'
    already = new_badge in c
    if not already:
        c = c.replace(badge_str, new_badge)
    print(f"Offre {badge_str[:14]} : {'déjà OK' if already else ('OK' if new_badge in c else 'ECHEC')}")

# ── 3. Rendu carte offre ──────────────────────────────────────────────────────
OLD_OCARD = r'<div class=\"top\" style=\"background:${o.top}\">'
NEW_OCARD = (
    r'<div class=\"top\" style=\"background:${o.top};'
    "background-image:linear-gradient(to bottom,rgba(0,0,0,.12) 0%,rgba(0,0,0,.55) 100%),url('${o.photo}');"
    r'background-size:cover;background-position:center\">'
)
already_done_o = "o.photo" in c and OLD_OCARD not in c
if not already_done_o:
    c = c.replace(OLD_OCARD, NEW_OCARD)
print("Rendu ocard :", "OK" if "o.photo" in c else "ECHEC")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print(f"\nindex.html mis à jour ({len(c)//1024} Ko)")
