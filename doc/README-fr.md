# Collection de Jeux Python
[English](../README.md) | [中文](README-cn.md) | [日本語](README-ja.md) | [한국어](README-ko.md) | Français | [فارسی](README-fa.md)

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