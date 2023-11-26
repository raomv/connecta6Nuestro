from re import L
import re
from defines import *
import time
import numpy as np 



# Point (x, y) if in the valid position of the board.
def isValidPos(x,y):
    return x>0 and x<Defines.GRID_NUM-1 and y>0 and y<Defines.GRID_NUM-1
    
def init_board(board):
    for i in range(21):
        board[i][0] = board[0][i] = board[i][Defines.GRID_NUM - 1] = board[Defines.GRID_NUM - 1][i] = Defines.BORDER
    for i in range(1, Defines.GRID_NUM - 1):
        for j in range(1, Defines.GRID_NUM - 1):
            board[i][j] = Defines.NOSTONE
            
def make_move(board, move, color):
    board[move.positions[0].x][move.positions[0].y] = color
    board[move.positions[1].x][move.positions[1].y] = color
    if color == Defines.BLACK:
        Defines.LVMOVE_N = [move.positions[0].x,move.positions[0].y, move.positions[1].x,move.positions[1].y]
    else: 
        Defines.LVMOVE_B = [move.positions[0].x,move.positions[0].y, move.positions[1].x,move.positions[1].y]
            
    Defines.ContadorTurnos += 1


def unmake_move(board, move):
    board[move.positions[0].x][move.positions[0].y] = Defines.NOSTONE
    board[move.positions[1].x][move.positions[1].y] = Defines.NOSTONE


def is_win_by_premove(board, preMove):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    board = np.array(board)  
    for direction in directions:
        for i in range(2):
            count = 0
            x1, y1 = preMove[i * 2], preMove[i * 2 + 1]
            movStone = board[x1, y1]

            if (movStone == Defines.BORDER or movStone == Defines.NOSTONE):
                return False;

            x = x1
            y = y1
            while 0 <= x < board.shape[0] and 0 <= y < board.shape[1] and board[x, y] == movStone:
                x += direction[0]
                y += direction[1]
                count += 1
            x = x1 - direction[0]
            y = y1 - direction[1]
            while 0 <= x < board.shape[0] and 0 <= y < board.shape[1] and board[x, y] == movStone:
                x -= direction[0]
                y -= direction[1]
                count += 1
            if count >= 6:
                return True
    return False


def get_msg(max_len):
    buf = input().strip()
    return buf[:max_len]


def log_to_file(msg):
    g_log_file_name = Defines.LOG_FILE
    try:
        with open(g_log_file_name, "a") as file:
            tm = time.time()
            ptr = time.ctime(tm)
            ptr = ptr[:-1]
            file.write(f"[{ptr}] - {msg}\n")
        return 0
    except Exception as e:
        print(f"Error: Can't open log file - {g_log_file_name}")
        return -1


def move2msg(move):
    if move.positions[0].x == move.positions[1].x and move.positions[0].y == move.positions[1].y:
        msg = f"{chr(ord('S') - move.positions[0].x + 1)}{chr(move.positions[0].y + ord('A') - 1)}"
        return msg
    else:
        msg = f"{chr(move.positions[0].y + ord('A') - 1)}{chr(ord('S') - move.positions[0].x + 1)}" \
              f"{chr(move.positions[1].y + ord('A') - 1)}{chr(ord('S') - move.positions[1].x + 1)}"
        return msg


def msg2move(msg):
    move = StoneMove()
    if len(msg) == 2:
        move.positions[0].x = move.positions[1].x = ord('S') - ord(msg[1]) + 1
        move.positions[0].y = move.positions[1].y = ord(msg[0]) - ord('A') + 1
        move.score = 0
        return move
    else:
        move.positions[0].x = ord('S') - ord(msg[1]) + 1
        move.positions[0].y = ord(msg[0]) - ord('A') + 1
        move.positions[1].x = ord('S') - ord(msg[3]) + 1
        move.positions[1].y = ord(msg[2]) - ord('A') + 1
        move.score = 0
        return move
    

