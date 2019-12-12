from tkinter import *
from tkinter import messagebox
from math import *

texte = open("plantes_melliferes_new.csv","r")
lignes = texte.readlines()

#Pour plus de clarté, lire graines_graphique en premier. Les fonctions ici sont légèrement différentes pour répondre à une autre question :
#Le mélange fournit par l'utilisateur est-il un bon mélange pour une prairie fleurie ?



##DEFINITION DES VARIABLES

checkButtonsInputsValues = []
tot_floraison = []
tot_famille = 0
tot_couleur = 0
viva = 0
annu = 0
nbr = 0

##Fonction appelée par le programme main
def test():
    r= Toplevel()
    r.title("Test d'un mélange")
    r.iconbitmap("icone_abeille.ico")

    plantes = tab() #Fonction définie plus tard

    ff=Frame(r, bg = "white")
    ff.pack()

    Label(ff, bg = "white", text="\nCette fenêtre vous permet de tester un mélange déjà existant.\nIl vous suffit de cocher les espèces végétales présentes\ndans le mélange, puis de cliquer sur 'lancer'.\nSi une plante est manquante, vérifiez les synonymes sur le site \nTela Botanica avant d'utiliser le formulaire de contact.", font = autre1).pack(expand = YES)

    widget = Button(ff, text = "Lancer", command = depart, bg = "grey70", font = autre1)
    widget.pack(expand=YES, fill=X)

    #Bouton pour tout décocher d'un coup. Le lambda permet d'appeler une variable pour la fonction dans une commande.
    ch = Button(ff, text="Décocher tout", bg = "grey70", command=lambda:deselection(list_check))
    ch.pack(expand = YES)

    #Dimensions de la fenêtre
    W = 450
    H = len(plantes) * 29

    canvas=Canvas(ff, width=W, scrollregion =(0, 0, 10, H), bg='ivory')
    canvas.pack(expand = YES, side=LEFT)

    frame = Frame(canvas, bg = "white")
    frame.pack(expand = YES)

    #Création de la scrollbar
    vbar=Scrollbar(ff,orient=VERTICAL)
    vbar.pack(expand = YES, side=RIGHT,fill=Y)
    vbar.config(command=canvas.yview)
    canvas['yscrollcommand']=vbar.set
    canvas.create_window((0,0),window=frame,width=W, height=H, anchor = "nw")

#creation des checkbutton : boucle pour mettre toutes les plantes dispos

    i = 0
    list_check = []

    for plante in plantes:
        valeur = IntVar()
        nom_variable = str(plante[0]) + "  (" + str(plante[1]) + ")"
        check = Checkbutton(frame, bg = "white", text = nom_variable, variable = valeur, font = autre1)
        i += 1

        checkButtonsInputsValues.append(valeur) #stocke valeur des boutons (0 si non coché, 1 si coché)

        check.pack(anchor = "w")
        list_check.append(check)


    frame.configure(width=400,height=500)



##Fonctions

#Fonction pour décocher tous les checkbuttons d'un coup
def deselection(list_check):
    for c in list_check:
        c.deselect()

# initialisation d'une liste
def tab():
    tab = []
# Lecture des lignes une par une
    for ligne in lignes:
    # segmentation de la liste et ajout dans tab
        tab.append(ligne.split(";"))
    del(tab[0])
    return tab


#On convertit les checkbutton en valeur et on créé une liste avec les checkbutton cochés
def listeplante():
    liste = []
    plantes = tab()
    if len(plantes) != len(checkButtonsInputsValues):
        fin = len(checkButtonsInputsValues) - len(plantes)
        del(checkButtonsInputsValues[0:fin]) #Quand on relance les résultats sans avoir tout fermer, les checkbuttons se retrouvent en double. Permet d'effacer les résultats du tour d'avant.
        #D'autres pbms rencontrés avec cette variable. De cette manière, on ne garde que les dernieres valeurs qui correspondent à ce qu'on fait actuellement.
        print(len(checkButtonsInputsValues))
    for i in range(0,len(checkButtonsInputsValues)):
        if checkButtonsInputsValues[i].get() == 1:
            liste.append(plantes[i])
    #Gestion de quelques erreurs
    if len(liste) == 0:
        messagebox.showerror("Nombre", "Vous n'avez pas coché de cases. Si jamais vous avez coché des cases mais que vous obtenez ce message, fermez l'application, relancez et réessayez. Merci de prévenir Margaux Julien si vous obtenez cette erreur.")
        quit()
    elif len(liste) > 40:
        messagebox.showerror("Nombre", "Votre mélange contient trop de plantes. Veuillez cocher moins de 40 plantes pour un mélange cohérent.")
        quit()
    return liste


