# Système de veille quotidienne — FIFA 2026 Watch

Surveillance automatique de flux RSS pour repérer les nouveaux scandales,
**sans publication automatique**. L'humain garde toujours la décision finale.

## Principe

```
RSS feeds → filtre mots-clés → fichier candidats du jour → TON review → JSON → publication
   (auto)        (auto)              (auto)                  (manuel)   (manuel)  (manuel)
```

Le script ne publie jamais rien sur le site. Il prépare une liste à vérifier.
Ça protège ta règle éditoriale : **source primaire vérifiée, pas de rumeur.**

---

## Option A — GitHub Actions (recommandé)

Tourne dans le cloud, même PC éteint. Gratuit pour un repo public.

1. Le fichier `.github/workflows/veille.yml` est déjà en place.
2. Sur GitHub : **Settings → Actions → General → Workflow permissions**
   → coche **"Read and write permissions"** et **"Allow GitHub Actions to create pull requests"**.
3. C'est tout. Chaque matin (~08h30 Paris), une **pull request** s'ouvre
   avec les candidats du jour dans `drafts/candidats-AAAA-MM-JJ.md`.
4. Tu ouvres la PR, tu coches ce qui est pertinent, tu génères le JSON, tu merges.

Pour lancer manuellement sans attendre : onglet **Actions → Veille quotidienne → Run workflow**.

---

## Option B — Cron sous WSL Ubuntu

Plus simple mais ne tourne que si ton PC est allumé.

```bash
# 1. Test manuel d'abord
cd ~/fifa26watch
python3 scripts/veille.py --days 1

# 2. Programmer à 8h chaque matin
crontab -e
# Ajoute cette ligne :
0 8 * * * cd ~/fifa26watch && /usr/bin/python3 scripts/veille.py --days 1 >> ~/veille.log 2>&1
```

Le fichier du jour apparaît dans `drafts/`. Tu le lis, tu traites les bons articles.

---

## Personnaliser

Tout est dans `scripts/veille.py`, en haut du fichier :

- **`FEEDS`** — ajoute/retire des flux RSS. La plupart des médias exposent
  un flux par rubrique (souvent `/rss` ou `/feed`). Teste l'URL dans un navigateur :
  si du XML s'affiche, c'est bon.
- **`CORE_TERMS`** — termes obligatoires liés à FIFA 2026.
- **`CONTEXT_TERMS`** — au moins un doit être présent (scandale, visa, corruption…).

Un article n'est retenu que s'il contient **au moins un CORE _et_ un CONTEXT**.
Ça limite le bruit.

---

## Flux RSS utiles à ajouter

Quelques pistes fiables (vérifie les URLs, elles évoluent) :

- The Guardian : `theguardian.com/<section>/rss`
- BBC : `feeds.bbci.co.uk/sport/...`
- Al Jazeera, NPR, France 24, Le Monde, RFI — flux par rubrique
- Pour la recherche thématique large : **GDELT** (gratuit, couvre la presse mondiale)

---

## Limites à connaître

- Le script lit **titre + résumé** du flux, pas l'article complet.
  Donc certains scandales ne ressortiront pas si le flux est avare en mots-clés.
- Quelques médias bloquent les requêtes sans User-Agent navigateur,
  ou n'ont pas de flux RSS du tout. Dans ce cas : veille manuelle pour ceux-là.
- **Ne jamais publier directement depuis cette liste** : c'est de la matière brute.
