class Defines:
    GRID_NUM=21          # Number of the board, 19*19 plus edges.
    GRID_COUNT=361         # Sum of the points in the board.
    BLACK=1           # Black flag in the board.
    WHITE=2           # White flag in the board.
    BORDER=3          # Border flag in the board.
    NOSTONE=0           # Empty flag.
    MSG_LENGTH=512 #Tamaño del mensaje
    GRID_NUM=21 #Number of the board, 19*19 plus edges.
    GRID_COUNT=361 #Sum of the points in the board.
    LOG_FILE="Arbeloa.log"
    ENGINE_NAME="sbfrmv"
    # Max values in the evaluation.
    MAXINT=20000
    MININT=-20000
    TAMANO = 4       #Tamaño de la ventana cuadrada de evaluacion para posicionar la ficha
    DEPTH = 4       #Profundidad de busqueda
    LVMOVE_N = []        #Last Valid Move Negro, almacena el ultimo movimiento valido
    LVMOVE_B = []        #Last Valid Move Blanco, almacena el ultimo movimiento valido 
    Multiplicador=[] #Multiplicador de la ventana de evaluacion si evita que gane el rival
    ContadorTurnos = 0
    flagMulti = 0
        

class StonePosition:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class StoneMove:
    def __init__(self):
        self.positions = [StonePosition(0,0),StonePosition(0,0)]
        self.score = 0

# One point and its value.
class Chess:
    def __init__(x,y,score):
        self.x = x
        self.y = y
        self.score = score