#Fonction pour voir si la floraison du mélange fournit est suffisamment étendue
# 1 pt par mois sauf juin et juillet qui sont les 2 mois les plus fleuris
def floraison(qualite_melange, probleme, caracteristiques):
    combinaison = listeplante() #la liste de plante est toujours la meme
    nombre_graines = len(combinaison)
    mars_mini = ceil(int(nombre_graines)/7) #On définit le minimum de plantes en fleurs pour chaque mois
    avril_mini = ceil(int(nombre_graines)/6)
    mai_mini = ceil(int(nombre_graines)/5)
    juin_mini = ceil(int(nombre_graines)/4)
    juillet_mini = ceil(int(nombre_graines)/4)
    aout_mini = ceil(int(nombre_graines)/4)
    septembre_mini = ceil(int(nombre_graines)/5)
    octobre_mini = ceil(int(nombre_graines)/6)
    mars = 0 #initialisation
    avril = 0
    mai = 0
    juin = 0
    juillet = 0
    aout = 0
    septembre = 0
    octobre = 0
    for plante in combinaison:
        mars += int(plante[6]) #Pour chaque combi on ajoute si plante en fleur à ce mois là
        avril += int(plante[7])
        mai += int(plante[8])
        juin += int(plante[9])
        juillet += int(plante[10])
        aout += int(plante[11])
        septembre += int(plante[12])
        octobre += int(plante[13])
    tot_floraison.append(mars)
    tot_floraison.append(avril)
    tot_floraison.append(mai)
    tot_floraison.append(juin)
    tot_floraison.append(juillet)
    tot_floraison.append(aout)
    tot_floraison.append(septembre)
    tot_floraison.append(octobre)
    score = 0
    if mars >= mars_mini:
        score += 1
    if avril >= avril_mini:
        score += 1
    if mai >= mai_mini:
        score += 1
    if aout >= aout_mini:
        score += 1
    if septembre >= septembre_mini:
        score += 1
    if octobre >= octobre_mini:
        score += 1
    if score < 6:
        probleme.append("Le pourcentage de plantes en fleurs est trop faible pour certains mois.")

    qualite_melange += score
    indigenat(qualite_melange, probleme, caracteristiques)


#On vérifie que chaque plante dans le mélange est indigène
# -2 pts par plante non indigène
def indigenat(qualite_melange, probleme, caracteristiques):
    combinaison = listeplante()
    non = []
    non_com = []
    score = 6
    for plante in combinaison:
        if "non" in plante[30]:
            non.append(plante[1])
            non_com.append(plante[0])
    if len(non) > 0:
        for i in range(0, len(non)): #Un message sera affiché pour chaque plante non indigène présent dans le mélange
            texte = "L'espèce " + str(non_com[i]) + " (" + str(non[i]) + ") n'est pas indigène."
            probleme.append(texte)
            score -= 2
    if score > 0:
        qualite_melange += score
    nombre(qualite_melange, probleme, caracteristiques)


#Le mélange comprend-il suffisamment de plantes ? Minimum 15 espèces requises.
# 0 pt si moins de 5 espèces, 1pt si entre 5 et 10 espèces, 2 pts si entre 10 et 15 espèces, 3 pts dessus de 15
def nombre(qualite_melange, probleme, caracteristiques):
    global nbr
    combinaison = listeplante()
    if len(combinaison) < 5:
        probleme.append("Le mélange contient trop peu d'espèces. Un minimum de 15 graines est recommandé.")
    elif len(combinaison) < 10:
        probleme.append("Le mélange contient trop peu d'espèces. Un minimum de 15 graines est recommandé.")
    elif len(combinaison) < 15:
        probleme.append("Le mélange contient trop peu d'espèces. Un minimum de 15 graines est recommandé.")
        qualite_melange += 1
    else:
        qualite_melange += 3
    nbr = len(combinaison)
    perennite(qualite_melange, probleme, caracteristiques)

