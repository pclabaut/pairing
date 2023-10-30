import numpy as np 
import pandas as pd
import random

with pd.ExcelFile("mypairing.xlsx") as source_us :
    df1 = pd.read_excel(source_us, 0)
    bt_us = df1['BT'].to_dict()
    bt_them = dict(enumerate(map(str, df1.columns.values[1:])))
    estimate = [pd.read_excel(source_us, i).to_numpy()[:,1:] for i in range(0,4)]

r_bt_us = {v: k for k, v in bt_us.items()}
r_bt_them = {v: k for k, v in bt_them.items()}
    
###Structure
##1 feuille par scénario
#lignes = nos bt (0 à 7)
#colonne = leurs bt (0 à 7)
#case = score de notre joueur (de 0 à 20)

#On se base pour le moment sur un unique estimate partagé

def calculate(matchs,estimate) :  #Retourne le score attendu correspondant a un ensemble de 8 matchs
    result = 0
    for s in range(0,4) :  #Unpack les senarii
        for p in range(0,2) :  #Unpack les parties par sénario
            bt_us = int(matchs[s][p][0])
            bt_them = int(matchs[s][p][1])
            result += estimate[s][bt_us,bt_them] #score attendue de notre bt match[s][p][0] contre leur bt match[s][p][1]
    return min(120,result)  #Cap a 12

def display(estimate, tour, l_us, l_them):    #Affiche la matrice des bt restants dans le scénarioo en cours
    
    affiche = np.empty((len(l_us),len(l_them)), dtype=object)   #initialisation
    for x,i in enumerate(l_us) :
        affiche[x,:] = estimate[tour-1][i,l_them]  #Collecte
    pda = pd.DataFrame(affiche,index=[bt_us[x] for x in l_us], columns=[bt_them[x] for x in l_them])
    
    print("***** Estimés pour le scnérario numéro : "+str(tour)+" *****") 
    print(pda)
    print("**********")
    return 
    
def quick_opt_blind_us_2(l_us, l_them, matchs, estimate) : #1er algo basique pour tenter de trouver le meilleur pick (nous)
    n_tries = 100      #Nombre de combinaisons aléatoires envisagées a chaque coup
    rem = len(l_us)   
    best_pick_them = l_us[0]
    max_res = 0
    
    for np in l_us :  #On donne une chance a chaque BT restant en main
        res = 0
        for i in range(0,n_tries):  #On calcule n_tries combinaison possible si on choisit ce bt là
            m = matchs.copy()
            l_us_rest = l_us.copy()
            l_us_rest.remove(np)
            mouv_them = random.sample(l_them, k=rem)   #On prends tout les futurs autres pick au hasard...
            mouv_us = [np]+random.sample(l_us_rest, k=rem-1)   #... pour les deux joueurs
            for j in range(0,int(rem/2)):
                m.append([[mouv_us[int(0+j*2)], mouv_them[int(0+j*2)]],[mouv_us[int(1+j*2)], mouv_them[int(1+j*2)]]])
            res += calculate(m, estimate)   #On recompose le set de 8 match et on calcul son score pour chaque combinaison

        m_res = res/n_tries  #On calcule la moyenne résultante pour chaque bt proposé à ce coup
        if m_res > max_res :
            max_res = m_res
            best_pick_us = np  #On détermine, en moyenne, le meilleur BT pour ce coup
            
    return best_pick_us

def quick_opt_blind_opponent_2(l_us, l_them, matchs, estimate_opp) : #Voir au dessus. Même principe mais en minimisant le score (donc enmaximisant celui de l'adversaire)
    rem = len(l_us)   
    best_pick_them = l_them[0]
    min_res = 120
    
    for np in l_them :  
        res = 0
        for i in range(0,100):
            m = matchs.copy()
            l_them_rest = l_them.copy()
            l_them_rest.remove(np)
            mouv_us = random.sample(l_us, k=rem)
            mouv_them = [np]+random.sample(l_them_rest, k=rem-1)
            for j in range(0,int(rem/2)):
                m.append([[mouv_us[int(0+j*2)], mouv_them[int(0+j*2)]],[mouv_us[int(1+j*2)], mouv_them[int(1+j*2)]]])
            res += calculate(m, estimate_opp)

        m_res = res/100
        if m_res < min_res :
            min_res = m_res
            best_pick_them = np
            
    return best_pick_them
 