def print_board(board, preMove=None):
    print("   " + "".join([chr(i + ord('A') - 1)+" " for i in range(1, Defines.GRID_NUM - 1)]))
    for i in range(1, Defines.GRID_NUM - 1):
        print(f"{chr(ord('A') - 1 + i)}", end=" ")
        for j in range(1, Defines.GRID_NUM - 1):
            x = Defines.GRID_NUM - 1 - j
            y = i
            stone = board[x][y]
            if stone == Defines.NOSTONE:
                print(" -", end="")
            elif stone == Defines.BLACK:
                print(" O", end="")
            elif stone == Defines.WHITE:
                print(" *", end="")
        print(" ", end="")        
        print(f"{chr(ord('A') - 1 + i)}", end="\n")
    print("   " + "".join([chr(i + ord('A') - 1)+" " for i in range(1, Defines.GRID_NUM - 1)]))
    

def print_score(move_list, n):
    board = [[0] * Defines.GRID_NUM for _ in range(Defines.GRID_NUM)]
    for move in move_list:
        board[move.x][move.y] = move.score

    print("  " + "".join([f"{i:4}" for i in range(1, Defines.GRID_NUM - 1)]))
    for i in range(1, Defines.GRID_NUM - 1):
        print(f"{i:2}", end="")
        for j in range(1, Defines.GRID_NUM - 1):
            score = board[i][j]
            if score == 0:
                print("   -", end="")
            else:
                print(f"{score:4}", end="")
        print()

#Manera alternativa de ordenar las casillas que vamos a evaluar. Se deja por si se quisiera cambiar y seguir probando.
def get_valid_locations_2(matriz, tamano, posicion):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    posiciones_disponibles=[]
    #for direction in directions:
    for multi in range(2):
        #for multi in range(2):
        for direction in directions:
            x1, y1 = posicion[0], posicion[1]
            movStone = matriz[x1, y1]
            x, y = x1+direction[0]*(multi+1), y1+direction[1]*(multi+1)
            if 0 <= x < matriz.shape[0] and 0 <= y < matriz.shape[1] and matriz[x, y] == Defines.NOSTONE:
                posiciones_disponibles.append((x, y)) 
                
            x, y = x1-direction[0]*(multi+1), y1-direction[1]*(multi+1)
            if 0 <= x < matriz.shape[0] and 0 <= y < matriz.shape[1] and matriz[x, y] == Defines.NOSTONE:
                posiciones_disponibles.append((x, y))     

    return posiciones_disponibles

def get_valid_locations(matriz, tamano, posicion):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    posiciones_disponibles = []
    for direction in directions:
        for multi in [1,-1]:
            x1, y1 = posicion[0], posicion[1]
            movStone = matriz[x1, y1]

            x, y = x1 + direction[0] * (multi * 1), y1 + direction[1] * (multi * 1)
            if 0 <= x < matriz.shape[0] and 0 <= y < matriz.shape[1] and matriz[x, y] == Defines.NOSTONE:
                posiciones_disponibles.append((x, y))

            x, y = x1 + direction[0] * (2*multi), y1 + direction[1] * (multi * 2)
            if 0 <= x < matriz.shape[0] and 0 <= y < matriz.shape[1] and matriz[x, y] == Defines.NOSTONE:
                posiciones_disponibles.append((x, y))

    return posiciones_disponibles

def posiciones_disponibles_sin_repetidos(matriz, tamano, posicion1, posicion2):

    # Obtiene las posiciones disponibles con duplicados
    disponibles_con_duplicados = posiciones_disponibles_con_duplicados(matriz, tamano, posicion1, posicion2)
    
    # Elimina duplicados manteniendo el orden
    disponibles_sin_repetidos = list(dict.fromkeys(disponibles_con_duplicados))
      
    return disponibles_sin_repetidos

