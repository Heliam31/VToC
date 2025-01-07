# VtoC voice to Command  

This code aims to produce macros using your voice.  
The database is filled with macros for the game ReadyOrNot but is usable for any other task

## Implémented

### Team colors : 

A tous = gold
Rouge = red team
Bleu = blue team

### viseur sur porte :

```
	1 = empiler
		1 = split               "Couleur sur cette porte"
		2 = gauche              "Couleur sur cette porte à gauche"
		3 = droite              "Couleur sur cette porte à droite"
		4 = auto                #TODO
```

```
	2 = aller
		1 = nettoyer            "couleur entrée et nettoyer"
		2 = flash               "couleur flash puis rentrer"
		3 = gmd 		        #TODO
		4 = lacrymo             "couleur lacrymo pu rentrer"
		5 = lance grenade	    #TODO
		6 = avec team leader    "couleur rentrer avec moi"
```

### viseur sur hotage :  

```
	1 = menottez                "mettez-lui des menottes"
	2 -> 2 = viens ici          "viens ici"
```

### viseur dans le vide : 

```
	1 = ICI                     "couleur aller là-bas"

	2 = Formation   
		1 = Une file            "couleur formation une fil"
		2 = 2 files             "couleur formation de fil",
		3 = diamant             "couleur formation diamant"
		4 = triangle            "couleur formation triangle"

	6 = Fouillez pour preuves   "couleur fouiller partout"
```

## TODO

```
3 = Breach
	1 = Pied
	2 = fusil a pompe
	3 = C4
	4 = belier
	5 avec moi	

	puis apres la selection 
	1 = normal
	2 = flash
	3 = GMD
	4 = lacrymo
	5 = lancegrenade
	6 = avec moi

4 = scannez
	1 = faufiler
	2 = balayer
	3 = jeter oeil
5 = passer mirroir

6 = mettre cale


7 = suivez moi


Sur porte verouillée : 2 = "Crochetez la porte"
```