#25% vivaces et 25% annuelles minimum pour un mélange équilibré
# 1 pt si au moins 25% de chaque
def perennite(qualite_melange, probleme, caracteristiques):
    global viva, annu
    vivace = 0
    annuelle = 0
    combinaison = listeplante()
    for plante in combinaison:
        if plante[3] == "P":
            vivace += 1
        else:
            annuelle += 1
    if vivace > len(combinaison)/4 and annuelle > len(combinaison)/4:
        qualite_melange += 1
    elif vivace < len(combinaison)/4:
        probleme.append("Il semble que votre mélange ne contienne pas assez d'espèces vivaces.")
    elif annuelle < len(combinaison)/4:
        probleme.append("Il semble que votre mélange ne contienne pas assez d'espèces annuelles.")
    viva = round(vivace/len(combinaison)*100,1)
    annu = round(annuelle/len(combinaison)*100,1)
    famille(qualite_melange, probleme, caracteristiques)


#On veut au moins 5 familles végétales
# 3 pts si 5 familles ou plus, 1 pt si 4 familles
def famille(qualite_melange, probleme, caracteristiques):
    global tot_famille
    famille = []
    combinaison = listeplante()
    for plante in combinaison:
        famille.append(plante[2])
    famille = set(famille) #suppression des doubles
    if len(combinaison) < 5:
        if len(famille) < len(combinaison):
            probleme.append("Il y a trop peu de familles végétales dans votre mélange.")
        else:
            qualite_melange += len(combinaison) -1
    else:
        if len(famille) < 5:
            probleme.append("Il y a trop peu de familles végétales dans votre mélange.")
        else:
            qualite_melange += 3
        if len(famille) == 4:
            qualite_melange += 1
    tot_famille = len(famille)
    couleur(qualite_melange, probleme, caracteristiques)


#On veut au moins 5 couleurs de fleurs différentes
# 1 pt si 5 couleurs ou plus
def couleur(qualite_melange, probleme, caracteristiques):
    global tot_couleur
    couleur = []
    combinaison = listeplante()
    for plante in combinaison:
        chaine = plante[28]
        chaine = chaine.split(",")
        couleur = couleur + chaine
    couleur = set(couleur)
    if len(combinaison) < 5:
        if len(couleur) < len(combinaison):
            probleme.append("Les couleurs des fleurs des espèces de votre mélange ne sont pas assez diversifiées.")
        else:
            qualite_melange += 2
    else:
        if len(couleur) < 5:
            probleme.append("Les couleurs des fleurs des espèces de votre mélange ne sont pas assez diversifiées.")
        else:
            qualite_melange += 1
    tot_couleur = len(couleur)
    sol(qualite_melange, probleme, caracteristiques)


