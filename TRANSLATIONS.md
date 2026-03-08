# 🌍 PyCon Togo 2026 – Système de Traductions

## Vue d'ensemble

Le site PyCon Togo 2026 est entièrement bilingue (Français / English) avec un système de traductions centralisé et facile à maintenir.

## Architecture

### 1. **Fichier de traductions** (`app/static/2026/i18n/translations.json`)

Fichier JSON structuré contenant **toutes les chaînes de texte** du site en deux langues :

```json
{
  "en": {
    "nav": { ... },
    "hero": { ... },
    "footer": { ... }
  },
  "fr": {
    "nav": { ... },
    "hero": { ... },
    "footer": { ... }
  }
}
```

**Avantages :**
- ✅ Modifications faciles sans toucher au code source
- ✅ Gestion centralisée des traductions
- ✅ Format standard JSON pour compatibilité avec d'autres outils

### 2. **Système de langues dans HTML** (data-i18n attributes)

Les éléments HTML utilisent les attributs de données pour stocker les traductions :

```html
<h1 data-i18n-en="The Python conference of Togo" 
    data-i18n-fr="La conférence Python du Togo">
  La conférence Python du Togo
</h1>
```

**Types supportés :**
- `data-i18n-en` / `data-i18n-fr` – Texte simple (utilise `textContent`)
- `data-i18n-html-en` / `data-i18n-html-fr` – Contenu HTML (utilise `innerHTML`)

### 3. **JavaScript** (`app/static/2026/js/script.js`)

Le système de traductions chargé depuis `translations.json` :

```javascript
// Charge les traductions au démarrage
await loadTranslations();

// Bascule de langue
applyLanguage('fr' || 'en');

// Accès aux traductions (optionnel)
const text = t('nav.home'); // récupère les traductions depuis le JSON
```

## 🔧 Comment modifier les traductions

### Option 1 : Directement via `translations.json` (Recommandé ✅)

**Fichier :** `/app/static/2026/i18n/translations.json`

```json
{
  "en": {
    "footer": {
      "made_with": "Made with ❤️ by"
    }
  },
  "fr": {
    "footer": {
      "made_with": "Fait avec ❤️ par"
    }
  }
}
```

### Option 2 : Directement dans les HTML templates

Si vous modifiez les attributs `data-i18n-en/fr` :

```html
<span data-i18n-en="New English Text" 
      data-i18n-fr="Nouveau texte français">
  Ancien texte français
</span>
```

## 📋 Workflow de traduction recommandé

### Ajouter une nouvelle chaîne de texte :

1. **Ajouter dans `translations.json`** (deux langues) :
```json
"about_page": {
  "mission": "Strengthen local technical skills",
  "vision": "Build a sustainable community"
}
```

2. **Ajouter dans le HTML** :
```html
<p data-i18n-en="Strengthen local technical skills" 
   data-i18n-fr="Renforcer les compétences techniques locales">
  Renforcer les compétences techniques locales
</p>
```

### Mettre à jour une traduction existante :

1. Ouvrir `/app/static/2026/i18n/translations.json`
2. Modifier les clés "en" et "fr" concernées
3. Sauvegarder
4. **Aucun rechargement de code source nécessaire !**

## 📚 Structure actuelle de `translations.json`

Sections disponibles :
- `nav` – Navigation et menus
- `hero` – Section héro de la page d'accueil
- `about_strip`, `edition_proof`, `program` – Sections de contenu
- `footer` – Pied de page
- `about_page`, `contact_page`, `coc_page`, `health_page` – Pages intérieures
- `team_members` – Données des membres de l'équipe

## 🎯 Créateurs du site ("Made With")

Les créateurs du site sont affichés dynamiquement dans le footer via la fonction `renderSiteCreators()`.

**Fichier de configuration :** `/app/static/2026/js/script.js`

```javascript
const siteCreators = [
  {
    name: "Tronka Diabate",
    linkedin: "https://www.linkedin.com/in/tronka-diabate/",
    portfolio: "https://tronkatech.dev"  // Optionnel : si vide, utilise LinkedIn
  },
  {
    name: "Wachiou Bouraima",
    linkedin: "https://www.linkedin.com/in/waschioubouraima/",
    portfolio: ""  // Utilise LinkedIn si portfolio vide
  }
];
```

### Ajouter un créateur :

1. Ouvrir `/app/static/2026/js/script.js`
2. Ajouter une entrée dans le tableau `siteCreators`
3. Sauvegarder

Le site mettra automatiquement à jour la section "Made With" !

## 🌐 Comment fonctionne le basculement de langue

1. **Au chargement :** Récupère la langue sauvegardée depuis localStorage
2. **Boutons de langue :** Quand l'utilisateur clique EN/FR
3. **applyLanguage()** parcourt tous les éléments avec data-i18n-* et les met à jour
4. **Sauvegarde :** La préférence est stockée dans localStorage pour la prochaine visite

## 📱 Pages traduites

- ✅ Homepage (index.html)
- ✅ About page (2026_about.html)  
- ✅ Contact page (2026_contact.html)
- ✅ Code of Conduct (2026_coc.html)
- ✅ Health & Safety (2026_health_security.html)
- ✅ Navigation et Footer (base.html)

## 🚀 Usage des créateurs

**Langue EN :**
```
Made with ❤️ by Tronka Diabate and Wachiou Bouraima
```

**Langue FR :**
```
Fait avec ❤️ par Tronka Diabate et Wachiou Bouraima
```

Les noms sont des liens cliquables vers :
- Portfolio (si disponible)
- LinkedIn (par défaut)

## ✨ Prochaines étapes facultatives

- [ ] Traductions complètes pour pages supplémentaires (2026_sponsors.html, 2026_teams.html, 2026_registration.html)
- [ ] Intégration avec un système de gestion de traductions externe (ex: Crowdin)
- [ ] Pluralisation et contextes régionaux
- [ ] Traductions SEO (meta descriptions, og:tags)

## 📞 Support

Pour ajouter une traduction manquante ou modifier le système, modifiez simplement :
1. `/app/static/2026/i18n/translations.json` (contenus)
2. `/app/static/2026/js/script.js` (logique et créateurs)
3. `/app/templates/2026/*.html` (structure HTML)
