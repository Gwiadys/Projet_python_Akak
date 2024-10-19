from itertools import groupby


# Fonction pour créer un nouveau plateau de jeu avec 'n' cases
def newBoard(n):
    # Je crée une liste de 'n' éléments avec des 0 (0 représente une case vide)
    return [0 for _ in range(n)]



# Fonction pour convertir un nombre en symbole pour l'affichage
def trans(number):
    # Si la case est vide (0), on affiche un point
    if number == 0:
        return '.'
    # Si c'est le joueur 1, on affiche 'x', sinon c'est le joueur 2, on affiche 'o'
    else:
        return 'x' if number == 1 else 'o'


# Fonction pour afficher le plateau de jeu et les numéros de cases
def display(board, n):
    # On convertit chaque case du plateau en symbole avec la fonction trans
    output = ' '.join(list(map(trans, board)))
    print(output)  # Affiche la ligne de symboles
    # Ensuite, j'affiche les numéros de case pour que les joueurs voient où jouer
    print(' '.join([str(i) for i in range(1, n + 1)]))


        
def possible(board, n, player, removed, i):
    # Vérifie si l'indice est dans les limites du plateau
    if not (0 <= i < n):
        return False
    
    # Vérifie si la case est libre (contient un 0)
    if board[i] != 0:
        return False
    
    # Vérifie si la case n'est pas dans la liste des cases retirées pour le joueur
    if i in removed[player - 1]:
        return False
    
    # Si toutes les conditions sont remplies, on retourne True
    return True




def player_input():
    # Utilisation d'une boucle for infinie simulée pour rendre le code plus cool
    for _ in iter(int, 1):  # Cette boucle ne s'arrête pas tant qu'une entrée valide n'est pas donnée
        try:
            # Demande à l'utilisateur de saisir un numéro de case
            i = int(input("Entrez le numéro d'une case : "))
            if i < 1:
                raise ValueError  # Lève une exception si le nombre est en dessous de 1
        except ValueError:
            print("Veuillez entrer un numéro valide (supérieur à 0).")
        else:
            return i - 1  # Retourne l'index 0-basé



def group_by_list(board):
    keys_list = []  # Liste pour stocker les valeurs rencontrées sur le plateau
    groups_list = []  # Liste pour stocker les indices de cases associées à chaque valeur
    index_tracker = 0  # Variable pour garder une trace de la position actuelle

    # Parcourir chaque groupe d'éléments similaires dans le plateau
    for value, group in groupby(board):
        current_group_indices = []  # Liste temporaire pour stocker les indices du groupe en cours

        # Remplir la liste temporaire avec les positions des éléments du groupe
        for _ in group:
            current_group_indices.append(index_tracker)
            index_tracker += 1  # Incrémenter l'index à chaque itération

        # Ajouter la valeur actuelle dans keys_list
        keys_list.append(value)
        # Ajouter la liste des indices associés dans groups_list
        groups_list.append(current_group_indices)

    # Retourner les deux listes créées
    return keys_list, groups_list



# Fonction pour vérifier si un pion adverse peut être retiré
def remove_pawn(part, player):
    # On vérifie qui est l'adversaire
    adversary = 2 if player == 1 else 1
    # Si la partie est vide ou ne commence pas par l'adversaire, pas de capture
    if not part or part[0] != adversary:
        return False
    try:
        # On cherche le premier pion du joueur
        player_index = part.index(player)
    except ValueError:
        # Si le joueur n'est pas dans la partie, il faut que tous les pions soient de l'adversaire
        return 0 not in part
    else:
        # Si avant le pion du joueur il n'y a pas de case vide (0), on peut capturer
        return 0 not in part[:player_index]


# Fonction pour analyser les pions adjacents autour de la case jouée
def check_pawn(keys_list, player, current_index, groups_list, removed, direction):
    # Identifier l'adversaire selon le joueur
    opponent = 2 if player == 1 else 1
    
    # Vérifier les pions à droite de la case jouée
    if direction != 'left':
        if current_index + 1 < len(keys_list):  # Vérifie qu'il y a bien des éléments à droite
            right_segment = keys_list[current_index + 1:]  # Récupère la partie droite
            if remove_pawn(right_segment, player):  # Si capture possible à droite
                removed[opponent - 1].extend(groups_list[current_index + 1])  # Marque les pions capturés

    # Vérifier les pions à gauche de la case jouée
    if direction != 'right':
        if current_index > 0:  # Vérifie qu'il y a bien des éléments à gauche
            left_segment = keys_list[:current_index][::-1]  # Récupère la partie gauche et l'inverse
            if remove_pawn(left_segment, player):  # Si capture possible à gauche
                removed[opponent - 1].extend(groups_list[current_index - 1])  # Marque les pions capturés


