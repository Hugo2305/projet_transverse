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
        for objet in self.salles[self.salle_actuelle].copy():
            # On actualise que les objets qui doivent l'être
            if objet.actualiser_:
                objet.actualiser(self)
            # On ne garde que les objets vivants au sein de la salle
            if objet.vivant:
                objets.append(objet)
                
        # Assignation des objets de la salle selon ceux qui ont été gardés
        if not self.salle_changee:
            self.salles[self.salle_actuelle] = objets
        self.salle_changee = False

    def filtrer(self, etiquette:str, salle:str=None):
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
    
    def lier(self, objet, salle:str=None):
        """
        Permet de lier un objet a une salle.
        """
        if salle == None:
            salle = self.salle_actuelle
        self.salles[salle].append(objet)
        
    def nouvelle_salle(self, nom:str):
        self.salles[nom] = []
        
    def changer_salle(self, nom:str):
        self.salle_actuelle = nom
        self.salle_changee = True
    

class Objet:
    """
    Cette classe, qui a vocation à être héritée, définit 
    les composantes de base d'un objet dans le moteur de jeu.
    """
    def __init__(self, jeu, z_pos:float=0):
        self.jeu = jeu
        self.z_pos = z_pos
        self.vivant = True 
        self.actualiser_ = True
        # Les etiquettes sont des textes qui permettent d'identifier les objets
        self.etiquettes = set({})
        
    def ajouter_etiquette(self, etiquette:str):
        # Le nom de cette methode est très explicite
        self.etiquettes.add(etiquette)
        
    def tuer(self):
        # Celui ci aussi
        self.vivant = False

    def actualiser(self, scene:Scene):
        """
        Cette métode par défaut ne fait rien car elle
        a vocation a être modifiée au sein des classes
        qui héritent de la classe Objet.
        
        Elle est apelée par la scène si l'objet en question
        est présent dans la scène courante.
        
        La scene entrée en parametre est celle qui apele justement
        cette méthode.
        """
        pass
