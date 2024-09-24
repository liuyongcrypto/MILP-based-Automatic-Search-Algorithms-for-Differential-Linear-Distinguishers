from gurobipy import *

def GetVariables(round,varName,varSize,variable):
    res = []
    for i in range(varSize):
        res.append(varName + "_" + str(round) + "_" + str(i))
        variable.add(varName + "_" + str(round) + "_" + str(i))
    return res

################################The Differential Part################################
def Constraint_initialize_D(R_D, f, variable):

    res = []
    for r in range (0, R_D):
        for i in range (16):
            res.append("2 " + GetVariables(r,"p_D",16,variable)[i])
            res.append("1 " + GetVariables(r,"q_D",16,variable)[i])

    for r in range (R_D+R_M, R_D+R_M+R_L):
        for i in range (16):
            res.append("4 " + GetVariables(r,"p_L",16,variable)[i])
            res.append("2 " + GetVariables(r,"q_L",16,variable)[i])
    f.write(" + ".join(res) + " - OBJ = 0 " + "\n")

    for i in range (size):
        f.write(GetVariables(R_D+R_M,"X",size,variable)[i] + " >= 0 \n")


    f.write("c" + " = 1 " + "\n")
    res = []
    for i in range (size):
        res.append(GetVariables(0,"X",size,variable)[i])
    f.write(" + ".join(res) + " >= 1 " + "\n")

    for i in range (size):
        f.write(GetVariables(R_D,"X",size,variable)[i] + " - " + str((INPUT_DIFFER[0]>>i)&0x1) + " c = 0 " + "\n")
    for i in range (size):
        if (((OUTPUT_MASK[0]>>i)&0x1) == 0):
            f.write(GetVariables(R_D+R_M,"X",size,variable)[i] + " - " + str((OUTPUT_MASK[0]>>i)&0x1) + " c = 0 " + "\n")

def Constraint_Sbox_D(r, f, variable):
    M0 = [[0, -1, -1, -1, -2, -2, -2, -1, 10, -3, 0], [4, 2, 2, 5, 1, 4, 1, 6, -12, 8, 0], [3, 4, 4, 2, 2, 0, 2, 1, -5, -1, 0], [-1, -8, 7, -3, -2, 4, -2, -9, 14, 11, 0], [-5, 4, -2, -3, 3, 1, -3, -1, 7, 4, 0], [0, -1, -1, 1, 2, 0, 2, 0, 1, -1, 0], [-1, 1, -2, 2, -5, -4, 3, 1, 6, 5, 0], [1, -5, 2, -2, 3, -5, -3, 1, 9, 4, 0], [3, 2, -5, -3, -2, -1, 3, -1, 7, 2, 0], [1, 2, 2, 0, -1, 0, -1, 0, 1, -1, 0], [-3, -2, 1, -2, -2, -1, 3, -1, 7, 1, 0], [1, -1, -1, 1, -1, 0, -1, -1, 5, -2, 0], [-2, -1, -1, -2, 1, 1, 0, 1, 5, -1, 0], [-8, -4, -4, 6, -1, 2, -1, 0, 10, 7, 0], [0, 1, 1, -1, 1, -1, 1, -1, 2, -1, 0], [3, 2, 1, 0, 2, 4, 2, 4, -6, 1, 0], [0, 3, -3, 1, -1, -1, -2, -2, 6, 1, 0], [1, -2, 3, 2, 1, 3, -2, -2, 2, 1, 0], [0, -3, -3, -2, -1, 2, -1, -2, 10, -1, 0], [-1, 2, 2, 5, 1, -1, 1, 3, -3, 1, 0], [0, 1, -1, 1, -1, 1, 0, -1, 0, 0, -2], [-1, 0, -1, -1, -1, 0, 1, 1, 4, -1, 0], [3, 1, 1, -3, -2, -3, -2, 1, 7, -1, 0], [0, -1, 1, 1, -1, -1, 0, -1, 0, 0, -3], [-1, 1, 1, -1, 0, 0, 0, -1, 0, 0, -2]]
    P = [0, 16, 32, 48, 1, 17, 33, 49, 2, 18, 34, 50, 3, 19, 35, 51, 4, 20, 36, 52, 5, 21, 37, 53, 6, 22, 38, 54, 7, 23, 39, 55, 8, 24, 40, 56, 9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59, 12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63]
    
    for i in range (16):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(r,"X",size,variable)[4*i+3])
            res.append(str(M0[t][1]) + " " + GetVariables(r,"X",size,variable)[4*i+2])
            res.append(str(M0[t][2]) + " " + GetVariables(r,"X",size,variable)[4*i+1])
            res.append(str(M0[t][3]) + " " + GetVariables(r,"X",size,variable)[4*i+0])
            res.append(str(M0[t][4]) + " " + GetVariables(r+1,"X",size,variable)[P[4*i+3]])
            res.append(str(M0[t][5]) + " " + GetVariables(r+1,"X",size,variable)[P[4*i+2]])
            res.append(str(M0[t][6]) + " " + GetVariables(r+1,"X",size,variable)[P[4*i+1]])
            res.append(str(M0[t][7]) + " " + GetVariables(r+1,"X",size,variable)[P[4*i+0]])
            res.append(str(M0[t][8]) + " " + GetVariables(r,"p_D",16,variable)[i])
            res.append(str(M0[t][9]) + " " + GetVariables(r,"q_D",16,variable)[i])
            f.write(" + ".join(res) + " - " + str(M0[t][10]) + " c >= 0 " + "\n")