def quick_opt_blind_us_3(l_us, l_them, matchs, estimate, a_them) : #2eme algo basique pour pick le meilleur parmis leurs 2 attaquants
    n_tries = 100      #Nombre de combinaisons aléatoires envisagées a chaque coup
    rem = len(l_us)   
    best_pick_them = l_us[0]
    max_res = 0
    
    for o in a_them :  #On teste les deux possibilitées
        res = 0
        for i in range(0,n_tries):  #On calcule n_tries combinaison possible si on choisit ce bt là
            m = matchs.copy()
            l_us_rest = l_us.copy()
            l_us_rest.remove(np)
            
            
            
            
            
            mouv_them = random.sample(l_them, k=rem)   #On prends tout les futurs autres pick au hasard...
            mouv_us = [np]+random.sample(l_us_rest, k=rem-1)   #... pour les deux joueurs
            
            
            
            
            for j in range(0,int(rem/2)):
                m.append([[mouv_us[int(0+j*2)], mouv_them[int(0+j*2)]],[mouv_us[int(1+j*2)], mouv_them[int(1+j*2)]]])
            res += calculate(m, estimate)   #On recompose le set de 8 match et on calcul son score pour chaque combinaison

        m_res = res/n_tries  #On calcule la moyenne résultante pour chaque bt proposé à ce coup
        if m_res > max_res :
            max_res = m_res
            best_pick_us = np  #On détermine, en moyenne, le meilleur BT pour ce coup
            
    return best_pick_us

