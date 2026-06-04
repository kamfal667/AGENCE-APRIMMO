# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A multi-template static website system for prospects in Abidjan (Côte d'Ivoire). Each prospect gets their own Git branch and a separate Vercel deployment. The `main` branch holds the master templates — never modify it directly.

## Templates disponibles

| Fichier | Secteur | Nom par défaut |
|---|---|---|
| `templates/template-immo.html` | Immobilier | AGENCE IMMOBILIERE LUMIERE |
| `templates/template-archi.html` | Architecture & Design | Confort Seven |

## Branch & deploy workflow

One branch per prospect. Branch names: lowercase, no accents, hyphens only (e.g. `sci-transville`).

```bash
git checkout main && git pull origin main
git checkout -b [nom-du-prospect]

# Copier le bon template en index.html
cp templates/template-immo.html index.html   # pour un prospect immobilier
# OU
cp templates/template-archi.html index.html  # pour un prospect architecture

# Modifier index.html (voir points de personnalisation ci-dessous)
git add index.html
git commit -m "feat: version [nom-du-prospect]"
git push origin [nom-du-prospect]

rm -rf .vercel   # obligatoire — retient la liaison au projet précédent
npx vercel --yes --name [nom-du-prospect]
```

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
| Nom du cabinet | Remplacement global de `Confort Seven` (~6 occurrences : title, nav-logo, footer, WhatsApp message) |
| Numéro WhatsApp | `const WA_NUMBER = '225XXXXXXXXXX'` (ligne ~1384) + liens `wa.me/225XXXXXXXXXX` |
| Téléphone affiché | `+225 07 00 00 00 00` (lignes ~1300 et ~1356) |
| Email | `contact@archetypafrica.com` (lignes ~1309 et ~1357) |
| Adresse | `Cocody Danga, Abidjan` (lignes ~1291, ~1358) |
| Couleur accent (cuivre) | `--cuivre:#B87333` dans `:root` (ligne ~19) |

## Vercel config

`vercel.json` rewrites all routes to `index.html` (single-page static site). No build step — Vercel serves the file directly.