def Constraint_D(f, variable):
    Constraint_initialize_D(R_D, f, variable)
    for r in range (0, R_D):
        Constraint_Sbox_D(r, f, variable)

################################The Linear Part################################
def Constraint_initialize_L(R_L, f, variable):
    f.write("c" + " = 1 " + "\n")

    res = []
    for i in range (size):
        res.append(GetVariables(R_D+R_M,"X",size,variable)[i])
    f.write(" + ".join(res) + " >= 1 " + "\n")

def Constraint_Sbox_L(r, f, variable):
    M0 = [[-7, -2, -4, -2, 4, -5, -10, -3, 33, 21, 0], [0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1], [4, 4, 4, 3, 1, 3, 1, 3, -5, -9, 0], [-7, -2, 1, -3, -3, -4, 2, 0, 19, 12, 0], [1, -1, -1, 0, 0, 0, 0, 0, 1, 2, 0], [0, 0, 0, 0, -1, 1, -1, 0, 1, 2, 0], [5, 1, 1, 0, 3, 5, 3, 2, -4, -7, 0], [1, 2, 2, 6, 3, 2, 3, -1, -3, -6, 0], [1, 1, 1, 0, 0, 0, 0, 0, -1, 0, 0], [2, -3, -1, -1, -1, -4, 1, -3, 11, 9, 0], [0, 0, 0, 0, 1, 1, 1, 0, -1, 0, 0], [1, -1, -1, 3, -2, 2, -2, 3, 3, 2, 0], [-1, 2, -1, -6, -3, 4, -3, -5, 15, 13, 0], [-1, -1, 1, 0, 0, 1, 0, 0, 1, 2, 0], [1, 0, 0, 0, 1, -1, -1, 0, 1, 2, 0], [1, 0, 0, 0, -1, -1, 1, 0, 1, 2, 0], [-1, 1, -1, 0, 0, 1, 0, 0, 1, 2, 0], [0, -1, -1, 0, -1, 0, -1, 0, 3, 4, 0], [0, -1, -1, 0, 1, 0, 1, 0, 1, 2, 0], [-2, 2, -5, 1, -2, -3, -1, 2, 13, 8, 0], [0, 1, 1, 0, -1, 0, -1, 0, 1, 2, 0], [1, 2, 5, 3, 6, -1, 1, 5, -1, -7, 0], [-2, 1, 1, 0, 1, -2, 1, 0, 3, 2, 0], [-4, -5, -2, 3, 2, 4, -1, 1, 12, 7, 0], [1, -1, -1, -1, 0, -2, 0, -2, 6, 5, 0], [-1, -2, 1, 0, -1, -1, -1, 1, 6, 4, 0], [0, 1, 1, 0, 0, 1, -1, -1, 2, 1, 0]]
    P = [0, 16, 32, 48, 1, 17, 33, 49, 2, 18, 34, 50, 3, 19, 35, 51, 4, 20, 36, 52, 5, 21, 37, 53, 6, 22, 38, 54, 7, 23, 39, 55, 8, 24, 40, 56, 9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59, 12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63]
    
    for i in range (16):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(r,"X",size,variable)[4*i+3])
            res.append(str(M0[t][1]) + " " + GetVariables(r,"X",size,variable)[4*i+2])
            res.append(str(M0[t][2]) + " " + GetVariables(r,"X",size,variable)[4*i+1])
            res.append(str(M0[t][3]) + " " + GetVariables(r,"X",size,variable)[4*i+0])
            res.append(str(M0[t][4]) + " " + GetVariables(r+1,"X",size,variable)[P[4*i+3]])
            res.append(str(M0[t][5]) + " " + GetVariables(r+1,"X",size,variable)[P[4*i+2]])
            res.append(str(M0[t][6]) + " " + GetVariables(r+1,"X",size,variable)[P[4*i+1]])
            res.append(str(M0[t][7]) + " " + GetVariables(r+1,"X",size,variable)[P[4*i+0]])
            res.append(str(M0[t][8]) + " " + GetVariables(r,"p_L",16,variable)[i])
            res.append(str(M0[t][9]) + " " + GetVariables(r,"q_L",16,variable)[i])
            f.write(" + ".join(res) + " - " + str(M0[t][10]) + " c >= 0 " + "\n")

