# Resolution d'un problème de planification de prise de vue  sans incertitude
# Helene Fargier, oct 2025
#
#  Version bootstrap, avec exemple de declaration de modele, ajout de variables de decision, 
# d'une fonction objectif  ne prenant pas en compte les incertitudes 
# une seule contrainte implementée



# on charge le solveur lineaire
from pyscipopt import Model, quicksum
from itertools import product

# on charge les données
from spotProba2 import nbImages, nbInstruments, PA, DD, AN, VI, DU, TY, PM, PMmax, Failure, ProbaInf, ProbaSup


# creation du modele lineaire
#############################

#model
mymodel = Model()

# pour chaque image i ,  le solveur doit affecter la variable booleen selection[i) à 1 ssi  l'image i est selectionnée
selection = {}
for i in range(nbImages):
    selection[i] = mymodel.addVar(vtype='B', name='select' + str(i))

#### pour chaque instrument i ,  le solveur doit affecter la variable booleen ass_i[i) à 1 ssi  l'instrument i est selectionné
assignedTo = {}
for i in range(nbImages):
    ass_i = {}
    for j in range(nbInstruments):
        ass_i[j] = mymodel.addVar(vtype='B', name='assignto' + str(i) + '_' + str(j))
    assignedTo[i] = ass_i

# la fonction objectif
######################

# en l'absence d'incertitude, on maximise la somme des payoff
mymodel.setObjective(quicksum(PA[i] * selection[i] for i in range(nbImages)), sense='maximize')



# ajout des contraintes au modele
################################

# taille memoire du satellite
# Ajout de la contrainte de taille mémoire
mymodel.addCons(quicksum(PM[i] * selection[i] for i in range(nbImages)) <= PMmax)


# la contrainte de non chevauchement
# considérons un instrument
# si, sur cet insrument, le temps de transition entre 2 images ima1 et ima2 
# ne tient pas entre la fin de ima1 et le debut de ima2 
# alors une seule de ces deux images au plus peut etre assignée à l'instrument

for ima1,ima2 in product(range(nbImages), range(nbImages)):
    if ima1 < ima2:
        for ins in range(nbInstruments):
            if  abs(DD[ima1][ins] - DD[ima2][ins]) * VI < DU * VI + abs(AN[ima1][ins] - AN[ima2][ins]):
                mymodel.addCons(assignedTo[ima1][ins] + assignedTo[ima2][ins] <= 1)
                
# stereo sur instrument 1 et 3
for i in range(nbImages):
    if TY[i] == 2:
        mymodel.addCons(assignedTo[i][0] == selection[i])  # instrument 1
        mymodel.addCons(assignedTo[i][2] == selection[i])  # instrument 3

        mymodel.addCons(assignedTo[i][1] == 0) # instrument 2
    else:
        # Pour une image mono, elle ne peut être prise que par un seul instrument parmi les trois
        mymodel.addCons(quicksum(assignedTo[i][j] for j in range(nbInstruments)) == selection[i])

# pas d'image simultanee pour un instrument
for ins in range(nbInstruments):
    for ima1, ima2 in product(range(nbImages), range(nbImages)):
        if ima1 < ima2:
            # Test de recouvrement des durées
            if abs(DD[ima1][ins] - DD[ima2][ins]) < DU:
                mymodel.addCons(assignedTo[ima1][ins] + assignedTo[ima2][ins] <= 1)

# resolution et affichage des resulats
#########################################

#visualiser le problem lineaire cree
mymodel.writeProblem("pb.cip")

# lancer l'optimisation
print("Resolution")
mymodel.hideOutput(False)
mymodel.optimize()

#afficiher  les resultats mode "scip"
print('statut ' + mymodel.getStatus())
print("solution", end='\t')
print(mymodel.getBestSol())

# afficher les resultats prorement
if mymodel.getStatus() == 'optimal':
    print("\n\nProblème resolu, valeur de l'objectif " + str(mymodel.getObjVal()))
    sol=mymodel.getBestSol()
    for ima in range(nbImages):
        for ins in range(nbInstruments):
            if (mymodel.getVal(assignedTo[ima][ins]) > 0):
                print("Image" + str(ima) + " selectionnée et  assignée à  " + str(ins) + "  (debut à " + str( DD[ima][ins]) + ")")