def turn12(l_us, l_them, matchs, estimate, mode, tour): #Boucle principale Pour le sénario 1 ou 2
    
    #choix des défenseurs d_us et d_them
    if mode == "bot" :
        d_us = quick_opt_blind_us_2(l_us, l_them, matchs, estimate)  #Ici, on utilise le premier algo pour notre choix
        d_them = quick_opt_blind_opponent_2(l_us, l_them, matchs, estimate) #Et là, pour leur choix
    elif mode == "training" :
        print("¤¤¤ Il nous reste :",', '.join([bt_us[x] for x in l_us]))
        print("xxx Il leur reste :",', '.join([bt_them[x] for x in l_them]))
        out = 'nan'
        while out not in [bt_us[x] for x in l_us] :
            out = input("Notre défenseur ? ")
        d_us = r_bt_us[out]
        d_them = quick_opt_blind_opponent_2(l_us, l_them, matchs, estimate)
        print("Leur défenseur : "+bt_them[d_them])
    elif mode == "manuel" :
        print("¤¤¤ Il nous reste :",', '.join([bt_us[x] for x in l_us]))
        print("xxx Il leur reste :",', '.join([bt_them[x] for x in l_them]))
        display(estimate, tour, l_us, l_them)
        out = 'nan'
        while out not in [bt_us[x] for x in l_us] :
            out = input("Notre défenseur ? ")
        d_us = r_bt_us[out]
        out = 'nan'
        while out not in [bt_them[x] for x in l_them] :
            out = input("Leur défenseur ? (choix par l'adversaire) ")
        d_them = r_bt_them[out]      
    
    #d_us = random.choice(l_us)                   #Alternative en random
    #d_them = random.choice(l_them)
    
    l_us.remove(d_us) #On retire les defenseurs proposés des BT disponibles de chaque équipe
    l_them.remove(d_them)
    
    #choix des attaquants a_us (deux) 
    #choix a_them (deux)
    if mode == "bot" :
        a_us = random.sample(l_us,k=2)                    #!!! Algo a dev
        a_them = random.sample(l_them,k=2)                #!!! Algo a dev
    elif mode == "training" :
        print("*****")
        print("¤¤¤ Il nous reste :",', '.join([bt_us[x] for x in l_us]))
        print("xxx Il leur reste :",', '.join([bt_them[x] for x in l_them]))
        print("*****")
        out = 'nan none'
        while not(len(out.split()) == 2 and out.split()[0] in [bt_us[x] for x in l_us] and out.split()[1] in [bt_us[x] for x in l_us]) :
            out = input("Nos attaquants contre leur "+ bt_them[d_them]+" ? (séparés par un espace) ")
        a_us = [r_bt_us[x] for x in out.split()]
        a_them = random.sample(l_them,k=2)
        print("Leurs attaquants : "+bt_them[a_them[0]]+" et "+bt_them[a_them[1]]+' contre notre '+bt_us[d_us])
    elif mode == "manuel" :
        print("*****")
        print("¤¤¤ Il nous reste :",', '.join([bt_us[x] for x in l_us]))
        print("xxx Il leur reste :",', '.join([bt_them[x] for x in l_them]))
        print("*****")
        out = 'nan none'
        while not(len(out.split()) == 2 and out.split()[0] in [bt_us[x] for x in l_us] and out.split()[1] in [bt_us[x] for x in l_us]) :
            out = input("Nos attaquants contre leur "+ bt_them[d_them]+" ? (séparés par un espace)  ")
        a_us = [r_bt_us[x] for x in out.split()]
        out = 'nan none'
        while not(len(out.split()) == 2 and out.split()[0] in [bt_them[x] for x in l_them] and out.split()[1] in [bt_them[x] for x in l_them]) :
            out = input("Leurs attaquants contre notre "+ bt_us[d_us]+" ? (séparés par un espace) (choix par l'adversaire) ")
        a_them = [r_bt_them[x] for x in out.split()]
    
    #choix de l'attaquant pick_us parmis les 2 a_them proposés  
    #choix de l'attaquant pick_them parmis les 2 a_us proposés  
    if mode == "bot" :
        pick_us = random.choice(a_them)                   #!!! Algo a dev
        pick_them = random.choice(a_us)                   #!!! Algo a dev
    elif mode == "training" :
        print("*****")
        out = 'nan'
        while out not in [bt_them[x] for x in a_them] :
            out = input("Attaquant retenu pour eux ? ")
        pick_us = r_bt_them[out]
        pick_them = random.choice(a_us)
        print("Ils ont retenu notre attaquant : "+bt_us[pick_them])
    elif mode == "manuel" :
        print("*****")
        out = 'nan'
        while out not in [bt_them[x] for x in a_them] :
            out = input("Attaquant retenu par nous parmis leurs "+bt_them[a_them[0]]+" et "+bt_them[a_them[1]]+" contre notre "+bt_us[d_us]+" ? ")
        pick_us = r_bt_them[out]
        out = 'nan'
        while out not in [bt_us[x] for x in a_us] :
            out = input("Attaquant retenu par eux parmis nos "+bt_us[a_us[0]]+" et "+bt_us[a_us[1]]+" contre leur "+bt_them[d_them]+" ? (choix par l'adversaire) ")
        pick_them = r_bt_us[out]
    
    l_us.remove(pick_them) #On retire les attaquants choisis des disponibles de chaque équipe
    l_them.remove(pick_us)
    
    match = [[d_us, pick_us],[pick_them, d_them]]
    if mode == 'training' or 'manuel' :
        print("#---------------------------------------------------#")
        print("Résumé des matchs :")
        print("Notre "+bt_us[d_us]+" VS leur "+bt_them[pick_us])
        print("Notre "+bt_us[pick_them]+" VS leur "+bt_them[d_them])
    ###les matchs sont une liste(4) [1/scenario] de liste (2) [1/partie] de listes (2) [1/bt]
    ## Chaque liste(2) de partie est donnée dans l'ordre : [notre bt, leur bt]
    # Chaque tour de scénario renvoie deux parties "match" a concaténer a la liste des "matchs"
    
    return (l_us, l_them, match)