# Fonction pour sélectionner une case valide à jouer
def select(board, n, player, removed):
    print(f"C'est au tour du joueur {player}.")  # Informer le joueur que c'est son tour
    while True:
        i = player_input()  # Demande au joueur de choisir une case
        # Vérifie si la case choisie est valide
        if possible(board, n, player, removed, i):
            return i  # Si valide, retourne l'index de la case choisie
        else:
            print("La case est invalide ou déjà occupée. Veuillez choisir une autre case.")


# Fonction pour placer un pion et gérer les captures
def put(board, player, removed, i):
    # Identifier l'adversaire
    opponent = 2 if player == 1 else 1
    removed[opponent - 1].clear()  # Réinitialiser les cases capturées pour ce tour
    board[i] = player  # Placer le pion du joueur sur la case choisie

    keys_list, groups_list = group_by_list(board)  # Regrouper les valeurs et les indices

    # Parcourir les groupes pour vérifier les captures potentielles
    for k, group in enumerate(groups_list):
        if i in (group[0], group[-1]):  # Vérifier si l'index se trouve en début ou fin de groupe
            direction = 'both' if i == group[0] == group[-1] else ('left' if i == group[0] else 'right')
            check_pawn(keys_list, player, k, groups_list, removed, direction)
            break  # Sortir après avoir vérifié le groupe correspondant

    # Enlever les pions capturés de l'adversaire
    for i in removed[opponent - 1]:
        board[i] = 0  # Remettre à zéro les cases capturées


# Fonction pour vérifier si le jeu doit continuer
def again(board, n, player, removed, turn_count):
    # Arrêter le jeu après 10 tours
    if turn_count >= 17:
        return False

    # Vérifier s'il reste des cases vides
    if 0 in board:
        # Si des pions ont été retirés pour ce joueur
        if removed[player - 1]:
            # Trouver les cases vides non bloquées
            available_spaces = {i for i in range(n) if board[i] == 0}
            # Le jeu continue si des cases libres ne sont pas bloquées
            return bool(available_spaces - set(removed[player - 1]))
        # Si aucune case n'est bloquée, le jeu continue
        return True
    
    # Si aucune case n'est vide, le jeu s'arrête
    return False



# Fonction pour afficher le gagnant ou déclarer un match nul
def win(board, n):
    display(board, n)  # Affiche le plateau final

    # Calculer les scores des deux joueurs
    score_player1 = board.count(1)
    score_player2 = board.count(2)

    # Afficher le résultat en fonction des scores
    if score_player1 > score_player2:
        print("Vainqueur : Joueur 1")
    elif score_player1 < score_player2:
        print("Vainqueur : Joueur 2")
    else:
        print("C'est un match nul !")



# Fonction principale pour démarrer le jeu
def start_game(n):
    # Initialisation du plateau et des variables de jeu
    board = newBoard(n)
    removed = [[], []]  # Liste des cases capturées pour chaque joueur
    player = 1  # Joueur 1 commence
    turn_count = 0  # Compteur de tours

    # Boucle principale du jeu
    while again(board, n, player, removed, turn_count):
        display(board, n)  # Afficher l'état actuel du plateau

        # Le joueur sélectionne une case à jouer
        i = select(board, n, player, removed)

        # Placer le pion sur la case choisie et gérer les captures
        put(board, player, removed, i)

        # Passer au joueur suivant
        player = 3 - player  # Alternance entre 1 et 2 (plus court que "2 if player == 1 else 1")

        # Incrémenter le compteur de tours
        turn_count += 1

    # Déterminer le gagnant une fois la partie terminée
    win(board, n)


# Code qui s'exécute quand le programme est lancé
if __name__ == '__main__':
    # Validation pour s'assurer que l'utilisateur entre un nombre valide pour la taille du plateau
    while True:
        try:
            board_size = int(input("Veuillez insérer un nombre de cases pour le plateau (minimum 9): "))
            if board_size < 9:
                print("Le nombre de cases doit être au moins de 9.")
            else:
                break
        except ValueError:
            print("Veuillez entrer un nombre valide.")

    start_game(board_size)

