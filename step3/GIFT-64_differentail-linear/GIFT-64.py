from gurobipy import *

def GetVariables(round,varName,varSize,variable):
    res = []
    for i in range(varSize):
        res.append(varName + "_" + str(round) + "_" + str(i))
        variable.add(varName + "_" + str(round) + "_" + str(i))
    return res

################################The Differential Part################################

def Constraint_initialize_D(R, f, variable):

    res = []
    for r in range (0, R_D):
        for i in range (16):
            res.append("3 " + GetVariables(r,"p0",16,variable)[i])
            res.append("2 " + GetVariables(r,"P1",16,variable)[i])
            res.append("1.415 " + GetVariables(r,"P2",16,variable)[i])

    for r in range (R_D+R_M, R_D+R_M+R_L):
        for i in range (16):
            res.append("4 " + GetVariables(r,"p0",16,variable)[i])
            res.append("2 " + GetVariables(r,"P1",16,variable)[i])
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
    M0 = [[1, 3, 2, 4, 4, 2, 2, 3, -8, -6, -10, 0], [-2, -1, -1, -1, -4, -1, 1, 0, 9, 6, 1, 0], [4, 3, 3, -2, 0, 4, 3, 2, 2, -9, -11, 0], [0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1], [-2, -4, 0, -2, 4, -1, -3, -3, 11, 9, 11, 0], [1, -1, -1, 3, -4, 0, -3, -4, 9, 10, 9, 0], [1, 1, -1, 3, 4, 1, 2, 2, -5, -2, -4, 0], [5, 1, 7, 5, -1, -1, -3, 3, -1, -3, 0, 0], [-3, 3, -3, -2, -1, -3, 1, -2, 12, 8, 1, 0], [0, 2, 1, 3, 2, 0, 1, 1, -4, -2, -4, 0], [-4, 1, -2, -3, -1, 2, -2, 1, 10, 6, 2, 0], [4, -4, -1, -1, 2, -4, -1, 2, 8, 6, 7, 0], [-1, -1, 0, -1, 0, 0, 1, 1, 0, 1, 0, -2], [1, -1, 0, -2, 1, 0, -2, -2, 5, 6, 5, 0], [-2, -2, 3, -2, -3, 3, 3, -1, 7, 3, -3, 0], [-1, -1, -1, 1, -1, 0, -1, 0, 4, 3, 3, 0], [-1, 1, 2, -1, -2, -2, -2, 1, 6, 6, 2, 0], [3, 1, -1, -1, 2, 3, 1, -1, 0, -1, 0, 0], [2, -2, -5, -1, -1, -5, -1, -1, 14, 11, 9, 0], [-1, 1, 2, 2, -1, 0, -1, -2, 2, 5, 2, 0], [-1, 0, 0, 0, 1, -1, 1, -1, 0, 0, 0, -2], [1, -1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0], [1, 1, 1, 0, -1, -1, 1, -1, 0, 0, 0, -2], [0, 1, -1, -1, 0, 1, -1, 1, 0, 0, 0, -2], [1, -1, 1, 0, -1, 1, -1, 0, 0, 0, 0, -2]]
    P = [0, 17, 34, 51, 48, 1, 18, 35, 32, 49, 2, 19, 16, 33, 50, 3, 4, 21, 38, 55, 52, 5, 22, 39, 36, 53, 6, 23, 20, 37, 54, 7, 8, 25, 42, 59, 56, 9, 26, 43, 40, 57, 10, 27, 24, 41, 58, 11, 12, 29, 46, 63, 60, 13, 30, 47, 44, 61, 14, 31, 28, 45, 62, 15]
    
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
            res.append(str(M0[t][8]) + " " + GetVariables(r,"p0",16,variable)[i])
            res.append(str(M0[t][9]) + " " + GetVariables(r,"P1",16,variable)[i])
            res.append(str(M0[t][10]) + " " + GetVariables(r,"P2",16,variable)[i])
            f.write(" + ".join(res) + " - " + str(M0[t][11]) + " c >= 0 " + "\n")

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
    M0 = [[-3, -3, -1, -1, -1, -1, -3, -2, 14, 10, 0], [2, 2, 4, 3, 1, 2, 0, 0, -5, -4, 0], [0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1], [1, 2, 2, -5, 4, -4, 1, 2, 9, 1, 0], [1, 1, -3, 3, -3, 2, 2, 1, 6, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, -1, 0, 0], [0, 0, 1, 1, 0, 0, 0, 0, -1, 0, 0], [0, 0, 0, 1, 1, -1, 0, 0, 0, 1, 0], [0, 0, -1, -1, -1, -1, 0, 0, 0, 1, -3], [0, 0, 1, 0, -1, 1, 0, 0, 0, 1, 0], [0, -1, 2, 0, 0, -1, 2, 1, 2, 0, 0], [0, -1, -2, 0, 0, -2, -1, -1, 7, 5, 0], [3, -2, -2, -4, 4, 4, 3, 5, 4, 0, 0], [-2, 2, -2, 0, -1, 1, 1, -1, 6, 3, 0], [1, 3, 1, 1, -1, 0, -2, 2, 2, 0, 0], [-1, -2, -2, -1, -3, 0, -1, -3, 13, 9, 0], [-2, -2, -1, 0, 0, -1, -2, -1, 9, 6, 0], [2, 1, 2, 0, 2, 1, 1, -1, 0, -2, 0], [-1, 0, 0, 0, 1, 1, -1, -1, 0, 0, -2], [0, 1, 0, 0, 0, -1, 1, 1, 0, -1, -1]]
    P = [0, 17, 34, 51, 48, 1, 18, 35, 32, 49, 2, 19, 16, 33, 50, 3, 4, 21, 38, 55, 52, 5, 22, 39, 36, 53, 6, 23, 20, 37, 54, 7, 8, 25, 42, 59, 56, 9, 26, 43, 40, 57, 10, 27, 24, 41, 58, 11, 12, 29, 46, 63, 60, 13, 30, 47, 44, 61, 14, 31, 28, 45, 62, 15]
    
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
            res.append(str(M0[t][8]) + " " + GetVariables(r,"p0",16,variable)[i])
            res.append(str(M0[t][9]) + " " + GetVariables(r,"P1",16,variable)[i])
            f.write(" + ".join(res) + " - " + str(M0[t][10]) + " c >= 0 " + "\n")