#Caractéristiques du sol : on regarde quels types de sols peuvent accueillir ce mélange.
def sol(qualite_melange, probleme, caracteristiques):
    combinaison = listeplante()
    acide = [] #liste qui contiendra les plantes ne poussant pas en milieu acide
    basique = []
    chaud = []
    froid = []
    sec = []
    humide = []
    for plante in combinaison:
        if "0" in plante[17]:
            acide.append(plante[1])
        if "0" in plante[18]:
            basique.append(plante[1])
        if "0" in plante[19]:
            chaud.append(plante[1])
        if "0" in plante[20]:
            sec.append(plante[1])
        if "0" in plante[21]:
            froid.append(plante[1])
        if "0" in plante[22]:
            humide.append(plante[1])
    if len(acide) != 0 and len(basique) != 0:
        chaine = ""
        #Changement : finalement on n'affiche pas les plantes qui ne poussent pas dans tel ou tel milieu.
        #On dit juste quels types de sols sont adaptés.
        #Je laisse le code au cas où il y ait un futur changement.
        for plantebasique in acide:
            chaine = chaine + " " + plantebasique + ","
        chaine = chaine + "ne pousse(nt) pas en milieu acide alors que "
        for planteacide in basique:
            chaine = chaine + planteacide + " "
        chaine = chaine + "ne pousse(nt) pas en milieu basique."
        caracteristiques.append("Mélange adapté pour un sol à pH neutre uniquement.")
    elif len(acide) != 0:
        chaine = ""
        for plante in acide:
            chaine = chaine + " " + plante + ","
        chaine = chaine + "ne pousse(nt) pas sur sol acide."
        caracteristiques.append("Mélange adapté pour un sol à pH basique ou neutre.")
    elif len(basique) != 0:
        chaine = ""
        for plante in basique:
            chaine = chaine + " " + plante + ","
        chaine = chaine + "ne pousse(nt) pas sur sol basique."
        caracteristiques.append("Mélange adapté pour un sol à pH acide ou neutre.")
    else:
        caracteristiques.append("Mélange compatible avec tout type de pH.")

    if len(chaud) != 0 and len(froid) != 0:
        chaine2 = ""
        for plantechaud in froid:
            chaine2 = chaine2 + plantechaud + " "
        chaine2 = chaine2 + "ne pousse(nt) pas en milieu froid alors que "
        for plantefroid in chaud:
            chaine2 = chaine2 + plantefroid + " "
        chaine2 = chaine2 + "ne pousse(nt) pas en milieu chaud."
        caracteristiques.append("Mélange adapté à un milieu tempéré uniquement.")
    elif len(chaud) != 0:
        chaine2 = ""
        for plante in chaud:
            chaine2 = chaine2 + plante + " "
        chaine2 = chaine2 + "ne pousse(nt) pas en milieu chaud."
        caracteristiques.append("Mélange adapté à un milieu tempéré ou froid.")
    elif len(froid) != 0:
        chaine2 = ""
        for plante in froid:
            chaine2 = chaine2 + plante + " "
        chaine2 = chaine2 + "ne pousse(nt) pas en milieu froid."
        caracteristiques.append("Mélange adapté à un milieu tempéré ou chaud.")
    else:
        caracteristiques.append("Mélange compatible à toutes températures")

    if len(sec) != 0 and len(humide) != 0:
        chaine3 = ""
        for plantesec in humide:
            chaine3 = chaine3 + " " + plantesec + ","
        chaine3 = chaine3 + "ne pousse(nt) pas sur sol sec alors que "
        for plantehumide in sec:
            chaine3 = chaine3 + " " + plantehumide + ","
        chaine3 = chaine3 + "ne pousse(nt) pas sur sol humide."
        caracteristiques.append("Mélange adapté à un sol intermédiaire (ni trop humide, ni trop sec).")
    elif len(sec) != 0:
        chaine3 = ""
        for plante in sec:
            chaine3 = chaine3 + plante + " "
        chaine3 = chaine3 + "ne pousse(nt) pas sur un sol sec."
        caracteristiques.append("Mélange adapté à un sol humide ou intermédiaire.")
    elif len(humide) != 0:
        chaine3 = ""
        for plante in humide:
            chaine3 = chaine3 + plante + " "
        chaine3 = chaine3 + "ne pousse(nt) pas sur un sol humide."
        caracteristiques.append("Mélange adapté à un sol sec ou intermédiaire.")
    else:
        caracteristiques.append("Mélange compatible pour tout type de sol (humidité).")
    hauteur(qualite_melange, probleme, caracteristiques)

#On regarde la taille maximum du mélange.
def hauteur(qualite_melange, probleme, caracteristiques):
    combinaison = listeplante()
    taille = []
    for plante in combinaison:
        taille.append(plante[23]) #on ajoute les tailles des plantes unes à unes
    if len(taille) > 0:
        taille = [int(i) for i in taille] #Chaque élément devient un nombre (on était en str avant)
        taillemax = max(taille)
        chaine = "La taille maximale de votre prairie sera de " + str(taillemax) + " cm."

    else: #Pbm rencontré souvent : taille était vide. Le pbm a été réglé mais on laisse ça au cas où.
        chaine = "Probleme avec max..."
    caracteristiques.append(chaine)
    nectarpollen(qualite_melange, probleme, caracteristiques)


