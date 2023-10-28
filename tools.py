from defines import *
import time
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
# import matplotlib
# matplotlib.use("Agg")



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

def unmake_move(board, move):
    board[move.positions[0].x][move.positions[0].y] = Defines.NOSTONE
    board[move.positions[1].x][move.positions[1].y] = Defines.NOSTONE

def is_win_by_premove(board, preMove):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    board = np.array(board)  # Convierte la matriz a un array de NumPy

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
    for i in range(1, Defines.GRID_NUM - 1):  #Esto crea un vector desde 1 hasta (21-1)-1
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


def show_m_board(m_board):
    """
    Visualizacion del estado del juego
    """

    col = 'ABCDEFGHIJKLMNOPQRS'
    fil = 'SRQPONMLKJIHGFEDCBA'

    # Array de anotaciones de 19x19
    annot = []
    for l1 in fil:
        fila = []
        for l2 in col:
            fila.append(l2 + l1)
        annot.append(fila)

    #Obtener el tablero sin los bordes
    m_board_rep = np.array(m_board)
    m_board_rep = m_board_rep[1:20,1:20]
    
    # Reemplazar los 2 por -1
    m_board_rep = np.where(m_board_rep == 2, -1, m_board_rep)
    
    fontdict = {'fontsize': 10,
                'fontweight' : 50}
    # Crear un colormap personalizado en el que el negro = 1, blanco = -1 y naranja = 0.
    # Define los colores
    colors = [(1, 1, 1), (1, 0.8, 0.4), (0, 0, 0)]

    # Crea el colormap
    n_bins = 3  
    cmap_name = "custom_colormap"
    cm = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)

    # Normaliza los valores para que estén en el rango [0, 1]
    norm = mcolors.Normalize(vmin=-1, vmax=1)

    plt.figure(figsize=(6,6))
    # Mostrar movimientos sobre el tablero
    plt.imshow(m_board_rep, cmap=cm, norm=norm) 
    
    # Mostrar anotaciones sobre la imagen
    for i in range(19):
        for j in range(19):
            plt.text(j, i, annot[i][j], ha="center", va="center", color="green", fontdict=fontdict)

    plt.axis('off')
    plt.tight_layout()
    plt.show()

def get_valid_locations(matriz,tamano,posicion):
      # matriz ya es numpy
        filas, columnas = matriz.shape
        inicio_fila = max(0, posicion[0] - tamano // 2)
        fin_fila = min(filas, posicion[0] + tamano // 2 + 1)
        inicio_columna = max(0, posicion[1] - tamano // 2)
        fin_columna = min(columnas, posicion[1] + tamano // 2 + 1)

        indices_fila, indices_columna = np.indices(matriz.shape)
        posiciones_disponibles = list(zip(indices_fila[inicio_fila:fin_fila, inicio_columna:fin_columna].ravel(),
                                          indices_columna[inicio_fila:fin_fila, inicio_columna:fin_columna].ravel()))

        # Filtrar las posiciones ocupadas o en el borde del tablero
        posiciones_disponibles = [pos for pos in posiciones_disponibles if matriz[pos[0], pos[1]] == Defines.NOSTONE]
        # Calcular la distancia al centro
        centro = (tamano // 2, tamano // 2)
        posiciones_disponibles.sort(key=lambda pos: np.linalg.norm(np.array(pos) - np.array(centro)))
        
        return posiciones_disponibles

def posiciones_disponibles_sin_repetidos(matriz, tamano, posicion1, posicion2):
    # matriz ya es numpy
    # Obtiene las posiciones disponibles con duplicados
    disponibles_con_duplicados = posiciones_disponibles_con_duplicados(matriz, tamano, posicion1, posicion2)
    
    # Elimina duplicados manteniendo el orden
    disponibles_sin_repetidos = list(dict.fromkeys(disponibles_con_duplicados))
    
    return disponibles_sin_repetidos

def posiciones_disponibles_con_duplicados(matriz, tamano, posicion1, posicion2):
    # Llama a la función posiciones_disponibles con la primera posición central
    disponibles1 = get_valid_locations(matriz, tamano, posicion1)
    
    # Llama a la función posiciones_disponibles con la segunda posición central
    disponibles2 = get_valid_locations(matriz, tamano, posicion2)
    
    # Combina las dos listas sin eliminar duplicados
    disponibles_combinados = disponibles1 + disponibles2
    
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
                # Busca la posición en casillas y obtén su índice para imprimir el número
                # num = casillas.index((x, y)) + 1
                print(" X", end="")
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