def Constraint_L(f, variable):
    Constraint_initialize_L(R_L, f, variable)
    for r in range (R_D+R_M, R_D+R_M+R_L):
        Constraint_Sbox_L(r, f, variable)

################################The differential-middle Part################################
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
    P = [0, 17, 34, 51, 48, 1, 18, 35, 32, 49, 2, 19, 16, 33, 50, 3, 4, 21, 38, 55, 52, 5, 22, 39, 36, 53, 6, 23, 20, 37, 54, 7, 8, 25, 42, 59, 56, 9, 26, 43, 40, 57, 10, 27, 24, 41, 58, 11, 12, 29, 46, 63, 60, 13, 30, 47, 44, 61, 14, 31, 28, 45, 62, 15]
    
    M0 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0], [-1, -1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, -1, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, -1, -1, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, -1, -1, 1, 0, 0, 0, 0], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, -1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, -1, 0, 0], [0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 1, 0, 0]]
    M1 = [[0, 0, -1, -1, 0, 0, -1, -1, 1, 0, 1, 0, 0], [0, 2, 0, 1, 0, 0, 0, 0, -3, -4, 3, 2, 0], [0, 0, 0, 1, 0, 0, 0, 0, 1, 2, -1, -2, 0], [-1, -1, -2, -2, 0, 0, 0, 0, 0, -1, 0, -1, -3], [0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 1, 0, 0], [-2, -1, 0, 0, 0, 0, 0, 0, 1, -1, 1, 2, 0], [0, -1, 0, 0, 0, 0, 0, 0, -1, 0, 0, -1, -2], [0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, -1], [0, 1, 0, 0, 0, 1, 0, 0, 2, 1, -2, -2, 0], [1, 0, 0, -1, 1, 0, 1, 1, -1, 0, -1, 0, -2], [1, 0, 1, 1, 1, 1, 1, 1, -1, 0, 0, 0, 0]]

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
            f.write(" + ".join(res) + " - " + str(M0[t][12]) + " c" + " >= 0 " + "\n")

    for i in range (int(size/4)):
        for t in range (len(M1)):
            res = []
            res.append(str(M1[t][0]) + " " + GetVariables(r,"X_MD0",size,variable)[4*i+3])
            res.append(str(M1[t][1]) + " " + GetVariables(r,"X_MD1",size,variable)[4*i+3])
            res.append(str(M1[t][2]) + " " + GetVariables(r,"X_MD0",size,variable)[4*i+2])
            res.append(str(M1[t][3]) + " " + GetVariables(r,"X_MD1",size,variable)[4*i+2])
            res.append(str(M1[t][4]) + " " + GetVariables(r,"X_MD0",size,variable)[4*i+1])
            res.append(str(M1[t][5]) + " " + GetVariables(r,"X_MD1",size,variable)[4*i+1])
            res.append(str(M1[t][6]) + " " + GetVariables(r,"X_MD0",size,variable)[4*i+0])
            res.append(str(M1[t][7]) + " " + GetVariables(r,"X_MD1",size,variable)[4*i+0])
            res.append(str(M1[t][8]) + " " + GetVariables(r+1,"X_MD0",size,variable)[P[4*i+1]])
            res.append(str(M1[t][9]) + " " + GetVariables(r+1,"X_MD1",size,variable)[P[4*i+1]])
            res.append(str(M1[t][10]) + " " + GetVariables(r+1,"X_MD0",size,variable)[P[4*i+0]])
            res.append(str(M1[t][11]) + " " + GetVariables(r+1,"X_MD1",size,variable)[P[4*i+0]])
            f.write(" + ".join(res) + " - " + str(M1[t][12]) + " c" + " >= 0 " + "\n")