#On calcul les potentiels pollinifères et nectarifères
#On n'a pas l'info pour toutes les plantes donc on fait une moyenne pour les plantes où on a l'info uniquement.
def nectarpollen(qualite_melange, probleme, caracteristiques):
    combinaison = listeplante()
    nectar = []
    pollen = []
    for plante in combinaison:
        if plante[15] == "0" or plante[15] == "1" or plante[15] == "2" or plante[15] == "3":
            nectar.append(int(plante[15]))
        if plante[16] == "0" or plante[16] == "1" or plante[16] == "2" or plante[16] == "3":
            pollen.append(int(plante[16]))
    if len(nectar) == 0:
        chaine = "Pas assez d'informations pour calculer le potentiel nectarifère."
    else:
        calcul = round(sum(nectar)/len(nectar),1)
        calcul = str(calcul)
        # print(calcul)
        chaine = "Potentiel nectarifère : "+ calcul + " /3"
    caracteristiques.append(chaine)
    if len(pollen) == 0:
        chaine2 = "Pas assez d'informations pour calculer le potentiel pollinifère."
    else:
        calcul2 = round(sum(pollen)/len(pollen),1)
        calcul2 = str(calcul2)
        chaine2 = "Potentiel pollinifère : "+ calcul2 + "/3"
    caracteristiques.append(chaine2)
    final(qualite_melange, probleme, caracteristiques)




