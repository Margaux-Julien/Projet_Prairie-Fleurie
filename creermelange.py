from tkinter import *
import random
from tkinter import messagebox
from tkinter import font
from math import *


# Charger le fichier sur pyzo
texte = open("plantes_melliferes_new.csv","r")

# stocke toutes les lignes du document ouvert dans lignes
lignes = texte.readlines()

##Définition des variables

couleur1 = 5
annuelle = 25
vivace = 25
famille1 = 5
var_temp = 0
var_sechumide = 0
var_ph = 0
hauteur1 = 0
nombre_graine = 0
var_dispo = 0
liste_tot = []

##Définition des fonctions

# initialisation d'une liste qui contient toutes les plantes melliferes du fichier
def tab():
    tab = []
# Lecture des lignes une par une
    for ligne in lignes:
    # segmentation de la liste et ajout dans tab
        tab.append(ligne.split(";"))
    return tab

def tri_dispo():
    global var_dispo, liste_tot
    liste_graine = tab()
    liste_tot = []
    if var_dispo == 0:
        dispo = 0
    else:
        dispo = int(var_dispo.get())
    if dispo == 1:
        for plante in liste_graine:
            if "CNPMAI" in plante[34] or "zygene" in plante[34] or "puy" in plante[34] or "sauveterre" in plante[34] or "graines-semences" in plante[34]:
                liste_tot.append(plante)
    elif dispo == 2:
        for plante in liste_graine:
            if "zygene" in plante[34]:
                liste_tot.append(plante)
    elif dispo == 3:
        for plante in liste_graine:
            if "CNPMAI" in plante[34]:
                liste_tot.append(plante)
    elif dispo == 4:
        for plante in liste_graine:
            if "sauveterre" in plante[34]:
                liste_tot.append(plante)
    elif dispo == 5:
        for plante in liste_graine:
            if "puy" in plante[34]:
                liste_tot.append(plante)
    else:
        liste_tot = liste_graine
    return liste_tot



# Fonction qui fait 2000 tirages aléatoires de n graines
# 1ere boucle : on fait le nombre de tirage voulu
# 2eme boucle : pour chacun des tirages on tire le nombre de graines voulu
def tirage():
    global nombre_graine, liste_tot
    nombre_graines = int(nombre_graine.get())
    combinaisons = []
    nb_combinaisons = 2000
    tri_dispo()
    for i in range(0, nb_combinaisons):
        liste = []
        liste_graine = list(liste_tot)
        j = 1
        while j < int(nombre_graines) + 1:
            numero = random.randint(2,len(liste_graine))
            if liste_graine[numero-1][30] == "oui": #On garde uniquement les plantes indigènes
                j += 1
                liste.append(liste_graine[numero-1])
                del(liste_graine[numero-1])
            elif "non" in liste_graine[numero-1][30]:
                del(liste_graine[numero-1])
            elif len(liste_graine) == 0:
                messagebox.showerror("Producteur", "Ce producteur n'a pas suffisamment de graines pour effectuer suffisamment de tirages aléatoires.")
                quit()
        combinaisons.append(liste)
    return(combinaisons)



# Tri par periode de floraison : on veut avoir des fleurs tous les mois
# Pour chaque mélange, on compte combien de plantes sont en fleurs chaque mois
# Dans les if imbriqués : on détermine combien de plantes doivent être en fleur au minimum --> à modifier pour que ce soit le plus cohérent possible
def tri_floraison():
    global nombre_graine
    nombre_graines = int(nombre_graine.get())
    combinaisons = tirage()
    nouvelle_liste = []
    for combinaison in combinaisons:
        mars_mini = int(nombre_graines)//7 #On définit le minimum de plantes en fleurs pour chaque mois
        avril_mini = int(nombre_graines)//6
        mai_mini = int(nombre_graines)//5
        juin_mini = int(nombre_graines)//4
        juillet_mini = int(nombre_graines)//4
        aout_mini = int(nombre_graines)//4
        septembre_mini = int(nombre_graines)//5
        octobre_mini = int(nombre_graines)//6
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
        if mars >= mars_mini:
            if avril >= avril_mini:
                if mai >= mai_mini:
                    if juin >= juin_mini:
                        if juillet >= juillet_mini:
                            if aout >= aout_mini:
                                if septembre >= septembre_mini:
                                    if octobre >= octobre_mini:
                                        nouvelle_liste.append(combinaison)
    return(nouvelle_liste)


