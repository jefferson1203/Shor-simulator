# Documentation Technique — Simulateur d’Algorithme de Shor

## Table des matières

- [1. Introduction](#1-introduction)
- [2. Architecture et Organisation du Projet](#2-architecture-et-organisation-du-projet)
- [3. Description des Modules](#3-description-des-modules)
  - [3.1. Partie Classique (`classical/`)](#31-partie-classique-classical)
  - [3.2. Partie Quantique (`quantum/`)](#32-partie-quantique-quantum)
  - [3.3. Interface Utilisateur et Application Principale (`app.py`)](#33-interface-utilisateur-et-application-principale-apppy)
  - [3.4. Ressources et Style](#34-ressources-et-style)
- [4. Fonctionnalités Clés et Logique de l’Application](#4-fonctionnalités-clés-et-logique-de-lapplication)
- [5. Améliorations Apportées pour la Soutenance TX IQ](#5-améliorations-apportées-pour-la-soutenance-tx-iq)
- [6. Points d’Extension et Conseils pour la Suite](#6-points-dextension-et-conseils-pour-la-suite)
- [7. Installation et Lancement](#7-installation-et-lancement)
- [8. Auteurs et Contacts](#8-auteurs-et-contacts)

---

## 1. Introduction

Ce projet est un simulateur pédagogique de l’algorithme de Shor, développé en Python avec Streamlit. Il permet de factoriser des entiers en simulant les étapes classiques et quantiques de l’algorithme, tout en offrant une interface interactive et des visualisations pour l’apprentissage.

---

## 2. Architecture et Organisation du Projet

Le projet est organisé de façon modulaire pour séparer la logique classique, la simulation quantique, l’interface et les ressources.

```
.
├── app.py                      # Application principale Streamlit
├── style.css                   # Feuille de style personnalisée
├── requirements.txt            # Dépendances Python
├── README.md                   # Présentation utilisateur
├── classical/
│   ├── continued_fraction.py   # Fractions continues et convergents
│   ├── explanations.py         # Explications pédagogiques
│   └── preprocessing.py        # Prétraitement et choix de la base a
├── quantum/
│   ├── circuit_visualizer_clean.py # Visualisation du circuit quantique
│   └── quantum_register.py         # Simulation du registre quantique
├── utc/
│   └── image.png               # Logo et ressources graphiques
└── .gitignore
```

---

## 3. Description des Modules

### 3.1. Partie Classique (`classical/`)

- **[`classical/preprocessing.py`](classical/preprocessing.py)**
  - Validation du nombre à factoriser (trivialité, parité, primalité, puissances parfaites)
  - Choix de la base `a` (aléatoire, premier avec `n`)
  - Recherche de petits facteurs par PGCD

- **[`classical/continued_fraction.py`](classical/continued_fraction.py)**
  - Calcul des coefficients de la fraction continue d’un nombre réel
  - Calcul des convergents pour l’approximation de la période

- **[`classical/explanations.py`](classical/explanations.py)**
  - Explications détaillées pour chaque étape, affichées dans l’interface

### 3.2. Partie Quantique (`quantum/`)

- **[`quantum/quantum_register.py`](quantum/quantum_register.py)**
  - Simulation d’un registre quantique (état, portes Hadamard, Oracle, IQFT, mesure)
  - Méthodes pour appliquer les transformations quantiques et simuler la mesure

- **[`quantum/circuit_visualizer_clean.py`](quantum/circuit_visualizer_clean.py)**
  - Visualisation du circuit quantique avec Plotly
  - Affichage des portes, des qubits, et des probabilités de mesure

### 3.3. Interface Utilisateur et Application Principale (`app.py`)

- **[`app.py`](app.py)**
  - Orchestration de la simulation étape par étape ou en mode automatique
  - Gestion de l’état de la simulation via `st.session_state`
  - Intégration des modules classiques et quantiques
  - Affichage des explications, des résultats, et des visualisations

### 3.4. Ressources et Style

- **[`style.css`](style.css)**
  - Personnalisation avancée de l’interface Streamlit (couleurs, boutons, cartes, sidebar)

- **[`utc/image.png`](utc/image.png)**
  - Logo de l'utc

---

## 4. Fonctionnalités Clés et Logique de l’Application

- **Simulation pas à pas** : L’utilisateur suit chaque étape, du choix de `N` à l’extraction des facteurs.
- **Mode automatique** : Permet d’enchaîner toutes les étapes sans intervention manuelle.
- **Choix et validation de la base `a`** : Sélection aléatoire, vérification de la coprimalité, gestion des échecs.
- **Simulation quantique** : Application des portes Hadamard, Oracle, IQFT, puis mesure.
- **Visualisation du circuit** : Affichage dynamique du circuit et des probabilités de mesure.
- **Post-traitement classique** : Utilisation des fractions continues pour retrouver la période.
- **Extraction des facteurs** : Calcul des facteurs à partir de la période trouvée.
- **Gestion des échecs** : Relance automatique ou manuelle en cas de période impaire, mesure nulle, etc.
- **Explications pédagogiques** : Chaque étape est accompagnée d’explications détaillées.

---

## 5. Améliorations à apporter suite à la Soutenance TX IQ

### 5.1. Forçage d’un Cas d’Échec

- **Fonctionnalité** : Rendre possible le fait de forcer un cas d’échec lors de la simulation quantique, par exemple en tombant sur de petits pics de probabilité ou en permettant à l’utilisateur de choisir un résultat de mesure particulier.
- **Utilité pédagogique** : Cela permet de montrer que l’algorithme de Shor n’est pas toujours un succès du premier coup, et d’illustrer la nécessité de relancer la simulation ou de changer la base `a`.

### 5.2. Mode Automatique et Journalisation

- **Mode automatique** : L’utilisateur peut activer un mode où toutes les étapes s’enchaînent automatiquement.
- **Journalisation** : Le nombre de tentatives de choix de la base `a` doit être comptabilisé et affiché, pour permettre de suivre le nombre d’essais nécessaires avant de trouver une base et une période convenables.
- **Intérêt** : Cela met en avant l’aspect probabiliste de l’algorithme et la réalité des échecs intermédiaires. Il pourra aussi être utile pour examiner le nombre d'iterations moyens selon le choix de `N`.

### 5.3. Extension de la Limite de Calcul

- **Limite actuellete** : Par défaut, la valeur de `N` était limitée à 100 pour des raisons de performance et de lisibilité.
- **Amélioration** : La limite doit être élargie (jusqu’à 1000 et plus) pour permettre la factorisation de nombres plus grands, rendant la simulation plus réaliste et plus flexible.
- **Remarque** : Pour des valeurs très grandes, la simulation peut devenir lente ou consommatrice de mémoire, mais cela permet d’expérimenter avec des cas plus complexes.

---

## 6. Points d’Extension et Conseils pour la Suite

- **Optimisation de la simulation quantique** : Pour des valeurs de `N` plus grandes, envisager des optimisations ou des approximations pour la gestion des états quantiques.
- **Ajout de tests unitaires** : Pour garantir la robustesse du code, ajouter des tests sur les modules classiques et quantiques.
- **Interface utilisateur** : Ajouter des options pour choisir explicitement le résultat de mesure ou visualiser l’historique des essais.
- **Support multi-utilisateur** : Envisager la sauvegarde des sessions ou l’export des résultats.
- **Documentation du code** : Maintenir des docstrings détaillés et des commentaires pour faciliter la reprise du projet.
- **Internationalisation** : Prévoir une version anglaise pour une diffusion plus large.

---

## 7. Installation et Lancement

### Prérequis

- Python 3.8 ou supérieur
- pip

### Installation

```bash
git clone <URL_DU_DEPOT>
cd <NOM_DU_DOSSIER>
python -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate sous Windows
pip install -r requirements.txt
```

### Lancement

```bash
streamlit run app.py
```

L’application s’ouvre dans votre navigateur.

---

## 8. Auteurs et Contacts

- **Jefferson MBOUOPDA**
- **Ruben MOUGOUE**

Responsable pédagogique : Ahmed LOUNIS  
Superviseur : Vincent ROBIN

---

**Bon courage à la prochaine génération ! N’hésitez pas à améliorer, documenter et partager vos retours pour faire vivre ce projet.**