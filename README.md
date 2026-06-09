# ⚽ FIFA 2026 Watch

> Journalisme citoyen — Suivi indépendant des scandales et controverses de la Coupe du Monde FIFA 2026 (USA · Canada · Mexique)

## Présentation

**FIFA 2026 Watch** est un site statique open source qui recense, classe et documente les scandales liés à l'organisation de la Coupe du Monde 2026. L'objectif est de centraliser des informations vérifiables avec leurs sources, accessibles à tous.

## Démo

Ouvrir `index.html` dans un navigateur (via un serveur local — voir ci-dessous).

## Stack technique

| Couche       | Techno                          |
|--------------|---------------------------------|
| Front-end    | HTML5 + CSS Variables + JS ES Modules |
| Données      | JSON statique (`data/scandales.json`) |
| Hébergement  | GitHub Pages (statique, aucun backend) |
| Build        | Aucun — zéro dépendance         |

## Structure

```
fifa26watch/
├── index.html            # Interface principale
├── data/
│   └── scandales.json    # Base de données des scandales
├── docs/
│   ├── SYSTEM_PROMPT.md  # Prompt système pour Claude Code
│   └── WORKFLOW.md       # Guide de contribution
├── CLAUDE.md             # Instructions pour Claude Code
└── README.md             # Ce fichier
```

## Lancer en local

```bash
# Python (recommandé)
python3 -m http.server 8080
# puis ouvrir http://localhost:8080

# Node.js (alternative)
npx serve .
```

> ⚠️ Ne pas ouvrir `index.html` directement via `file://` : le `fetch()` sera bloqué par CORS.

## Contribuer

1. Forkez le dépôt
2. Ajoutez votre scandale dans `data/scandales.json` en respectant le schéma
3. Vérifiez avec `python3 -m json.tool data/scandales.json`
4. Ouvrez une Pull Request avec une source crédible

Voir `docs/WORKFLOW.md` pour le guide complet.

## Schéma d'un scandale

```json
{
  "id": 6,
  "titre": "Titre court et explicite",
  "date": "YYYY-MM-DD",
  "categorie": "Corruption | Infrastructure | Droits humains | Billetterie | Sponsoring",
  "gravite": "haute | moyenne | basse",
  "statut": "confirmé | vérifié | allégation | en cours",
  "description": "Description factuelle en 2-3 phrases.",
  "pays_concernes": ["Pays"],
  "sources": [{ "titre": "Nom de la source", "url": "https://..." }],
  "tags": ["tag-slug"]
}
```

## Licence

MIT — Utilisation libre à des fins d'information et de journalisme citoyen.
