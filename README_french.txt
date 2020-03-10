Hello!

Je vais donner les bases de l'utilisation de mon programme:

1) Lancer le programme:
	Une interface utilisateur interactive est disponible en éxecutant "projetv2.py"
	On peut choisir d'utiliser les paramètres par défauts, ou customs, qui vont affecter la géométrie du resultat final
	Normalement, si on prend bien le temps de lire les messages affichés à l'écran, tout est clair


2) Structure:
	Le programme manipule des objets "segments" de classe "Segment" définie dans segment.py, de même pour les objets point (Point, point.py)

	le programme est constitué de différentes fonctions qui réalisent les différentes etapes de la création de la mosaïque,
	leur nom (ex: pavage) est relativement explicite et une description de l'effet de la fonction est disponible
	Il arrive que, pour faciliter lecture et compréhension, ces fonctions soient séparées en parties dont par ex, une applique l'effet sur un segment, et l'autre applique la 1ere fonction à un liste (+ quelques détails)

	fonctions spéciales:
		-printsegment() et printpoints() qui écrivent sur la sortie standart les listes de segments/points en svg (situé en fin du fichier, ligne 250+)
		-UI() lance l'interface interactive (situé en début de fichier) dans la console (UI est appelé lors de l'éxecution de projetv2.py via la derniere ligne du programme)
			elle appelle main() avec les arguments par défaut/custom, puis affiche image.svg (via tycat)
	
	fonction main(): (ligne 200)
		prend des paramètres en arguments

		la fonction main() fonctionne de la manière suivante: le couple "listesegment, taille" (taille du canvas svg) est créé puis passé en argument des différentes fonctions
		 qui retournent un nouveau couple "listesegment, taille"
		 Remarque: pour observer l'image à une etape donnée, il suffit de commenter les lignes "listesegment, taille = fonctionssuivantes(.....)" 

		 Ensuite, le programme écrit (overwrite) sur le fichier image.svg l'entête, des segments en svg (via printsegment) et la balise de fin
	

3) Erreurs et exceptions:
	- il arrive, mais c'est normal, que parfois la liste finale de segment soit vide (les segments étaient tous disjoints, ou en dehors du rognage) 
	Dans ce cas, au lieu d'afficher un perturbant svg vide, on choisit d'arrêter le programme et d'afficher un message expliquant la situation
	le fichier "image.svg" n'ayant pas été réécrit, il contient toujours l'ancienne image. Ca peut être perturbant!

	- C'est un cas assez rare, mais parfois il arrive qu'un segment ne soit pas supprimé à la dernière étape (suppression des "bouts qui dépassent")
	Si un segment "touche"/"en relie"  deux autres, il est gardé. Mais il est possible qu'un de ces segments ne touche que le premier et donc soit supprimé plus tard
	Le premier segment a donc été gardé alors qu'il est finalement "un bout qui dépasse"
	On peut régler ce problème en appelant plusieurs fois la derniere fonction, mais vu le coût en complexité et la performance satisfaisante d'un seul appel, hé bien, on ne le fait pas

4) Credits
	- A Frederic Wagner pour les fichiers Point et Segment qui ont été reutilisés, (parce que recycler c'est bien)
	Vous l'avez surement remarqué, mais les classes Segment et Point proviennent du projet de début d'année sur les intersections de segments, des ajouts on été faits notamment pour optimiser 
	les calculs qui sont necessaires à ce projet en particulier
