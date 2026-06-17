"""
add_images_voyage.py
Ajoute des photos Unsplash (libres de droit) à index.html du template voyage :
  - Hero : photo de fond avion/voyage
  - Cartes destinations : vraies photos par pays
  - Offres spéciales : photos correspondantes
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

UNS = "https://images.unsplash.com/photo-"

PHOTOS = {
    "hero":      UNS + "1436491865332-7a61a109cc05?auto=format&fit=crop&w=1920&q=80",
    "dubai":     UNS + "1512453979798-5ea266f8880c?auto=format&fit=crop&w=800&q=80",
    "istanbul":  UNS + "1541432901042-2d8bd64b4a9b?auto=format&fit=crop&w=800&q=80",
    "mecque":    UNS + "1591178024-4f71b32a3f9a?auto=format&fit=crop&w=800&q=80",
    "paris":     UNS + "1502602898657-3e91760cbb34?auto=format&fit=crop&w=800&q=80",
    "bangkok":   UNS + "1508193638397-1c4234db14d8?auto=format&fit=crop&w=800&q=80",
    "marrakech": UNS + "1539020140153-e479b8c22e70?auto=format&fit=crop&w=800&q=80",
    "caire":     UNS + "1539650116574-75c0f1e23196?auto=format&fit=crop&w=800&q=80",
    "maldives":  UNS + "1514282401047-d79a71a590e8?auto=format&fit=crop&w=800&q=80",
}

with open('index.html', encoding='utf-8') as f:
    c = f.read()

# ── 1. Hero : photo de fond avec le dégradé en overlay semi-transparent ────────
OLD_HERO_BG = (
    'background: linear-gradient(162deg, #FF9D4D 0%, #FB6F5C 26%, #D14B7E 48%, '
    '#6B3F96 72%, #042A52 100%);'
)
NEW_HERO_BG = (
    'background: '
    'linear-gradient(162deg,rgba(255,157,77,.72) 0%,rgba(251,111,92,.72) 26%,'
    'rgba(209,75,126,.72) 48%,rgba(107,63,150,.72) 72%,rgba(4,42,82,.88) 100%),'
    f"url('{PHOTOS['hero']}') center/cover no-repeat;"
)
c = c.replace(OLD_HERO_BG, NEW_HERO_BG)
print("Hero :", "OK" if NEW_HERO_BG in c else "ECHEC")

# ── 2. Ajouter le champ photo dans le tableau destinations ────────────────────
OLD_DESTINATIONS = '''const destinations = [
  { flag:"🇦🇪", em:"🏙️", name:"Dubaï",     dur:"5 jours / 4 nuits", price:690000,  grad:"linear-gradient(135deg,#f6c177,#e8893f)", promo:true },
  { flag:"🇹🇷", em:"🕌", name:"Istanbul",   dur:"6 jours / 5 nuits", price:575000,  grad:"linear-gradient(135deg,#5b8def,#9d6ed6)", promo:false },
  { flag:"🇸🇦", em:"🕋", name:"La Mecque",  dur:"12 jours (Omra)",   price:1150000, grad:"linear-gradient(135deg,#1f8a5b,#0f5c3a)", promo:false },
  { flag:"🇫🇷", em:"🗼", name:"Paris",      dur:"5 jours / 4 nuits", price:820000,  grad:"linear-gradient(135deg,#7b6cd6,#d98bbf)", promo:false },
  { flag:"🇹🇭", em:"🛕", name:"Bangkok",    dur:"7 jours / 6 nuits", price:980000,  grad:"linear-gradient(135deg,#16b89a,#1f9d6b)", promo:true },
  { flag:"🇲🇦", em:"🐫", name:"Marrakech",  dur:"4 jours / 3 nuits", price:410000,  grad:"linear-gradient(135deg,#e06a3b,#c43d2a)", promo:true },
  { flag:"🇪🇬", em:"🏜️", name:"Le Caire",   dur:"6 jours / 5 nuits", price:560000,  grad:"linear-gradient(135deg,#d8a55f,#b9794a)", promo:false },
  { flag:"🇲🇻", em:"🏝️", name:"Maldives",   dur:"7 jours / 6 nuits", price:1450000, grad:"linear-gradient(135deg,#23bfe0,#0a72c4)", promo:false }
];'''

NEW_DESTINATIONS = f'''const destinations = [
  {{ flag:"🇦🇪", em:"🏙️", name:"Dubaï",     dur:"5 jours / 4 nuits", price:690000,  grad:"linear-gradient(135deg,#f6c177,#e8893f)", photo:"{PHOTOS['dubai']}",     promo:true }},
  {{ flag:"🇹🇷", em:"🕌", name:"Istanbul",   dur:"6 jours / 5 nuits", price:575000,  grad:"linear-gradient(135deg,#5b8def,#9d6ed6)", photo:"{PHOTOS['istanbul']}",  promo:false }},
  {{ flag:"🇸🇦", em:"🕋", name:"La Mecque",  dur:"12 jours (Omra)",   price:1150000, grad:"linear-gradient(135deg,#1f8a5b,#0f5c3a)", photo:"{PHOTOS['mecque']}",    promo:false }},
  {{ flag:"🇫🇷", em:"🗼", name:"Paris",      dur:"5 jours / 4 nuits", price:820000,  grad:"linear-gradient(135deg,#7b6cd6,#d98bbf)", photo:"{PHOTOS['paris']}",     promo:false }},
  {{ flag:"🇹🇭", em:"🛕", name:"Bangkok",    dur:"7 jours / 6 nuits", price:980000,  grad:"linear-gradient(135deg,#16b89a,#1f9d6b)", photo:"{PHOTOS['bangkok']}",   promo:true }},
  {{ flag:"🇲🇦", em:"🐫", name:"Marrakech",  dur:"4 jours / 3 nuits", price:410000,  grad:"linear-gradient(135deg,#e06a3b,#c43d2a)", photo:"{PHOTOS['marrakech']}", promo:true }},
  {{ flag:"🇪🇬", em:"🏜️", name:"Le Caire",   dur:"6 jours / 5 nuits", price:560000,  grad:"linear-gradient(135deg,#d8a55f,#b9794a)", photo:"{PHOTOS['caire']}",     promo:false }},
  {{ flag:"🇲🇻", em:"🏝️", name:"Maldives",   dur:"7 jours / 6 nuits", price:1450000, grad:"linear-gradient(135deg,#23bfe0,#0a72c4)", photo:"{PHOTOS['maldives']}",  promo:false }}
];'''

c = c.replace(OLD_DESTINATIONS, NEW_DESTINATIONS)
print("Destinations :", "OK" if "photo:" in c else "ECHEC")

# ── 3. Rendu cartes destinations : utiliser la photo + overlay sombre ─────────
OLD_DEST_RENDER = '    <div class="photo" style="background:${d.grad}">'
NEW_DEST_RENDER = (
    '    <div class="photo" style="background:${d.grad};'
    'background-image:linear-gradient(to bottom,rgba(0,0,0,.08) 0%,rgba(0,0,0,.52) 100%),'
    'url(\'${d.photo}\');background-size:cover;background-position:center">'
)
c = c.replace(OLD_DEST_RENDER, NEW_DEST_RENDER)
print("Rendu dcard :", "OK" if "d.photo" in c else "ECHEC")

# ── 4. Ajouter le champ photo dans le tableau offers ─────────────────────────
OLD_OFFERS = f'''const offers = [
  {{ badge:"best", label:"Meilleure offre", em:"🏙️", top:"linear-gradient(135deg,#f6c177,#e8893f)",
    name:"Escapade Dubaï VIP", dur:"5 jours / 4 nuits", inc:["Vol aller-retour inclus","Hôtel 5★ + petit-déjeuner","Visa &amp; assistance","Excursion désert + dîner"],
    old:890000, now:690000, featured:true }},
  {{ badge:"last", label:"Dernières places", em:"🕋", top:"linear-gradient(135deg,#1f8a5b,#0f5c3a)",
    name:"Omra Confort", dur:"12 jours", inc:["Vol aller-retour inclus","Hôtel proche du Haram","Visa Omra inclus","Transferts + guide"],
    old:1350000, now:1150000, featured:false }},
  {{ badge:"new", label:"Nouveau", em:"🏝️", top:"linear-gradient(135deg,#23bfe0,#0a72c4)",
    name:"Lune de miel Maldives", dur:"7 jours / 6 nuits", inc:["Vol aller-retour inclus","Villa sur pilotis","Visa à l\'arrivée","Dîner privé + spa"],
    old:1690000, now:1450000, featured:false }}
];'''

NEW_OFFERS = f'''const offers = [
  {{ badge:"best", label:"Meilleure offre", em:"🏙️", top:"linear-gradient(135deg,#f6c177,#e8893f)", photo:"{PHOTOS['dubai']}",
    name:"Escapade Dubaï VIP", dur:"5 jours / 4 nuits", inc:["Vol aller-retour inclus","Hôtel 5★ + petit-déjeuner","Visa &amp; assistance","Excursion désert + dîner"],
    old:890000, now:690000, featured:true }},
  {{ badge:"last", label:"Dernières places", em:"🕋", top:"linear-gradient(135deg,#1f8a5b,#0f5c3a)", photo:"{PHOTOS['mecque']}",
    name:"Omra Confort", dur:"12 jours", inc:["Vol aller-retour inclus","Hôtel proche du Haram","Visa Omra inclus","Transferts + guide"],
    old:1350000, now:1150000, featured:false }},
  {{ badge:"new", label:"Nouveau", em:"🏝️", top:"linear-gradient(135deg,#23bfe0,#0a72c4)", photo:"{PHOTOS['maldives']}",
    name:"Lune de miel Maldives", dur:"7 jours / 6 nuits", inc:["Vol aller-retour inclus","Villa sur pilotis","Visa à l\'arrivée","Dîner privé + spa"],
    old:1690000, now:1450000, featured:false }}
];'''

c = c.replace(OLD_OFFERS, NEW_OFFERS)
print("Offres :", "OK" if 'photo:"' + PHOTOS['dubai'] in c else "ECHEC")

# ── 5. Rendu cartes offres : utiliser la photo + overlay ─────────────────────
OLD_OFF_RENDER = '    <div class="top" style="background:${o.top}">'
NEW_OFF_RENDER = (
    '    <div class="top" style="background:${o.top};'
    'background-image:linear-gradient(to bottom,rgba(0,0,0,.12) 0%,rgba(0,0,0,.55) 100%),'
    'url(\'${o.photo}\');background-size:cover;background-position:center">'
)
c = c.replace(OLD_OFF_RENDER, NEW_OFF_RENDER)
print("Rendu ocard :", "OK" if "o.photo" in c else "ECHEC")

# ── 6. CSS : ajuster l'emoji sur la carte offre pour lisibilité ──────────────
# Rendre l'emoji plus visible sur fond photo foncé
OLD_EMOJI_CSS = '.dcard .photo .emoji { font-size: 62px; filter: drop-shadow(0 8px 16px rgba(0,0,0,.25)); transition: transform .35s ease; transform: scale(1); }'
NEW_EMOJI_CSS = '.dcard .photo .emoji { font-size: 62px; filter: drop-shadow(0 8px 20px rgba(0,0,0,.55)); transition: transform .35s ease; transform: scale(1); }'
c = c.replace(OLD_EMOJI_CSS, NEW_EMOJI_CSS)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print(f'\nindex.html mis à jour ({len(c)//1024} Ko)')