def posiciones_disponibles_con_duplicados(matriz, tamano, posicion1, posicion2):
    # Llama a la funcion posiciones_disponibles con la primera posici�n central
    disponibles1 = get_valid_locations(matriz, tamano, posicion1)
    
    # Llama a la funcion posiciones_disponibles con la segunda posici�n central
    disponibles2 = get_valid_locations(matriz, tamano, posicion2)
    
    # Combina las dos listas sin eliminar duplicados
    #disponibles_combinados=[item for pair in zip(disponibles1, disponibles2) for item in pair] # Intercalados
    disponibles_combinados = disponibles1 + disponibles2 # Uno detras del otro 
    
    return disponibles_combinados


# Metodo de comprobacion para las casillas disponibles a analizar
def print_board_2(board, casillas):
    print("   " + "".join([chr(i + ord('A') - 1)+" " for i in range(1, Defines.GRID_NUM - 1)]))
    for i in range(1, Defines.GRID_NUM - 1):
        print(f"{chr(ord('A') - 1 + i)}", end=" ")
        for j in range(1, Defines.GRID_NUM - 1):
            x = Defines.GRID_NUM - 1 - j
            y = i
            stone = board[x][y]
            if (x, y) in casillas:
                # Busca la posicion en casillas y obt�n su �ndice para imprimir el n�mero
                # num = casillas.index((x, y)) + 1
                hh=casillas.index((x,y))
                if hh<10:
                    print(f" {hh}", end="")
                else:
                    print(f"{hh}", end="")
            elif stone == Defines.NOSTONE:
                print(" -", end="")
            elif stone == Defines.BLACK:
                print(" O", end="")
            elif stone == Defines.WHITE:
                print(" *", end="")
        
        print(" ", end="")        
        print(f"{chr(ord('A') - 1 + i)}", end="\n")
    print("   " + "".join([chr(i + ord('A') - 1)+" " for i in range(1, Defines.GRID_NUM - 1)]))
    

# Metodo de colocacion de fichas pero trabajando con numpy
def make_move_2(board, move, color):
    board[move[0]][move[1]] = color
    
 
def hmove_evaluation(board, player, row, col):
    E = 0
    epsilon = 0.5  # Valor epsilon
    weights = [8, 6, 5, 3, 2, 0]  # Valores w1, w2, w3, w4, w5

    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for direction in directions:
        Edirectional = 1
        for k in range(1, 6):
            r = row + direction[0] * k
            c = col + direction[1] * k

            if not (0 <= r < len(board) and 0 <= c < len(board[0])):
                break

            if board[r][c] == 3 - player:  # Oponente's stone or border
                Edirectional += 0
                break
            elif board[r][c] == 0:  # Empty point
                Edirectional += epsilon
            elif board[r][c] == player:  # Own stone
                Edirectional *= weights[k]

        E += Edirectional

    return E


def undo_move(board, pos):
    # Supongamos que la posición pos es una tupla (x, y)
    x, y = pos

    # Revertir el movimiento en el tablero
    board[x][y] = Defines.NOSTONE  # O el valor adecuado para indicar una casilla vacía en tu juego