#Cette fonction permet d'avoir à la fois une part de plantes vivaces (P) et de plantes annuelles (A et B) dans le mélange
def tri_perennite():
    global nombre_graine, annuelle, vivace
    nombre_graines = int(nombre_graine.get())
    combinaisons = tri_floraison()
    nouvelle_liste = []
    annuel = int(annuelle) #25% par défaut
    vivac = int(vivace)
    annuel_mini = floor(annuel/100*int(nombre_graines)) #Nombre minimum de plantes annuelles qu'on souhaite dans le mélange. floor permet de garder partie entiere
    perenne_mini = floor(vivac/100*int(nombre_graines))
    for combinaison in combinaisons:
        annuel = 0
        perenne = 0
        for plante in combinaison:
            if plante[3] == "A" or plante[3] == "B":
                annuel += 1
            else:
                perenne += 1
        if annuel >= annuel_mini and perenne >= perenne_mini:
            nouvelle_liste.append(combinaison)
    return(nouvelle_liste)


#Cette fonction permet d'avoir un nombre de famille de graines diversifié
#Les familles de chaque plante sont ajoutées dans une liste puis on supprime les doublons et on compte le nombre de familles presentes dans la liste
def tri_famille():
    global nombre_graine, famille1
    nombre_graines = int(nombre_graine.get())
    combinaisons = tri_perennite()
    nouvelle_liste = []
    famille_mini = int(famille1) #nombre de famille minimum par défaut
    for combinaison in combinaisons:
        famille = []
        for plante in combinaison:
            famille.append(plante[2])
        famille = set(famille) #On supprime les familles qui apparaissent en double
        if int(nombre_graines) > famille_mini:
            if len(famille) >= famille_mini:
                nouvelle_liste.append(combinaison)
        else:
            if len(famille) == int(nombre_graines):
                nouvelle_liste.append(combinaison)
    return(nouvelle_liste)



#Permet d'avoir un melange avec des fleurs de differentes couleurs
#Fonctionne de la meme facon que la fonction tri_famille
#A l'exception qu'on peut avoir plusieurs couleurs par plante donc on fait de la couleur de chaque plante une liste qu'on split puis on l'ajoute au reste avant de faire comme pour tri_famille
def tri_couleur():
    global nombre_graine, couleur1
    nombre_graines = int(nombre_graine.get())
    combinaisons = tri_famille()
    nouvelle_liste = []
    couleur_mini = int(couleur1)
    for combinaison in combinaisons:
        couleur = []
        for plante in combinaison:
            chaine = plante[28]
            chaine = chaine.split(",")
            couleur = couleur + chaine
        couleur = set(couleur)
        if int(nombre_graines) >= couleur_mini:
            if len(couleur) >= couleur_mini:
                nouvelle_liste.append(combinaison)
        else:
            if len(couleur) == int(nombre_graines):
                nouvelle_liste.append(combinaison)
    return(nouvelle_liste)




#Permet de retirer les melanges comprenant des plantes trop hautes
#Pour chaque combinaison, on regarde si chaque plante est bien en dessous de la hauteur souhaitée. Si c'est en dessous, le compteur prend +1.
def tri_hauteur():
    global nombre_graine, hauteur1
    nombre_graines = int(nombre_graine.get())
    combinaisons = tri_couleur()
    hauteur = int(hauteur1.get())
    nouvelle_liste = []
    for combinaison in combinaisons:
        compteur = 0
        for plante in combinaison:
            if int(plante[23]) <= int(hauteur):
                compteur +=1
            else:
                continue #on coupe la boucle pour gagner du temps
        if compteur == int(nombre_graines):
            nouvelle_liste.append(combinaison)
    return(nouvelle_liste)



