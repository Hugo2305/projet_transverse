"""
Définition individuelle des objets.
"""
import pygame, time, math
from moteur import *
from typing import *

class Boutton(Objet):
    """
    Le boutton est un objet rectangulaire associé à une image qui peut 
    être cliqué pour effectuer des actions diverses.
    """
    def __init__(self, jeu, position:Tuple[int, int], taille:Tuple[int, int], id):
        super().__init__(jeu, z_pos=1)
        self.position = position
        self.taille_initiale = taille
        self.taille = taille
        self.texte = ""
        self.zoom = 0.5 
        self.id = id # L'id permet d'identifier les bouttons entre eux
        self.actualiser_rectangle()
        
    def actualiser_rectangle(self):
        
        """
        On modifie la taille en continu pour l'adapter au zoom,
        c'est utile pour redimensionner le boutton en cas de 
        besoin.
        """
        self.taille = (
            self.taille_initiale[0] * self.zoom, 
            self.taille_initiale[1] * self.zoom
        )
        
        """
        sur pygame, la position donnée à un rectangle 
        est celle du coin supérieur droit : 
        
        P : (x, y)
        
        P---------*
        |         |
        |         |
        |         |
        *---------*
            
        Nous devons décaler la position entrée en fonction
        de la taille du rectangle pour qu'il soit centré 
        en la position finale.
        
        P : (x + taille_en_x / 2, y + taille_en_y / 2) 
        
        *---------*
        |         |
        |    P    |
        |         |
        *---------*

        L'axe des ordonnées est bien sur inversé en pygame c'est 
        pour cela qu'ajouter une valeur à un point en y le fait 
        "descendre" au lieu de "monter".
            
        """
        
        self.rectangle = pygame.Rect(
            # Ici on retranche la taille en x et en y
            # au lieu de l'augmenter car on décale le 
            # rectangle au complet et non un point.
            self.position[0] - self.taille[0] / 2, 
            self.position[1] - self.taille[1] / 2,
            self.taille[0],
            self.taille[1]
        )
        
    def actualiser(self, scene):
        # Logique individuelle de chaque boutton
        self.logiques_separees(scene)
        
        # On verifie si la souris touche le boutton
        if self.rectangle.collidepoint(pygame.mouse.get_pos()):
            self.jeu.souris_sur_boutton = True
            # Si en plus on clique ...
            if pygame.mouse.get_pressed()[0]:
                # On apelle la méthode designée à l'action du boutton
                self.click(scene) 
            
        self.actualiser_rectangle()
        self.dessiner()
        self.animation()

    def animation(self):
        """
        Gère l'animation du boutton qui grandit ou se recracte selon s'il touche la souris
        """
        if self.rectangle.collidepoint(pygame.mouse.get_pos()):
            # Incrémentation limitée à 0.8
            self.zoom = min(self.zoom + 0.01 * self.jeu.dt, 0.8)
        else:
            # Décrémentation limitée à 0.7
            self.zoom = max(self.zoom - 0.01 * self.jeu.dt, 0.7)
            
    def dessiner(self):
        self.jeu.dessiner(
            # On prends bien soin de redimensionner l'image en fonction de la taille du boutton
            pygame.transform.scale(self.jeu.images["boutton"], self.taille), 
            # On l'affiche au coin supérieur droit du boutton
            self.rectangle.topleft
        )
        
        # Dessin du texte
        
        # On génère le texte
        texte = self.jeu.generer_texte(self.texte, "arial", 80, gras=True)
        # On l'adapte à la taille du boutton 
        texte = pygame.transform.scale(texte, self.taille)
        # Enfin, on le dessine
        self.jeu.dessiner(texte, self.rectangle.topleft)
    
    def logiques_separees(self, scene):
        # Gère le texte de chaque boutton
        if self.id == 0:
            self.texte = "  Jouer  "
        if self.id == 1:
            self.texte = " Quitter "
        if self.id == 2:
            self.texte = " Credits "
            
    def click(self, scene):
        if self.id == 0: 
            # Transite vers la salle nommée "jeu"
            self.jeu.lancer_transition("jeu")
        if self.id == 1:
            # Quitte le jeu
            self.jeu.quitter()
        if self.id == 2:
            # Transite vers la salle "credits"
            self.jeu.lancer_transition("credits")
            
"""
Les gestionnaires sont des objets génériques, il y en a un par 
scène, ils permettent d'effectuer des actions ciblées sur chaque 
salle.
"""
class GestionnaireMenu(Objet):
    def __init__(self, jeu):
        super().__init__(jeu)
        
    def actualiser(self, scene):
        # Affichage du fond d'ecran
        self.jeu.dessiner(self.jeu.images["fond_menu"], (0, 0))
        # Dessin du logo
        # PS : l'utilisation d'une fonction sinusoidale du temps donne l'effet de va et viens du logo
        self.jeu.dessiner(self.jeu.images["logo"], (-200, -140 + math.sin(time.time() * 2) * 40))

# Le reste est assez similaire

class GestionnaireJeu(Objet):
    def __init__(self, jeu):
        super().__init__(jeu)
        
    def actualiser(self, scene):
        self.jeu.dessiner(self.jeu.images["fond_menu"], (0, 0))
        
class GestionnaireCredits(Objet):
    def __init__(self, jeu):
        super().__init__(jeu)
        
    def actualiser(self, scene):
        self.jeu.dessiner(self.jeu.images["fond_menu"], (0, 0))