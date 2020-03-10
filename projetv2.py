#!/usr/bin/env python3

"""un certain projet de bpi"""

#pour des élément d'UI
import sys
import os
from time import time
from random import randint


from point import *
from segment import *
from math import floor, pi

def printsegment(liste):
    """fonction capable d'imprimer les lignes svg pour les segments d'une liste 'liste'
    sur la sortie standart
    , à utiliser intelligement au vu de la postition des balises svg"""
    for segment in liste:
        print('<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="red" stroke-width="2" />'.
              format(floor(segment.coordonnees()[0][0]), floor(segment.coordonnees()[0][1]),
                     floor(segment.coordonnees()[1][0]), floor(segment.coordonnees()[1][1])))


def printpoints(liste):
    """fonction capable d'imprimer des cerles (en svg)
    correspondant aux points de la liste en argument"""
    for point in liste:
        print('<circle cx="{}" cy="{}" r="{}" stroke="red" stroke-width="3" fill="red" />'.
              format(floor(point.abscisse), floor(point.ordonnee), 5))


def decaleorigine(L, ox, oy):
    """Translate tous les segment pour que l'ancienne origine (0,0)
    soit à présent placée sur (ox,oy) ,ox et oy sont les coordonnees de la nouvelle origine"""
    for segment in L:
        for p in segment.points:
            p.abscisse = ox + p.abscisse
            p.ordonnee = oy + p.ordonnee


def Lsegment(nombre, taille):
    """retourne une liste de <nombre> segment aléatoires
    dont les coordonnées sont comprises dans un rectangle de taille <taille>"""
    L = []
    largeur = taille[1]
    hauteur = taille[0]
    for i in range(nombre):
        L.append(segment_aleatoire(largeur, hauteur))
    return L, taille

def symetrie(L, taille):
    """crée un symétrique (selon l'axe vertical 'de gauche')
    de la liste de segment (plus facile à voir comme une image)"""
    L2 = [inversehorizontal(segment, taille) for segment in L]
    decaleorigine(L, taille[1], 0)
    taille[1] = 2 * taille[1]
    return L + L2, taille


def tourne(L, taille):
    """par rapport au centre du rectangle de taille <taille>,
    cette fonction renvoie une liste contenant tous les segment de <L>
    pivotés d'un angle de 2*k*pi/8, k entier"""
    L2 = []
    for tour  in range(0, 8):
        for segment in L:
            L2.append(segmenttourne(segment, tour*2*pi/8, [taille[1]/2, taille[0]/2]))
    return L2, taille

def crop(L, taille, nouvelletaille, bords):
    """renvoie une liste de segments de <L> appartenant au rectangle
    de taille <nouvelletaille> centré par rapport à celui de taille <taille>
    si un segment croise le nouveau bord, il est coupé et la partie intérieure est conservée"""
    decaleorigine(L, (nouvelletaille[1]-taille[1]>>1), (nouvelletaille[0]-taille[0]>>1))
    # ici ^ on centre la liste sur le nouveau centre

    #on crée la liste des segments représentant les bords
    Lbords = [Segment([Point(0, nouvelletaille[1]), Point(0, 0)]),
              Segment([Point(0, nouvelletaille[1]), Point(nouvelletaille[0], nouvelletaille[1])]),
              Segment([Point(nouvelletaille[0], 0), Point(0, 0)]),
              Segment([Point(nouvelletaille[0], 0), Point(nouvelletaille[0], nouvelletaille[1])])]

    for segment in L: #on crée un liste des points d'intersection de chaque segment
        #avec chaque bord et on examine les différents cas possibles
        points = []
        for bord in Lbords:
            points.append(segment.intersection_avec(bord))
        points = [x for x in points if x != None]

        if len(points) == 0:#si le segment ne coupe pas un des bords
            if point_interieur(segment.points, nouvelletaille) == None:
                segment.points = None #indentificateur de si un segment doit être enlevé
        elif len(points) == 1:#si le segment coupe un seul bord
            segment.points = [points[0], point_interieur(segment.points, nouvelletaille)]
        elif len(points) == 2: #si le segment coupe deux bords
            p1, p2 = points
            segment.points = [p1, p2]
        #le cas où un segment coupe trois bords est considéré trop rare
        #(quasi impossible, il faudrait que ce soit un des bords) n'est pas considéré
    #fin de cette grosse boucle

    if bords:#uniquement un paramètre esthétique
        L += Lbords
    return [x for x in L if x.points != None], nouvelletaille
    #ici ^ on enlève les segment marqués segment.points == None

def pavage(L, taille):
    """prend une liste de segments <L> en argument et renvoie une liste contenant 9 fois <L>
    décalée successivement pour faire un pavage 9x9 du carré que <L> remplissait de base"""
    L = [x for x in L if x is not None] #on se protège d'un cas rare
    #(mais qui soulève une erreur; lorsqu'un des segments n'est pas un segment valide),
    #on aurait pu le faire dans la fonction précédente aussi

    supervecteur = [L]
    for i in range(8):#on crée des copies de la liste <L>
        unvecteur = []
        for segment in L:
            unvecteur.append(copiesegment(segment))
        supervecteur.append(unvecteur)
    for x in range(0, 3):#on décale ces copies
        for y in range(0, 3):
            decaleorigine(supervecteur[x+3*y], x*taille[1], y*taille[0])
    taille[0] *= 3
    taille[1] *= 3
    L2 = []
    for vecteur in supervecteur:
        for segment in vecteur:
            L2.append(segment)
    return L2, taille

