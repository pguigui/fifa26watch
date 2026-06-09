# WORKFLOW — FIFA 2026 Watch

Guide de contribution et de maintenance du projet.

---

## 1. Ajouter un nouveau scandale

### 1.1 Éditer `data/scandales.json`

```json
{
  "id": <prochain_id>,
  "titre": "Titre court et accrocheur",
  "date": "YYYY-MM-DD",
  "categorie": "Corruption | Infrastructure | Droits humains | Billetterie | Sponsoring",
  "gravite": "haute | moyenne | basse",
  "statut": "confirmé | vérifié | allégation | en cours",
  "description": "Description factuelle et neutre en 2-3 phrases.",
  "pays_concernes": ["Pays 1", "Pays 2"],
  "sources": [
    { "titre": "Nom source", "url": "https://url-verifiable.com/article" }
  ],
  "tags": ["tag-en-minuscule", "sans-espaces"]
}
```

### 1.2 Règles de saisie

| Champ       | Règle                                                      |
|-------------|------------------------------------------------------------|
| `id`        | Entier unique, jamais réutilisé, toujours croissant        |
| `date`      | Date de révélation publique, format ISO 8601               |
| `gravite`   | `haute` = impact systémique / `moyenne` = significatif / `basse` = mineur |
| `statut`    | `confirmé` = multiple sources fiables / `vérifié` = une source fiable / `allégation` = non encore prouvé / `en cours` = investigation active |
| `sources`   | Minimum 1 source. Préférer des médias reconnus.            |
| `tags`      | Slugs en minuscules, séparés par des tirets                |

### 1.3 Valider le JSON

```bash
python3 -m json.tool data/scandales.json
```

### 1.4 Tester visuellement

```bash
python3 -m http.server 8080
# Ouvrir http://localhost:8080
```

---

## 2. Mettre à jour un scandale existant

- Modifier uniquement les champs pertinents (`statut`, `description`, `sources`)
- Ne jamais changer l'`id`
- Ajouter la nouvelle source dans le tableau `sources`
- Pour archiver : `"statut": "archivé"` (ne jamais supprimer l'entrée)

---

## 3. Modifier l'interface (`index.html`)

- Toutes les couleurs via variables CSS dans `:root`
- Pas de CDN externe, pas de `<script src="...">` vers des domaines tiers
- Tester sur Chrome et Firefox avant de committer
- Mode sombre uniquement (design intentionnel)

---

## 4. Conventions Git

### Format des commits (Conventional Commits)

```
type(scope): description courte en français
```

| Type       | Usage                                         |
|------------|-----------------------------------------------|
| `feat`     | Nouvelle fonctionnalité interface             |
| `fix`      | Correction bug                                |
| `data`     | Ajout / mise à jour dans `scandales.json`    |
| `style`    | Changement CSS uniquement                     |
| `docs`     | README, WORKFLOW, CLAUDE.md                   |
| `refactor` | Restructuration sans changement fonctionnel   |

### Exemples

```bash
git commit -m "data(scandales): ajouter scandale billetterie FIFA #6"
git commit -m "feat(filter): ajouter filtre par gravité"
git commit -m "fix(ui): corriger l'affichage mobile des cards"
git commit -m "docs(workflow): mettre à jour guide de contribution"
```

---

## 5. Déploiement GitHub Pages

```bash
# S'assurer que la branche main est à jour
git push origin main

# GitHub Pages : activer dans Settings > Pages > Source: main / root
# URL publique : https://<username>.github.io/fifa26watch/
```

---

## 6. Checklist avant chaque commit

- [ ] `python3 -m json.tool data/scandales.json` → pas d'erreur
- [ ] Visuel vérifié sur `http://localhost:8080`
- [ ] Aucune source inventée
- [ ] Message de commit au format Conventional Commits
