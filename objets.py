"""
Définition individuelle des objets.
"""
import pygame, time, math, random
from moteur import *
from typing import *

SCORE = 0

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
salle, ils permettent d'effectuer des actions ciblées sur chaque 
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
        self.jeu.dessiner(self.jeu.images["logo"], (-200, -110 + math.sin(time.time() * 2) * 40))
        # Musique du menu
        if not pygame.mixer.Channel(0).get_busy():
            self.jeu.jouer_son("menu", 0)

class GestionnaireJeu(Objet):
    def __init__(self, jeu):
        super().__init__(jeu)
        
    def actualiser(self, scene):
        self.jeu.dessiner(self.jeu.images["fond_menu"], (0, 0))
        self.jeu.dessiner(self.jeu.images["sol"], (0, 0))
        try:
            debut = True
            joueur = scene.filtrer("joueur")[0]
        except:
            debut = False
        # Musique du jeu
        if not pygame.mixer.Channel(0).get_busy():
            self.jeu.jouer_son("jeu", 0)
        if random.randint(1, 300) == 3 and debut:
            joueur.balles += 1
            if random.randint(1, 2) == 1:
                scene.lier(Ennemi1(self.jeu, (-200, 300), "droite"))
            else:
                scene.lier(Ennemi1(self.jeu, (2000, 300), "gauche"))
        if debut:
            texte_score = self.jeu.generer_texte("SCORE | " + str(SCORE), "arial", 60, True, fond=(255, 255, 255))
            self.jeu.dessiner(texte_score, (30, 10))
            texte_balles = self.jeu.generer_texte("MANA | " + str(joueur.balles), "arial", 60, True, fond=(255, 255, 255))
            self.jeu.dessiner(texte_balles, (950, 10)) 
        
class Joueur(Entitee):
    """ 
    Le Joueur est bel et bien une entitée car affecté par la 
    physique.
    """ 
    def __init__(self, jeu, position):
        super().__init__(jeu, position)
        self.z_pos = 3
        # Direction dans laquelle le joueur regarde
        self.direction = "gauche"
        # Deux variables pour vérifier séparément si on touche le sol
        # PS : c'est utile car le joueur fait des petits rebons quand 
        # il se déplace et quitte donc le sol brievement, on veut quand 
        # même pouvoir sauter si c'est le cas.
        self.touche_sol = False
        self.touche_sol_ = False
        self.balles = 2
    
    def actualiser(self, scene):
        super().actualiser(scene)
        self.logique_verticale()
        self.controles()
        self.dessiner()
        self.logique_attaque(scene)
        self.ajouter_etiquette("joueur")
        self.rectangle = pygame.Rect(self.x, self.y, 50, 50)
        
    def logique_attaque(self, scene):
        if self.jeu.souris_pressee and self.balles > 0:
            # On récupère la position de la souris
            x, y = pygame.mouse.get_pos()
            # On calcule l'angle à l'horizontale du vecteur entre la position
            # de la souris et celle du joueur
            angle = math.atan2(x - self.x, y - self.y)
            # On récupère le cosinus et sinus de l'angle
            cos, sin = math.cos(angle), math.sin(angle)
            # On injecte ces valeurs dans le code de la boule
            scene.lier(Boule(self.jeu, (self.x - 50, self.y - 70),  (cos, sin)), "jeu")
            self.jeu.jouer_son("laser", random.randint(10, 1000))
            self.balles -= 1
        
    def controles(self):
        """  
        Gère les touches de clavier
        """
        # Déplacement vers la gauche
        if self.jeu.touches[pygame.K_q] and self.x > 0:
            self.dx = -10
            self.direction = "gauche"
        # Déplacement vers la droite
        if self.jeu.touches[pygame.K_d] and self.x < 1230:
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
            self.dy = -30
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
        