#Permet d'enlever les melanges contenant des plantes non adaptées au sol
#ATTENTION l'algorithme n'est pas adapté pour les sols à condition extreme.
def tri_sol():
    global nombre_graine, var_ph, var_sechumide, var_temp
    nombre_graines = int(nombre_graine.get())
    combinaisons = tri_hauteur()
    compteur = 0
    for combinaison in combinaisons:
        plante_acide = 1
        plante_basique = 1
        plante_sec = 1
        plante_humide = 1
        plante_chaud = 1
        plante_froid = 1
        for plante in combinaison:
            plante_acide += int(plante[17])
            plante_basique += int(plante[18])
            plante_chaud += int(plante[19])
            plante_sec += int(plante[20])
            plante_froid += int(plante[21])
            plante_humide += int(plante[22])
        ph = var_ph.get()
        sechumide = var_sechumide.get()
        temp = var_temp.get()
        if "acide" in ph:
            if plante_acide != int(nombre_graines):
                del(combinaisons[compteur])
        elif "basique" in ph:
            if plante_basique != int(nombre_graines):
                del(combinaisons[compteur])
        if "sec" in sechumide:
            if plante_sec != int(nombre_graines):
                del(combinaisons[compteur])
        elif "humide" in sechumide:
            if plante_humide != int(nombre_graines):
                del(combinaisons[compteur])
        if "chaud" in temp:
            if plante_chaud != int(nombre_graines):
                del(combinaison[compteur])
        elif "froid" in temp:
            if plante_froid != int(nombre_graines):
                del(combinaisons[compteur])
    return(combinaisons)


#On veut que au moins la moitié des plantes de notre mélange attire les abeilles sauvages.
#Donc pour chaque plante, on regarde dans la colonne s'il y a un oui.
#On n'a pas les infos pour l'intégralité des plantes. Pour cela qu'on ne demande que la moitié.
def tri_sauvages():
    global nombre_graine
    nombre_graines = int(nombre_graine.get())
    combinaisons = tri_sol()
    nouvelle_liste = []
    for combinaison in combinaisons:
        oui = 0
        for plante in combinaison:
            if "oui" in plante[33]:
                oui += 1
        if oui > nombre_graines/4:
            nouvelle_liste.append(combinaison)
    return(nouvelle_liste)


#Cette fonction garde les 20 combinaisons qui comportent le plus de nectar
#D'abord on favorise les melanges avec le plus de nectar car larves et adultes en  mange (pollen seulement larves)
def tri_nectar():
    global nombre_graine
    nombre_graines = int(nombre_graine.get())
    combinaisons = tri_sauvages()
    nouvelle_liste = []
    nectar = []
    if len(combinaisons) < 21:
        return(combinaisons)
    for combinaison in combinaisons:
        nectar_compt = 0
        compteur_nectar = 0
        for plante in combinaison:
            if plante[15] == "0" or plante[15] == "1" or plante[15] == "2" or plante[15] == "3": #Colonne score nectar
                nectar_compt += int(plante[15])
                compteur_nectar += 1
        nectar_compt = nectar_compt/(compteur_nectar+1) #Pour avoir une moyenne et ne pas prendre en compte les plantes sans info / +1 pour éviter division par 0
        nectar.append(nectar_compt)
    index_max_nectar = []
    for combinaison in range(0,20): #Attention pbm si combinaisons contient moins de 20 combinaisons au début
        nectar = [int(i) for i in nectar]
        maxi = nectar.index(max(nectar))
        nouvelle_liste.append(combinaisons[maxi])
        index_max_nectar.append(maxi)
        nectar[maxi] = 0
    return(nouvelle_liste)



#Parmi les 20, on prend les 3 avec le plus de pollen
def tri_pollen():
    combinaisons = tri_nectar()
    nouvelle_liste = []
    pollen = []
    if len(combinaisons) < 3:
        return(combinaisons)
    for combinaison in combinaisons:
        pollen_compt = 0
        compteur_pollen = 0
        for plante in combinaison:
            if  plante[16] == "0" or plante[16] == "1" or plante[16] == "2" or plante[16] == "3": #Colonne score pollen
                pollen_compt += int(plante[16])
                compteur_pollen += 1
        pollen_compt = pollen_compt/(compteur_pollen+1)
        pollen.append(pollen_compt)
    index_max_pollen = []
    for combinaison in range(0,3):
        pollen = [int(i) for i in pollen] #On convertit tout en nombre
        maxi = pollen.index(max(pollen))
        nouvelle_liste.append(combinaisons[maxi])
        index_max_pollen.append(maxi)
        pollen[maxi] = 0
    return(nouvelle_liste)


