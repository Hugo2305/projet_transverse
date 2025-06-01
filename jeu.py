"""
Fichier principal, à exectuer pour lancer le jeu.
"""


import pygame, time, sys

from moteur import *
from objets import *

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
        # Initialisation classique de pygame
        pygame.init()
        self.ecran = pygame.display.set_mode((1280, 720), pygame.SCALED)
        self.horloge = pygame.time.Clock()
        
        self.souris_sur_boutton = False
        
        # Initialisation du "dernier temps", utile au calcul du delta time
        self.dernier_temps = time.time()
        
        # Chargement des ressources
        self.charger_images()
        
        TAILLE_BOUTTON = self.images["boutton"].get_size()

        # Initialisation des scenes
        self.scene = Scene(self)
        
        self.scene.nouvelle_salle("menu")
        self.scene.nouvelle_salle("jeu")
        self.scene.nouvelle_salle("credits")
        
        self.scene.lier(GestionnaireMenu(self), "menu")
        self.scene.lier(GestionnaireJeu(self), "jeu")
        self.scene.lier(Boutton(self, (1280 // 2, 150), TAILLE_BOUTTON, 0), "menu")
        self.scene.lier(Boutton(self, (1280 // 2, 350), TAILLE_BOUTTON, 1), "menu")
        self.scene.lier(Boutton(self, (1280 // 2, 550), TAILLE_BOUTTON, 2), "menu")
        
        self.scene.changer_salle("menu")

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
            self.delta_time()
            self.logique_curseur()
            self.souris_sur_boutton = False
            # Evenements pygame
            for event in pygame.event.get():
                # Lorqu'on ferme le jeu ...
                if event.type == pygame.QUIT:
                    # ... on le quitte
                    self.quitter()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()
            # Tour de l'horloge du jeu
            self.horloge.tick(1000)
            # Actualisation de l'affichage
            pygame.display.update()
            self.ecran.fill((0, 0, 0))
            self.scene.actualiser()
            
    def quitter(self):
        pygame.quit()
        sys.exit()
    
            
    def charger_images(self):
        self.images = {
            "fond_menu" : pygame.transform.scale(pygame.image.load("images/fond.png"), (1280, 720)).convert_alpha(),
            "boutton" : pygame.image.load("images/boutton.png").convert_alpha()
        }
        
    def dessiner(self, surface, position):
        self.ecran.blit(surface, position)
        
    def generer_texte(self, texte:str, police:pygame.font.Font, taille:int,  gras:bool=False, antialias:bool=True, couleur:Tuple[int, int, int]=(0, 0, 0)):
        police_ = pygame.font.SysFont(police, taille, gras)
        return police_.render(texte, antialias, couleur)
        
    def logique_curseur(self):
        if self.souris_sur_boutton:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            


# Démarrage du jeu et de sa boucle.
Jeu().boucle()
