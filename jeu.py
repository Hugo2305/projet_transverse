"""
Fichier principal, à exectuer pour lancer le jeu.
"""


import pygame, time

from moteur import *

class Jeu:
    """
    Classe qui gère le jeu.

    L'utilisation de la POO pour encapsuler le jeu dans une classe
    permet d'avoir accès à ses attributs et donc à tous les éléments 
    du jeu depuis n'importe quelle partie du code.

    Cela nous evite d'utiliser des variables globales et de devoir
    définir des fonctions a 40 paramètres répétitifs.
    """
    def __init__(self):
        # Définition de l'ecran
        self.ecran = pygame.display.set_mode((1280, 720))
        # Définition de l'horloge
        self.horloge = pygame.time.Clock()
        # Initialisation du "dernier temps", utile au calcul du delta time
        self.dernier_temps = time.time()

        self.scene = Scene(self)

    def delta_time(self):
        """
        Le delta time permet de calculer le temps entre deux iterations de 
        notre jeu.

        Nous pouvons ainsi controler la vitesse des evenements du jeu en fonction
        de si celui-ci s'accélère ou se ralentit.

        Par exemple, dans un jeu à 30 FPS, les objets doivent être 2 fois plus 
        rapides que dans jeu à 60 FPS car il y a moins de frames par secondes 
        pour affecter les objets.
        """
        # Le delta time représente la différence de temps entre celui mesuré à l'appel
        # de la méthode, et celui mesuré à la dernière itération, multuplié par 60
        # Une valeur choisie arbitrairement pour uniformiser la vitesse des objets
        # pour que dt = 1, à 60 FPS, une valeur courante dans le jeu vidéo.
        self.dt = (time.time() - self.dernier_temps) * 60
        # On recalcule ensuite le dernier temps.
        self.dernier_temps = time.time()

    def boucle(self):
        """
        Boucle du jeu qui s'execute en continu jusqu'à la fin de celui-ci
        """
        while True:
            # Evenements pygame
            for event in pygame.event.get():
                # Lorqu'on ferme le jeu ...
                if event.type == pygame.QUIT:
                    # ... on le quitte
                    pygame.quit() 
            # Tour de l'horloge du jeu
            self.horloge.tick(1000)
            # Actualisation de l'affichage
            pygame.display.update()

# Démarrage du jeu et de sa boucle.
Jeu().boucle()
