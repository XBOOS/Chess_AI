# Chinese Chess AI game
Implementing the chinese chess game playing between computer and human.

## Methodology
###1. For game search:  MiniMax algorithm with alpha-beta pruning. 

###2. Evaluation function & heuristics:

+ Evaluation function = Value(Computer side) - Value(User side)
  
+ For the value function:  
	I used 3 factors for the heuristics



```python
    def calcValue(self,RedSide):
        # accept a set of pieces from one player side a.k.a red or black
        if RedSide:
            pieceSet = self._board._redSet
        else:
            pieceSet = self._board._blackSet

        value = 0
        for piece in pieceSet:
            coordlist = pieceSet[piece]
            for coord in coordlist:
                pieceValue = self.evaValue(piece)
                positionValue = self.evaPosition(piece,coord)
                flexibilityValue = self.evaFlexibility(piece,coord)
                #relationshipValue
                value += self._piece_coef*pieceValue + self._position_coef*positionValue+self._flexibility_coef*flexibilityValue
        return value
```

3. Heuristic factors:  
1) value of each chess type   
2) position value, can see the position value table in postitionTable.py   

```python
the position value table for main attacking pieces
Rook, Horse, Cannon, Pawn

R_table = np.array([[14,14,12,18,16,18,12,14,14],
        [16,20,18,24,26,24,18,20,16],
        [12,12,12,18,18,18,12,12,12],
        [12,18,16,22,22,22,16,18,12],
        [12,14,12,18,18,18,12,14,12],
        [12,16,14,20,20,20,14,16,12],
        [6,10,8,14,14,14,8,10,6],
        [4,8,6,14,12,14,6,8,4],
        [8,4,8,16,8,16,8,16,8,4,8],
        [-2,10,6,14,12,14,6,10,-2]])

r_table = np.flipud(R_table)

H_table = np.array([[4,8,16,12,4,12,16,8,4],
    [4,10,28,16,8,16,28,10,4],
    [12,14,16,20,18,20,16,14,12],
    [8,24,18,24,20,24,18,24,8],
    [6,16,14,18,16,18,14,16,6],
    [4,12,16,14,12,14,16,12,4],
    [2,6,8,6,10,6,8,6,2],
    [4,2,8,8,4,8,8,2,4],
    [0,2,4,4,-2,4,4,2,0],
    [0,-4,0,0,0,0,0,-4,0]])

h_table = np.flipud(H_table)

C_table = np.array([[6,4,0,-10,-12,-10,0,4,6],
    [2,2,0,-4,-14,-4,0,2,2],
    [2,2,0,-10,-8,-10,0,2,2],
    [0,0,-2,4,10,4,-2,0,0],
    [0,0,0,2,8,2,0,0,0],
    [-2,0,4,2,6,2,4,-2,0,0],
    [0,0,0,2,4,2,0,0,0],
    [4,0,8,6,10,6,8,0,4],
    [0,2,4,6,6,6,4,2,0],
    [0,0,2,6,6,6,2,0,0]])

c_table = np.flipud(C_table)

P_table = np.array([[0,3,6,9,12,9,6,3,0],
    [18,36,56,80,120,80,56,36,18],
    [14,26,42,60,80,60,42,26,14],
    [10,20,30,34,40,34,30,20,10],
    [6,12,18,18,20,18,18,12,6],
    [2,0,8,0,8,0,8,0,2],
    [0,0,-2,0,4,0,-2,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]])

p_table = np.flipud(P_table)


def getPositionValue(piece,coord):

    if piece == "R":
        return R_table[coord[0]][coord[1]]
    elif piece == "r":
        return r_table[coord[0]][coord[1]]
    elif piece == "C":
        return C_table[coord[0]][coord[1]]
    elif piece == "c":
        return c_table[coord[0]][coord[1]]
    elif piece == "H":
        return H_table[coord[0]][coord[1]]
    elif piece == "h":
        return h_table[coord[0]][coord[1]]
    elif piece == "P":
        return P_table[coord[0]][coord[1]]
    elif piece == "p":
        return p_table[coord[0]][coord[1]]
    else:
        return 0
```
3) flexibility: num of possible moves  
	 I set the  weights of the three factors to 7,15,1. 	(could be adjusted with more experiments)
	 
	 	
###4.Search variables :   
     
+ Depth: default set to 4.
+ Breadth: default set to 20 ( the real is about average of 40 each step, but when the depth is 4 it is too slow, but much clever step)
+ As to cut the searching breadth, I sort the returned possible legal moves according to 2 factors
	+ wether they are capturing user’s pieces or just moving to another position.
	+ when it is capturing move, determine the move quality by value(eaten piece)/value(attacker)
	+ Extra: I tried 2 methods when they are just moving position, one is thet all these moves have quality value of 0. another is still promotional to their attacking power (Rook>Cannon=Horse>Elephant=Advisor)
