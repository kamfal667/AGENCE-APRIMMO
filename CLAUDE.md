# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A multi-template static website system for prospects in Abidjan (Côte d'Ivoire). Each prospect gets their own Git branch and a separate Vercel deployment. The `main` branch holds the master templates — never modify it directly.

## Templates disponibles

| Fichier | Secteur | Nom par défaut |
|---|---|---|
| `templates/template-immo.html` | Immobilier | AGENCE IMMOBILIERE LUMIERE |
| `templates/template-archi.html` | Architecture & Design | Confort Seven |
| `templates/template-juridique.html` | Cabinet juridique / Avocat | Cabinet CJ2A — Me ADOU et Associés |
| `templates/template-compta.html` | Cabinet comptable / Expert-comptable | [Nom du Cabinet] |
| `templates/template-voyage.html` | Agence de voyage | [Nom de l'Agence] |

## Branch & deploy workflow

One branch per prospect. Branch names: lowercase, no accents, hyphens only (e.g. `sci-transville`).

```bash
git checkout main && git pull origin main
git checkout -b [nom-du-prospect]

# Copier le bon template en index.html
cp templates/template-immo.html index.html      # pour un prospect immobilier
# OU
cp templates/template-archi.html index.html     # pour un prospect architecture
# OU
cp templates/template-juridique.html index.html # pour un cabinet juridique / avocat
# OU
cp templates/template-compta.html index.html    # pour un cabinet comptable
# OU
cp templates/template-voyage.html index.html   # pour une agence de voyage

# Modifier index.html (voir points de personnalisation ci-dessous)
git add index.html
git commit -m "feat: version [nom-du-prospect]"
git push origin [nom-du-prospect]

rm -rf .vercel   # OBLIGATOIRE avant chaque nouveau prospect
npx vercel --yes --name [nom-du-prospect]
```

## Erreurs connues et correctifs

**Problème `.vercel` :** Sans `rm -rf .vercel`, Vercel redéploie sur le projet précédent au lieu d'en créer un nouveau. Toujours supprimer ce dossier avant de déployer un nouveau prospect.

**`vercel` introuvable en bash :** Utiliser `npx vercel` — `vercel` installé globalement n'est pas dans le PATH bash.

**`--name` déprécié :** Le flag fonctionne encore malgré l'avertissement. Ne pas le supprimer — sans lui, le nom du dossier ("prospection site immo" avec espaces) provoque une erreur 400.

**Remplacement archi en deux passes :** Le template archi contient deux formes du nom. Remplacer d'abord la forme longue, puis la courte :
1. `Confort Seven Architecture et Design` → `[NOM COMPLET]`
2. `Confort Seven` → `[NOM COURT]`

## Points de personnalisation — template-immo.html

| Quoi | Comment trouver |
|---|---|
| Nom de l'agence | Remplacement global (~14 occurrences : title, meta, og:title, og:site_name, header, footer…) |
| Slogan | Attribut `data-slogan=""` (lignes ~535 et ~874) |
| Numéro WhatsApp | `const WA_NUMBER='225XXXXXXXXXX'` (ligne ~1124) + liens `wa.me/225XXXXXXXXXX` |
| Téléphone affiché | `<a href="tel:">[NUMÉRO]</a>` (ligne ~898) |
| Email | `<a href="mailto:">[EMAIL]</a>` (ligne ~899) |
| Adresse | `[ADRESSE], Abidjan` (lignes ~828, ~832, ~900) |
| Couleur principale | `--navy:#1B2A4A` dans `:root` (ligne ~20) |
| Couleur accent (or) | `--gold:#C8A951` dans `:root` (ligne ~22) |

## Points de personnalisation — template-archi.html

| Quoi | Comment trouver |
|---|---|
| Nom du cabinet (long) | `Confort Seven Architecture et Design` — remplacer en premier (~5 occurrences) |
| Nom du cabinet (court) | `Confort Seven` — remplacer en second (~4 occurrences : title, nav-logo, footer) |
| Numéro WhatsApp | `const WA_NUMBER = '225XXXXXXXXXX'` (ligne ~1384) + liens `wa.me/225XXXXXXXXXX` |
| Téléphone affiché | `+225 07 00 00 00 00` (lignes ~1300 et ~1356) |
| Email | `contact@archetypafrica.com` (lignes ~1309 et ~1357) |
| Adresse | `Cocody Danga, Abidjan` (lignes ~1291, ~1358) |
| Couleur accent (cuivre) | `--cuivre:#B87333` dans `:root` (ligne ~19) |

## Points de personnalisation — template-juridique.html

**Identité — remplacements texte (~4 occurrences chacun) :**

| Quoi | Valeur à remplacer |
|---|---|
| Sigle court | `CJ2A` (title, hero, footer) |
| Nom complet | `Cabinet CJ2A — Me ADOU et Associés` (title, about, footer) |
| Nom nav/logo | `ADOU et Associés` (lignes ~352 et ~560) |
| Nom affiché avocat | `Maître Adou` (ligne ~397, hero crest) |
| Mention barreau | `Cabinet inscrit au Barreau de Côte d'Ivoire` (footer) |

**Contact — bloc CONFIG JS centralisé (ligne ~591) :**

```js
var CONFIG = {
  whatsapp: "225XXXXXXXXXX",          // numéro WhatsApp sans +
  telephone: "+225 XX XX XX XX XX",
  email: "contact@cj2a-avocats.ci",
  adresse: "Cocody, Abidjan — Côte d'Ivoire",
  messageWhatsApp: "..."
};
```

Un seul bloc à modifier — le JS propage les valeurs partout automatiquement.

**Stats (lignes ~407-410) :** `+15` ans · `+500` dossiers · `+200` clients · `95%` satisfaction

**Couleurs :**

| Variable | Valeur |
|---|---|
| Couleur principale | `--green: #1F5C49` dans `:root` (ligne ~149) |
| Accent or | `--gold: #9B8A4E` dans `:root` (ligne ~153) |

## Points de personnalisation — template-compta.html

**Système de props centralisé** — toutes les valeurs sont dans le bloc `data-props` (ligne ~824 du fichier bundlé). Un seul endroit à modifier, le JS propage partout automatiquement.

| Prop | Valeur par défaut | Quoi changer |
|---|---|---|
| `cabinetName` | `[Nom du Cabinet]` | Nom complet du cabinet (~5 occurrences : title, og, nav, about, footer) |
| `expertName` | `[Expert-Comptable]` | Nom du directeur / expert-comptable (section À propos) |
| `phone` | `+225 07 00 00 00 00` | Téléphone affiché (section contact + footer) |
| `email` | `contact@votrecabinet.ci` | Email de contact |
| `whatsapp` | `2250700000000` | Numéro WhatsApp sans `+` (génère le lien `wa.me/…`) |

**Méthode de modification :** rechercher et remplacer directement dans le HTML bundlé les valeurs par défaut :
- `[Nom du Cabinet]` → nom du prospect
- `[Expert-Comptable]` → nom de l'expert
- `+225 07 00 00 00 00` → téléphone réel
- `contact@votrecabinet.ci` → email réel
- `2250700000000` → numéro WhatsApp réel

**Stats codées en dur** (lignes ~609–622 du template extrait) :

| Stat | Valeur | Label |
|---|---|---|
| `data-count="15"` | `+15` | ans d'expérience |
| `data-count="200"` | `+200` | entreprises accompagnées |
| `data-count="1200"` | `+1 200` | déclarations traitées / an |
| `data-count="98"` | `98%` | de clients satisfaits |

**Couleurs (inline dans le HTML, pas de variables CSS) :**

| Rôle | Couleur |
|---|---|
| Bleu marine (fond hero, titres) | `#1B3A6B` |
| Vert (CTA, accent) | `#1A7A4A` |
| Or (stats, détails) | `#C8A951` |

## Points de personnalisation — template-voyage.html

**Bloc CONFIG JS centralisé (ligne ~1074 du template) :**

```js
const AGENCE = {
  nom: "[Nom de l'Agence]",
  whatsapp: "225XXXXXXXXXX",     // numéro WhatsApp sans + ni espaces
  tel: "+225 XX XX XX XX XX",
  email: "contact@votreagence.ci",
  adresse: "Abidjan, Côte d'Ivoire"
};
```

Un seul bloc à modifier — le JS propage `nom`, `adresse`, liens WhatsApp et contact partout automatiquement.

**Couleurs (variables CSS dans `:root`) :**

| Variable | Valeur | Rôle |
|---|---|---|
| `--ocean` | `#0077B6` | Couleur principale (bleu océan) |
| `--orange` | `#FF8C42` | CTA et boutons d'action |
| `--gold` | `#FFB627` | Accents et détails |
| `--navy` | `#023E73` | Fond hero, nav scrollée |

**Stats codées en dur (ligne ~1135) :**

| Prop `n` | Affichage | Label |
|---|---|---|
| `5000` | `+5 000` | Voyageurs satisfaits |
| `50` | `+50` | Destinations couvertes |
| `8` | `+8` | Ans d'expérience |
| `24` | `24h/24` | Assistance 7j/7 |

**Destinations (tableau `destinations` ligne ~1097) :** 8 destinations par défaut (Dubaï, Istanbul, La Mecque, Paris, Bangkok, Marrakech, Le Caire, Maldives) avec prix en FCFA. Modifier directement dans le JS.

**Offres spéciales (tableau `offers` ligne ~1123) :** 3 offres mises en avant. Modifier prix `old`/`now` et contenu `inc[]`.

## Prospects déployés

| Branche | URL Vercel | Template |
|---|---|---|
| `sci-transville` | https://sci-transville.vercel.app | immo |
| `immo-doks` | https://immo-doks.vercel.app | immo |
| `lassistance-immobilier` | https://lassistance-immobilier.vercel.app | immo |
| `a-plus-a-architecture-adou` | https://a-plus-a-architecture-adou.vercel.app | archi |
| `regis-immobilier` | https://regis-immobilier.vercel.app | immo |
| `king-immobilier` | https://king-immobilier.vercel.app | immo |
| `r2i-immobilier` | https://r2i-immobilier.vercel.app | immo |
| `source-immobilier` | https://source-immobilier.vercel.app | immo |
| `archetyp-africa` | https://archetyp-africa.vercel.app | archi |
| `cj2a-adou` | https://cj2a-adou-seven.vercel.app | juridique |
| `dso-architect` | https://dso-architect.vercel.app | archi |
| `prest-company` | https://prest-company.vercel.app | immo |
| `homestec` | https://homestec.vercel.app | immo |
| `dna-architects` | https://dna-architects-three.vercel.app | archi |
| `aca-architectes` | https://aca-architectes.vercel.app | archi |
| `success-agence` | https://success-agence.vercel.app | immo |
| `generale-ivoire` | https://generale-ivoire.vercel.app | immo |
| `dreams-immobilier` | https://dreams-immobilier.vercel.app | immo |
| `adou-architecture` | https://adou-architecture.vercel.app | archi (portfolio complet) |
| `solex-sas` | https://solex-sas.vercel.app | compta |
| `ascg-international` | https://ascg-international.vercel.app | compta |
| `caliel-consulting` | https://caliel-consulting.vercel.app | compta |
| `soumko-voyage` | https://soumko-voyage.vercel.app | voyage |
| `el-bezri-sacha` | https://el-bezri-sacha.vercel.app | archi |

## Vercel config

`vercel.json` rewrites all routes to `index.html` (single-page statique, pas de build). Login : `npx vercel login` (une seule fois par poste).
