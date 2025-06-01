"""
Définition individuelle des objets.
"""

from moteur import *

class GestionnaireMenu(Objet):
    def __init__(self, jeu):
        super().__init__(jeu)
        
    def actualiser(self, scene):
        self.jeu.dessiner(self.jeu.images["fond_menu"], (0, 0))
        print("Menu")
        
class GestionnaireJeu(Objet):
    def __init__(self, jeu):
        super().__init__(jeu)
        
    def actualiser(self, scene):
        print("Jeu")