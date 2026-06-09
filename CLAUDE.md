# CLAUDE.md — FIFA 2026 Watch

Instructions pour Claude Code lors du travail sur ce projet.

## Présentation

**FIFA 2026 Watch** est un site statique de journalisme citoyen qui recense
les scandales liés à la Coupe du Monde FIFA 2026 (USA · Canada · Mexique).

Stack : HTML vanilla + CSS Variables + JavaScript ES Modules — aucun build tool, aucune dépendance.

## Structure

```
fifa26watch/
├── index.html            # Interface principale
├── data/
│   └── scandales.json    # Source de vérité (ne jamais supprimer d'entrée)
├── docs/
│   ├── SYSTEM_PROMPT.md  # Chargé via : claude --system-prompt docs/SYSTEM_PROMPT.md
│   └── WORKFLOW.md       # Guide de contribution détaillé
├── CLAUDE.md             # Ce fichier
└── README.md             # Présentation publique
```

## Règles de développement

### `data/scandales.json`
- Respecter strictement le schéma (voir `docs/WORKFLOW.md` §1.2)
- Trier par date décroissante
- Ne jamais supprimer un ID — utiliser `"statut": "archivé"` à la place
- Minimum 1 source vérifiable par entrée
- Valider après chaque modification : `python3 -m json.tool data/scandales.json`

### `index.html`
- Zéro dépendance externe (pas de CDN, pas de framework)
- Couleurs exclusivement via variables CSS dans `:root`
- Design dark uniquement
- Le JS utilise `fetch("data/scandales.json")` — toujours tester via serveur HTTP

### Git — Conventional Commits
```
type(scope): message en français
```
Types autorisés : `feat` · `fix` · `data` · `style` · `docs` · `refactor`

Exemples :
```
data(scandales): ajouter scandale droits TV #1
feat(filter): ajouter filtre par gravité
fix(ui): corriger affichage mobile
```

## Commandes courantes

```bash
# Serveur local
python3 -m http.server 8080

# Valider le JSON
python3 -m json.tool data/scandales.json

# Historique git
git log --oneline -10
```

## Ce que Claude NE doit PAS faire

- Introduire React, Vue ou tout autre framework JS sans accord explicite
- Modifier les `id` existants dans `scandales.json`
- Ajouter des faits sans source vérifiable
- Utiliser `git push --force` ou `git reset --hard` sans demande explicite
- Ouvrir `index.html` en `file://` (utiliser le serveur HTTP)
