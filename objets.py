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
        if self.jeu.horloge_transition == -1:
            self.jeu.jouer_son("menu_click", 1)
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
        if not pygame.mixer.Channel(0).get_busy():
            self.jeu.jouer_son("menu", 0)

# Le reste est assez similaire

class GestionnaireJeu(Objet):
    def __init__(self, jeu):
        super().__init__(jeu)
        
    def actualiser(self, scene):
        self.jeu.dessiner(self.jeu.images["fond_menu"], (0, 0))
        self.jeu.dessiner(self.jeu.images["sol"], (0, 0))
        if not pygame.mixer.Channel(0).get_busy():
            self.jeu.jouer_son("jeu", 0)
        
class GestionnaireCredits(Objet):
    def __init__(self, jeu):
        super().__init__(jeu)
        
    def actualiser(self, scene):
        self.jeu.dessiner(self.jeu.images["fond_menu"], (0, 0))
        
        
class Joueur(Entitee):
    """ 
    Le Joueur est bel et bien une entitée car affecté par la 
    physique.
    """ 
    def __init__(self, jeu, position):
        super().__init__(jeu, position)
        # Direction dans laquelle le joueur regarde
        self.direction = "gauche"
        # Deux variables pour vérifier séparément si on touche le sol
        # PS : c'est utile car le joueur fait des petits rebons quand 
        # il se déplace et quitte donc le sol brievement, on veut quand 
        # même pouvoir sauter si c'est le cas.
        self.touche_sol = False
        self.touche_sol_ = False
    
    def actualiser(self, scene):
        super().actualiser(scene)
        self.logique_verticale()
        self.controles()
        self.dessiner()
        self.logique_attaque(scene)
        
    def logique_attaque(self, scene):
        print(scene)
        if self.jeu.souris_pressee:
            scene.lier(Boule(self.jeu, (self.x, self.y)), "jeu")
        
    def controles(self):
        """  
        Gère les touches de clavier
        """
        # Déplacement vers la gauche
        if self.jeu.touches[pygame.K_q]:
            self.dx = -10
            self.direction = "gauche"
        # Déplacement vers la droite
        if self.jeu.touches[pygame.K_d]:
            self.dx = 10
            self.direction = "droite"
        # Si aucune touche n'est préssée
        if not (self.jeu.touches[pygame.K_RIGHT] or self.jeu.touches[pygame.K_LEFT]):
            # On freine le joueur
            self.dx *= 0.8 ** self.jeu.dt
        # Logique des rebons
        if self.touche_sol_ and (self.jeu.touches[pygame.K_q] or self.jeu.touches[pygame.K_d]):
            # Qui sont des petits sauts
            self.dy = -10
            self.touche_sol_ = False
    
    def logique_verticale(self):
        # Gravité
        self.dy += 1.2 * self.jeu.dt
        # Si on tombe en dessous du sol
        if self.y > 550:
            # On annule notre vitesse vertivale
            self.dy = 0
            # Et on indique dans une variable que le sol a été touché
            self.touche_sol = True
            self.touche_sol_ = True
        # Si on touche le sol et qu'on appuye sur espace
        if self.touche_sol and self.jeu.touches[pygame.K_SPACE]:
            # On saute
            self.dy = -20
            # Et le sol n'est plus touché
            self.touche_sol = False
            
    def dessiner(self):
        # On récup_re l'image du joueur
        image = self.jeu.images["joueur"]
        # Elle est ensuite inversée selon la direction de celui-ci
        if self.direction == "gauche":
            image = pygame.transform.flip(image, True, False)
        # Enfin on la dessine
        self.jeu.dessiner(
            image, 
            # Avec des décalages, pour l'image epouse la position du joueur
            (self.x - 72, self.y - 350)
        )
        
class Boule(Entitee):
    """ 
    Représente les boules d'energie que le joueur peut tirer.
    """ 
    def __init__(self, jeu, position):
        super().__init__(jeu, position)
        self.dx = 5
    
    def actualiser(self, scene):
        super().actualiser(scene)
        self.appliquer_gravite()
        self.dessiner()
        
    def appliquer_gravite(self):
        self.dy += 0.8 * self.jeu.dt
    
    def dessiner(self):
        self.jeu.dessiner(self.jeu.images["boule"], (self.x, self.y))