def Constraint_L(f, variable):
    Constraint_initialize_L(R_L, f, variable)
    for r in range (R_D+R_M, R_D+R_M+R_L):
        Constraint_Sbox_L(r, f, variable)

################################The middle-Differential Part################################
def Constraint_initialize_M_D(R_M, f, variable):
    f.write("c" + " = 1 " + "\n")
    res = []
    for i in range (size):
        res.append(GetVariables(R_D,"X_MD0",size,variable)[i])
    f.write(" + ".join(res) + " = 0 " + "\n")

    res = []
    for i in range (size):
        res.append(GetVariables(R_D,"X_MD1",size,variable)[i])
    f.write(" + ".join(res) + " >= 1 " + "\n")

    for i in range (size):
        f.write(GetVariables(R_D,"X_MD1",size,variable)[i] + " - " + GetVariables(R_D,"X",size,variable)[i] + " = 0 " + "\n")

def Constraint_Sbox_M_D(r, f, variable):
    P = [0, 16, 32, 48, 1, 17, 33, 49, 2, 18, 34, 50, 3, 19, 35, 51, 4, 20, 36, 52, 5, 21, 37, 53, 6, 22, 38, 54, 7, 23, 39, 55, 8, 24, 40, 56, 9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59, 12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63]
    M0 = [[-1, -1, 0, 0, 0, 0, -1, -1, 0, 0, 2, 0, 0, 0, 0, -1, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, -1, 0, 0], 
    [0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, -1, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, -1, -1, 0], 
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, -2, 0, 0, 0, 2, 1, 0], 
    [0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1], 
    [-1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1], 
    [1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0], 
    [0, 1, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 1, 1, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, -1, 0]]
    
    for i in range (int(size/4)):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(r,"X_MD0",size,variable)[4*i+3])
            res.append(str(M0[t][1]) + " " + GetVariables(r,"X_MD1",size,variable)[4*i+3])
            res.append(str(M0[t][2]) + " " + GetVariables(r,"X_MD0",size,variable)[4*i+2])
            res.append(str(M0[t][3]) + " " + GetVariables(r,"X_MD1",size,variable)[4*i+2])
            res.append(str(M0[t][4]) + " " + GetVariables(r,"X_MD0",size,variable)[4*i+1])
            res.append(str(M0[t][5]) + " " + GetVariables(r,"X_MD1",size,variable)[4*i+1])
            res.append(str(M0[t][6]) + " " + GetVariables(r,"X_MD0",size,variable)[4*i+0])
            res.append(str(M0[t][7]) + " " + GetVariables(r,"X_MD1",size,variable)[4*i+0])
            res.append(str(M0[t][8]) + " " + GetVariables(r+1,"X_MD0",size,variable)[P[4*i+3]])
            res.append(str(M0[t][9]) + " " + GetVariables(r+1,"X_MD1",size,variable)[P[4*i+3]])
            res.append(str(M0[t][10]) + " " + GetVariables(r+1,"X_MD0",size,variable)[P[4*i+2]])
            res.append(str(M0[t][11]) + " " + GetVariables(r+1,"X_MD1",size,variable)[P[4*i+2]])
            res.append(str(M0[t][12]) + " " + GetVariables(r+1,"X_MD0",size,variable)[P[4*i+1]])
            res.append(str(M0[t][13]) + " " + GetVariables(r+1,"X_MD1",size,variable)[P[4*i+1]])
            res.append(str(M0[t][14]) + " " + GetVariables(r+1,"X_MD0",size,variable)[P[4*i+0]])
            res.append(str(M0[t][15]) + " " + GetVariables(r+1,"X_MD1",size,variable)[P[4*i+0]])
            f.write(" + ".join(res) + " - " + str(M0[t][16]) + " c" + " >= 0 " + "\n")