#Les 3 meilleurs mélanges sont renvoyés à l'utilisateur
def tri_final():
    combinaisons = tri_pollen()
    nom_scient_tot = []
    nom_com_tot = []
    if len(combinaisons) == 3:
        for combinaison in combinaisons:
            nom_scient = []
            nom_com = []
            for plante in combinaison:
                nom_scient.append(plante[1])
                nom_com.append(plante[0])
            nom_scient_tot.append(nom_scient)
            nom_com_tot.append(nom_com)
        n = str(nom_scient_tot[0])
        fenetre2 = Toplevel(bg = "white") #Ouverture d'une deuxième fenetre graphique
        fenetre2.title('Résultats')
        fenetre2.iconbitmap("icone_abeille.ico")

        texte = Label(fenetre2, bg = "white", text = "Voici 3 propositions de mélanges qui répondent à vos critères", font = petit_titre)
        texte.pack()


        W = 1000

        #La taille de la fenêtre est très différente selon le nombre de plantes donc on ajuste...
        if len(combinaisons[0]) < 12:
            H = len(combinaisons[0]) * 79
        elif len(combinaisons[0]) < 20:
            H = len(combinaisons[0]) * 73
        elif len(combinaisons[0]) < 30:
            H = len(combinaisons[0]) * 70
        elif len(combinaison[0]) < 40:
            H = len(combinaisons[0]) * 65

        #Création d'un canvas pour rajouter une scrollbar
        canvas=Canvas(fenetre2, width=W, scrollregion =(0, 0, 10, H), bg='ivory')
        canvas.pack(side=LEFT)

        frame = Frame(canvas, bg = "white")
        frame.pack()

        #Création de la scrollbar
        vbar=Scrollbar(fenetre2,orient=VERTICAL)
        vbar.pack(side=RIGHT,fill=Y)
        vbar.config(command=canvas.yview)
        canvas['yscrollcommand']=vbar.set
        canvas.create_window((0,0),window=frame,width=W, height=H, anchor = "nw")

        frame2 = LabelFrame(frame, bg = "white")
        frame2.pack(side = BOTTOM, expand = YES)

        premier = LabelFrame(frame, bg = "white", text="Premier mélange", padx=20, pady=20, font = autre)
        premier.pack(fill="both", expand="yes", side = LEFT) #creation d'un premier cadre. side = LEFT permet d'avoir les 3 cadres sur la meme ligne
        for i in range(0,len(nom_scient_tot[0])): #boucle pour avoir chaque nom de plante à la suite en colonne
            texte_melange1 = Label(premier, bg = "white", text = str(nom_com_tot[0][i]), font = autre)
            texte_melange1.pack()
            texte_melange = Label(premier, bg = "white", text = "("+ nom_scient_tot[0][i] + ")\n", font = nom_latin)
            texte_melange.pack()
        widget1 = Button(premier, text = "En savoir plus", command=lambda:precis_melange(combinaisons[0]), bg = "grey70", font = autre1)
        #On utilise une fonction lambda qui permet d'utiliser une seule fonction dont la variable va changer selon ce qu'on veut faire.
        widget1.pack(expand=YES, fill=X)


        deuxieme = LabelFrame(frame, bg = "white", text="Deuxième mélange", padx=20, pady=20, font = autre)
        deuxieme.pack(fill="both", expand="yes", side = LEFT)

        for i in range(0, len(nom_scient_tot[1])):
            texte_melange2 = Label(deuxieme, bg = "white", text = str(nom_com_tot[1][i]), font = autre)
            texte_melange2.pack()
            texte_melange2 = Label(deuxieme, bg = "white", text = "(" + nom_scient_tot[1][i] + ")\n", font = nom_latin)
            texte_melange2.pack()
        widget2 = Button(deuxieme, text = "En savoir plus", command=lambda:precis_melange(combinaisons[1]), bg = "grey70", font = autre1)
        widget2.pack(expand=YES, fill=X)

        troisieme = LabelFrame(frame, bg = "white", text="Troisième mélange", padx=20, pady=20, font = autre)
        troisieme.pack(fill="both", expand="yes", side = LEFT)
        for i in range(0, len(nom_scient_tot[2])):
            texte_melange3 = Label(troisieme, bg = "white", text = str(nom_com_tot[2][i]), font = autre)
            texte_melange3.pack()
            texte_melange3 = Label(troisieme, bg = "white", text = "(" + nom_scient_tot[2][i] + ")\n", font = nom_latin)
            texte_melange3.pack()
        widget3 = Button(troisieme, text = "En savoir plus", command=lambda:precis_melange(combinaisons[2]), bg = "grey70", font = autre1)
        widget3.pack(expand=YES, fill=X)



        texte2 = Label(frame2, bg = "white", text = "Attention, si vous enregistrez ces résultats, votre précédente sauvegarde sera supprimée.\nVous trouverez votre sauvegarde dans le dossier Prairie Fleurie qui se trouve dans le dossier Programmes.", font = autre1)
        texte2.pack(side = BOTTOM)

        widget4 = Button(frame2, text = "Enregistrer les mélanges", bg = "grey70", command = lambda:enregistrer(nom_scient_tot), font = autre1)
        widget4.pack(expand = YES, fill = X)



    else:
        messagebox.showerror("Conditions trop strictes","Les conditions requises sont trop strictes pour avoir un choix assez larges de graines. Nous vous conseillons de revoir vos conditions.") #Ouvre une fenetre d'erreur

