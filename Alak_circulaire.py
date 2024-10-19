# Fonction pour créer un nouveau plateau de jeu avec 'n' cases
def newBoard(n):
    return [0 for _ in range(n)]  # Plateau de 'n' cases vides

# Fonction pour convertir un nombre en symbole pour l'affichage
def trans(number):
    return '.' if number == 0 else ('x' if number == 1 else 'o')

# Fonction pour afficher le plateau de jeu et les numéros de cases
def display(board, n):
    output = ' '.join(list(map(trans, board)))
    print(output)  # Affiche les symboles du plateau
    print(' '.join([str(i) for i in range(1, n + 1)]))  # Affiche les numéros de case

# Fonction pour vérifier si une case est valide
def possible(board, n, player, removed, i):
    return 0 <= i < n and board[i] == 0 and i not in removed[player - 1]

# Fonction pour demander au joueur de choisir une case
def player_input():
    while True:
        try:
            i = int(input("Entrez le numéro d'une case : "))
            if i < 1:
                raise ValueError
        except ValueError:
            print("Veuillez entrer un numéro valide (supérieur à 0).")
        else:
            return i - 1

# Fonction pour regrouper les éléments similaires sur le plateau
from itertools import groupby

def group_by_list(board):
    keys_list_list = []
    groups_list = []
    index_tracker = 0

    for value, group in groupby(board):
        current_group_indices = [index_tracker + i for i in range(len(list(group)))]
        index_tracker += len(current_group_indices)
        keys_list_list.append(value)
        groups_list.append(current_group_indices)

    return keys_list_list, groups_list

# Fonction pour vérifier si un pion adverse peut être retiré
def remove_pawn(part, player):
    opponent = 2 if player == 1 else 1
    if not part or part[0] != opponent:
        return False
    try:
        player_index = part.index(player)
    except ValueError:
        return 0 not in part
    else:
        return 0 not in part[:player_index]

# Fonction pour vérifier les pions autour de la case jouée


def check_pawn(keys_list, player, current_index, groups, removed, direction):
    # On détermine qui est l'adversaire
    opponent = 2 if player == 1 else 1
    
    # On récupère les pions à gauche et à droite du pion joué
    left = keys_list[:current_index]  # Partie gauche
    right = keys_list[current_index + 1:]  # Partie droite
    rang = right + left  # On combine les deux côtés pour les vérifier ensemble

    # Si on regarde à droite, on vérifie s'il y a des pions à capturer
    if direction != 'left':
        result = remove_pawn(rang, player)  # Appelle la fonction pour voir s'il y a des captures
        while result > 0:  # Tant qu'il y a des pions capturés
            if current_index < len(groups) - 1:
                # Ajoute les pions capturés au joueur adverse
                removed[opponent - 1].extend(groups[current_index + 1])
            else:
                # Si on arrive à la fin de la liste
                removed[opponent - 1].extend(groups[0])  # On revient au début
            current_index += 1  # On avance d'une case à droite
            result -= 1  # On décrémente le résultat (simple logique pour débutants)

    # Si on regarde à gauche, on fait pareil
    if direction != 'right':
        rang.reverse()  # On inverse la liste pour regarder à gauche
        result = remove_pawn(rang, player)  # Encore une vérification pour capturer
        while result > 0:  # On capture les pions tant que c'est possible
            if current_index > 0:
                removed[opponent - 1].extend(groups[current_index - 1])  # On capture les pions à gauche
            else:
                removed[opponent - 1].extend(groups[len(groups) - 1])  # On retourne au dernier groupe si nécessaire
            current_index -= 1  # On avance d'une case à gauche
            result -= 1  # Même logique pour avancer




# Fonction pour sélectionner une case valide à jouer
def select(board, n, player, removed):
    print(f"C'est au tour du joueur {player}.")
    while True:
        i = player_input()
        if possible(board, n, player, removed, i):
            return i
        else:
            print("La case est invalide ou déjà occupée. Veuillez choisir une autre case.")



# Fonction pour placer un pion et gérer les captures
def put(board, player, removed, i):
    opponent = 2 if player == 1 else 1
    removed[opponent - 1].clear()
    board[i] = player

    keys_list_list, groups_list = group_by_list(board)

    for k, group in enumerate(groups_list):
        if i in group:
            direction = 'both' if i == group[0] == group[-1] else ('left' if i == group[0] else 'right')
            check_pawn(keys_list_list, player, k, groups_list, removed, direction)
            break

    for idx in removed[opponent - 1]:
        board[idx] = 0

# Fonction pour vérifier si le jeu doit continuer
def again(board, n, player, removed, turn_count):
    if turn_count >= 17:
        return False
    if 0 in board:
        if removed[player - 1]:
            available_spaces = {i for i in range(n) if board[i] == 0}
            return bool(available_spaces - set(removed[player - 1]))
        return True
    return False

# Fonction pour afficher le gagnant ou déclarer un match nul
def win(board, n):
    display(board, n)
    score_player1 = board.count(1)
    score_player2 = board.count(2)

    if score_player1 > score_player2:
        print("Vainqueur : Joueur 1")
    elif score_player1 < score_player2:
        print("Vainqueur : Joueur 2")
    else:
        print("C'est un match nul !")

# Fonction principale pour démarrer le jeu
def start_game(n):
    board = newBoard(n)
    removed = [[], []]
    player = 1
    turn_count = 0

    while again(board, n, player, removed, turn_count):
        display(board, n)
        i = select(board, n, player, removed)
        put(board, player, removed, i)
        player = 3 - player
        turn_count += 1

    win(board, n)

# Lancement du jeu
if __name__ == '__main__':
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
