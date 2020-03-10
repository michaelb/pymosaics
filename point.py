"""
des points du plans
"""

from math import sqrt, cos ,sin
from random import randint


class Point:
    """
    un point du plan
    """
    def __init__(self, abscisse, ordonnee):
        """
        creation d'un point a partir d'une abscisse et d'une ordonnee
        """
        self.abscisse = abscisse
        self.ordonnee = ordonnee

    def __str__(self):
        return str(self.abscisse) + "," + str(self.ordonnee)

    def distance_a(self, autre_point):
        """
        renvoie la distance entre deux points
        """
        difference_x = autre_point.abscisse - self.abscisse
        difference_y = autre_point.ordonnee - self.ordonnee
        return sqrt(difference_x*difference_x + difference_y*difference_y)

def tournepoint(p, centre, angle):
    x1,y1 = p.abscisse, p.ordonnee
    x0,y0 = centre
    x2 = (x1 - x0) * cos(angle) + (y1 - y0) * sin(angle) + x0
    y2 = (y1 - y0) * cos(angle) - (x1 - x0) * sin(angle) + y0
    return Point(x2,y2)

def point_aleatoire(largeur=800, hauteur=600):
    """
    renvoie un point aleatoire,
    x compris entre 0 et largeur
    et y entre 0 et hauteur
    """
    return Point(randint(0, largeur), randint(0, hauteur))

def point_interieur(Lpoints, taille):
    for p in Lpoints:
        x,y = p.abscisse, p.ordonnee
        if not(not(0<=x<=taille[0]) or not(0<=y<=taille[1])):
            return p