def enregistrer(nom_scient):

    melange = ""
    for plante in nom_scient:
        melange = melange + "Mélange : "
        for i in range(0, len(plante)):
            melange = melange + str(plante[i]) + " "
        melange = melange + "\n"


    NomFichier = 'Melanges de graines Prairie Fleurie.txt'

    Fichier = open(NomFichier,'w')
    Fichier.write(melange)
    Fichier.close()
    messagebox.showinfo("Enregistrement", "Enregistrement réussi")


#Permet d'ouvrir une fenetre pour chaque mélange qui détaille les caracteristiques du melange.
#On refait les calculs à chaque fois.
#On l'appelle avec un lambda : ça permet de ne créer qu'une fonction pour les 3 mélanges tout en ayant un argument qui change dans la fonction.
def precis_melange(x):
    f_melange = Toplevel(bg = "white") #Ouverture d'une deuxième fenetre graphique
    f_melange.title('Caractéristiques du mélange créé')
    f_melange.iconbitmap("icone_abeille.ico")

    melangecree = x
    nombre_graines = int(nombre_graine.get())
    famille = []
    hauteur = []
    couleur = []
    vivace, annuelle = 0, 0
    nectar, pollen, compt_nectar, compt_pollen = 0, 0, 0, 0
    mars, avril, mai, juin, juillet, aout, septembre, octobre = 0, 0, 0, 0, 0, 0, 0, 0
    for plante in melangecree:
        famille.append(plante[2])
        mars += int(plante[6])
        avril += int(plante[7])
        mai += int(plante[8])
        juin += int(plante[9])
        juillet += int(plante[10])
        aout += int(plante[11])
        septembre += int(plante[12])
        octobre += int(plante[13])
        hauteur.append(plante[23])
        chaine = plante[28]
        chaine = chaine.split(",")
        couleur = couleur + chaine
        if plante[15] == "0" or plante[15] == "1" or plante[15] == "2" or plante[15] == "3":
            compt_nectar += 1
            nectar += int(plante[15])
        if plante[16] == "0" or plante[16] == "1" or plante[16] == "2" or plante[16] == "3":
            compt_pollen += 1
            pollen += int(plante[16])
        if plante[3] == "P":
            vivace += 1
        if plante[3] == "A" or plante[3] == "B":
            annuelle += 1
    famille = set(famille)
    couleur = set(couleur)
    hauteur = [int(i) for i in hauteur] #Pour être sûr d'avoir des nombres et non des chaînes de caractères


    texte = Label(f_melange, bg = "white", text = "Nombre de familles végétales : " + str(len(famille)), font = petit_titre)
    texte.pack()
    texte_flo = Label(f_melange, bg = "white", text = "Nombre de plantes en fleurs par mois : \nMars : " + str(mars) + "\nAvril : " + str(avril) + "\nMai : " + str(mai)+ "\nJuin : " + str(juin) + "\nJuillet : " + str(juillet) + "\nAoût : " + str(aout) + "\nSeptembre : " + str(septembre) + "\nOctobre : " + str(octobre), font = petit_titre)
    texte_flo.pack()
    texte_taille = Label(f_melange, bg = "white", text = "La taille maximale de la prairie sera de " + str(max(hauteur)) + " cm.", font = petit_titre)
    texte_taille.pack()
    texte_couleur = Label(f_melange, bg = "white", text = "Nombre de couleurs de fleurs : " + str(len(couleur)), font = petit_titre)
    texte_couleur.pack()
    texte_annuelle = Label(f_melange, bg = "white", text = "Pourcentage de plantes annuelles : " + str(round(annuelle/nombre_graines*100, 1)) + "%", font = petit_titre)
    texte_annuelle.pack()
    texte_vivace = Label(f_melange, bg = "white", text = "Pourcentage de plantes vivaces : " + str(round(vivace/nombre_graines*100, 1)) + "%", font = petit_titre)
    texte_vivace.pack()
    texte_pollen = Label(f_melange, bg = "white", text = "Potentiel pollinifère : " + str(round(pollen/compt_pollen, 1)) + "/3", font = petit_titre)
    texte_pollen.pack()
    texte_nectar = Label(f_melange, bg = "white", text = "Potentiel nectarifère : " + str(round(nectar/compt_pollen, 1)) + "/3", font = petit_titre)
    texte_nectar.pack()




