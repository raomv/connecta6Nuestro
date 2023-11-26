from email import contentmanager
from hmac import new
from os import terminal_size
from pickle import TRUE
from re import A
from token import ISTERMINAL
from turtle import color, pos
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
          
        Defines.Multiplicador = []
        Defines.flagMulti=0

        #------------- Alguien ha ganado ya? -------------
        if self.m_chess_type==Defines.BLACK: #juega negro    
            own_lastPlay = Defines.LVMOVE_N
            rival_lastPlay = Defines.LVMOVE_B
        else: #Juega blanca
            own_lastPlay = Defines.LVMOVE_B
            rival_lastPlay = Defines.LVMOVE_N
        
            #Check game result
        if len(own_lastPlay)>2 and (is_win_by_premove(self.m_board, rival_lastPlay)):
            if (ourColor == self.m_chess_type):
                #Opponent wins.
                return 0;
            else: 
                #Self wins.
                return Defines.MININT + 1;
    
        #------------- ATAQUE -------------
        if  len(own_lastPlay)>2:
            Jugada = SituacionAtaque(np.array(self.m_board),own_lastPlay) #Puedo ganar ya? ;^P
            if Jugada[0]:
                    Defines.Multiplicador = Jugada[1]
                    [mejoresMov, alpha]=self.minimax(np.array(self.m_board), 2,Defines.MININT,Defines.MAXINT, True, own_lastPlay,[],3) #3 es el número del ataque. Lo he implementado el ultimo
                    bestMove.positions[0].x = mejoresMov[0][0]
                    bestMove.positions[0].y = mejoresMov[0][1]
                    bestMove.positions[1].x = mejoresMov[1][0]
                    bestMove.positions[1].y = mejoresMov[1][1]

                    return alpha 
        
        #------------- DEFENSA -------------
        if  len(rival_lastPlay)>2:
            Jugada = SituacionDefensa(np.array(self.m_board),rival_lastPlay) #Puede ganarme el rival en el siguiente turno? :^(
            if Jugada[0]:
                if Jugada[2]==1: #Solo tengo que tapar por un lado
                    Defines.Multiplicador = Jugada[1]
                    [mejoresMov, alpha]=self.minimax(np.array(self.m_board), 3,Defines.MININT,Defines.MAXINT, True, own_lastPlay,[],1)
                    bestMove.positions[0].x = mejoresMov[0][0]
                    bestMove.positions[0].y = mejoresMov[0][1]
                    bestMove.positions[1].x = mejoresMov[1][0]
                    bestMove.positions[1].y = mejoresMov[1][1]

                    return alpha
                else: #Si tengo que tapar oblogatoriamente por los dos lados :^{
                    bestMove.positions[0].x = Jugada[1][0][0][0] 
                    bestMove.positions[0].y = Jugada[1][0][0][1]
                    bestMove.positions[1].x = Jugada[1][1][0][0]
                    bestMove.positions[1].y = Jugada[1][1][0][1]
                    return alpha
        
        #------------- Primer movimiento -------------
        alpha = 0
        if(Defines.ContadorTurnos):
            bestMove.positions[0].x = 10
            bestMove.positions[0].y = 10
            bestMove.positions[1].x = 10
            bestMove.positions[1].y = 10

        #------------- NI DEFENSA NI ATAQUE. A JUGAR!! -------------
        else:   
            # self,board, depth, alpha, beta, maximizingPlayer, position1, position2)
            if Defines.ContadorTurnos == 1: #Primeros turnos minimaxprofundidad 1
                bestMove.positions[0].x = 9
                bestMove.positions[0].y = 9
                bestMove.positions[1].x = 9
                bestMove.positions[1].y = 11
                return alpha
            elif Defines.ContadorTurnos < 4: #Primeros turnos minimaxprofundidad 2
                [mejoresMov, alpha]=self.minimax(np.array(self.m_board),2,Defines.MININT,Defines.MAXINT,True,own_lastPlay,[],2)
            else:
                [mejoresMov, alpha]=self.minimax(np.array(self.m_board),Defines.DEPTH,Defines.MININT,Defines.MAXINT,True,own_lastPlay,[],2)
            
            bestMove.positions[0].x = mejoresMov[0][0]
            bestMove.positions[0].y = mejoresMov[0][1]
            bestMove.positions[1].x = mejoresMov[1][0]
            bestMove.positions[1].y = mejoresMov[1][1]

        return alpha
        
    def check_first_move(self):  #Recorre todas las posiciones y devuelve false si esta vacio
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


    def minimax(self,board, depth, alpha, beta, maximizingPlayer, positions,evaluation_position,first_call):

        if first_call!=0:
            tamanito=Defines.TAMANO
            evaluation_position=posiciones_disponibles_sin_repetidos(board,tamanito,positions[:2],positions[2:])
            valid_locations=evaluation_position
            if first_call==1: #Si es la primera llamada y es desde defensa 
                valid_locations+=Defines.Multiplicador 
                #valid_locations = Defines.Multiplicador + valid_locations
                valid_locations=list(dict.fromkeys(valid_locations))
            elif  first_call==3: #Jugada de ataque
                valid_locations=Defines.Multiplicador 
            print_board_2(board, valid_locations)     
        else:
            tamanito=2
            valid_locations_tmp =  posiciones_disponibles_sin_repetidos(board,tamanito,positions[:2],positions[2:])
            valid_locations= [pos for pos in valid_locations_tmp if pos in evaluation_position]
            #print_board_2(board, valid_locations)     
           
            
        is_terminal =  is_win_by_premove(board, positions)

        if depth == 0 or is_terminal:
            if is_terminal:
                if maximizingPlayer:
                    return (None,Defines.MININT) 
                else:
                    #print_board(board)
                    return (None,Defines.MAXINT)
                # else: # Game is over, no more valid moves
                #     return (None, 0)
            else: # Depth is
                if maximizingPlayer:
                    return (None,hmove_evaluation(board,self.m_chess_type,positions[0],positions[1])+hmove_evaluation(board,self.m_chess_type,positions[2],positions[3]))
                else:
                     return (None,hmove_evaluation(board,self.m_chess_type^3,positions[0],positions[1])+hmove_evaluation(board,self.m_chess_type^3,positions[2],positions[3]))       
        elif len(valid_locations) < 2:
                if maximizingPlayer:
                    return (None,hmove_evaluation(board,self.m_chess_type,positions[0],positions[1])+hmove_evaluation(board,self.m_chess_type,positions[2],positions[3]))
                else:
                     return (None,hmove_evaluation(board,self.m_chess_type^3,positions[0],positions[1])+hmove_evaluation(board,self.m_chess_type^3,positions[2],positions[3]))       

        if maximizingPlayer:
            value = Defines.MININT
            best_move = None
            for i in range(len(valid_locations)):
                pos1 = valid_locations[i]
                for j in range(i + 1, len(valid_locations)):
                    pos2 = valid_locations[j]     
                    if first_call==1 and (pos1 in Defines.Multiplicador or pos2 in Defines.Multiplicador):
                        Defines.flagMulti=1
                    elif first_call==1 and (pos1 not in Defines.Multiplicador or pos2 not in Defines.Multiplicador):
                        Defines.flagMulti=0

                    make_move_2(board,pos1,self.m_chess_type) #He hecho este método para trabajar con Numpy y no con listas
                    make_move_2(board,pos2,self.m_chess_type)     
                    # print_board_2(b_copy, valid_locations)  
                    # print_board(b_copy, [pos1,pos2])

                    # Llamar recursivamente al algoritmo Minimax con las dos posiciones
                    new_score = self.minimax(board, depth-1, alpha, beta, False,[pos1[0],pos1[1], pos2[0],pos2[1]],evaluation_position,0)
                    puntuacion_positiva=new_score[1]
                    
                    if Defines.flagMulti==1:
                        puntuacion_positiva+=15000#Defines.MAXINT
                            
                    if puntuacion_positiva> value:
                        value = puntuacion_positiva
                        best_move = (pos1, pos2)
                        alpha = max(alpha, value)
                        
                    # Deshacemos el movimiento para que no se quede en el tablero
                    undo_move(board, pos2)
                    undo_move(board, pos1)
                    
                    if alpha >= beta:
                        break
                if alpha >= beta:
                  break
            return best_move, value
        
        else:  # Minimizing player
            value = Defines.MAXINT
            best_move = None
            for i in range(len(valid_locations)):
                pos1 = valid_locations[i]
                for j in range(i + 1, len(valid_locations)):
                    pos2 = valid_locations[j]
                        
                    make_move_2(board,pos1,self.m_chess_type ^ 3)
                    make_move_2(board,pos2,self.m_chess_type ^ 3) 

                    new_score = self.minimax(board, depth-1, alpha, beta, True,[pos1[0],pos1[1], pos2[0],pos2[1]],evaluation_position,0)
                    puntuacion_negativa=new_score[1]
                        
                    if puntuacion_negativa < value:
                        value = puntuacion_negativa
                        best_move = (pos1, pos2)
                        beta = min(beta, value)
                        
                    # Deshacemos el movimiento para que no se quede en el tablero
                    undo_move(board, pos2)
                    undo_move(board, pos1)

                    if alpha <= beta:
                        break
                if alpha <= beta:
                    break
            return best_move, value
    
def flush_output():
    import sys
    sys.stdout.flush()


