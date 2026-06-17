"""
Échappe </script> à l'intérieur du JSON bundlé.
En HTML, un parser voit </script> et ferme le tag <script> immédiatement,
même si on est à l'intérieur d'une chaîne JSON. Résultat : JSON tronqué,
bundler KO (surtout sur mobile, plus strict).
Solution : </script> → <\/script> dans le JSON brut.
  - Valide en JSON  : \/  est une séquence d'échappement légale
  - Invisible HTML  : <\/ n'est pas reconnu comme une fin de tag par le parser HTML
  - Rendu correct   : JSON.parse() donne </script> dans le HTML décodé
"""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    content = f.read()

OPEN_TAG  = '<script type="__bundler/template">'
CLOSE_TAG = '</script>'

start = content.find(OPEN_TAG)
if start == -1:
    print("ERREUR : balise bundler introuvable")
    sys.exit(1)

json_start = start + len(OPEN_TAG)

# Trouver la fin réelle du JSON : chercher </script> suivi uniquement
# d'espaces/newlines puis de la fin du document ou d'autres balises.
# On identifie la fin du JSON en cherchant le dernier " avant le vrai </script>.
# Approche simple : remplacer TOUTES les occurrences de </script> dans le JSON,
# puis remettre UNE seule vraie balise fermante à la fin.
end = content.rfind(CLOSE_TAG)   # dernier </script> = le vrai closing tag du bundler
if end == -1 or end <= json_start:
    print("ERREUR : balise fermante introuvable")
    sys.exit(1)

json_raw = content[json_start:end]

# Compter les </script> non échappés dans le JSON (à corriger)
bad_count = json_raw.count('</script>')
print(f"</script> non échappés dans le JSON : {bad_count}")

# Remplacer par <\/script>
json_fixed = json_raw.replace('</script>', r'<\/script>')

# Vérification
remaining = json_fixed.count('</script>')
print(f"Après correction : {remaining} </script> non échappé (attendu : 0)")
print(f"<\\/script> insérés : {json_fixed.count(r'<\/script>')}")

new_content = content[:json_start] + json_fixed + content[end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"\nindex.html mis à jour ({len(new_content)//1024} Ko)")