def Constraint_M_D(f, variable):
    Constraint_initialize_M_D(R_M, f, variable)
    for r in range (R_D, R_D+R_M):
        Constraint_Sbox_M_D(r, f, variable)

################################The middle-Linear Part################################
def Constraint_initialize_M_L(R_M, f, variable):
    f.write("c" + " = 1 " + "\n")
    res = []
    for i in range (size):
        res.append(GetVariables(R_D+R_M,"X_ML0",size,variable)[i])
    f.write(" + ".join(res) + " = 0 " + "\n")

    res = []
    for i in range (size):
        res.append(GetVariables(R_D+R_M,"X_ML1",size,variable)[i])
    f.write(" + ".join(res) + " >= 1 " + "\n")

    for i in range (size):
        f.write(GetVariables(R_D+R_M,"X_ML1",size,variable)[i] + " - " + GetVariables(R_D+R_M,"X",size,variable)[i] + " = 0 " + "\n")

def Constraint_Sbox_M_L(r, f, variable):
    P = [0, 16, 32, 48, 1, 17, 33, 49, 2, 18, 34, 50, 3, 19, 35, 51, 4, 20, 36, 52, 5, 21, 37, 53, 6, 22, 38, 54, 7, 23, 39, 55, 8, 24, 40, 56, 9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59, 12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63]
    M0 = [[0, 0, 0, 0, 0, 0, -1, -1, -1, 0, 2, 0, 0, 0, 0, -1, 0], [-1, -1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0], [0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, -1, -1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, -1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, -1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 1, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, -1, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1], [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, -2, 0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 0, 1, 0, 0, -1, 0, 0, 0, 0, 0, 1, 0, 0], [0, -1, 1, 1, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, -1, 0, -2], [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0], [0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0]]

    for i in range (int(size/4)):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(r+1,"X_ML0",size,variable)[P[4*i+3]])
            res.append(str(M0[t][1]) + " " + GetVariables(r+1,"X_ML1",size,variable)[P[4*i+3]])
            res.append(str(M0[t][2]) + " " + GetVariables(r+1,"X_ML0",size,variable)[P[4*i+2]])
            res.append(str(M0[t][3]) + " " + GetVariables(r+1,"X_ML1",size,variable)[P[4*i+2]])
            res.append(str(M0[t][4]) + " " + GetVariables(r+1,"X_ML0",size,variable)[P[4*i+1]])
            res.append(str(M0[t][5]) + " " + GetVariables(r+1,"X_ML1",size,variable)[P[4*i+1]])
            res.append(str(M0[t][6]) + " " + GetVariables(r+1,"X_ML0",size,variable)[P[4*i+0]])
            res.append(str(M0[t][7]) + " " + GetVariables(r+1,"X_ML1",size,variable)[P[4*i+0]])
            res.append(str(M0[t][8]) + " " + GetVariables(r,"X_ML0",size,variable)[4*i+3])
            res.append(str(M0[t][9]) + " " + GetVariables(r,"X_ML1",size,variable)[4*i+3])
            res.append(str(M0[t][10]) + " " + GetVariables(r,"X_ML0",size,variable)[4*i+2])
            res.append(str(M0[t][11]) + " " + GetVariables(r,"X_ML1",size,variable)[4*i+2])
            res.append(str(M0[t][12]) + " " + GetVariables(r,"X_ML0",size,variable)[4*i+1])
            res.append(str(M0[t][13]) + " " + GetVariables(r,"X_ML1",size,variable)[4*i+1])
            res.append(str(M0[t][14]) + " " + GetVariables(r,"X_ML0",size,variable)[4*i+0])
            res.append(str(M0[t][15]) + " " + GetVariables(r,"X_ML1",size,variable)[4*i+0])
            f.write(" + ".join(res) + " - " + str(M0[t][16]) + " c" + " >= 0 " + "\n")

def Constraint_M_L(f, variable):
    Constraint_initialize_M_L(R_M, f, variable)
    for r in range (R_D, R_D+R_M):
        Constraint_Sbox_M_L(r, f, variable)