#Fonction finale : on affiche les problèmes rencontrés dans une nouvelle fenetre, ainsi qu'une note /20. On donne également les caractéristiques de ce mélange (plantes qui ne supportent pas les milieux basiques etc)
def final(qualite_melange,probleme, caracteristiques):
    global nbr, viva, annu, tot_famille, tot_couleur
    fenetre2 = Toplevel(bg = "white") #Ouverture d'une deuxième fenetre graphique
    fenetre2.title('Résultats')
    fenetre2.iconbitmap("icone_abeille.ico")
    texte = Label(fenetre2, text = "\nRésultats de votre mélange\n", bg = "white", font = gros_titre)
    texte.pack()
    cadre = LabelFrame(fenetre2, labelanchor = "n", text="Problèmes rencontrés", bg = "white", font = petit_titre)
    cadre.pack(fill="both", expand="yes")
    if len(probleme) > 0:
        for i in probleme:
            textepbm = Label(cadre, text = i, bg = "white", font = autre1)
            textepbm.pack()
    else:
        textepbm = Label(cadre, text = "Bravo, votre mélange est parfait !", bg = "white", font = autre1)
        textepbm.pack()
    if qualite_melange > 5: #On supprime 5 si peu de plantes dans le mélange
        if nbr < 3:
            qualite_melange -= 5
    cadre2 = LabelFrame(fenetre2, labelanchor = "n", text = "Note", bg = "white", font = petit_titre)
    cadre2.pack(fill = "both", expand = "yes", side = BOTTOM)
    note = str(qualite_melange)+" /20"
    textenote = Label(cadre2, text = note, bg = "white", font = petit_titre)
    textenote.pack()
    if qualite_melange < 12:
        com = Label(cadre2, text = "\nLa qualité de votre mélange est mauvaise, prenez en compte les commentaires au dessus pour l'améliorer\n.", bg = "white", font = autre1)
    elif qualite_melange < 15:
        com = Label(cadre2, text = "\nLa qualité de votre mélange n'est pas très bonne, vous pouvez l'améliorer en prenant en compte les commentaires ci-dessus.\n", bg = "white", font = autre1)
    elif qualite_melange < 18:
        com = Label(cadre2, text = "\nLa qualité de votre mélange est plutôt bonne mais vous pouvez encore l'améliorer en prenant en compte les commentaires ci-dessus.\n", bg = "white", font = autre1)
    elif qualite_melange < 20:
        com = Label(cadre2, text = "\nVotre mélange est très bon. N'hésitez pas à regarder les commentaires pour atteindre les 20/20.\n", bg = "white", font = autre1)
    else:
        com = Label(cadre2, text = "\nBravo, votre mélange est parfait !\n", bg = "white", font = autre1)
    com.pack()

    cadre3 = LabelFrame(fenetre2, labelanchor = "n", text = "Caractéristiques du terrain", bg = "white", font = petit_titre)
    cadre3.pack(fill = "both", expand = "yes", side = BOTTOM)

    for i in caracteristiques:
        textecara = Label(cadre3, text = i, bg = "white", font = autre1)
        textecara.pack()

    cadre4 = LabelFrame(fenetre2, labelanchor = "n", text = "Pourcentage d'espèces en fleurs par mois", bg = "white", font = petit_titre)
    cadre4.pack(fill = "both", expand = "yes", side = LEFT)
    mars = Label(cadre4, text = "Mars : "+ str(round(tot_floraison[0]/nbr*100)) + "%", bg = "white", font = autre1)
    mars.pack()
    avril = Label(cadre4, text = "Avril : "+ str(round(tot_floraison[1]/nbr*100)) + "%", bg = "white", font = autre1)
    avril.pack()
    mai = Label(cadre4, text = "Mai : "+ str(round(tot_floraison[2]/nbr*100)) + "%", bg = "white", font = autre1)
    mai.pack()
    juin = Label(cadre4, text = "Juin : "+ str(round(tot_floraison[3]/nbr*100)) + "%", bg = "white", font = autre1)
    juin.pack()
    juillet = Label(cadre4, text = "Juillet : "+ str(round(tot_floraison[4]/nbr*100)) + "%", bg = "white", font = autre1)
    juillet.pack()
    aout = Label(cadre4, text = "Août : "+ str(round(tot_floraison[5]/nbr*100)) + "%", bg = "white", font = autre1)
    aout.pack()
    septembre = Label(cadre4, text = "Septembre : "+ str(round(tot_floraison[6]/nbr*100)) + "%", bg = "white", font = autre1)
    septembre.pack()
    octobre = Label(cadre4, text = "Octobre : "+ str(round(tot_floraison[7]/nbr*100)) + "%", bg = "white", font = autre1)
    octobre.pack()

    cadre5 = LabelFrame(fenetre2, labelanchor = "n", text = "Caractéristiques du mélange", bg = "white", font = petit_titre)
    cadre5.pack(fill = "both", expand = "yes", side = LEFT)
    nbpl = Label(cadre5, text = "Nombre d'espèces : "+ str(nbr), bg = "white", font = autre1)
    nbpl.pack()
    fam = Label(cadre5, text = "Nombre de familles végétales : "+str(tot_famille), bg = "white", font = autre1)
    fam.pack()
    coul = Label(cadre5, text = "Nombre de couleurs florales : "+str(tot_couleur), bg = "white", font = autre1)
    coul.pack()
    per = Label(cadre5, text = str(viva)+"% de plantes vivaces et "+ str(annu)+"% de plantes annuelles.", bg = "white", font = autre1)
    per.pack()
    zero()



#Remise a zero des parametres pour pouvoir relancer sans soucis.
def zero():
    checkButtonsInputsValues = []
    tot_floraison = []
    tot_famille = 0
    tot_couleur = 0
    viva = 0
    annu = 0
    nbr = 0
    qualite_melange = 0
    probleme = []
    caracteristiques = []



#Initialisation des 2 variables qu'on étudie
#qualite_melange est une note qui prend 1 lorsque le critère étudié est bon pour le mélange
#probleme est une liste qui prend les problèmes qu'on rencontrera pour le mélange comme chaine de caractere pour chaque critère étudié
def depart():
    qualite_melange = 0 #C'est la note, pour le moment à 0.
    probleme = [] #Va contenir des chaines de caractères, par la suite qui vont être affichés.
    caracteristiques = [] #Pareil
    floraison(qualite_melange, probleme, caracteristiques) #Lancement des fonctions en cascade

#Definition des polices
nom_latin = "{Arial} 12 italic"
gros_titre = "{Arial} 16 bold"
petit_titre = "{Arial} 14"
autre = "{Arial} 12"
autre1 = "{Arial} 10"

