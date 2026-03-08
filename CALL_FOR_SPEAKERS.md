# Call for Speakers Form - Documentation

## Overview
La page "Call for Speakers" permet aux speakers de soumettre leurs propositions de talks pour PyCon Togo 2026.

## Routes d'accès
- `/speakers` - Route principale
- `/call-for-speakers` - Alias pour la même page
- `/cfp` - Alias pour la même page (Call For Papers)

## Structure du formulaire

Le formulaire est divisé en 4 sections principales :

### 1. À Propos de Vous
- **Full Name** (Nom Complet) - Requis
- **Email Address** (Adresse Email) - Requis, validation email
- **Short Bio** (Courte Biographie) - Requis, textarea
- **Location / Country** (Localisation / Pays) - Requis
- **Years of Experience** (Années d'Expérience) - Requis, select
  - Beginner (0-2 ans)
  - Intermediate (2-5 ans)
  - Advanced (5+ ans)

### 2. Votre Présentation
- **Presentation Title** (Titre de la Présentation) - Requis
- **Format** (Format) - Requis, select
  - Workshop (Hands-on, 3-4 heures)
  - Keynote (Talk d'ouverture inspirant, 45 min)
  - Standard Talk (Présentation technique, 30-45 min)
  - Panel Discussion (Plusieurs speakers, 45 min)
  - Lightning Talk (Session rapide, 10-15 min)
- **Target Audience Level** (Niveau du Public Cible) - Requis, select
  - Beginner
  - Intermediate
  - Advanced
  - All Levels
- **Presentation Description** (Description de la Présentation) - Requis, textarea (min 50 caractères)
- **Topics/Tags** (Sujets/Tags) - Requis

### 3. Vos Liens (Optionnel)
- **LinkedIn Profile** - Optionnel
- **GitHub Profile** - Optionnel
- **Personal Website / Portfolio** - Optionnel
- **Twitter/X Profile** - Optionnel

### 4. Timeline (Informationnel)
- Submission Deadline: 31 mai 2026
- Notification Date: 15 juin 2026
- Speaker Confirmation: Avant le 30 juin 2026

## Traductions

Toutes les étiquettes, placeholders et messages d'aide sont stockés dans `/app/static/2026/i18n/translations.json` sous la clé `call_for_speakers_page`.

Pour modifier les traductions, éditez directement le fichier JSON - aucun changement de code n'est nécessaire.

Exemple de structure des traductions :
```json
"call_for_speakers_page": {
  "form_fullname": "Full Name",
  "form_fullname_fr": "Nom Complet",
  "form_email": "Email Address",
  ...
}
```

## Styles CSS

Les styles sont en `/app/static/2026/css/pages/call-for-speakers.css`.

### Classes principales utilisées :
- `.cfs-form-section` - Section du formulaire
- `.cfs-form-wrapper` - Wrapper du formulaire
- `.form-fieldset` - Groupement de champs
- `.form-group` - Groupe de formulaires individuels
- `.form-row` - Row avec grid layout (2 colonnes)
- `.cfs-timeline` - Section timeline
- `.cfs-faq` - Section FAQ
- `.cfs-intro` - Section introduction avec bénéfices

## Comportement du formulaire

### Validation client
- Tous les champs requis sont validés avec l'attribut HTML5 `required`
- Email validé avec `type="email"`
- URLs validées avec `type="url"`
- Minlength pour la description (50 caractères)

### Soumission
Actuellement, le formulaire affiche un message de succès après 1.5 secondes :

```javascript
function handleSpeakerSubmit(e) {
  e.preventDefault();
  // Le bouton se désactive
  // Après 1.5s, le formulaire est caché et le message de succès s'affiche
}
```

## Intégration avec le système de traductions

Le formulaire utilise les attributs `data-i18n-en` et `data-i18n-fr` pour les libellés statiques, mais le système de traduction JavaScript applique automatiquement les traductions du JSON au chargement de la page.

```html
<label data-i18n-en="Full Name" data-i18n-fr="Nom Complet">Nom Complet *</label>
```

Le JavaScript met à jour tous les éléments avec ces attributs quand la langue change.

## Mise en place de la soumission backend

Pour recevoir les données du formulaire, vous devez :

1. Ajouter un endpoint POST dans les routes :
```python
@router.post("/speakers/submit")
async def submit_speaker(request: Request):
    data = await request.json()
    # Traiter les données
    # Envoyer un email de confirmation
    # Sauvegarder en base de données
    return {"status": "success"}
```

2. Modifier le JavaScript pour envoyer les données :
```javascript
function handleSpeakerSubmit(e) {
  e.preventDefault();
  const formData = new FormData(document.getElementById('speaker-form'));
  const data = Object.fromEntries(formData);
  
  fetch('/speakers/submit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  .then(res => res.json())
  .then(data => {
    // Afficher le message de succès
  });
}
```

## Questions fréquentes

Le formulaire inclut une section FAQ avec 6 questions prédéfinies (bilingues).

## Section "Why Submit a Talk?"

Une section introduction affiche 3 bénéfices principaux avec icons emoji et descriptions.