################################The middle Part################################
def Constraint_MDD_M_DL(r, f, variable):
    M0 = [[-1, -1, 0, 0, 0, -1], [0, 0, -1, -1, 0, -1], [0, 1, 0, 1, -1, 0], [1, 0, 1, 0, -1, 0], [-1, 0, 0, -1, 1, -1], [0, -1, -1, 0, 1, -1]]

    for i in range (size):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(r,"X_MD0",size,variable)[i])
            res.append(str(M0[t][1]) + " " + GetVariables(r,"X_MD1",size,variable)[i])
            res.append(str(M0[t][2]) + " " + GetVariables(r,"X_ML0",size,variable)[i])
            res.append(str(M0[t][3]) + " " + GetVariables(r,"X_ML1",size,variable)[i])
            res.append(str(M0[t][4]) + " " + GetVariables(r,"p_M",size,variable)[i])
            f.write(" + ".join(res) + " - " + str(M0[t][5]) + " c" + " >= 0 " + "\n")

def Constraint_M_DL(f, variable):
    for r in range (R_D, R_D + R_M + 1):
        Constraint_MDD_M_DL(r, f, variable)

################################total################################
def Constraint(f, variable):
    Constraint_D(f, variable)
    
    Constraint_M_D(f, variable)
    Constraint_M_L(f, variable)

    Constraint_M_DL(f, variable)

    Constraint_L(f, variable)

def ObjectiveFunction(f, variable):
    res = []
    for r in range (0, R_D):
        for i in range (16):
            res.append("2 " + GetVariables(r,"p_D",16,variable)[i])
            res.append("1 " + GetVariables(r,"q_D",16,variable)[i])

    if (WEIGHT == 1):
        for r in range (R_D, R_D + R_M + 1):
            for i in range (size):
                res.append("1 " + GetVariables(r,"p_M",size,variable)[i])

    elif (WEIGHT == 2):
        for r in range (R_D, R_D + R_M + 1):
            for i in range (size):
                res.append("2 " + GetVariables(r,"p_M",size,variable)[i])

    elif (WEIGHT == 3):
        for r in range (R_D, R_D + R_M + 1):
            for i in range (size):
                res.append("3 " + GetVariables(r,"p_M",size,variable)[i])

    elif (WEIGHT == 4):
        for r in range (R_D, R_D + R_M + 1):
            for i in range (size):
                res.append("4 " + GetVariables(r,"p_M",size,variable)[i])

    elif (WEIGHT == 5):
        for r in range (R_D, R_D + R_M + 1):
            for i in range (size):
                res.append("5 " + GetVariables(r,"p_M",size,variable)[i])

    elif (WEIGHT == 6):
        for r in range (R_D, R_D + R_M + 1):
            for i in range (size):
                res.append("6 " + GetVariables(r,"p_M",size,variable)[i])

    elif (WEIGHT == 7):
        for r in range (R_D, R_D + R_M + 1):
            for i in range (size):
                res.append("7 " + GetVariables(r,"p_M",size,variable)[i])

    elif (WEIGHT == 8):
        for r in range (R_D, R_D + R_M + 1):
            for i in range (size):
                res.append("8 " + GetVariables(r,"p_M",size,variable)[i])

    elif (WEIGHT == 9):
        for r in range (R_D, R_D + R_M + 1):
            for i in range (size):
                res.append("9 " + GetVariables(r,"p_M",size,variable)[i])

    elif (WEIGHT == 10):
        for r in range (R_D, R_D + R_M + 1):
            for i in range (size):
                res.append("10 " + GetVariables(r,"p_M",size,variable)[i])

    elif (WEIGHT == 11):
        for r in range (R_D, R_D + R_M + 1):
            for i in range (size):
                res.append("11 " + GetVariables(r,"p_M",size,variable)[i])

    elif (WEIGHT == 12):
        for r in range (R_D, R_D + R_M + 1):
            for i in range (size):
                res.append("12 " + GetVariables(r,"p_M",size,variable)[i])

    elif (WEIGHT == 13):
        for r in range (R_D, R_D + R_M + 1):
            for i in range (size):
                res.append("13 " + GetVariables(r,"p_M",size,variable)[i])

    elif (WEIGHT == 14):
        for r in range (R_D, R_D + R_M + 1):
            for i in range (size):
                res.append("14 " + GetVariables(r,"p_M",size,variable)[i])

    elif (WEIGHT == 15):
        for r in range (R_D, R_D + R_M + 1):
            for i in range (size):
                res.append("15 " + GetVariables(r,"p_M",size,variable)[i])

    elif (WEIGHT == 16):
        for r in range (R_D, R_D + R_M + 1):
            for i in range (size):
                res.append("16 " + GetVariables(r,"p_M",size,variable)[i])

    elif (WEIGHT == 17):
        for r in range (R_D, R_D + R_M + 1):
            for i in range (size):
                res.append("17 " + GetVariables(r,"p_M",size,variable)[i])

    elif (WEIGHT == 18):
        for r in range (R_D, R_D + R_M + 1):
            for i in range (size):
                res.append("18 " + GetVariables(r,"p_M",size,variable)[i])

    elif (WEIGHT == 19):
        for r in range (R_D, R_D + R_M + 1):
            for i in range (size):
                res.append("19 " + GetVariables(r,"p_M",size,variable)[i])

    else:
        for r in range (R_D, R_D + R_M + 1):
            for i in range (size):
                res.append("20 " + GetVariables(r,"p_M",size,variable)[i])

    for r in range (R_D+R_M, R_D+R_M+R_L):
        for i in range (16):
            res.append("4 " + GetVariables(r,"p_L",16,variable)[i])
            res.append("2 " + GetVariables(r,"q_L",16,variable)[i])
    f.write(" + ".join(res) + "\n")