##TRAITEMENT DES ERREURS QU'ON PEUT AVOIR

#Message d'erreur si les parametres remplis par l'utilisateur ne sont pas compatibles
def verif_erreur():
    global nombre_graine, famille1, annuelle, vivace, couleur1, hauteur1
    if famille1 != 5 and annuelle != 25 and vivace != 25 and couleur1 != 5:
        famille1 = famille1.get()
        vivace = vivace.get()
        annuelle = annuelle.get()
        couleur1 = couleur1.get()

    if int(nombre_graine.get()) < int(famille1):
        messagebox.showerror("Famille","Il y a plus de familles végétales que d'espèces végétales demandées dans le mélange, merci de corriger puis recommencer.'")
    elif int(annuelle) + int(vivace) > 100:
        messagebox.showerror("% Vivace/Annuelle", "La somme des pourcentages de plantes vivaces et annuelles est supérieure à 100%. Merci de corriger puis recommencer.")
    elif int(nombre_graine.get()) < 5 or int(nombre_graine.get()) > 40:
        messagebox.showerror("Nombre de graines", "Le nombre de graines doit être compris entre 5 et 40. Merci de corriger puis recommencer")
    elif int(nombre_graine.get()) < int(couleur1):
        messagebox.showerror("Couleur", "Vous ne pouvez pas avoir plus de couleurs que d'espèces dans votre mélange, merci de corriger puis recommencer.")
    elif int(hauteur1.get()) < 80 or int(hauteur1.get()) > 400:
        messagebox.showerror("Hauteur", "La hauteur doit être comprise entre 80 et 400 cm, merci de corriger puis recommencer.")
    else:
        tri_final()



##CREATION FENETRE GRAPHIQUE ET WIDGETS

#Définition des font (taille et style de caractere)
nom_latin = "{Arial} 10 italic"
gros_titre = "{Arial} 16 bold"
petit_titre = "{Arial} 12"
autre = "{Arial} 10"
autre1 = "{Arial} 10"