def Constraint_M_D(f, variable):
    Constraint_initialize_M_D(R_M, f, variable)
    for r in range (R_D, R_D+R_M):
        Constraint_Sbox_M_D(r, f, variable)

################################The middle-linear Part################################
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
    P = [0, 17, 34, 51, 48, 1, 18, 35, 32, 49, 2, 19, 16, 33, 50, 3, 4, 21, 38, 55, 52, 5, 22, 39, 36, 53, 6, 23, 20, 37, 54, 7, 8, 25, 42, 59, 56, 9, 26, 43, 40, 57, 10, 27, 24, 41, 58, 11, 12, 29, 46, 63, 60, 13, 30, 47, 44, 61, 14, 31, 28, 45, 62, 15]
    
    M0 = [[-1, -1, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0], [0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, -1, -2, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, -1, -1, 0, -1, 1, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, -1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 1, 0, 0], [0, 0, -1, -1, 0, 0, 0, 0, 0, -1, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, -1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, -1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, -1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 1, 0, 0, 0, 0], [-1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, -1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, -1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, -1], [0, 0, 0, 0, 0, 0, -1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, -1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1, 0, 0]]

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
            res.append("3 " + GetVariables(r,"p0",16,variable)[i])
            res.append("2 " + GetVariables(r,"P1",16,variable)[i])
            res.append("1.415 " + GetVariables(r,"P2",16,variable)[i])

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
            res.append("4 " + GetVariables(r,"p0",16,variable)[i])
            res.append("2 " + GetVariables(r,"P1",16,variable)[i])
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

        for j in range ((48*R_D+64*R_M+64+32*R_L)+1, (48*R_D+64*R_M+64+32*R_L)+1+64):
            if (abs(Solution[j]) < 0.1):
                X = X + (0 << (j-((48*R_D+64*R_M+64+32*R_L)+1)))
            else:
                X = X + (1 << (j-((48*R_D+64*R_M+64+32*R_L)+1)))

    #     Solutions_0x.append([X,Y,Solution[32*R_D+64*R_M+64+32*R_L]])
    # for i in range (len(Solutions_0x)):
        f.write("[" + str(hex(INPUT_DIFFER[0])) + ", " + str(hex(X)) + ", " + str(Solution[48*R_D+64*R_M+64+32*R_L])+ "],\n")

if __name__ == "__main__":
    ANSWER = [[0x1, 0x8000888008088088],
[0x2, 0x4],
[0x1000000000002, 0x400000],
[0x4, 0x800],
[0x4000000000008, 0x8000],
[0x10, 0x8880080880908008],
[0x100, 0x808880008888],
[0x1000, 0x8080800088800800],
[0x20001000, 0x4000000],
[0x8000000000001000, 0x100400000000],
[0x2000, 0x80000000000],
[0x40002000, 0x800000],
[0x4000, 0x4000],
[0x8000, 0x10000],
[0x10000, 0x880088880800888],
[0x20000, 0x800000000000000],
[0x100000, 0x880008088880a00],
[0x200000, 0x800],
[0x8000400000, 0x4040000000],
[0x1000000, 0x80888808008888],
[0x800000002000000, 0x20000000000],
[0x80004000000, 0x1000000000000000],
[0x100000004000000, 0x1000000000000000],
[0x8000000, 0x800000000000],
[0x10000000, 0x8888088008080000],
[0x20000000, 0xa00000000000000],
[0x40000000, 0x8000000],
[0x80000000, 0x10000],
[0x100000000, 0x80088000008880],
[0x200000000, 0x8000000000000],
[0x400000000, 0x8000000000000],
[0x8000400000000, 0x400],
[0x800000000, 0x2000000000000000],
[0x1000000000, 0x8088000888800088],
[0x2000000000, 0x8],
[0x8000000000, 0x800000000000000],
[0x10000000000, 0x800808800800088],
[0x20000000000, 0x800000],
[0x100000000000, 0x8880008888880008],
[0x200000000000, 0x8000000000],
[0x400000000000, 0x80000],
[0x800000000000, 0x800000000000000],
[0x1000000000000, 0x8088888800800880],
[0x2000000000000, 0x8000000000000],
[0x10000000000000, 0xc008888008880008],
[0x20000000000000, 0x8000],
[0x100000000000000, 0x8000080800088008],
[0x200000000000000, 0x8000000],
[0x1000000000000000, 0x880000800888080],
[0x4000000000000000, 0x200000000]]
    cor_min = 64
    cor_index = []
    for ans in range (len(ANSWER)):
        for WEIGHT in range (1, 21):
            INPUT_DIFFER = [ANSWER[ans][0]]
            OUTPUT_MASK = [ANSWER[ans][1]]
            R_D = 3
            R_M = 7
            R_L = 2
            size = 64
            variable = set()
            lpFileName = "gift64_dl.lp"
            solFileName = "gift64_dl_%d_%d_%d.sol" % (R_D, R_M, R_L)
            lpFileName_result = "gift64_dl_%d_%d_%d.txt" % (R_D, R_M, R_L)
            CreateModel(lpFileName, variable)
            SolveModel(lpFileName, solFileName, lpFileName_result)