def turn34(l_us, l_them, matchs, estimate, mode) :
    
    #choix des défenseurs d3_us 
    #et d3_them
    
    if mode == "bot" :
        d3_us = quick_opt_blind_us_2(l_us, l_them, matchs, estimate)  #Ici, on utilise le premier algo pour notre choix
        d3_them = quick_opt_blind_opponent_2(l_us, l_them, matchs, estimate) #Et là, pour leur choix
    elif mode == "training" :
        print("¤¤¤ Il nous reste :",', '.join([bt_us[x] for x in l_us]))
        print("xxx Il leur reste :",', '.join([bt_them[x] for x in l_them]))
        out = 'nan'
        while out not in [bt_us[x] for x in l_us] :
            out = input("Notre défenseur ? ")
        d3_us = r_bt_us[out]
        d3_them = quick_opt_blind_opponent_2(l_us, l_them, matchs, estimate)
        print("Leur défenseur : "+bt_them[d3_them])
    elif mode == "manuel" :
        print("¤¤¤ Il nous reste :",', '.join([bt_us[x] for x in l_us]))
        print("xxx Il leur reste :",', '.join([bt_them[x] for x in l_them]))
        display(estimate, 3, l_us, l_them)
        display(estimate, 4, l_us, l_them)
        out = 'nan'
        while out not in [bt_us[x] for x in l_us] :
            out = input("Notre défenseur pour le scénario 3 ? ")
        d3_us = r_bt_us[out]
        out = 'nan'
        while out not in [bt_them[x] for x in l_them] :
            out = input("Leur défenseur pour le scénario 3 ? (choix par l'adversaire) ")
        d3_them = r_bt_them[out]

    #d3_us = random.choice(l_us)                   #Alternative en random
    #d3_them = random.choice(l_them)
    
    l_us.remove(d3_us) #On retire les defenseurs proposés des BT disponibles de chaque équipe
    l_them.remove(d3_them)

    #choix des attaquants a_us (deux) 
    #choix a_them (deux)
    if mode == "bot" :
        a_us = random.sample(l_us,k=2)                    #!!! Algo a dev
        a_them = random.sample(l_them,k=2)                #!!! Algo a dev
    elif mode == "training" :
        print("*****")
        print("¤¤¤ Il nous reste :",', '.join([bt_us[x] for x in l_us]))
        print("xxx Il leur reste :",', '.join([bt_them[x] for x in l_them]))
        print("*****")
        out = 'nan none'
        while not(len(out.split()) == 2 and out.split()[0] in [bt_us[x] for x in l_us] and out.split()[1] in [bt_us[x] for x in l_us]) :
            out = input("Nos attaquants contre leur "+ bt_them[d3_them]+" ? (séparés par un espace) ")
        a_us = [r_bt_us[x] for x in out.split()]
        a_them = random.sample(l_them,k=2)
        print("Leurs attaquants : "+bt_them[a_them[0]]+" et "+bt_them[a_them[1]]+' contre notre '+bt_us[d3_us])
    elif mode == "manuel" :
        print("*****")
        print("¤¤¤ Il nous reste :",', '.join([bt_us[x] for x in l_us]))
        print("xxx Il leur reste :",', '.join([bt_them[x] for x in l_them]))
        print("*****")
        out = 'nan none'
        while not(len(out.split()) == 2 and out.split()[0] in [bt_us[x] for x in l_us] and out.split()[1] in [bt_us[x] for x in l_us]) :
            out = input("Nos attaquants contre leur "+ bt_them[d3_them]+" ? (séparés par un espace) ")
        a_us = [r_bt_us[x] for x in out.split()]
        out = 'nan none'
        while not(len(out.split()) == 2 and out.split()[0] in [bt_them[x] for x in l_them] and out.split()[1] in [bt_them[x] for x in l_them]) :
            out = input("Leurs attaquants contre notre "+ bt_us[d3_us]+" ? (séparés par un espace) (choix par l'adversaire) ")
        a_them = [r_bt_them[x] for x in out.split()]    
    
    l_us.remove(a_us[0]) #On retire cette fois-ci les 2 bt attaquants des disponibles de chaque équipe
    l_us.remove(a_us[1])
    l_them.remove(a_them[0])
    l_them.remove(a_them[1])
    
    d4_us = l_us[0] #Le dernier Bt restant de chaque team devient le défenseur du dernièr scénario
    d4_them = l_them[0] 
    if mode == 'training' or  mode == 'manuel':
        print("*****")
        print(bt_us[d4_us]+" est donc automatiquement le défenseur du scénario 4 pour nous")
        print(bt_them[d4_them]+" est donc automatiquement le défenseur du scénario 4 pour eux")
        print("*****")
    
    #choix parmis les attaquants proposés de celui qui sera sur le 3 et sur le 4eme sénario : pick_us 3 ou 4
    #pour l'adversaire pick_them 3 ou 4
    if mode == "bot" :
        [pick3_us, pick4_us] = random.sample(a_them, 2)     #!!! Algo a dev
        [pick3_them, pick4_them] = random.sample(a_us, 2)   #!!! Algo a dev
    elif mode == "training" :
        out = 'nan'
        while out not in [bt_them[x] for x in a_them] :
            out = input("Parmi leurs attaquants ("+bt_them[a_them[0]]+" et "+bt_them[a_them[1]]+"), lequel pour affronter notre 3eme défenseur ? ")
        pick3_us = r_bt_them[out]
        a_them.remove(pick3_us)
        pick4_us = int(a_them[0])
        print(bt_them[pick4_us]+' affrontera donc notre 4eme défenseur')
        [pick3_them, pick4_them] = random.sample(a_us, 2)   #!!! Algo a dev
    elif mode == "manuel" :
        out = 'nan'
        while out not in [bt_them[x] for x in a_them] :
            out = input("Parmi leurs attaquants ("+bt_them[a_them[0]]+" et "+bt_them[a_them[1]]+"), lequel pour affronter notre 3eme défenseur ("+bt_us[d3_us]+") ? ")
        pick3_us = r_bt_them[out]
        a_them.remove(pick3_us)
        pick4_us = int(a_them[0])
        print(bt_them[pick4_us]+' affrontera donc notre 4eme défenseur')
        out = 'nan'
        while out not in [bt_us[x] for x in a_us] :
            out = input("Parmi nos attaquants ("+bt_us[a_us[0]]+" et "+bt_us[a_us[1]]+"), lequel pour affronter leur 3eme défenseur ("+bt_them[d3_them]+") ? (choix par l'adversaire) ")
        pick3_them = r_bt_us[out]
        a_us.remove(pick3_them)
        pick4_them = int(a_us[0])
        print(bt_us[pick4_them]+' affrontera donc leur 4eme défenseur')

    #Reconstitution des matchs pour les scénario 3 et 4
    match3 = [[d3_us, pick3_us],[pick3_them, d3_them]]
    match4 = [[d4_us, pick4_us],[pick4_them, d4_them]]
    if mode == 'training' or  mode == 'manuel' :
        print("#---------------------------------------------------#")
        print("Résumé des matchs :")
        print("Troisième scnérario :")
        print(bt_us[d3_us]+" VS "+bt_them[pick3_us])
        print(bt_us[pick3_them]+" VS "+bt_them[d3_them])
        print("Et quatrième scnérario :")
        print(bt_us[d4_us]+" VS "+bt_them[pick4_us])
        print(bt_us[pick4_them]+" VS "+bt_them[d4_them])   
    
    return match3, match4

