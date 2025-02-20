# Collection de Jeux Python
[English](../README.md) | [中文](README-cn.md) | [日本語](README-ja.md) | [한국어](README-ko.md) | Français | [فارسی](README-fa.md)

Une collection de jeux d'arcade et de puzzle classiques construite avec Pygame, proposant sept jeux divertissants : Casse-briques, Serpent, Pac-Man, Tetris, Pong, Gomoku (Cinq en ligne) et 2048. Le projet implémente des transitions de menu fluides, le support de la manette de jeu et un design d'interface moderne. Parfait pour l'apprentissage du développement de jeux et le divertissement.

## Démarrage Rapide

### Configuration Requise

- Python 3.8 ou supérieur
- Pygame 2.0 ou supérieur
- Autres dépendances listées dans requirements.txt

### Installation

1. Assurez-vous que Python 3.8 ou supérieur est installé
2. Installez les dépendances requises :
   ```bash
   pip install -r requirements.txt
   ```

### Lancement du Jeu

```bash
# Exécuter le menu du jeu
python main.py
```

## Liste des Jeux

1. **Casse-briques**
   - Jeu classique de casse-briques
   - Briques de différentes couleurs avec des valeurs de points variables
   - Mécanique de rebond de balle basée sur l'angle

2. **Serpent**
   - Version moderne du jeu du serpent classique
   - Contrôles fluides et détection des collisions
   - Suivi du score et difficulté progressive

3. **Pac-Man**
   - Jeu de style Pac-Man simplifié
   - Ennemis de différentes couleurs
   - Collecte de points pour marquer

4. **Tetris**
   - Jeu de puzzle classique d'empilement de blocs
   - Formes de blocs multiples
   - Mécanique d'effacement de lignes

5. **Pong**
   - Jeu de Pong compétitif à deux joueurs
   - Physique de balle basée sur l'angle
   - Premier à 5 points gagne

6. **Gomoku**
   - Jeu traditionnel de Gomoku
   - Contrôles simples et intuitifs
   - Condition de victoire : aligner 5 pierres

7. **2048**
   - Jeu de puzzle populaire
   - Fusionnez les tuiles pour atteindre 2048
   - Défiez les meilleurs scores

## Structure du Projet

```
.
├── main.py          # Point d'entrée du programme principal
├── games/           # Répertoire des modules de jeux
│   ├── __init__.py
│   ├── breakout.py  # Jeu de casse-briques
│   ├── snake.py     # Jeu du serpent
│   ├── pacman.py    # Jeu de Pac-Man
│   ├── tetris.py    # Jeu de Tetris
│   ├── pong.py      # Jeu de Pong
│   ├── gomoku.py    # Jeu de Gomoku
│   └── game2048.py  # Jeu 2048
├── requirements.txt  # Dépendances du projet
├── build.py         # Script de construction
└── resources/       # Fichiers de ressources
    └── icon.ico     # Icône de l'application
```

## Contrôles

### Contrôles Clavier
- Touches fléchées : Navigation dans les menus et contrôle des jeux
- Entrée : Sélection des éléments du menu
- ESC : Pause du jeu/retour au menu
- R : Redémarrer le jeu
- I : Afficher/masquer les instructions

### Contrôles Manette
- Stick gauche/Croix directionnelle : Navigation dans les menus et contrôle des jeux
- Bouton A : Sélectionner/confirmer
- Bouton B : Retour/annuler
- Bouton Start : Pause du jeu
- Boutons X/Y : Contrôles supplémentaires spécifiques aux jeux

### Contrôles Spécifiques aux Jeux

#### Casse-briques
- Flèches gauche/droite : Déplacer la raquette
- Manette : Utiliser le stick gauche ou la croix directionnelle pour déplacer la raquette

#### Serpent
- Touches fléchées : Changer de direction
- Manette : Utiliser le stick gauche ou la croix directionnelle pour se déplacer

#### Pac-Man
- Touches fléchées : Déplacer le personnage
- Manette : Utiliser le stick gauche ou la croix directionnelle pour se déplacer

#### Tetris
- Gauche/Droite : Déplacer le bloc
- Haut : Rotation du bloc
- Bas : Accélérer la chute
- Espace : Chute instantanée
- Manette : Stick gauche/croix directionnelle pour déplacer, bouton A pour pivoter

#### Pong
- Joueur 1 : Touches W/S
- Joueur 2 : Flèches haut/bas
- Manette 1 : Stick gauche contrôle la raquette gauche
- Manette 2 : Stick gauche contrôle la raquette droite

#### Gomoku
- Souris : Cliquer pour placer une pierre
- Manette : Utiliser le stick gauche/croix directionnelle pour déplacer le curseur, bouton A pour placer une pierre

#### 2048
- Touches fléchées : Déplacer les tuiles
- Manette : Utiliser le stick gauche/croix directionnelle pour déplacer les tuiles

## Fonctionnalités

- Transitions de menu fluides et animations d'échelle
- Support complet des manettes de jeu
- Système de tutoriel pour chaque jeu
- Menu pause avec options de sauvegarde/quitter
- Difficulté de jeu progressive
- Système de suivi des scores
- Interface moderne et retour visuel

## Construction pour Distribution

Ce projet utilise PyInstaller pour l'empaquetage en exécutables autonomes.

### Étapes de Construction

1. Installer PyInstaller :
   ```bash
   pip install pyinstaller
   ```

2. Exécuter la commande de construction :
   ```bash
   # Windows
   pyinstaller build.py --onefile --noconsole --icon=icon.ico --name="GameCollection"
   ```

3. L'exécutable sera généré dans le répertoire `dist`

## Guide de Développement
### Ajouter un Nouveau Jeu

Pour ajouter un nouveau jeu, suivez ces étapes :

1. Créez un nouveau fichier Python
2. Implémentez une classe Game avec les méthodes requises suivantes :
   - `__init__()`: Initialisation de l'état du jeu
   - `run()`: Boucle principale du jeu
   - `handle_input()`: Gestion des entrées utilisateur
   - `update()`: Mise à jour de l'état du jeu
   - `draw()`: Rendu graphique
3. Ajoutez les informations du jeu dans `main.py`

## Licence

Ce projet est sous licence MIT.

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à soumettre des Pull Requests.