from os import terminal_size
from pickle import TRUE
from token import ISTERMINAL
from turtle import color
from tools import *
import random


class SearchEngine():
    def __init__(self):
        self.m_board = None
        self.m_chess_type = None
        self.m_alphabeta_depth = None
        self.m_total_nodes = 0

    def before_search(self, board, color, alphabeta_depth):
        self.m_board = [row[:] for row in board]
        self.m_chess_type = color
        self.m_alphabeta_depth = alphabeta_depth
        self.m_total_nodes = 0
        
    def alpha_beta_search(self, depth, alpha, beta, ourColor, bestMove, preMove):
    
        #Check game result
        if len(Defines.LVMOVE)>2 and (is_win_by_premove(self.m_board, Defines.LVMOVE)):
            if (ourColor == self.m_chess_type):
                #Opponent wins.
                return 0;
            else:
                #Self wins.
                return Defines.MININT + 1;
        
        alpha = 0
        if(self.check_first_move()):
            bestMove.positions[0].x = 10
            bestMove.positions[0].y = 10
            bestMove.positions[1].x = 10
            bestMove.positions[1].y = 10
            # Guarda el ultimo movimiento 
            Defines.LVMOVE = [10,10]

        else:   
            # self,board, depth, alpha, beta, maximizingPlayer, position1, position2)
            [mejoresMov, alpha]=self.minimax(np.array(self.m_board),Defines.DEPTH,Defines.MININT,Defines.MAXINT,True,Defines.LVMOVE)
            #move1 = self.find_possible_move()
            bestMove.positions[0].x = mejoresMov[0][0]
            bestMove.positions[0].y = mejoresMov[0][1]
            bestMove.positions[1].x = mejoresMov[1][0]
            bestMove.positions[1].y = mejoresMov[1][1]
            make_move(self.m_board,bestMove,ourColor)
            '''#Check game result
            if (is_win_by_premove(self.m_board, bestMove)):
                #Self wins.
                return Defines.MININT + 1;'''
            
            # move2 = self.find_possible_move()
            # bestMove.positions[1].x = move2[0]
            # bestMove.positions[1].y = move2[1]
            # make_move(self.m_board,bestMove,ourColor)
            Defines.LVMOVE = [mejoresMov[0][0],mejoresMov[0][1], mejoresMov[1][0],mejoresMov[1][1]]

        return alpha
        
    def check_first_move(self):  #Recorre todas las posiciones y devuelve false si está vacio
        for i in range(1,len(self.m_board)-1):              #Recorre numero de filas
            for j in range(1, len(self.m_board[i])-1):      #Recorre numero de columnas 
                if(self.m_board[i][j] != Defines.NOSTONE):
                    return False
        return True
        
    def find_possible_move(self):
        for i in range(1,len(self.m_board)-1):
            for j in range(1, len(self.m_board[i])-1):
                if(self.m_board[i][j] == Defines.NOSTONE):
                    return (i,j)
        return (-1,-1)


    def minimax(self,board, depth, alpha, beta, maximizingPlayer, positions):
              
        is_terminal =  is_win_by_premove(board, positions)
        if depth == 0 or is_terminal:
            if is_terminal:
                if maximizingPlayer:
                    print_board(board)
                    return (None,Defines.MININT)
                else:
                    print_board(board)
                    return (None,Defines.MAXINT)
                # else: # Game is over, no more valid moves
                #     return (None, 0)
            else: # Depth is
                #return (None, score_position(board, AI_PIECE)) #Comentado por ahora la llamada a un metodo, voy a probar con numeros random primero    
                return (None,random.uniform(1, 300))
        else:   #Antes lo tenia arriba, pero si esto para evaluar, pa que evaluar posibles posiciones 
            if len(positions)==2:
                valid_locations = get_valid_locations(board,Defines.TAMANO,positions)
            else:
                valid_locations =  posiciones_disponibles_sin_repetidos(board,Defines.TAMANO,positions[:2],positions[2:])
        
           # Este print es para mostrar las posibles jugadas que harian mindy y maximiliano
            # print_board_2(board, valid_locations) 

        if maximizingPlayer:
            value = Defines.MININT
            best_move = None
            for pos1 in valid_locations:
                for pos2 in valid_locations:
                    if pos1 != pos2:
                        # Realizar la copia del tablero y simular el movimiento
                        b_copy = board.copy()
                        make_move_2(b_copy,pos1,self.m_chess_type) #He hecho este método para trabajar con Numpy y no con listas
                        make_move_2(b_copy,pos2,self.m_chess_type)
                        
                        # Llamar recursivamente al algoritmo Minimax con las dos posiciones
                        new_score = self.minimax(b_copy, depth-1, alpha, beta, False,[pos1[0],pos1[1], pos2[0],pos2[1]])

                        if new_score[1]> value:
                            value = new_score[1]
                            best_move = (pos1, pos2)
                            alpha = max(alpha, value)

                        if alpha >= beta:
                            break
                if alpha >= beta:
                    break

            return best_move, value
        else:  # Minimizing player
            value = Defines.MAXINT
            best_move = None
            for pos1 in valid_locations:
                for pos2 in valid_locations:
                    if pos1 != pos2:
                        b_copy = board.copy()
                        make_move_2(b_copy,pos1,self.m_chess_type ^ 3)
                        make_move_2(b_copy,pos2,self.m_chess_type ^ 3)

                        new_score = self.minimax(b_copy, depth-1, alpha, beta, True,[pos1[0],pos1[1], pos2[0],pos2[1]])

                        if new_score[1] < value:
                            value = new_score[1]
                            best_move = (pos1, pos2)
                            beta = min(beta, value)

                        if alpha <= beta:
                            break
                if alpha <= beta:
                    break
            return best_move, value



def flush_output():
    import sys
    sys.stdout.flush()