def pairing(estimate, mode) :

    l_us = list(range(0,8)) #bt restants pour nous 
    l_them = list(range(0,8)) #bt restants pour eux
    matchs = []  #Initialisation du set des matchs à jouer

    if mode == 'training' or mode == 'manuel':
        print("#---------------------------------------------------#")
        print("#-----------------Premier scenario------------------#")
        print("#---------------------------------------------------#")
    tour = 1
    l_us, l_them, pairing = turn12(l_us, l_them, matchs, estimate, mode, tour) #Tour 1 
    matchs.append(pairing) #On concatene les resultats

    if mode == 'training' or mode == 'manuel':
        print("#---------------------------------------------------#")
        print("#-----------------Deuxième scenario-----------------#")
        print("#---------------------------------------------------#")
    tour = 2
    l_us, l_them, pairing = turn12(l_us, l_them, matchs, estimate, mode, tour) #Tour 2
    matchs.append(pairing) #On concatene les resultats
    
    if mode == 'training' or mode == 'manuel':
        print("#---------------------------------------------------#")
        print("#--------Troisième et quatrième scenarii------------#")
        print("#---------------------------------------------------#")
    
    match3, match4 = turn34(l_us, l_them, matchs, estimate, mode) #Tour 3 + 4
    matchs.append(match3)
    matchs.append(match4)  
    
    if mode == 'training' or mode == 'manuel':
        print("#---------------------------------------------------#")
        print("#----------Résumé de tout les scénarii--------------#")
        print("#---------------------------------------------------#")
        for i,s in enumerate(matchs):
            print("** Scénario "+str(i+1)+" **")
            for g in s :
                print("Notre "+bt_us[g[0]]+" VS leur "+bt_them[g[1]]+" (estimé =) "+str(estimate[i][int(g[0]),int(g[1])]))
        print("#---------------------------------------------------#")
    
    return calculate(matchs, estimate) #Calcule du score d'équipe
    
### Cette partie est là pour des tests non-interactifs

# res = []  #Liste de tout les scores d'équipes

# for t in range(0,100) :  #Nombre d'essai de pairing
#     res.append(pairing(estimate,"bot"))  #Calcule du score d'équipe
    
# r = np.asarray(res)
# print(r.mean(), r.max(), r.min(), r.std())
    
# plt.hist(res,bins=120)  #Distribution des scores d'équipes
# plt.show()

# main 
mode ='none'
modes = ['bot', 'training', 'manuel']
while mode not in modes :
    mode = str(input("Mode : "))
print("~~~~~~~~~~~~~~~~~~~~")
resultat = pairing(estimate, mode)
print("Le résultat total estimé pour l'équipe est de : "+str(resultat))