def VariablesType(f):
    f.write("\n".join(variable) + "\n")

def CreateModel(lpFileName, variable):
    f = open(lpFileName, "w")
    f.write("Minimum\n")
    ObjectiveFunction(f, variable)
    f.write("Subject To\n")
    Constraint(f, variable)
    f.write("Binaries\n")
    VariablesType(f)
    f.write("End\n")
    f.close()

def SolveModel(lpFileName, solFileName, lpFileName_result):
    model = read(lpFileName)
    model.Params.PoolSearchMode = 2
    model.Params.PoolSolutions = 1
    model.optimize()
    model.write(solFileName)
    f = open(lpFileName_result,"a")
    # Solutions_0x = []
    PR = []
    ss = [[]for i in range (model.getAttr("SolCount"))]

    for i in range(model.SolCount):
        Solution = []
        model.Params.SolutionNumber = i
        # print("Obj_{} = {}" .format(i+1, model.PoolObjVal))

        x = model.getVars()
        Solution = (model.getAttr('Xn',x))
        X = 0
        Y = 0

        for j in range ((32*R_D+64*R_M+64+32*R_L)+1, (32*R_D+64*R_M+64+32*R_L)+1+64):
            if (abs(Solution[j]) < 0.1):
                X = X + (0 << (j-((32*R_D+64*R_M+64+32*R_L)+1)))
            else:
                X = X + (1 << (j-((32*R_D+64*R_M+64+32*R_L)+1)))

    #     Solutions_0x.append([X,Y,Solution[32*R_D+64*R_M+64+32*R_L]])
    # for i in range (len(Solutions_0x)):
        f.write("[" + str(hex(INPUT_DIFFER[0])) + ", " + str(hex(X)) + ", " + str(Solution[32*R_D+64*R_M+64+32*R_L])+ "],\n")

