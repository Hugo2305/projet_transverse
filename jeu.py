"""
Fichier principal, à exectuer pour lancer le jeu.
"""


import pygame, time, sys, math, random

from moteur import *
from objets import *

def gaussienne_normalisee(x: float, centre: float = 0.5, ecart_type: float = 0.2) -> float:
    """
    fonction retournant une forme de cloche (comme la courble du Q.I) : 
    
    #
    |     ###
    |    #   #
    |  ##     ##
    |##         ##
    #--------------#
    
    Utile pour l'animation de transition (utilisée pour la gestion de la transparence)
    """
    coef = 1 / (math.exp(-((centre - centre) ** 2) / (2 * ecart_type ** 2)))
    return coef * math.exp(-((x - centre) ** 2) / (2 * ecart_type ** 2))

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
        self.ecran_ = pygame.display.set_mode((1280, 720), pygame.SCALED)
        self.horloge = pygame.time.Clock()
        
        # L'utilisation de deux ecran permet la gestion de l'effet de tremblement
        self.ecran = pygame.Surface((1280, 720))
        
        # L'horloge de transition gère le timing des transitions
        self.horloge_transition = -1
        
        # Verifie si la souris passe sur un boutton
        self.souris_sur_boutton = False
        
        # Initialisation du "dernier temps", utile au calcul du delta time
        self.dernier_temps = time.time()
        
        # Chargement des ressources
        self.charger_images()
        
        TAILLE_BOUTTON = self.images["boutton"].get_size()

        # Initialisation de la scène
        self.scene = Scene(self)
        
        # Et des salles
        self.scene.nouvelle_salle("menu")
        self.scene.nouvelle_salle("jeu")
        self.scene.nouvelle_salle("credits")
        
        # Lien de chaque objet à chaque salle
        self.scene.lier(GestionnaireMenu(self), "menu")
        self.scene.lier(GestionnaireJeu(self), "jeu")
        self.scene.lier(GestionnaireCredits(self), "credits")
        self.scene.lier(Boutton(self, (900, 150), TAILLE_BOUTTON, 0), "menu")
        self.scene.lier(Boutton(self, (900, 350), TAILLE_BOUTTON, 1), "menu")
        self.scene.lier(Boutton(self, (900, 550), TAILLE_BOUTTON, 2), "menu")
        
        # On débute le jeu dans le menu
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
                        # On met en plein ecran quand F11 est pressé
                        pygame.display.toggle_fullscreen()
                        
            # Tour de l'horloge du jeu
            self.horloge.tick(1000)
            # Actualisation de l'affichage
            pygame.display.update()
            self.gerer_tremblement()
            # On actualise la scène
            self.scene.actualiser()
            # Et gère les transitions
            self.gerer_transition()
            
    def quitter(self):
        pygame.quit()
        sys.exit()
         
    def charger_images(self):
        """
        Charge toutes les images dans un dictionnaire.
        """
        self.images = {
            "fond_menu" : pygame.transform.scale(pygame.image.load("images/fond.png"), (1280, 720)).convert_alpha(),
            "boutton" : pygame.image.load("images/boutton.png").convert_alpha(),
            "logo" : pygame.transform.scale(pygame.image.load("images/logo.png"), (1000, 1000)).convert_alpha()
        }
        
    def dessiner(self, surface, position):
        self.ecran.blit(surface, position)
        
    def lancer_transition(self, salle):
        """ 
        Débute une transition
        """
        # Salle ou transitionner
        self.salle_cible = salle
        # Demarre l'horloge de transition (par défaut à -1 lorqu'il n'y a aucune transition)
        self.horloge_transition = 0
        
    def gerer_transition(self):
        # Si l'horloge de transition est active
        if self.horloge_transition != -1:
            # On augmente celle-ci (limité à 1)
            self.horloge_transition = min(self.horloge_transition + 0.01 * self.dt, 1)
            # On affiche le rectangle transparant (qui est l'utilité même de la transition)
            self.afficher_transition()
            # A la moitié de la transition, on change de salle (car l'ecran est completement noir à la mi transition)
            if self.horloge_transition > 0.5:
                self.scene.changer_salle(self.salle_cible)
            # Si on atteint 1, on arrête la transition
            if self.horloge_transition == 1:
                self.horloge_transition = -1
                
    def afficher_transition(self):
        """  
        Cette méthode sert simplement à afficher le rectangle 
        transparant qui apparait lors des transitions.
        """
        # On crée une nouvelle surface de la taille de l'ecran
        surface = pygame.surface.Surface((1280, 720))
        # On la rend noire
        surface.fill((0, 0, 0))
        # On définit sa transparance grâce à une courble gaussienne
        surface.set_alpha(gaussienne_normalisee(self.horloge_transition) * 255)
        # Enfin, on la dessine
        self.dessiner(surface, (0, 0))
        
    def generer_texte(self, texte:str, police:pygame.font.Font, taille:int,  gras:bool=False, antialias:bool=True, couleur:Tuple[int, int, int]=(0, 0, 0)):
        """
        Permet de générer une surface avec un texte inscrit dessus
        """
        police_ = pygame.font.SysFont(police, taille, gras)
        return police_.render(texte, antialias, couleur)
        
    def logique_curseur(self):
        """  
        Permet simplement de modifier le curseur de la souris selon 
        si un boutton la touche ou non. 
        """
        if self.souris_sur_boutton:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) # Curseur en mode "main"
        else: 
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) # Curseur classique
            
    def gerer_tremblement(self):
        if self.horloge_transition == -1:
            self.ecran_.blit(self.ecran, (0, 0))
        else:
            self.ecran_.blit(self.ecran, (random.randint(-5, 5), random.randint(-5, 5)))
            
# Démarrage du jeu et de sa boucle.
Jeu().boucle()
