# 👥 Créateurs du site PyCon Togo 2026

## À propos de la section "Made With"

La section "Made With" (Fait avec ❤️) dans le footer du site affiche les créateurs et leurs profils de manière dynamique.

## Créateurs actuels

### 1. **Tronka Diabate**
- **Portfolio :** https://tronkatech.dev
- **LinkedIn :** https://www.linkedin.com/in/tronka-diabate/
- **Rôle :** Développement et Architecture

### 2. **Wachiou Bouraima**
- **LinkedIn :** https://www.linkedin.com/in/waschioubouraima/
- **Rôle :** Président de PyCon Togo, Fondateur de Python Togo

## Configuration

La liste des créateurs est stockée dans `/app/static/2026/js/script.js` :

```javascript
const siteCreators = [
  {
    name: "Tronka Diabate",
    linkedin: "https://www.linkedin.com/in/tronka-diabate/",
    portfolio: "https://tronkatech.dev"
  },
  {
    name: "Wachiou Bouraima",
    linkedin: "https://www.linkedin.com/in/waschioubouraima/",
    portfolio: ""
  }
];
```

## Ajouter/Modifier un créateur

### Ajouter un nouveau créateur :

```javascript
const siteCreators = [
  // ... créateurs existants
  {
    name: "Nouveau Créateur",
    linkedin: "https://www.linkedin.com/in/nouveau-createur/",
    portfolio: "https://portfolio-url.com"  // optionnel
  }
];
```

### Priorité des liens :

1. **Si `portfolio` est renseigné :** le lien pointe vers le portfolio
2. **Si `portfolio` est vide :** le lien pointe vers LinkedIn
3. **Toujours :** ouverture dans un nouvel onglet (`target="_blank"`)

## Rendu final

### En Anglais :
```
Made with ❤️ by Tronka Diabate and Wachiou Bouraima
```

### En Français :
```
Fait avec ❤️ par Tronka Diabate et Wachiou Bouraima
```

Les noms sont cliquables et d'une couleur différente pour montrer qu'ils sont interactifs.

## Fonction JavaScript

La fonction `renderSiteCreators()` gère :
- Chargement dynamique des créateurs
- Traduction du texte "Made with" selon la langue
- Génération des liens avec les bonnes URLs  
- Formatage avec "and" / "et" selon la langue

```javascript
function renderSiteCreators() {
  const footerBottom = document.querySelector(".footer-bottom-inner span:last-child");
  if (!footerBottom) return;

  const lang = currentLang || "en";
  const madeWithText = translations[lang]?.footer?.made_with || "Made with ❤️ by";
  const andText = lang === "fr" ? " et " : " and ";
  
  // ... génération des liens ...
  footerBottom.innerHTML = html;
}
```

## Note

Tous les changements dans `script.js` nécessitent un rechargement de page ou un redémarrage du serveur pour être visibles.