def principale():
    global couleur1, annuelle, vivace, famille1, var_temp, var_sechumide, var_ph, hauteur1, nombre_graine, var_dispo
    fenetre = Toplevel(bg = "white")
    fenetre.title('Mélange pour prairie fleurie')
    fenetre.iconbitmap("icone_abeille.ico")

    #Petit texte explication
    l = LabelFrame(fenetre, bg = "white", text="Choix des graines pour prairie fleurie", labelanchor = "n", font = gros_titre, relief = "flat")
    l.pack( fill="both", expand="yes")

    Label(l, bg = "white", text="\nCette fenêtre vous permet de créer des mélanges de graines pour prairies fleuries. \n\nMerci de donner le nombre d'espèces végétales, la hauteur souhaitée de votre prairie, \nainsi que les conditions de votre sol. \nPour les options avancées vous pouvez changer les valeurs par défaut si vous le souhaitez.\n", font = autre1).pack()


    fenetre2 = LabelFrame(fenetre, bg = "white", relief = "flat")
    fenetre2.pack(fill = "both", expand = "yes")

    #Nnombres de graines
    label = Label(fenetre2, bg = "white", text="Nombre d'espèces végétales que vous souhaitez dans votre mélange (entre 5 et 40) : ", font = autre)
    label.pack()

    nombre_graine =  Spinbox(fenetre2, from_ = 5, to = 40, wrap = TRUE) #wrap permet de revenir à 5 quand on est à 40
    nombre_graine.delete(0, 5) #On supprime la valeur de départ...
    nombre_graine.insert(0,15) #...pour mettre notre valeur par défaut.
    nombre_graine.pack()



    #Hauteur
    label = Label(fenetre2, bg = "white", text = "Hauteur maximum souhaitée de la prairie (entre 80 et 400 cm) : ", font = autre)
    label.pack()

    hauteur1 =  Spinbox(fenetre2, from_ = 80, to = 400, wrap = TRUE)
    hauteur1.delete(0, 5)
    hauteur1.insert(0,120)
    hauteur1.pack()


    #Création d'un cadre tout en bas qui contiendra les boutons
    bottomframe = Frame(fenetre, bg = "white")
    bottomframe.pack( side = BOTTOM, expand = "yes" )

    #Création de 3 cadres côte à côté qui contiendront les radiobuttons
    ph = LabelFrame(fenetre, bg = "white", text="pH du sol", labelanchor = "n", font = petit_titre)
    ph.pack(fill="both", expand="yes", side = LEFT)
    hum = LabelFrame(fenetre, bg = "white", text="Humidité du sol", labelanchor = "n", font = petit_titre)
    hum.pack(fill="both", expand="yes", side = LEFT)
    climat = LabelFrame(fenetre, bg = "white", text="Climat", labelanchor = "n", font = petit_titre)
    climat.pack(fill="both", expand="yes", side = LEFT)


    #Creation des Radiobutton : ils fonctionnent par 3, soit on coche acide soit basique soit neutre mais pas les 3
    # Radiobutton Basique ou Acide
    var_ph = StringVar() #En sortie on a une chaine de caractere donné par value du Radiobutton

    basique = Radiobutton(ph, bg = "white", text="Sol basique", variable = var_ph, value = "basique", font = autre)
    acide = Radiobutton(ph, bg = "white", text = "Sol acide", variable = var_ph, value = "acide", font = autre)
    neutre = Radiobutton(ph, bg = "white", text = "Sol neutre", variable = var_ph, value = "neutre", font = autre)
    basique.pack(anchor = "w")
    acide.pack(anchor = "w")
    neutre.pack(anchor = "w")
    var_ph.set("neutre") #coche la valeur par défaut

    #Radiobutton Sec ou Humide
    var_sechumide = StringVar()

    sec = Radiobutton(hum, bg = "white", text = "Sol sec", variable = var_sechumide, value =  "sec", font = autre)
    humide = Radiobutton(hum, bg = "white", text = "Sol humide", variable = var_sechumide, value = "humide", font = autre)
    interm = Radiobutton(hum, bg = "white", text = "Intermédiaire", variable = var_sechumide, value = "interm", font = autre)

    sec.pack(anchor = "w")
    humide.pack(anchor = "w")
    interm.pack(anchor = "w")
    var_sechumide.set("interm")

    #Radiobutton Temperature
    var_temp = StringVar()

    chaud = Radiobutton(climat, bg = "white", text = "Climat chaud", variable = var_temp, value = "chaud", font = autre)
    froid = Radiobutton(climat, bg = "white", text = "Climat froid", variable = var_temp, value = "froid", font = autre)
    moyen = Radiobutton(climat, bg = "white", text = "Intermédiaire", variable = var_temp, value = "moyen", font = autre)
    froid.pack(anchor = "w")
    chaud.pack(anchor = "w")
    moyen.pack(anchor = "w")
    var_temp.set("moyen")

    #Creation du bouton pour lancer le programme
    widget = Button(bottomframe, bg = "grey70", text = "Lancer le programme", command = verif_erreur, font = petit_titre)
    widget.pack(expand=YES, fill=X)