#Como está la situacion en defesa
def SituacionDefensa(board,preMove):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for direction in directions:
        direccion1=0
        direccion2=0
        for i in range(2): # Para mirar las dos piedras
            x1, y1 = preMove[i * 2], preMove[i * 2 + 1]
            movStone = board[x1, y1]

            if movStone == Defines.BORDER or movStone == Defines.NOSTONE: 
                continue

            countFichas = 0  # Contador de fichas consecutivas
            recommended_positions = []
            recommended_positions1 = []
            recommended_positions2 = []

            # Avanza en una dirección
            x, y = x1, y1
            for ii in range(6):
                if 0 <= x < board.shape[0] and 0 <= y < board.shape[1] and (board[x, y] == movStone or board[x, y] == Defines.NOSTONE) :
                    if board[x, y] == movStone:
                        countFichas += 1
                        x += direction[0]
                        y += direction[1]
                    else:
                        direccion1=1
                        recommended_positions1.append((x, y)) 
                        x += direction[0]
                        y += direction[1]
                else:
                    direccion1=0
                    break
                
            x, y = x1 - direction[0], y1 - direction[1]   
            for jj in range(5):
                if 0 <= x < board.shape[0] and 0 <= y < board.shape[1] and (board[x, y] == movStone or board[x, y] == Defines.NOSTONE) :
                    if board[x, y] == movStone:
                        countFichas += 1
                        x -= direction[0]
                        y -= direction[1]                        
                    else: 
                        direccion2=1
                        recommended_positions2.append((x, y))
                        x -= direction[0]
                        y -= direction[1]
                else:
                    direccion2=0
                    break

            if countFichas >= 4:
                if direccion1+direccion2==2:
                    recommended_positions=[recommended_positions1[0:1], recommended_positions2[0:1]]
                elif direccion1==1:
                    recommended_positions=recommended_positions1[0:1]
                else:
                    recommended_positions=recommended_positions2[0:1]
                
                # El oponente tiene al menos 4 fichas en una línea de 6
                # Devolver True y las posiciones recomendadas para bloquear
                return True, recommended_positions, direccion1+direccion2

    # Si no se encontró ninguna posibilidad de que el oponente gane, devolver False
    return False, []


def SituacionAtaque(board,preMove):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    
    for direction in directions:
        for i in range(2): # Para mirar las dos piedras
            x1, y1 = preMove[i * 2], preMove[i * 2 + 1]
            movStone = board[x1, y1]

            if movStone == Defines.BORDER or movStone == Defines.NOSTONE: 
                continue

            countFichas = 0  # Contador de fichas consecutivas
            recommended_positions = []

            # Avanza en una dirección
            x, y = x1, y1
            for ii in range(6):
                if 0 <= x < board.shape[0] and 0 <= y < board.shape[1] and (board[x, y] == movStone or board[x, y] == Defines.NOSTONE) :
                    if board[x, y] == movStone:
                        countFichas += 1
                        x += direction[0]
                        y += direction[1]
                    else:
                        recommended_positions.append((x, y)) 
                        x += direction[0]
                        y += direction[1]
                else:
                    break
                
            x, y = x1 - direction[0], y1 - direction[1]  
            for jj in range(5):
                if 0 <= x < board.shape[0] and 0 <= y < board.shape[1] and (board[x, y] == movStone or board[x, y] == Defines.NOSTONE) :
                    if board[x, y] == movStone:
                        countFichas += 1
                        x -= direction[0]
                        y -= direction[1]                        
                    else: 
                        recommended_positions.append((x, y))
                        x -= direction[0]
                        y -= direction[1]
                else:
                    break

            if countFichas >= 4 and len(recommended_positions)>0 :
                # Tengo menos 4 fichas en una línea de 6
                # Devolver True y las posiciones recomendadas para bloquear
                return True, recommended_positions

    # Si no se encontró ninguna posibilidad de que el oponente gane, devolver False
    return False, []


#Busqueda de amenazas (3 en raya mio) para buscar dos amenazas disponibles y colocar ahi las fichas
def buscar_amenaza(board, chess_type,amenaza_actual):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == chess_type:
                for direction in directions:
                    amenaza = validar_amenaza(board, i, j, chess_type, direction)
                    if amenaza and amenaza!=amenaza_actual:
                        return amenaza

    return None

def validar_amenaza(board, row, col, chess_type, direction):
    count = 1
    amenaza = []

    for k in range(1, 6):
        r = row + direction[0] * k
        c = col + direction[1] * k

        if not (0 <= r < len(board) and 0 <= c < len(board[0])):
            break

        if board[r][c] == chess_type:
            count += 1
            amenaza.append((r, c))
        elif board[r][c] == 0:
            amenaza.append((r, c))
        else:
            count = 1
            amenaza = []

    if count >= 3 and len(amenaza) >= 3:
        return amenaza, direction
    else:
        return None
