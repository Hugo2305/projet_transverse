import numpy as np
import matplotlib.pyplot as plt

# Constantes
g = 9.81  # Gravité en m/s²


# Fonction pour calculer la trajectoire
def calcul_trajectoire(v0, angle, dt=0.01):
    angle_rad = np.radians(angle)  # Conversion en radians
    v0x = v0 * np.cos(angle_rad)  # Composante horizontale de la vitesse
    v0y = v0 * np.sin(angle_rad)  # Composante verticale de la vitesse

    # Temps de vol total
    T = (2 * v0y) / g

    if T <= 0:  # Vérification pour éviter une erreur
        print("Erreur : le temps de vol est invalide.")
        return [], []

    # Discrétisation du temps (remplacé arange par linspace)
    t = np.linspace(0, T, num=100)

    # Calcul des positions x et y
    x = v0x * t
    y = v0y * t - 0.5 * g * t ** 2

    return x, y


# Demander à l'utilisateur la vitesse et l'angle de tir
v0 = float(input("Entrez la vitesse initiale (m/s) : "))
angle = float(input("Entrez l'angle de tir (degrés) : "))

# Calcul de la trajectoire
x, y = calcul_trajectoire(v0, angle)

# Vérifier s'il y a une trajectoire valide
if len(x) > 0:
    # Affichage de la trajectoire
    plt.figure(figsize=(10, 5))
    plt.plot(x, y, label=f"Tir à {angle}° et {v0} m/s")
    plt.xlabel("Distance (m)")
    plt.ylabel("Hauteur (m)")
    plt.title("Trajectoire du projectile")
    plt.legend()
    plt.grid()
    plt.show()
