# coding: utf-8
"""
Script pour initialiser des grilles vides dans le dossier Grilles.
Permet de préremplir tous les tirets, il ne restera alors plus qu'à mettre les chiffres.
"""
import os

while True:
    print("Quel numéro donner à la nouvelle grille ?")
    i=input("-> ")
    if i+".txt" not in os.listdir(".\Grilles"): break
    else: print("Ce numéro est déjà pris !\n\n")
while True:
    print("Combien de lignes pour cette grille ?")
    try:
        n = int(input("-> "))
        if n<=0: print("Le nombre de lignes doit être au moins 1 !")
        elif n>25: print("25 est le nombre maximal de lignes !")
        else: break
    except KeyboardInterrupt:
        raise
    except:
        print("Cela ne ressemble pas à un nombre !")
while True:
    print("Combien de colonnes pour cette grille ?")
    try:
        m = int(input("-> "))
        if m<=0: print("Le nombre de colonnes doit être au moins 1 !")
        elif m>25: print("25 est le nombre maximal de colonnes !")
        else: break
    except KeyboardInterrupt:
        raise
    except:
        print("Cela ne ressemble pas à un nombre !")
with open(os.path.join("Grilles", i+".txt"), 'w') as f:
    f.write(f"{n} lignes\n")
    f.write(f"{m} colonnes\n")
    for i in range(n):
        for j in range(m-1):
            f.write("- ")
        f.write("-\n")
print("Grille vide créée ! Vous pouvez la trouver dans le dossier Grilles.\nDans votre grille, vous n'aurez plus qu'à remplacer certains tirets par vos nombres.\nAppuyez sur Entrer pour fermer cette fenêtre.")
input()