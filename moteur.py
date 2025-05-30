"""
Fichier gérant toute la partie inhérente au moteur de jeu, gestion des objets,
scènes, ...
"""


class Scene:
    """
    Cette classe gère la scène de jeu dans laquelle tous les objets de 
    celui-ci sont contenus.

    Elle se comporte comme un dictionnaire où chaque clé représente le nom 
    d'une salle, et sa valeur associée, la liste des objets présentes dans la 
    salle.
    """
    def __init__(self, jeu):
        self.jeu = jeu 
        # Initialisation des salles
        self.salles = {"defaut" : []}
        self.salle_actuelle = "defaut"

    def actualiser(self):
        """
        Actualise la salle courante et donc tous les objets qui s'y trouvent
        """
        # Objets présents à la fin de l'actualisation de la salle
        objets = []

        for objet in self.salles[self.salle_actuelle]:
            # On actualise que les objets qui doivent l'être
            if objet.actualiser_:
                objet.actualiser(self)
            # On ne garde que les objets vivants au sein de la salle
            if objet.vivant:
                objets.append(objet)
                
        # Assignation des objets de la salle selon ceux qui ont été gardés
        self.salles[self.salle_actuelle] = objets

    def filtrer(self, etiquette, salle=None):
        """
        Permet de filtrer les objets présents dans une salle en fonction d'une
        etiquette demandée.
        """
        # Si la salle n'est pas précisé, on ciblera la salle courante
        if salle == None:
            salle = self.salle_actuelle

        # On récupère les objets qui ont l'etiquette recherchée
        objets = []
        for objet in self.salles[salle]:
            if etiquette in objet.etiquettes:
                objets.append(objet)
                
        # Avant de les retourner
        return objets
    

class Objet:
    """
    Cette classe, qui a vocation à être héritée, définit 
    les composantes de base d'un objet dans le moteur de jeu
    qui sont les suivantes : 

    ATTRIBUTS ->

    * jeu          (Jeu) : référance à l'instance de la classe 'Jeu' 
    * z_pos      (float) : ordre d'actualisation de l'objet, utile pour gérer
    la superposition des objets (pour mettre l'arrière plan derrière
    le joueur par exemple)
    * vivant      (bool) : vérifie si l'objet est encore vivant 
    * actualiser_ (bool) : vérifie si l'objet doit encore être actualisé
    * etiquettes   (set) : permet d'individualiser les objets en leur collant
    des etiquettes. L'utilisation d'un set assure qu'il n'y a pas de doublons.

    METHODES ->
    * actualiser : apelée si l'objet doit être actualisé

    """
    def __init__(self, jeu, z_pos:float):
        self.jeu = jeu
        self.z_pos = z_pos
        self.vivant = True 
        self.actualiser_ = True
        self.etiquettes = set({})

    def actualiser(self, scene:Scene): # 'scene' représente la scène depuis laquelle l'objet est actualisé
        pass