class Ennemi1(Entitee):
    """ 
    La logique du premier ennemi est quasiment la même que celle du joueur.
    Seul les controles et quelque details sont différents.
    """ 
    def __init__(self, jeu, position, direction):
        super().__init__(jeu, position)
        self.direction = direction
        self.ajouter_etiquette("ennemi1")
        if self.direction == "gauche":
            self.dx = -10
        else:
            self.dx = 10
        self.touche_sol = False
        self.touche_sol_ = False
        self.mort = False
    
    def actualiser(self, scene):
        super().actualiser(scene)
        joueur = scene.filtrer("joueur")[0]
        self.rectangle = pygame.Rect(self.x - 50, self.y - 280, 100, 200)
        self.logique_verticale()
        self.ia()
        self.dessiner()
        self.verif_touche(scene)
        if self.rectangle.colliderect(joueur.rectangle):
            self.jeu.lancer_transition("menu")
            self.jeu.jouer_son("menu", 0)
            for objet in scene.salles[scene.salle_actuelle]:
                if "ennemi1" in objet.etiquettes:
                    objet.tuer()
                    
        
    def ia(self):
        # Comme le joueur, l'ennemi effectue des petits sauts en continu
        if self.touche_sol_:
            self.dy = -10
            self.touche_sol_ = False
        # On tue les ennemis trop eloignés de la carte
        if self.x > 3000 or self.x < -1000 or self.y > 2000:
            self.tuer()
            
    def verif_touche(self, scene):
        global SCORE
        boules = scene.filtrer("boule")
        for balle in boules:
            if balle.rectangle.colliderect(self.rectangle):
                self.mort = True
                balle.tuer()
                SCORE += 1
    
    def logique_verticale(self):
        self.dy += 1.2 * self.jeu.dt
        if not self.mort:
            if self.y > 695:
                self.dy = 0
                self.touche_sol = True
                self.touche_sol_ = True
            if self.touche_sol and random.randint(1, 100) == 5:
                self.dy = -20
                self.touche_sol = False
        else:
            self.dx = 0
            
    def dessiner(self):
        image = self.jeu.images["ennemi1"]
        image = pygame.transform.flip(image, self.direction == "gauche", self.mort)
        self.jeu.dessiner(
            image, 
            (self.x - 72, self.y - 350)
        )
        
class Boule(Entitee):
    """ 
    Représente les boules d'energie que le joueur peut tirer.
    
    Un petit point sur la physique: 
    on a calculé l'angle à l'horizontale du vecteur entre la position du 
    joueur et de la souris.
    
    Les cosinus et sinus de cet angle nous permettent de définir la vitesse
    initiale de la boule pour qu'elle suive la souris.
    La gravité s'occupe ensuite de la faire tomber.
    
    Il n'est pas nécéssaire et nous n'avons pas choisit d'intégrer les equations
    du second degré de newton concernant la chute d'un corps puisque l'utilisation
    de la gravité, qui est une accélération, dérive (littéralement) de ces equations.
    Si on prends une equation de position en fonction du temps, et qu'on la dérive 
    deux fois, on obtiens une equation d'accélération en fonction du temps, qui est 
    constante (car dériver un polynôme baisse son degré d'une unité).
    Etant constante, on a juste a ajuster la vitesse de notre boule pour lui appliquer
    la gravité et la trajectoire voulue en suivra.
    """ 
    def __init__(self, jeu, position, trigo):
        super().__init__(jeu, position)
        # On coeficiente plus fort la vitesse horizontale pour créer 
        # un gameplay plus horizontal, ce qui est cohérent avec notre jeu
        self.dx = 40 * trigo[1] 
        self.dy = 30 * trigo[0]
        self.ajouter_etiquette("boule")
        self.rectangle = pygame.Rect(self.x + 15, self.y + 7, 100, 100)
    
    def actualiser(self, scene):
        super().actualiser(scene)
        self.appliquer_gravite()
        self.rectangle = pygame.Rect(self.x + 15, self.y + 7, 100, 100)
        self.dessiner()
        if self.y > 2000:
            self.tuer()
        
    def appliquer_gravite(self):
        self.dy += 1.2 * self.jeu.dt
    
    def dessiner(self):
        self.jeu.dessiner(self.jeu.images["boule"], (self.x, self.y))
