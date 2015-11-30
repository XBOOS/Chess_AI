import numpy as np

# the position value table is only neccessary for the attacking pieces
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





if __name__=="__main__":
    print "Testing for position table "
    """
    print "==========================="
    print "===========R==============="
    for i in range(10):
        for j in range(9):
            print R_table[i][j],
        print    
            
    print "===========H==============="
    for i in range(10):
        for j in range(9):
            print H_table[i][j],
        print    

    
    print "===========C==============="
    for i in range(10):
        for j in range(9):
            print C_table[i][j],
        print    
    print "===========P==============="
    for i in range(10):
        for j in range(9):
            print R_table[i][j],
        print    
    """
    print "R (3,2) should be 16 = ",getPositionValue("R",(3,2))
    print "H (2,7) should be 14 = ",getPositionValue("H",(2,7))
    print "C (5,6) should be 4 = ",getPositionValue("C",(5,6))
    print "P (8,4) should be 0 = ",getPositionValue("P",(8,4))
    print "The pieces we dont care should be 0 = ",getPositionValue("A",(1,1))
    