def decoupe(segment, Lpoints):
    """prend un segment en argument et renvoie une liste contenant plusieurs
    bouts de <segment> découpés selons les points de la liste <Lpoints>"""
    if len(Lpoints) <= 1:
        segment.seul = 1 #surement redondant avec la ligne identique de la fonction decoupe_tout()
        return []
    Lsegment = []
    debutligne = Lpoints[0]
    Lpoints.sort(key=lambda p: p.distance_a(segment.points[0]))
    for i, p  in enumerate(Lpoints[:-1]):
        Lsegment.append(Segment([p, Lpoints[i + 1]]))
    return Lsegment



def decoupe_tout(L, taille):
    nvLsegment = []
    for segment in L:
        Lpoints = [segment.intersection_avec(autre) for autre in L if autre is not segment]
        Lpoints = [x for x in Lpoints if x is not None]
        #printpoints(Lpoints) #utile pour visualiser les intersections de segments
        #attention au printpoint qu'il faut intercaler entre l'entete et la fin svg

        if  len(Lpoints) != 0:
            nvLsegment += (decoupe(segment, Lpoints))
        if len(Lpoints) <= 1:#un peu d'optimisation pour l'etape d'après
            segment.seul = 1
    return nvLsegment, taille

def compte(point, listepoint):
    compteur = 0
    approximation = 4  #a partir de quelle distance on considère que des points sont confondus
    for p in listepoint:
        if p is not point and (abs(p.abscisse - point.abscisse) + abs(p.ordonnee - point.ordonnee)) < approximation:
            #une telle methode de calcul de la "distance" permet de s'affranchir de bizzareries
            #d'approximations verticales/horizontales qui mènent à la suppression de
            #certains segments mais pas leur symétrique par ex
            compteur += 1
    #print(compteur)
    return compteur


def elimine_seuls(L, taille):
    L = [x for x in L if x.seul == 0]
    Lpoints = []
    for segment in L:
        for p in segment.points:
            Lpoints.append(p)
    Lsegment = []
    for segment in L:
        p1, p2 = segment.points
        if compte(p1, Lpoints) >= 1 or compte(p2, Lpoints) >= 1:
            Lsegment.append(segment)
    return Lsegment, taille



def main(nbrsegmentbase=2, taillebase=[200, 200], taillecrop=[200, 200], bords=0):
    listesegment, taille = Lsegment(nbrsegmentbase, taillebase)
    listesegment, taille = symetrie(listesegment, taille)
    listesegment, taille = tourne(listesegment, taille)
    listesegment, taille = crop(listesegment, taille, taillecrop, bords)
    listesegment, taille = pavage(listesegment, taille)
    listesegment, taille = decoupe_tout(listesegment, taille)
    listesegment, taille = elimine_seuls(listesegment, taille)
    print(len(listesegment))

    if len(listesegment) == 0:
        print("\n ATTENTION!!\nPas de chance, l'aléatoire fait que cette fois l'image est vide :-/, relancez le programme (note: 'afficher l'image' affichera l'ANCIENNE image\n")
    else:
        imagesvg = open("image.svg", 'w')
        sys.stdout = imagesvg
        print('<svg height="{}" width="{}">'.format(taille[0], taille[1]))
        printsegment(listesegment)
        print('</svg>')
        sys.stdout = sys. __stdout__
        imagesvg.close()
        print("\nFini")































#rien d'interressant ci-après
def UI():
    print("Lancement du programme...")
    reponse = input("Utiliser les paramètres par défaut? [Y/n]:")
    while True:
        if reponse in ("", "Y", "y", "yes", "Yes"):
            t1 = time()
            main()
            break
        elif reponse in ("n", "N", "No", "no"):
            t1 = time()
            n = int(input("\nUn nombre entier spécifiant le nombre de segment aléatoires à choisir au début. !Attention! des valeurs >= 4 donnent un temps d'éxecution très long!:"))
            taille = int(input("\nTaille du canvas de base (rentrer 200 donne un canvas de taille initial 200x200) (remarque: le canvas final fait 9x la surface de l'initial, à prendre en compte:"))
            taille2 = int(input("\nTaille du canvas rogné (consignes idem que ci-dessus):"))
            bords = int(input("\n Est-ce que les carrés des 'pavés' doivent apparaitre? repondre 1/0 pour Yes/No:"))
            main(nbrsegmentbase=n, taillebase=[taille, taille], taillecrop=[taille2, taille2], bords=bords)
            break
        else:
            reponse = input("\nUtiliser les paramètres par défaut? [Y/n]:")

        

    t2 = time()
    print("(Temps d'éxecution = {} s)".format(round(t2 - t1, 2)))
    #quelques éléments d'UI
    reponse = input("\nAfficher l'image? (assurez-vous d'avoir un tycat fonctionnel, ou d'être dans terminology)  [Y/n]:")
    while True:
        if reponse in ("", "Y", "y", "yes", "Yes"):
            os.system("tycat image.svg")
            break
        elif reponse in ("n", "N", "No", "no"):
            print("l'image à afficher se trouve dans ./image.svg")
            break
        else: 
            reponse = input("\nAfficher l'image? (assurez-vous d'avoir un tycat fonctionnel, ou d'être dans terminology)  [Y/n]:")
    reponse = input("Sauvegarder l'image? [y/N]:")
    while True:
        if reponse in ("Y", "y", "yes", "Yes"):
            numero = randint(1,100)
            os.system("cp ./image.svg ./example_images_generees/image{}.svg".format(numero))
            print("Image sauvegardée sous ./example_images_generees/image{}.svg".format(numero))
            break
        elif reponse in ("", "n", "N", "No", "no"):
            break
        else: 
            reponse = input("Sauvegarder l'image? [y/N]:")



UI()