if __name__ == "__main__":
    ANSWER = [[0x1, 0xeae0e2e0eae00000],
[0x100000001, 0x80000000200000],
[0x2, 0xeee0a8e0eee00000],
[0x20002, 0x8080000000000000],
[0x200000002, 0x8000810000],
[0x2000000000002, 0x20000008000000],
[0x4, 0xeee0eac0eae00000],
[0x400000004, 0xa0000000c0000000],
[0x4000000000004, 0x200000],
[0x8, 0xfee0a020aaa00000],
[0x10, 0xeae0e8e0e8e00000],
[0x1000000010, 0x6000000000000000],
[0x20, 0xeee0e8e0eee00000],
[0x2000000020, 0x8000000000000000],
[0x40, 0xeae0a8e0fae00000],
[0x400040, 0x200000],
[0x4000000040, 0x4000224000200008],
[0x40000000000040, 0x800],
[0x80, 0xa2e0e480e0e00000],
[0x800080, 0x100],
[0x8000000080, 0x10000000000000],
[0x100, 0xe8e0caa0eae00000],
[0x10000000100, 0xc0200020000000],
[0x200, 0xeee0e2e0eee00000],
[0x2000200, 0x200000],
[0x20000000200, 0x200000000000],
[0x400, 0xeee0eee0eee00000],
[0x40000000400, 0x2000000020000000],
[0x800, 0xe2e06880eaa00000],
[0x1000, 0xe8e02020e2a00000],
[0x10001000, 0x100000000000000],
[0x1000000000001000, 0x800000000000000],
[0x2000, 0xeaa00020e2e00000],
[0x4000, 0xaaa08000a8800000],
[0x40004000, 0x20000000],
[0x400000004000, 0x2008000000],
[0x8000, 0xa060200000800000],
[0x800000008000, 0x8000000000],
[0x10000, 0xe2e0e860a2b80000],
[0x1000000010000, 0x40000000],
[0x20000, 0xeee0a2a0eae00000],
[0x2000000020000, 0x200000],
[0x40000, 0xeae0e8c0aee00000],
[0x400040000, 0x2000004000000000],
[0x80000, 0xe0a82000a8a00000],
[0x100000, 0xe2e020a0aae00000],
[0x200000, 0xe8e0e8a0eae00000],
[0x400000, 0xaae0eea0eee00000],
[0x40000000400000, 0x4004200000],
[0x800000, 0xa8a08080e0a40000],
[0x8000800000, 0x80000000000],
[0x1000000, 0x6ae0a260eae00000],
[0x100000001000000, 0x200000],
[0x2000000, 0xeae0e0a0eae00000],
[0x4000000, 0xeee0e6a0eee00800],
[0x8000000, 0xa2a080c0aae00000],
[0x10000000, 0xa0a02080a2200000],
[0x1000000010000000, 0x100000000],
[0x20000000, 0xa0a02260a0a00000],
[0x40000000, 0xa2a000002aa00000],
[0x80000000, 0x8080202020a00000],
[0x100000000, 0xeaa0a8a0eee00000],
[0x200000000, 0xeee0eaa0eee00000],
[0x400000000, 0xeee0a2a0e6e00000],
[0x800000000, 0xa2e000a0a0a00000],
[0x1000000000, 0xaae0a0a0a8a00000],
[0x2000000000, 0xeee022a0eae00000],
[0x4000000000, 0xeae0aa60aaf00000],
[0x8000000000, 0xa0a080a0e0a00000],
[0x80008000000000, 0x800000],
[0x10000000000, 0xe8e022e0e2e00000],
[0x20000000000, 0xe2e0a2e0eae00000],
[0x40000000000, 0xa6e0a2e0eee00000],
[0x80000000000, 0xa060a020a0a00000],
[0x100000000000, 0xa8010000a0e00000],
[0x200000000000, 0xa8a0600020a00000],
[0x400000000000, 0x2040a00088a00000],
[0x800000000000, 0x2000000000000000],
[0x1000000000000, 0x82e00080e0a00000],
[0x2000000000000, 0xeaa00000ec600000],
[0x4000000000000, 0xa8a02080eee00000],
[0x8000000000000, 0x2000000000800000],
[0x10000000000000, 0xe080a080a8c00000],
[0x20000000000000, 0xece0e26082e00000],
[0x40000000000000, 0xeae082c0eaa00000],
[0x80000000000000, 0xa000000080200000],
[0x100000000000000, 0xe0a02000a0600000],
[0x200000000000000, 0xece08480aea00000],
[0x400000000000000, 0xe2a08820e8a00000],
[0x800000000000000, 0x8010004080400000],
[0x1000000000000000, 0xc0200000],
[0x2000000000000000, 0x22204000a8a00000],
[0x4000000000000000, 0x2000800004000000],
[0x8000000000000000, 0x2000000000080000]]
    cor_min = 64
    cor_index = []
    for ans in range (len(ANSWER)):
        for WEIGHT in range (1, 21):
            INPUT_DIFFER = [ANSWER[ans][0]]
            OUTPUT_MASK = [ANSWER[ans][1]]
            R_D = 2
            R_M = 8
            R_L = 4
            size = 64
            variable = set()
            lpFileName = "PRESENT_dl.lp"
            solFileName = "PRESENT_dl_%d_%d_%d.sol" % (R_D, R_M, R_L)
            lpFileName_result = "PRESENT_dl_%d_%d_%d.txt" % (R_D, R_M, R_L)
            CreateModel(lpFileName, variable)
            SolveModel(lpFileName, solFileName, lpFileName_result)
