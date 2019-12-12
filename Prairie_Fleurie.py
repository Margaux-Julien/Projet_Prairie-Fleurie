from tkinter import *
from tkinter import messagebox
#import os
import smtplib

#os.chdir("C:/Users/Rihanon/Documents/Stage M2/Algo choix graines")

#Importation des 2 autres scripts pour pouvoir utiliser les fonctions contenues dedans.
import testermelange
import creermelange



##DEFINITION DES FONCTIONS

#Cette fonction permet de lancer la fenêtre de test de mélange.
#Si une autre fenêtre est ouverte, celle-ci se ferme avant ouverture de l'autre.
def testmelange():
     for widget in fenetre_main.winfo_children():
          if isinstance(widget,Toplevel):
               widget.destroy()

     testermelange.test()

#Cette fonction permet de lancer la fenêtre pour créer un mélange.
def fairemelange():
     for widget in fenetre_main.winfo_children():
          if isinstance(widget,Toplevel):
               widget.destroy()
     creermelange.principale()

#Ouvre le pdf guide
def aide():
     if os.path.isfile("Guide.pdf"): #On vérifie que le pdf n'a pas été supprimé du dossier.
          os.startfile("Guide.pdf")
     else:
          messagebox.showinfo("Aide", "Vous semblez avoir supprimé le fichier pdf du dossier. Veuillez recommencer le téléchargement du logiciel pour avoir accès à l'aide complète.")

#Permet d'envoyer un mail pour reporter un problème
#ATTENTION CETTE FONCTION SEMBLE NE PLUS FONCTIONNER
def sendmail():
    fenetremail = Toplevel()
    fenetremail.title('Formulaire de contact')
    fenetremail.iconbitmap("icone_abeille.ico")

    fenetre1 = LabelFrame(fenetremail, bg = "white", relief = 'flat')
    fenetre1.pack(fill = "both", expand = "yes")

    fenetre2 = LabelFrame(fenetremail, bg = "white", relief = 'flat')
    fenetre2.pack(fill = "both", expand = "yes")

    fenetre3 = LabelFrame(fenetremail, bg = "white", relief = 'flat')
    fenetre3.pack(fill = "both", expand = "yes")

    fenetre4 = LabelFrame(fenetremail, bg = "white", relief = 'flat')
    fenetre4.pack(fill = "both", expand = "yes", side = BOTTOM)

    Label(fenetre1, bg = "white", text="Veuillez remplir le formulaire de contact.\n", font = autre).pack(side = TOP)

    #Choix du sujet du mail
    Label(fenetre1, bg = "white", text = "Sujet : ", font = autre1).pack(side = LEFT)
    sujet = Spinbox(fenetre1, values = ("Ajouter une plante",  "Ajouter un semencier", "Signaler un problème", "Faire une suggestion", "Autre"), state = 'readonly', wrap = True)
    sujet.pack(side = LEFT)


    #Adresse mail
    Label(fenetre2, bg = "white", text = "Votre adresse mail : ", font = autre1).pack(side = LEFT)
    value = StringVar()
    entree = Entry(fenetre2, textvariable= value, width=50)
    entree.pack(side = RIGHT)

    #Corps du message
    Label(fenetre3, bg = "white", text = "Votre message : ", font = autre1).pack(side = LEFT)
    message = Text(fenetre3, width = 38, height = 10)
    message.pack(side = RIGHT)

    #Bouton pour envoyer le mail
    widget = Button(fenetre4, text = "Envoyer le mail", command = lambda:envoyer(sujet, value, message), bg = "grey70", font = autre1)
    widget.pack(expand = YES, fill = X)

    Label(fenetre4, text = "\nNB : Il vous faut une connexion internet pour envoyer un mail.", font = autre1, bg = "white").pack(fill = "both", expand = 'yes', side = BOTTOM)

#Fonction en lien avec la précédente pour l'envoi du mail
def envoyer(sujet, value, message):
     if len(message.get(1.0,END)) == 1:
          messagebox.showinfo("Message vide", "Vous ne pouvez pas envoyer un message vide.")
     elif "@" not in str(value.get()) or "." not in str(value.get()):
          messagebox.showinfo("Mail incorrect", "Votre adresse mail est incorrect.")
     else:
          server = smtplib.SMTP()
          server.connect('smtp.u-psud.fr')
          server.helo()
          fromaddr = 'margaux.julien@u-psud.fr'
          toaddrs = ['margaux.julien@u-psud.fr'] # On peut mettre autant d'adresses que l'on souhaite
          sujet = str(sujet.get())
          message = (str(message.get(1.0, END)),str(value.get()))
          msg = """\
From: %s\r\n\
To: %s\r\n\
Subject: %s\r\n\
\r\n\
%s
""" % (fromaddr, ", ".join(toaddrs), sujet, message)
          try:
               server.sendmail(fromaddr, toaddrs, msg)
               messagebox.showinfo("Envoyé", "Votre e-mail a bien été envoyé.")
          except smtplib.SMTPException as e:
               messagebox.showinfo("Problème","Votre e-mail n'a pas été envoyé. Vérifiez que vous êtes bien connecté à internet.")
# {} # Réponse du serveur
          server.quit()

#Définition des font (taille et style de caractere)
nom_latin = "{Arial} 12 italic"
gros_titre = "{Arial} 16 bold"
petit_titre = "{Arial} 14"
autre = "{Arial} 12"
autre1 = "{Arial} 10"


##CREATION DE LA FENETRE PRINCIPALE
fenetre_main = Tk()
fenetre_main.title("Prairie fleurie")
fenetre_main.iconbitmap("icone_abeille.ico")

l = LabelFrame(fenetre_main, labelanchor = "n", text="Bienvenue sur Prairie Fleurie !", padx=20, pady=20, font = gros_titre, bg = "white", relief = "flat")
l.pack(fill="both", expand="yes")

Label(l, text="Ce logiciel est un outil d'aide à la création de prairies fleuries pour attirer les pollinisateur.\nSi vous avez déjà un mélange et que vous voulez savoir s'il est de qualité, cliquez sur 'Tester mon mélange'.\nSi vous n'avez pas encore de mélange et que vous souhaitez en créer un, cliquez sur 'Faire un mélange'.\n", font = autre1, bg = "white").pack()

Label(l, text="Que voulez-vous faire ?\n", font = petit_titre, bg = "white").pack()


#Création des boutons qui sont liés aux fonctions définies plus haut

widget = Button(l, text = "Tester votre mélange", command = testmelange, bg = "grey70", font = autre1)
widget.pack(expand=YES, fill=X)

widget = Button(l, text = "Faire votre mélange", command = fairemelange, bg = "grey70", font = autre1)
widget.pack(expand=YES, fill=X)

widget = Button(l, text = "Aide", command = aide, bg = "grey70", font = autre1)
widget.pack(expand = YES, fill = X)

widget = Button(l, text = "Contact", command = sendmail, bg = "grey70", font = autre1)
widget.pack(expand = YES, fill = X)



#Ouverture de la fenêtre
fenetre_main.mainloop()

