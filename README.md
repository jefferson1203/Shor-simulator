# Simulateur d'Algorithme de Shor

![Logo](utc/image.png)

Projet réalisé dans le cadre de l'UV **Tx n°7708**, ce simulateur offre une exploration interactive et pédagogique de l'algorithme quantique de Shor pour la factorisation des nombres entiers. L'application est développée en Python avec la bibliothèque Streamlit.

## Table des matières
- [Fonctionnalités](#fonctionnalités)
- [Technologies Utilisées](#technologies-utilisées)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Structure du Projet](#structure-du-projet)
- [Auteurs et Encadrement](#auteurs-et-encadrement)

## Fonctionnalités

- **Simulation Pas à Pas** : Suivez chaque étape de l'algorithme, du prétraitement classique à l'extraction des facteurs.
- **Interface Interactive** : Choisissez le nombre à factoriser et la base `a`, et contrôlez le déroulement de la simulation.
- **Mode Automatique** : Lancez la simulation complète en un seul clic.
- **Visualisation du Circuit Quantique** : Observez la construction du circuit quantique en temps réel avec les portes Hadamard, Oracle et IQFT.
- **Graphiques de Probabilité** : Visualisez la distribution de probabilité des états quantiques avant et après la mesure.
- **Explications Détaillées** : Chaque étape est accompagnée d'explications claires pour faciliter la compréhension des concepts théoriques.
- **Gestion des Échecs** : L'application gère les cas d'échec (période impaire, mesure nulle, etc.) et propose de réessayer avec de nouveaux paramètres.

## Technologies Utilisées

- **Python 3**
- **Streamlit** : Pour la création de l'interface web interactive.
- **Plotly** : Pour les visualisations dynamiques (circuit quantique, graphiques).
- **NumPy** : Pour les calculs numériques et la simulation de l'état quantique.
- **Pandas** : Pour la manipulation et l'affichage des données (convergents).

## Installation

Pour lancer le simulateur sur votre machine locale, suivez ces étapes :

1.  **Clonez le dépôt** (si ce n'est pas déjà fait) :
    ```bash
    git clone <URL_DU_DEPOT>
    cd <NOM_DU_DOSSIER>
    ```

2.  **Créez un environnement virtuel** :
    ```bash
    python -m venv venv
    ```

3.  **Activez l'environnement virtuel** :
    -   Sur Windows :
        ```bash
        .\venv\Scripts\activate
        ```
    -   Sur macOS/Linux :
        ```bash
        source venv/bin/activate
        ```

4.  **Installez les dépendances** :
    ```bash
    pip install -r requirements.txt
    ```

## Utilisation

Une fois l'installation terminée, lancez l'application avec la commande suivante :

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur web.

## Structure du Projet

Le projet est organisé de manière modulaire pour séparer les différentes logiques :

```
.shor_simulator/
├── classical/            # Modules pour les calculs classiques (PGCD, fractions continues...)
│   ├── continued_fraction.py
│   ├── explanations.py
│   └── preprocessing.py
├── quantum/              # Modules pour la simulation quantique
│   ├── circuit_visualizer_clean.py
│   └── quantum_register.py
├── utc/                  # Ressources graphiques
│   └── image.png
├── .gitignore            # Fichier pour ignorer les fichiers non désirés par Git
├── app.py                # Fichier principal de l'application Streamlit
├── README.md             # Ce fichier
├── requirements.txt      # Liste des dépendances Python
└── style.css             # Fichier de style pour l'interface
```

## Auteurs et Encadrement

Ce projet a été développé par :
-   **Jefferson MBOUOPDA**
-   **Ruben MOUGOUE**

Sous la responsabilité de :
-   **Ahmed LOUNIS**

Et la supervision de :
-   **Vincent ROBIN**