##Création du cadre avec les options avancées
#Ce cadre permet de modifier les valeurs par défaut. Fonctionne aussi très bien si on n'y touche pas.

    options2 = LabelFrame(bottomframe, bg = "white", text = "Vérifier la disponibilité chez les semenciers", labelanchor = "n", font = petit_titre, relief = "flat")
    options2.pack(fill="both", expand= YES, side = BOTTOM)

    options = LabelFrame(bottomframe, bg = "white", text="Options avancées", labelanchor = "n", font = petit_titre, relief = "flat")
    options.pack(fill="both", expand= YES, side = BOTTOM)

    Label(options, bg = "white", text="\n", font = autre1).pack(side = BOTTOM)

    frame1 = Frame(options, bg = "white",)
    frame1.pack(expand = YES, side = LEFT )
    frame2 = Frame(options, bg = "white",)
    frame2.pack(expand = YES, side = RIGHT)

    #Famille
    defaut_famille = 5
    famille1 =  Spinbox(frame2, from_ = 1, to = 40, wrap = TRUE)
    famille1.delete(0,5) #suppression de ce qui est dans la case du spinbox
    famille1.insert(0,defaut_famille) #On met la valeur par défaut dans la case
    famille1.pack(side = BOTTOM)
    fam = Label(frame2, bg = "white", text = "Nombre de familles végétales minimum : ", font = autre)
    fam.pack(side = BOTTOM)

    #% plantes vivaces
    defaut_vivace = 25
    vivace = Spinbox(frame1, from_ = 0, to = 100, increment=1)
    vivace.delete(0, 5) # supprime entièrement la case valeur
    vivace.insert(0, defaut_vivace) # insère la valeur défaut, donc 1084
    vivace.pack(side = BOTTOM)
    viv = Label(frame1, bg = "white", text = "Pourcentage minimum de plantes vivaces : ", font = autre)
    viv.pack(side = BOTTOM)

    #% plantes annuelles/bisannuelles
    defaut_annuel = 25
    annuelle = Spinbox(frame1, from_ = 0, to = 100, increment=1)
    annuelle.delete(0, 5) # supprime entièrement la case valeur
    annuelle.insert(0, defaut_annuel) # insère la valeur défaut, donc 1084
    annuelle.pack(side = BOTTOM)
    an = Label(frame1, bg = "white", text = "Pourcentage minimum de plantes annuelles : ", font = autre)
    an.pack(side = BOTTOM)

    #Couleur
    defaut_couleur = 5
    couleur1 = Spinbox(frame2, from_ = 1, to = 40, increment=1)
    couleur1.delete(0, 5) # supprime entièrement la case valeur
    couleur1.insert(0, defaut_couleur) # insère la valeur défaut, donc 1084
    couleur1.pack(side = BOTTOM)
    coul = Label(frame2, bg = "white", text = "Nombre de couleurs de fleurs différentes : ", font = autre)
    coul.pack(side = BOTTOM)

    #Disponibilite des graines

    var_dispo = StringVar()

    Non = Radiobutton(options2, bg = "white", text = "Non", variable = var_dispo, value =  0, font = autre)
    Tous = Radiobutton(options2, bg = "white", text = "Oui, tous les semenciers", variable = var_dispo, value = 1, font = autre)
    Zygene = Radiobutton(options2, bg = "white", text = "Oui, uniquement chez Zygène", variable = var_dispo, value = 2, font = autre)
    CNPMAI = Radiobutton(options2, bg = "white", text = "Oui, uniquement au CNPMAI", variable = var_dispo, value = 3, font = autre)
    sauveterre = Radiobutton(options2, bg = "white", text = "Oui, uniquement au jardin de sauveterre", variable = var_dispo, value = 4, font = autre)
    Puy = Radiobutton(options2, bg = "white", text = "Oui, uniquement chez les semences du Puy", variable = var_dispo, value = 5, font = autre)

    Non.pack(anchor = "w")
    Tous.pack(anchor = "w")
    Zygene.pack(anchor = "w")
    CNPMAI.pack(anchor = "w")
    sauveterre.pack(anchor = "w")
    Puy.pack(anchor = "w")
    var_dispo.set(0) # default value



