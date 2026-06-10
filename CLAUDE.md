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
| `cj2a-adou` | https://cj2a-adou.vercel.app | juridique |
| `dso-architect` | https://dso-architect.vercel.app | archi |
| `prest-company` | https://prest-company.vercel.app | immo |

## Vercel config

`vercel.json` rewrites all routes to `index.html` (single-page statique, pas de build). Login : `npx vercel login` (une seule fois par poste).
