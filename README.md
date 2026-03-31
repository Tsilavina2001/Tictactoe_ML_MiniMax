# Tictactoe_ML_MiniMax
Examen S1 M1 Machine Learning

 #               INSTITUT SURERIEUR POLYTHECNIQUE DE MADAGASCAR
#                           MACHINE LEARNING
www.ispm-edu.com

# Nom du groupe:    Projet Matotra Be
# Les memmbres du groupe: 
-RATOVOMANALINA Sitraka Mamy n°19 <br>
-ANDRIANARIARIMANANA Manoasoa n°21 <br>
-RAMALARISON Tsiory Nomena n°22 <br>
-RANDRIAMAHEFA Tsilavina Mia n°23 <br>                 
-RANDRIANTSEHENO Mitandro Ny Aina Arivelo n°24<br>
# Description du projet

# Structure du repository
    -Dans un premier temps on trouve le fichier "ressources" ou on trouve le "datase.csv", qui est d'ailleurs la reponses a l'etapes 0.
    -Le fichier "static" ou on trouve les scripts "script.js" de l'interface jouable, et le "style.css" qui correspond au style de front-end
    -Fichier "templates" qui comporte le bases "index.html" du front-end.
    -"app.py" contient le serveur flask et le fonction utilisable de minimax.
    -"generator.py" se trouve le generation du dataset.
    -"requirements.txt" dependances du projet (pip install -r requirements.txt)
  

# Résultats Machine Learning

# Réponse aux questions
    Q1- ANALYSE DES COEFICIENTS
    Pour les deux modèles (x_wins et is_draw), les coefficients les plus élevés en valeur absolue correspondent: à la case centrale occupée par X,aux coins occupés par X, et enfin aux cases où O bloque X (coefficients négatifs)

    La case centrale est particulièrement influente, car elle permet : plus de combinaisons gagnantes et un contrôle du plateau
    
    Ceci est cohérent avec la stratégie humaine :les joueurs expérimentés jouent souvent au centre ou dans les coins pour maximiser leurs chances de victoire.

    Q2- DESEQUILIBRE DES CLASSES
    Le dataset n'est généralement pas équilibré : (x_wins = 1) est souvent moins fréquent que (x_wins = 0). (is_draw = 1) est souvent encore plus rare. Donc le dataset est déséquilibré.

    La métrique priviligié est le F1-score (plutôt que Accuracy) car accuracy peut être trompeuse si une classe domine, F1-score prend en compte précision +rappel, meilleure mesure pour classes déséquilibrées

    Q3- COMPARAISON DES DEUX MODELES
    Le classificateur (x_wins) obtient généralement un meilleur score que (is_draw).

    ils se trompent generalemant: dans les positions presque gagnantes, ou dans les situations bloquées, quand plusieurs coups sont possibles

    Q4-MODE HYBRIDE
    En mode hybride (Minimax + ML), on observe : Un jeu plus stable, moins d'erreurs stratégiques,meilleure anticipation des pièges.
    Oui, le joueur hybride evite mieux les pièges.
    IA-ML pur peut-être parfois imprécise que l'hybride qui est plus proche d’un joueur optimal

#Video presentation :Demonstration : https://drive.google.com/file/d/18-8AkYqJVMnLWHnVyv9ZBb-XsKIc-dyH/view?usp=drivesdk
                     Presentation : https://drive.google.com/file/d/1YtkOoGwzE_oOoYSwDRQzc9ct-pFIwwk-/view?usp=drivesdk
