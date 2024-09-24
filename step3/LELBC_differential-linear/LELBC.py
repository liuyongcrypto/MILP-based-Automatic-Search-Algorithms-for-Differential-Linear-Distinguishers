from gurobipy import *

def GetVariables(round,varName,varSize,variable):
    res = []
    for i in range(varSize):
        res.append(varName + "_" + str(round) + "_" + str(i))
        variable.add(varName + "_" + str(round) + "_" + str(i))
    return res

##################################################The Differential Part##################################################
def Constraint_initialize_D(R_D, f, variable):

    res = []
    for r in range (R_D):
        for i in range (int(STATE_LENGTH/4)):
            res.append("2 " + GetVariables(r,"p0_D",int(STATE_LENGTH/4),variable)[i])
            res.append(GetVariables(r,"q0_D",int(STATE_LENGTH/4),variable)[i])
            res.append("2 " + GetVariables(r,"p1_D",int(STATE_LENGTH/4),variable)[i])
            res.append(GetVariables(r,"q1_D",int(STATE_LENGTH/4),variable)[i])

    for r in range (R_D+R_M, R_D+R_M+R_L):
        for i in range (int(STATE_LENGTH/4)):
            res.append("4 " + GetVariables(r,"p0_L",int(STATE_LENGTH/4),variable)[i])
            res.append("2 " + GetVariables(r,"q0_L",int(STATE_LENGTH/4),variable)[i])
            res.append("4 " + GetVariables(r,"p1_L",int(STATE_LENGTH/4),variable)[i])
            res.append("2 " + GetVariables(r,"q1_L",int(STATE_LENGTH/4),variable)[i])
    f.write(" + ".join(res) + " - OBJ = 0 " + "\n")

    for i in range (STATE_LENGTH):
        f.write(GetVariables(R_D+R_M,"X",STATE_LENGTH,variable)[i] + " >= 0 \n")
    for i in range (STATE_LENGTH):
        f.write(GetVariables(R_D+R_M,"Y",STATE_LENGTH,variable)[i] + " >= 0 \n")

    f.write("c" + " = 1 " + "\n")
    res = []
    for i in range (STATE_LENGTH):
        res.append(GetVariables(0,"X",STATE_LENGTH,variable)[i])
        res.append(GetVariables(0,"Y",STATE_LENGTH,variable)[i])
    f.write(" + ".join(res) + " >= 1 " + "\n")

    for i in range (STATE_LENGTH):
        f.write(GetVariables(R_D,"X",STATE_LENGTH,variable)[i] + " - " + str((INPUT_DIFFER[0]>>i)&0x1) + " c = 0 " + "\n")
        f.write(GetVariables(R_D,"Y",STATE_LENGTH,variable)[i] + " - " + str((INPUT_DIFFER[1]>>i)&0x1) + " c = 0 " + "\n")
    for i in range (STATE_LENGTH):
        if (((OUTPUT_MASK[0]>>i)&0x1) == 0):
            f.write(GetVariables(R_D+R_M,"X",STATE_LENGTH,variable)[i] + " - " + str((OUTPUT_MASK[0]>>i)&0x1) + " c = 0 " + "\n")
        if (((OUTPUT_MASK[1]>>i)&0x1) == 0):
            f.write(GetVariables(R_D+R_M,"Y",STATE_LENGTH,variable)[i] + " - " + str((OUTPUT_MASK[1]>>i)&0x1) + " c = 0 " + "\n")

def Constraint_MDD_D(r, f, variable):
    M0 = [[-1, -1, -1, -1, 1, -1, 0, -1, 5, -1, 0],
        [6, 1, 2, 1, 0, -2, 0, -2, -2, 5, 0],
        [0, -2, 0, -2, 6, 1, 2, 1, -2, 5, 0],
        [-2, 1, 0, 1, -2, 1, 0, 1, 4, -3, 0], 
        [1, 2, 5, 2, -3, -1, -2, -1, 1, 3, 0],
        [-3, -1, -2, -1, 1, 2, 5, 2, 1, 3, 0],
        [2, 5, 2, 5, -2, -1, 0, -1, 0, -1, 0],
        [2, -2, -1, -2, -1, 1, -1, 1, 6, -2, 0],
        [2, 1, 2, 1, 1, -2, -3, -2, 4, -1, 0],
        [1, -1, -2, -1, 5, 2, 4, 2, -3, 3, 0], 
        [-3, 3, -3, 1, 1, -2, -1, 1, 7, -1, 0], 
        [-3, -5, 1, 1, 3, 2, 0, 3, 3, 2, 0], 
        [-2, 3, -5, -3, -3, 3, 1, -1, 9, 2, 0], 
        [1, -2, 3, -2, -1, -1, 0, -3, 5, 2, 0], 
        [0, -2, -4, 4, -2, -2, 1, 1, 6, 3, 0], 
        [-2, 0, -2, 2, 1, 1, 0, -1, 4, -1, 0], 
        [-1, 1, 0, 1, -2, 2, -2, 2, 5, -4, 0], 
        [2, -1, 5, -2, -2, -5, -1, 0, 6, 3, 0], 
        [-2, 2, 2, -2, 1, 1, 0, -1, 4, -1, 0], 
        [1, -1, 0, -1, -1, -1, -1, -1, 5, -1, 0], 
        [0, 0, 0, 1, -1, 1, -1, 0, 2, -1, 0], 
        [-1, -3, 0, 0, 1, -1, 3, -2, 4, 2, 0], 
        [-1, -1, -2, 1, -1, -1, 0, 1, 4, 1, 0], 
        [-2, 2, 0, 3, -5, -1, 1, 3, 6, -3, 0], 
        [0, 2, 0, 1, -2, -1, -1, 1, 3, -1, 0],
        [1, 1, 0, -1, -2, 2, 2, -2, 4, -1, 0]]

    for i in range (int(STATE_LENGTH/4)):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(r,"X",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][1]) + " " + GetVariables(r,"X",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][2]) + " " + GetVariables(r,"X",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][3]) + " " + GetVariables(r,"X",STATE_LENGTH,variable)[4*i+0])
            res.append(str(M0[t][4]) + " " + GetVariables(r,"B_D",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][5]) + " " + GetVariables(r,"B_D",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][6]) + " " + GetVariables(r,"B_D",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][7]) + " " + GetVariables(r,"B_D",STATE_LENGTH,variable)[4*i+0])
            res.append(str(M0[t][8]) + " " + GetVariables(r,"p0_D",int(STATE_LENGTH/4),variable)[i])
            res.append(str(M0[t][9]) + " " + GetVariables(r,"q0_D",int(STATE_LENGTH/4),variable)[i])
            f.write(" + ".join(res) + " - " + str(M0[t][10]) + " " + "c" + " >= 0 " + "\n")
    
    for i in range (int(STATE_LENGTH/4)):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(r,"A_D",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][1]) + " " + GetVariables(r,"A_D",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][2]) + " " + GetVariables(r,"A_D",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][3]) + " " + GetVariables(r,"A_D",STATE_LENGTH,variable)[4*i+0])
            res.append(str(M0[t][4]) + " " + GetVariables(r+1,"Y",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][5]) + " " + GetVariables(r+1,"Y",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][6]) + " " + GetVariables(r+1,"Y",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][7]) + " " + GetVariables(r+1,"Y",STATE_LENGTH,variable)[4*i+0])
            res.append(str(M0[t][8]) + " " + GetVariables(r,"p1_D",int(STATE_LENGTH/4),variable)[i])
            res.append(str(M0[t][9]) + " " + GetVariables(r,"q1_D",int(STATE_LENGTH/4),variable)[i])
            f.write(" + ".join(res) + " - " + str(M0[t][10]) + " " + "c" + " >= 0 " + "\n")

def Constraint_XOR_D(r, f, variable):
    for i in range (STATE_LENGTH):
        f.write(GetVariables(r,"X",STATE_LENGTH,variable)[(i-5)%STATE_LENGTH] + " + " + GetVariables(r,"Y",STATE_LENGTH,variable)[i] + " - " + GetVariables(r,"A_D",STATE_LENGTH,variable)[i] + " >= 0 " + "\n")
        f.write(GetVariables(r,"X",STATE_LENGTH,variable)[(i-5)%STATE_LENGTH] + " - " + GetVariables(r,"Y",STATE_LENGTH,variable)[i] + " + " + GetVariables(r,"A_D",STATE_LENGTH,variable)[i] + " >= 0 " + "\n")
        f.write(" - " + GetVariables(r,"X",STATE_LENGTH,variable)[(i-5)%STATE_LENGTH] + " + " + GetVariables(r,"Y",STATE_LENGTH,variable)[i] + " + " + GetVariables(r,"A_D",STATE_LENGTH,variable)[i] + " >= 0 " + "\n")
        f.write(GetVariables(r,"X",STATE_LENGTH,variable)[(i-5)%STATE_LENGTH] + " + " + GetVariables(r,"Y",STATE_LENGTH,variable)[i] + " + " + GetVariables(r,"A_D",STATE_LENGTH,variable)[i] + " <= 2 " + "\n")

    for i in range (STATE_LENGTH):
        f.write(GetVariables(r+1,"Y",STATE_LENGTH,variable)[(i-5)%STATE_LENGTH] + " + " + GetVariables(r,"B_D",STATE_LENGTH,variable)[i] + " - " + GetVariables(r+1,"X",STATE_LENGTH,variable)[i] + " >= 0 " + "\n")
        f.write(GetVariables(r+1,"Y",STATE_LENGTH,variable)[(i-5)%STATE_LENGTH] + " - " + GetVariables(r,"B_D",STATE_LENGTH,variable)[i] + " + " + GetVariables(r+1,"X",STATE_LENGTH,variable)[i] + " >= 0 " + "\n")
        f.write(" - " + GetVariables(r+1,"Y",STATE_LENGTH,variable)[(i-5)%STATE_LENGTH] + " + " + GetVariables(r,"B_D",STATE_LENGTH,variable)[i] + " + " + GetVariables(r+1,"X",STATE_LENGTH,variable)[i] + " >= 0 " + "\n")
        f.write(GetVariables(r+1,"Y",STATE_LENGTH,variable)[(i-5)%STATE_LENGTH] + " + " + GetVariables(r,"B_D",STATE_LENGTH,variable)[i] + " + " + GetVariables(r+1,"X",STATE_LENGTH,variable)[i] + " <= 2 " + "\n")

def Constraint_D(f, variable):
    Constraint_initialize_D(R_D, f, variable)
    for r in range (0, R_D):
        Constraint_MDD_D(r, f, variable)
        Constraint_XOR_D(r, f, variable)   


##################################################The middle-Differential Part (probability)##################################################
def Constraint_initialize_M_PD(R_M, f, variable):
    res = []
    for i in range (STATE_LENGTH):
        res.append(GetVariables(R_D,"X_MD0",STATE_LENGTH,variable)[i])
        res.append(GetVariables(R_D,"Y_MD0",STATE_LENGTH,variable)[i])
    f.write(" + ".join(res) + " = 0 " + "\n")

    for i in range (STATE_LENGTH):
        f.write(GetVariables(R_D,"X",STATE_LENGTH,variable)[i] + " - " + GetVariables(R_D,"X_MD1",STATE_LENGTH,variable)[i] + " = 0 " + "\n")
        f.write(GetVariables(R_D,"Y",STATE_LENGTH,variable)[i] + " - " + GetVariables(R_D,"Y_MD1",STATE_LENGTH,variable)[i] + " = 0 " + "\n")

def Constraint_MDD_M_PD(r, f, variable):
    M0 = [[-1, -1, -1, -1, 2, 3, 2, 3, 0], [2, 3, 2, 3, -1, -1, -1, -1, 0], [-3, 1, -1, 1, -1, 1, 3, 1, -2], [1, -2, 1, -2, -1, -1, 0, -1, -5], [0, -1, -1, -1, 1, 0, 0, 0, -2], [-2, -2, 1, 2, -1, 1, -2, 2, -4], [-2, 2, 1, -2, -1, 2, -2, 1, -4], [-1, -1, 0, -1, 1, -2, 1, -2, -5], [1, 0, 0, 0, 0, -1, -1, -1, -2], [1, 2, 0, 3, -3, -3, 1, 1, -3], [3, 2, 3, 2, 1, -1, -2, -1, 0], [-2, 1, -2, 2, 1, 1, -1, -2, -5], [1, 2, -1, -1, -1, 2, 2, -2, -3], [-2, 2, -3, -1, 2, -1, 1, 2, -4], [1, 1, 0, -1, -1, 0, -1, 1, -2], [1, -1, 0, 1, -1, 1, -1, 0, -2], [0, -1, -1, 0, 1, 1, 1, 0, -1], [1, -2, -1, -2, 1, 1, 0, 1, -3], [1, -1, -1, 0, 1, 0, 1, 1, -1], [-1, 1, 1, -1, 1, 0, 1, -1, -2], [-1, -1, 1, 1, 1, -1, 1, 0, -2], [-1, 1, 0, 0, -1, 0, 1, 1, -1], [-1, 0, 0, 1, -1, 1, 1, 0, -1], [1, 1, 0, 1, 1, 1, -1, 1, 0], [1, 1, 0, 1, 0, -1, 0, -1, -1]]
    
    for i in range (int(STATE_LENGTH/4)):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(r,"X_MD1",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][1]) + " " + GetVariables(r,"X_MD1",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][2]) + " " + GetVariables(r,"X_MD1",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][3]) + " " + GetVariables(r,"X_MD1",STATE_LENGTH,variable)[4*i+0])
            res.append(str(M0[t][4]) + " " + GetVariables(r,"B_MD1",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][5]) + " " + GetVariables(r,"B_MD1",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][6]) + " " + GetVariables(r,"B_MD1",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][7]) + " " + GetVariables(r,"B_MD1",STATE_LENGTH,variable)[4*i+0])
            f.write(" + ".join(res) + " - " + str(M0[t][8]) + " c" + " >= 0 " + "\n")

    for i in range (int(STATE_LENGTH/4)):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(r,"A_MD1",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][1]) + " " + GetVariables(r,"A_MD1",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][2]) + " " + GetVariables(r,"A_MD1",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][3]) + " " + GetVariables(r,"A_MD1",STATE_LENGTH,variable)[4*i+0])
            res.append(str(M0[t][4]) + " " + GetVariables(r+1,"Y_MD1",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][5]) + " " + GetVariables(r+1,"Y_MD1",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][6]) + " " + GetVariables(r+1,"Y_MD1",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][7]) + " " + GetVariables(r+1,"Y_MD1",STATE_LENGTH,variable)[4*i+0])
            f.write(" + ".join(res) + " - " + str(M0[t][8]) + " c" + " >= 0 " + "\n")

    res = []
    for i in range (STATE_LENGTH):
        res.append(GetVariables(r,"X_MD0",STATE_LENGTH,variable)[i])
        res.append(GetVariables(r,"Y_MD0",STATE_LENGTH,variable)[i])
        res.append(GetVariables(r,"A_MD0",STATE_LENGTH,variable)[i])
        res.append(GetVariables(r,"B_MD0",STATE_LENGTH,variable)[i])
        res.append(GetVariables(r+1,"X_MD0",STATE_LENGTH,variable)[i])
        res.append(GetVariables(r+1,"Y_MD0",STATE_LENGTH,variable)[i])
    f.write(" + ".join(res) + " = 0 " + "\n")

def Constraint_XOR_M_PD(r, f, variable):

    for i in range (STATE_LENGTH):
        f.write(GetVariables(r,"X_MD1",STATE_LENGTH,variable)[(i-5)%STATE_LENGTH] + " + " + GetVariables(r,"Y_MD1",STATE_LENGTH,variable)[i] + " - " + GetVariables(r,"A_MD1",STATE_LENGTH,variable)[i] + " >= 0 " + "\n")
        f.write(GetVariables(r,"X_MD1",STATE_LENGTH,variable)[(i-5)%STATE_LENGTH] + " - " + GetVariables(r,"Y_MD1",STATE_LENGTH,variable)[i] + " + " + GetVariables(r,"A_MD1",STATE_LENGTH,variable)[i] + " >= 0 " + "\n")
        f.write(" - " + GetVariables(r,"X_MD1",STATE_LENGTH,variable)[(i-5)%STATE_LENGTH] + " + " + GetVariables(r,"Y_MD1",STATE_LENGTH,variable)[i] + " + " + GetVariables(r,"A_MD1",STATE_LENGTH,variable)[i] + " >= 0 " + "\n")
        f.write(GetVariables(r,"X_MD1",STATE_LENGTH,variable)[(i-5)%STATE_LENGTH] + " + " + GetVariables(r,"Y_MD1",STATE_LENGTH,variable)[i] + " + " + GetVariables(r,"A_MD1",STATE_LENGTH,variable)[i] + " <= 2 " + "\n")

    for i in range (STATE_LENGTH):
        f.write(GetVariables(r+1,"Y_MD1",STATE_LENGTH,variable)[(i-5)%STATE_LENGTH] + " + " + GetVariables(r,"B_MD1",STATE_LENGTH,variable)[i] + " - " + GetVariables(r+1,"X_MD1",STATE_LENGTH,variable)[i] + " >= 0 " + "\n")
        f.write(GetVariables(r+1,"Y_MD1",STATE_LENGTH,variable)[(i-5)%STATE_LENGTH] + " - " + GetVariables(r,"B_MD1",STATE_LENGTH,variable)[i] + " + " + GetVariables(r+1,"X_MD1",STATE_LENGTH,variable)[i] + " >= 0 " + "\n")
        f.write(" - " + GetVariables(r+1,"Y_MD1",STATE_LENGTH,variable)[(i-5)%STATE_LENGTH] + " + " + GetVariables(r,"B_MD1",STATE_LENGTH,variable)[i] + " + " + GetVariables(r+1,"X_MD1",STATE_LENGTH,variable)[i] + " >= 0 " + "\n")
        f.write(GetVariables(r+1,"Y_MD1",STATE_LENGTH,variable)[(i-5)%STATE_LENGTH] + " + " + GetVariables(r,"B_MD1",STATE_LENGTH,variable)[i] + " + " + GetVariables(r+1,"X_MD1",STATE_LENGTH,variable)[i] + " <= 2 " + "\n")

def Constraint_M_PD(f, variable):
    Constraint_initialize_M_PD(R_M, f, variable)
    for r in range (R_D, R_D + R_M_PD):
        Constraint_MDD_M_PD(r, f, variable)
        Constraint_XOR_M_PD(r, f, variable)

##################################################The middle-Differential Part (deterministic)##################################################
def Constraint_initialize_M_D(R_M, f, variable):
    # f.write("c" + " = 1 " + "\n")
    res = []
    for i in range (STATE_LENGTH):
        f.write(GetVariables(R_D,"X_MD0",STATE_LENGTH,variable)[i] + " = 0 " + "\n")
        f.write(GetVariables(R_D,"Y_MD0",STATE_LENGTH,variable)[i] + " = 0 " + "\n")
        f.write(GetVariables(R_D,"X",STATE_LENGTH,variable)[i] + " - " + GetVariables(R_D,"X_MD1",STATE_LENGTH,variable)[i] + " = 0 " + "\n")
        f.write(GetVariables(R_D,"Y",STATE_LENGTH,variable)[i] + " - " + GetVariables(R_D,"Y_MD1",STATE_LENGTH,variable)[i] + " = 0 " + "\n")

def Constraint_MDD_M_D(r, f, variable):
    M0 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 1, 0, 0, 0, 0], [0, 0, -1, -1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, -1, 0, 0, 0, 0], [0, 0, 0, 0, -1, -1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, -1, -1, 1, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, -1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 1, 0, 0], [-1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, -1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 1, 1, 0, -1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0], [1, 0, 1, 1, 1, 1, 1, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, -1, 0, -1, 0, -1, 0, 1, 0, 0, 0, 0, 0, 0, -2], [0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [-1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, -1, 0, 0]]

    for i in range (int(STATE_LENGTH/4)):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(r,"X_MD0",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][1]) + " " + GetVariables(r,"X_MD1",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][2]) + " " + GetVariables(r,"X_MD0",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][3]) + " " + GetVariables(r,"X_MD1",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][4]) + " " + GetVariables(r,"X_MD0",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][5]) + " " + GetVariables(r,"X_MD1",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][6]) + " " + GetVariables(r,"X_MD0",STATE_LENGTH,variable)[4*i+0])
            res.append(str(M0[t][7]) + " " + GetVariables(r,"X_MD1",STATE_LENGTH,variable)[4*i+0])
            res.append(str(M0[t][8]) + " " + GetVariables(r,"B_MD0",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][9]) + " " + GetVariables(r,"B_MD1",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][10]) + " " + GetVariables(r,"B_MD0",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][11]) + " " + GetVariables(r,"B_MD1",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][12]) + " " + GetVariables(r,"B_MD0",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][13]) + " " + GetVariables(r,"B_MD1",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][14]) + " " + GetVariables(r,"B_MD0",STATE_LENGTH,variable)[4*i+0])
            res.append(str(M0[t][15]) + " " + GetVariables(r,"B_MD1",STATE_LENGTH,variable)[4*i+0])
            f.write(" + ".join(res) + " - " + str(M0[t][16]) + " c" + " >= 0 " + "\n")

    for i in range (int(STATE_LENGTH/4)):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(r,"A_MD0",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][1]) + " " + GetVariables(r,"A_MD1",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][2]) + " " + GetVariables(r,"A_MD0",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][3]) + " " + GetVariables(r,"A_MD1",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][4]) + " " + GetVariables(r,"A_MD0",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][5]) + " " + GetVariables(r,"A_MD1",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][6]) + " " + GetVariables(r,"A_MD0",STATE_LENGTH,variable)[4*i+0])
            res.append(str(M0[t][7]) + " " + GetVariables(r,"A_MD1",STATE_LENGTH,variable)[4*i+0])
            res.append(str(M0[t][8]) + " " + GetVariables(r+1,"Y_MD0",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][9]) + " " + GetVariables(r+1,"Y_MD1",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][10]) + " " + GetVariables(r+1,"Y_MD0",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][11]) + " " + GetVariables(r+1,"Y_MD1",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][12]) + " " + GetVariables(r+1,"Y_MD0",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][13]) + " " + GetVariables(r+1,"Y_MD1",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][14]) + " " + GetVariables(r+1,"Y_MD0",STATE_LENGTH,variable)[4*i+0])
            res.append(str(M0[t][15]) + " " + GetVariables(r+1,"Y_MD1",STATE_LENGTH,variable)[4*i+0])
            f.write(" + ".join(res) + " - " + str(M0[t][16]) + " c" + " >= 0 " + "\n")

def Constraint_XOR_M_D(r, f, variable):
    M0 = [[-1, -1, -1, -1, 0, -1, -2], 
    [1, 0, 1, 0, -1, 0, 0], 
    [-1, -1, 0, 1, 1, 1, 0], 
    [0, 1, 0, 1, 0, -1, 0], 
    [0, 1, -1, -1, 1, 1, 0]]
    
    for i in range (STATE_LENGTH):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(r,"X_MD0",STATE_LENGTH,variable)[(i-5)%STATE_LENGTH])
            res.append(str(M0[t][1]) + " " + GetVariables(r,"X_MD1",STATE_LENGTH,variable)[(i-5)%STATE_LENGTH])
            res.append(str(M0[t][2]) + " " + GetVariables(r,"Y_MD0",STATE_LENGTH,variable)[i])
            res.append(str(M0[t][3]) + " " + GetVariables(r,"Y_MD1",STATE_LENGTH,variable)[i])
            res.append(str(M0[t][4]) + " " + GetVariables(r,"A_MD0",STATE_LENGTH,variable)[i])
            res.append(str(M0[t][5]) + " " + GetVariables(r,"A_MD1",STATE_LENGTH,variable)[i])
            f.write(" + ".join(res) + " - " + str(M0[t][6]) + " c" + " >= 0 " + "\n")

    for i in range (STATE_LENGTH):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(r+1,"Y_MD0",STATE_LENGTH,variable)[(i-5)%STATE_LENGTH])
            res.append(str(M0[t][1]) + " " + GetVariables(r+1,"Y_MD1",STATE_LENGTH,variable)[(i-5)%STATE_LENGTH])
            res.append(str(M0[t][2]) + " " + GetVariables(r,"B_MD0",STATE_LENGTH,variable)[i])
            res.append(str(M0[t][3]) + " " + GetVariables(r,"B_MD1",STATE_LENGTH,variable)[i])
            res.append(str(M0[t][4]) + " " + GetVariables(r+1,"X_MD0",STATE_LENGTH,variable)[i])
            res.append(str(M0[t][5]) + " " + GetVariables(r+1,"X_MD1",STATE_LENGTH,variable)[i])
            f.write(" + ".join(res) + " - " + str(M0[t][6]) + " c" + " >= 0 " + "\n")

def Constraint_M_D(f, variable):
    # Constraint_initialize_M_D(R_M, f, variable)
    for r in range (R_D+R_M_PD, R_D+R_M):
        Constraint_MDD_M_D(r, f, variable)
        Constraint_XOR_M_D(r, f, variable)

##################################################The middle-Linear Part (probability)##################################################
def Constraint_initialize_M_PL(R_M, f, variable):
    # f.write("c" + " = 1 " + "\n")
    res = []
    for i in range (STATE_LENGTH):
        res.append(GetVariables(R_D+R_M,"X_ML0",STATE_LENGTH,variable)[i])
        res.append(GetVariables(R_D+R_M,"Y_ML0",STATE_LENGTH,variable)[i])
    f.write(" + ".join(res) + " = 0 " + "\n")

    for i in range (STATE_LENGTH):
        f.write(GetVariables(R_D+R_M,"X",STATE_LENGTH,variable)[i] + " - " + GetVariables(R_D+R_M,"X_ML1",STATE_LENGTH,variable)[i] + " = 0 " + "\n")
        f.write(GetVariables(R_D+R_M,"Y",STATE_LENGTH,variable)[i] + " - " + GetVariables(R_D+R_M,"Y_ML1",STATE_LENGTH,variable)[i] + " = 0 " + "\n")

def Constraint_MDD_M_PL(r, f, variable):
    M0 = [[-1, -1, 1, -1, 1, 2, 2, 2, 0], [1, 2, 2, 2, -1, -1, 1, -1, 0], [-1, -2, 2, -2, -1, -1, 2, -1, -5], [0, -1, -1, 1, 1, 1, 2, 1, 0], [1, 1, 2, 1, 0, -1, -1, 1, 0], [0, 1, -1, -1, 1, 0, 1, 0, -1], [1, 0, 1, 0, 0, 1, -1, -1, -1], [0, -1, -1, -1, 0, 1, -1, 1, -3], [0, 1, -1, 1, 0, -1, -1, -1, -3], [-1, 1, -1, -1, 0, 1, 2, 2, -1], [0, 1, 2, 2, -1, 1, -1, -1, -1], [1, -1, 1, -1, 1, 0, -1, 0, -2], [1, 0, -1, 0, 1, -1, 1, -1, -2], [-1, -1, 2, -1, 0, -1, 1, -1, -3], [1, -1, -1, -1, -1, -1, 0, -1, -5], [-1, -1, 0, -1, 1, -1, -1, -1, -5], [-1, 1, -1, 1, 1, 1, 0, 1, -1], [1, 1, 0, 1, -1, 1, -1, 1, -1], [-1, -1, -1, 1, 0, 1, 1, 0, -2], [1, 1, -1, -1, 0, 1, 1, 0, -1], [0, 1, 1, 0, 1, 1, -1, -1, -1], [1, -1, -1, 1, 0, 0, 1, 1, -1], [0, 1, 1, 0, -1, -1, -1, 1, -2], [0, 0, 1, 1, 1, -1, -1, 1, -1], [-1, -1, 0, -1, 0, 1, 0, 1, -2], [-1, 0, 0, 0, 0, 1, 1, 1, 0], [0, -1, -1, 1, 1, 0, 1, 0, -1], [0, 1, 0, 1, -1, -1, 0, -1, -2], [1, 0, 1, 0, 0, -1, -1, 1, -1]]
    for i in range (int(STATE_LENGTH/4)):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(r+1,"X_ML1",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][1]) + " " + GetVariables(r+1,"X_ML1",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][2]) + " " + GetVariables(r+1,"X_ML1",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][3]) + " " + GetVariables(r+1,"X_ML1",STATE_LENGTH,variable)[4*i+0])
            res.append(str(M0[t][4]) + " " + GetVariables(r,"A_ML1",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][5]) + " " + GetVariables(r,"A_ML1",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][6]) + " " + GetVariables(r,"A_ML1",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][7]) + " " + GetVariables(r,"A_ML1",STATE_LENGTH,variable)[4*i+0])
            f.write(" + ".join(res) + " - " + str(M0[t][8]) + " c" + " >= 0 " + "\n")
    
    for i in range (int(STATE_LENGTH/4)):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(r,"B_ML1",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][1]) + " " + GetVariables(r,"B_ML1",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][2]) + " " + GetVariables(r,"B_ML1",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][3]) + " " + GetVariables(r,"B_ML1",STATE_LENGTH,variable)[4*i+0])
            res.append(str(M0[t][4]) + " " + GetVariables(r,"Y_ML1",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][5]) + " " + GetVariables(r,"Y_ML1",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][6]) + " " + GetVariables(r,"Y_ML1",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][7]) + " " + GetVariables(r,"Y_ML1",STATE_LENGTH,variable)[4*i+0])
            f.write(" + ".join(res) + " - " + str(M0[t][8]) + " c" + " >= 0 " + "\n")

    res = []
    for i in range (STATE_LENGTH):
        res.append(GetVariables(r,"X_ML0",STATE_LENGTH,variable)[i])
        res.append(GetVariables(r,"Y_ML0",STATE_LENGTH,variable)[i])
        res.append(GetVariables(r,"A_ML0",STATE_LENGTH,variable)[i])
        res.append(GetVariables(r,"B_ML0",STATE_LENGTH,variable)[i])
        res.append(GetVariables(r+1,"X_ML0",STATE_LENGTH,variable)[i])
        res.append(GetVariables(r+1,"Y_ML0",STATE_LENGTH,variable)[i])
    f.write(" + ".join(res) + " = 0 " + "\n")

def Constraint_THREE_M_PL(r, f, variable):
    for i in range (STATE_LENGTH):
        f.write(GetVariables(r,"A_ML1",STATE_LENGTH,variable)[i] + " + " + GetVariables(r,"Y_ML1",STATE_LENGTH,variable)[(i+5)%STATE_LENGTH] + " - " + GetVariables(r,"X_ML1",STATE_LENGTH,variable)[i] + " >= 0 " + "\n")
        f.write(GetVariables(r,"A_ML1",STATE_LENGTH,variable)[i] + " - " + GetVariables(r,"Y_ML1",STATE_LENGTH,variable)[(i+5)%STATE_LENGTH] + " + " + GetVariables(r,"X_ML1",STATE_LENGTH,variable)[i] + " >= 0 " + "\n")
        f.write(" - " + GetVariables(r,"A_ML1",STATE_LENGTH,variable)[i] + " + " + GetVariables(r,"Y_ML1",STATE_LENGTH,variable)[(i+5)%STATE_LENGTH] + " + " + GetVariables(r,"X_ML1",STATE_LENGTH,variable)[i] + " >= 0 " + "\n")
        f.write(GetVariables(r,"A_ML1",STATE_LENGTH,variable)[i] + " + " + GetVariables(r,"Y_ML1",STATE_LENGTH,variable)[(i+5)%STATE_LENGTH] + " + " + GetVariables(r,"X_ML1",STATE_LENGTH,variable)[i] + " <= 2 " + "\n")

    for i in range (STATE_LENGTH):
        f.write(GetVariables(r+1,"Y_ML1",STATE_LENGTH,variable)[i] + " + " + GetVariables(r+1,"X_ML1",STATE_LENGTH,variable)[(i+5)%STATE_LENGTH] + " - " + GetVariables(r,"B_ML1",STATE_LENGTH,variable)[i] + " >= 0 " + "\n")
        f.write(GetVariables(r+1,"Y_ML1",STATE_LENGTH,variable)[i] + " - " + GetVariables(r+1,"X_ML1",STATE_LENGTH,variable)[(i+5)%STATE_LENGTH] + " + " + GetVariables(r,"B_ML1",STATE_LENGTH,variable)[i] + " >= 0 " + "\n")
        f.write(" - " + GetVariables(r+1,"Y_ML1",STATE_LENGTH,variable)[i] + " + " + GetVariables(r+1,"X_ML1",STATE_LENGTH,variable)[(i+5)%STATE_LENGTH] + " + " + GetVariables(r,"B_ML1",STATE_LENGTH,variable)[i] + " >= 0 " + "\n")
        f.write(GetVariables(r+1,"Y_ML1",STATE_LENGTH,variable)[i] + " + " + GetVariables(r+1,"X_ML1",STATE_LENGTH,variable)[(i+5)%STATE_LENGTH] + " + " + GetVariables(r,"B_ML1",STATE_LENGTH,variable)[i] + " <= 2 " + "\n")

def Constraint_M_PL(f, variable):
    Constraint_initialize_M_PL(R_M, f, variable)
    for r in range (R_D + R_M_L, R_D + R_M):
        Constraint_MDD_M_PL(r, f, variable)
        Constraint_THREE_M_PL(r, f, variable)


##################################################The middle-Linear Part (deterministic)##################################################
def Constraint_initialize_M_L(R_M, f, variable):
    # f.write("c" + " = 1 " + "\n")
    res = []
    for i in range (STATE_LENGTH):
        f.write(GetVariables(R_D+R_M,"X_ML0",STATE_LENGTH,variable)[i] + " = 0 " + "\n")
        f.write(GetVariables(R_D+R_M,"Y_ML0",STATE_LENGTH,variable)[i] + " = 0 " + "\n")
        f.write(GetVariables(R_D+R_M,"X",STATE_LENGTH,variable)[i] + " - " + GetVariables(R_D+R_M,"X_ML1",STATE_LENGTH,variable)[i] + " = 0 " + "\n")
        f.write(GetVariables(R_D+R_M,"Y",STATE_LENGTH,variable)[i] + " - " + GetVariables(R_D+R_M,"Y_ML1",STATE_LENGTH,variable)[i] + " = 0 " + "\n")

def Constraint_MDD_M_L(r, f, variable):
    M0 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0], [-1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, -1, -1, 0, 0, 1, 0, 0, 0, 1, 0, -1, 0, 0], [0, 0, -1, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, -1, 0, 0], [0, 0, 0, 0, 0, 0, -1, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, -1], [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, -2, 0, 0], [0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 1, 0, 0], [1, 0, 1, 1, 1, 1, 1, 1, -1, 0, 0, 0, 1, 0, -1, 0, 0], [0, -1, 0, -1, 1, 1, 0, -1, 0, 0, 0, 0, 0, 1, 0, 0, -2], [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, -1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, -1, 0, 0, 0]]

    for i in range (int(STATE_LENGTH/4)):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(r+1,"X_ML0",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][1]) + " " + GetVariables(r+1,"X_ML1",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][2]) + " " + GetVariables(r+1,"X_ML0",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][3]) + " " + GetVariables(r+1,"X_ML1",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][4]) + " " + GetVariables(r+1,"X_ML0",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][5]) + " " + GetVariables(r+1,"X_ML1",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][6]) + " " + GetVariables(r+1,"X_ML0",STATE_LENGTH,variable)[4*i+0])
            res.append(str(M0[t][7]) + " " + GetVariables(r+1,"X_ML1",STATE_LENGTH,variable)[4*i+0])
            res.append(str(M0[t][8]) + " " + GetVariables(r,"A_ML0",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][9]) + " " + GetVariables(r,"A_ML1",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][10]) + " " + GetVariables(r,"A_ML0",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][11]) + " " + GetVariables(r,"A_ML1",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][12]) + " " + GetVariables(r,"A_ML0",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][13]) + " " + GetVariables(r,"A_ML1",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][14]) + " " + GetVariables(r,"A_ML0",STATE_LENGTH,variable)[4*i+0])
            res.append(str(M0[t][15]) + " " + GetVariables(r,"A_ML1",STATE_LENGTH,variable)[4*i+0])
            f.write(" + ".join(res) + " - " + str(M0[t][16]) + " c" + " >= 0 " + "\n")
    
    for i in range (int(STATE_LENGTH/4)):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(r,"B_ML0",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][1]) + " " + GetVariables(r,"B_ML1",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][2]) + " " + GetVariables(r,"B_ML0",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][3]) + " " + GetVariables(r,"B_ML1",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][4]) + " " + GetVariables(r,"B_ML0",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][5]) + " " + GetVariables(r,"B_ML1",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][6]) + " " + GetVariables(r,"B_ML0",STATE_LENGTH,variable)[4*i+0])
            res.append(str(M0[t][7]) + " " + GetVariables(r,"B_ML1",STATE_LENGTH,variable)[4*i+0])
            res.append(str(M0[t][8]) + " " + GetVariables(r,"Y_ML0",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][9]) + " " + GetVariables(r,"Y_ML1",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][10]) + " " + GetVariables(r,"Y_ML0",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][11]) + " " + GetVariables(r,"Y_ML1",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][12]) + " " + GetVariables(r,"Y_ML0",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][13]) + " " + GetVariables(r,"Y_ML1",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][14]) + " " + GetVariables(r,"Y_ML0",STATE_LENGTH,variable)[4*i+0])
            res.append(str(M0[t][15]) + " " + GetVariables(r,"Y_ML1",STATE_LENGTH,variable)[4*i+0])
            f.write(" + ".join(res) + " - " + str(M0[t][16]) + " c" + " >= 0 " + "\n")

def Constraint_THREE_M_L(r, f, variable):
    M0 = [[0, -1, -1, -1, -1, -1, -2], [-1, 0, 1, 0, 1, 0, 0], [1, 1, -1, -1, 0, 1, 0], [0, -1, 0, 1, 0, 1, 0], [1, 1, 0, 1, -1, -1, 0]]

    # [0, 0, 0, 0, 0, 0]
    # [0, 1, 0, 0, 0, 1]
    # [1, 0, 0, 0, 1, 0]
    # [0, 1, 0, 1, 0, 0]
    # [0, 0, 0, 1, 0, 1]
    # [1, 0, 0, 1, 1, 0]
    # [1, 0, 1, 0, 0, 0]
    # [1, 0, 1, 0, 0, 1]
    # [1, 0, 1, 0, 1, 0]
    
    for i in range (STATE_LENGTH):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(r,"X_ML0",STATE_LENGTH,variable)[i])
            res.append(str(M0[t][1]) + " " + GetVariables(r,"X_ML1",STATE_LENGTH,variable)[i])
            res.append(str(M0[t][2]) + " " + GetVariables(r,"A_ML0",STATE_LENGTH,variable)[i])
            res.append(str(M0[t][3]) + " " + GetVariables(r,"A_ML1",STATE_LENGTH,variable)[i])
            res.append(str(M0[t][4]) + " " + GetVariables(r,"Y_ML0",STATE_LENGTH,variable)[(i+5)%STATE_LENGTH])
            res.append(str(M0[t][5]) + " " + GetVariables(r,"Y_ML1",STATE_LENGTH,variable)[(i+5)%STATE_LENGTH])

            f.write(" + ".join(res) + " - " + str(M0[t][6]) + " c" + " >= 0 " + "\n")


    for i in range (STATE_LENGTH):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(r,"B_ML0",STATE_LENGTH,variable)[i])
            res.append(str(M0[t][1]) + " " + GetVariables(r,"B_ML1",STATE_LENGTH,variable)[i])
            res.append(str(M0[t][2]) + " " + GetVariables(r+1,"Y_ML0",STATE_LENGTH,variable)[i])
            res.append(str(M0[t][3]) + " " + GetVariables(r+1,"Y_ML1",STATE_LENGTH,variable)[i])
            res.append(str(M0[t][4]) + " " + GetVariables(r+1,"X_ML0",STATE_LENGTH,variable)[(i+5)%STATE_LENGTH])
            res.append(str(M0[t][5]) + " " + GetVariables(r+1,"X_ML1",STATE_LENGTH,variable)[(i+5)%STATE_LENGTH])

            f.write(" + ".join(res) + " - " + str(M0[t][6]) + " c" + " >= 0 " + "\n")

def Constraint_M_L(f, variable):
    # Constraint_initialize_M_L(R_M, f, variable)
    for r in range (R_D, R_D+R_M_L):
        Constraint_MDD_M_L(r, f, variable)
        Constraint_THREE_M_L(r, f, variable)

##################################################The Linear Part##################################################
def Constraint_initialize_L(R_L, f, variable):
    # f.write("c" + " = 1 " + "\n")
    res = []
    for i in range (STATE_LENGTH):
        res.append(GetVariables(R_D+R_M,"X",STATE_LENGTH,variable)[i])
        res.append(GetVariables(R_D+R_M,"Y",STATE_LENGTH,variable)[i])
    f.write(" + ".join(res) + " >= 1 " + "\n")

def Constraint_MDD_L(r, f, variable):
    M0 = [[1, -2, -1, -2, -1, -3, 1, -3, 9, 10, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1], 
        [-3, -1, 1, -1, 0, 2, 2, 2, 2, 1, 0], 
        [7, 3, 5, 4, -1, 4, -3, -5, 4, -2, 0], 
        [2, 1, -2, 3, 1, -6, -2, 2, 10, 4, 0], 
        [-2, -3, -7, -1, 2, 5, -2, -1, 16, 9, 0], 
        [0, 2, 2, 2, -3, -1, 1, -1, 2, 1, 0], 
        [0, -1, 1, -1, 0, 0, 0, 0, 1, 2, 0], 
        [0, 1, -1, -1, 0, 1, 2, 1, 0, 1, 0], 
        [0, 1, 2, 1, 0, -1, -1, 1, 0, 1, 0], 
        [0, 0, 0, 0, 0, -1, 1, -1, 1, 2, 0], 
        [0, -1, -1, 1, 0, 1, 2, 1, 0, 1, 0], 
        [1, 3, -4, -8, 6, 3, 1, 2, 11, 3, 0], 
        [-2, -1, 3, -1, 0, -2, 1, -2, 6, 5, 0], 
        [2, 3, -2, 1, -2, -5, -6, 1, 15, 8, 0], 
        [0, 1, 2, 1, 0, 1, -1, -1, 0, 1, 0], 
        [0, 1, 0, 1, 0, 1, 0, 1, -1, 0, 0], 
        [0, -1, -2, -1, 0, 1, -2, 1, 5, 4, 0], 
        [0, 1, -2, 1, 0, -1, -2, -1, 5, 4, 0], 
        [6, -4, -3, 2, -1, -4, -3, 6, 15, 6, 0], 
        [0, -1, -1, 1, 2, 0, 1, 1, 1, 0, 0], 
        [0, -2, 1, -2, 1, -1, 0, -1, 4, 5, 0], 
        [-1, 0, -1, -1, 0, 0, 0, 1, 3, 2, 0]]

    for i in range (int(STATE_LENGTH/4)):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(r,"A_L",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][1]) + " " + GetVariables(r,"A_L",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][2]) + " " + GetVariables(r,"A_L",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][3]) + " " + GetVariables(r,"A_L",STATE_LENGTH,variable)[4*i+0])
            res.append(str(M0[t][4]) + " " + GetVariables(r+1,"X",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][5]) + " " + GetVariables(r+1,"X",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][6]) + " " + GetVariables(r+1,"X",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][7]) + " " + GetVariables(r+1,"X",STATE_LENGTH,variable)[4*i+0])
            res.append(str(M0[t][8]) + " " + GetVariables(r,"p0_L",int(STATE_LENGTH/4),variable)[i])
            res.append(str(M0[t][9]) + " " + GetVariables(r,"q0_L",int(STATE_LENGTH/4),variable)[i])
            f.write(" + ".join(res) + " - " + str(M0[t][10]) + " " + "c" + " >= 0 " + "\n")
    
    for i in range (int(STATE_LENGTH/4)):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(r,"Y",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][1]) + " " + GetVariables(r,"Y",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][2]) + " " + GetVariables(r,"Y",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][3]) + " " + GetVariables(r,"Y",STATE_LENGTH,variable)[4*i+0])
            res.append(str(M0[t][4]) + " " + GetVariables(r,"B_L",STATE_LENGTH,variable)[4*i+3])
            res.append(str(M0[t][5]) + " " + GetVariables(r,"B_L",STATE_LENGTH,variable)[4*i+2])
            res.append(str(M0[t][6]) + " " + GetVariables(r,"B_L",STATE_LENGTH,variable)[4*i+1])
            res.append(str(M0[t][7]) + " " + GetVariables(r,"B_L",STATE_LENGTH,variable)[4*i+0])
            res.append(str(M0[t][8]) + " " + GetVariables(r,"p1_L",int(STATE_LENGTH/4),variable)[i])
            res.append(str(M0[t][9]) + " " + GetVariables(r,"q1_L",int(STATE_LENGTH/4),variable)[i])
            f.write(" + ".join(res) + " - " + str(M0[t][10]) + " " + "c" + " >= 0 " + "\n")

def Constraint_THREE_L(r, f, variable):
    for i in range (STATE_LENGTH):
        f.write(GetVariables(r,"X",STATE_LENGTH,variable)[i] + " + " + GetVariables(r,"Y",STATE_LENGTH,variable)[(i+5)%STATE_LENGTH] + " - " + GetVariables(r,"A_L",STATE_LENGTH,variable)[i] + " >= 0 " + "\n")
        f.write(GetVariables(r,"X",STATE_LENGTH,variable)[i] + " - " + GetVariables(r,"Y",STATE_LENGTH,variable)[(i+5)%STATE_LENGTH] + " + " + GetVariables(r,"A_L",STATE_LENGTH,variable)[i] + " >= 0 " + "\n")
        f.write(" - " + GetVariables(r,"X",STATE_LENGTH,variable)[i] + " + " + GetVariables(r,"Y",STATE_LENGTH,variable)[(i+5)%STATE_LENGTH] + " + " + GetVariables(r,"A_L",STATE_LENGTH,variable)[i] + " >= 0 " + "\n")
        f.write(GetVariables(r,"X",STATE_LENGTH,variable)[i] + " + " + GetVariables(r,"Y",STATE_LENGTH,variable)[(i+5)%STATE_LENGTH] + " + " + GetVariables(r,"A_L",STATE_LENGTH,variable)[i] + " <= 2 " + "\n")

    for i in range (STATE_LENGTH):
        f.write(GetVariables(r,"B_L",STATE_LENGTH,variable)[i] + " + " + GetVariables(r+1,"X",STATE_LENGTH,variable)[(i+5)%STATE_LENGTH] + " - " + GetVariables(r+1,"Y",STATE_LENGTH,variable)[i] + " >= 0 " + "\n")
        f.write(GetVariables(r,"B_L",STATE_LENGTH,variable)[i] + " - " + GetVariables(r+1,"X",STATE_LENGTH,variable)[(i+5)%STATE_LENGTH] + " + " + GetVariables(r+1,"Y",STATE_LENGTH,variable)[i] + " >= 0 " + "\n")
        f.write(" - " + GetVariables(r,"B_L",STATE_LENGTH,variable)[i] + " + " + GetVariables(r+1,"X",STATE_LENGTH,variable)[(i+5)%STATE_LENGTH] + " + " + GetVariables(r+1,"Y",STATE_LENGTH,variable)[i] + " >= 0 " + "\n")
        f.write(GetVariables(r,"B_L",STATE_LENGTH,variable)[i] + " + " + GetVariables(r+1,"X",STATE_LENGTH,variable)[(i+5)%STATE_LENGTH] + " + " + GetVariables(r+1,"Y",STATE_LENGTH,variable)[i] + " <= 2 " + "\n")

def Constraint_L(f, variable):
    Constraint_initialize_L(R_L, f, variable)
    for r in range (R_D+R_M, R_D+R_M+R_L):
        Constraint_MDD_L(r, f, variable)
        Constraint_THREE_L(r, f, variable)   

##################################################The middle Part##################################################
def Constraint_MDD_M_DL(r, f, variable):
    M0 = [[-1, -1, 0, 0, 0, -1], 
    [0, 0, -1, -1, 0, -1], 
    [0, 1, 0, 1, -1, 0], 
    [1, 0, 1, 0, -1, 0], 
    [-1, 0, 0, -1, 1, -1], 
    [0, -1, -1, 0, 1, -1]]

    for i in range (STATE_LENGTH):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(r,"X_MD0",STATE_LENGTH,variable)[i])
            res.append(str(M0[t][1]) + " " + GetVariables(r,"X_MD1",STATE_LENGTH,variable)[i])
            res.append(str(M0[t][2]) + " " + GetVariables(r,"X_ML0",STATE_LENGTH,variable)[i])
            res.append(str(M0[t][3]) + " " + GetVariables(r,"X_ML1",STATE_LENGTH,variable)[i])
            res.append(str(M0[t][4]) + " " + GetVariables(r,"p0_M",STATE_LENGTH,variable)[i])
            f.write(" + ".join(res) + " - " + str(M0[t][5]) + " c" + " >= 0 " + "\n")

    for i in range (STATE_LENGTH):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(r,"Y_MD0",STATE_LENGTH,variable)[i])
            res.append(str(M0[t][1]) + " " + GetVariables(r,"Y_MD1",STATE_LENGTH,variable)[i])
            res.append(str(M0[t][2]) + " " + GetVariables(r,"Y_ML0",STATE_LENGTH,variable)[i])
            res.append(str(M0[t][3]) + " " + GetVariables(r,"Y_ML1",STATE_LENGTH,variable)[i])
            res.append(str(M0[t][4]) + " " + GetVariables(r,"p1_M",STATE_LENGTH,variable)[i])
            f.write(" + ".join(res) + " - " + str(M0[t][5]) + " c" + " >= 0 " + "\n")

def Constraint_M_DL(f, variable):
    for r in range (R_D, R_D+R_M+1):
        Constraint_MDD_M_DL(r, f, variable)

##################################################total##################################################
def Constraint(f, variable):
    Constraint_D(f, variable)
    
    Constraint_M_PD(f, variable)
    Constraint_M_D(f, variable)
    Constraint_M_PL(f, variable)
    Constraint_M_L(f, variable)
    
    Constraint_L(f, variable)

    Constraint_M_DL(f, variable)

def ObjectiveFunction(f, variable):
    res = []

    for r in range (R_D):
        for i in range (int(STATE_LENGTH/4)):
            res.append("2 " + GetVariables(r,"p0_D",int(STATE_LENGTH/4),variable)[i])
            res.append(GetVariables(r,"q0_D",int(STATE_LENGTH/4),variable)[i])
            res.append("2 " + GetVariables(r,"p1_D",int(STATE_LENGTH/4),variable)[i])
            res.append(GetVariables(r,"q1_D",int(STATE_LENGTH/4),variable)[i])
    if (WEIGHT == 1):
        for r in range (R_D, R_D+R_M+1):
            for i in range (STATE_LENGTH):
                res.append("1 " + GetVariables(r,"p0_M",STATE_LENGTH,variable)[i])
                res.append("1 " + GetVariables(r,"p1_M",STATE_LENGTH,variable)[i])
    elif (WEIGHT == 2):
        for r in range (R_D, R_D+R_M+1):
            for i in range (STATE_LENGTH):
                res.append("2 " + GetVariables(r,"p0_M",STATE_LENGTH,variable)[i])
                res.append("2 " + GetVariables(r,"p1_M",STATE_LENGTH,variable)[i])
    elif (WEIGHT == 3):
        for r in range (R_D, R_D+R_M+1):
            for i in range (STATE_LENGTH):
                res.append("3 " + GetVariables(r,"p0_M",STATE_LENGTH,variable)[i])
                res.append("3 " + GetVariables(r,"p1_M",STATE_LENGTH,variable)[i])
    elif (WEIGHT == 4):
        for r in range (R_D, R_D+R_M+1):
            for i in range (STATE_LENGTH):
                res.append("4 " + GetVariables(r,"p0_M",STATE_LENGTH,variable)[i])
                res.append("4 " + GetVariables(r,"p1_M",STATE_LENGTH,variable)[i])
    elif (WEIGHT == 5):
        for r in range (R_D, R_D+R_M+1):
            for i in range (STATE_LENGTH):
                res.append("5 " + GetVariables(r,"p0_M",STATE_LENGTH,variable)[i])
                res.append("5 " + GetVariables(r,"p1_M",STATE_LENGTH,variable)[i])
    elif (WEIGHT == 6):
        for r in range (R_D, R_D+R_M+1):
            for i in range (STATE_LENGTH):
                res.append("6 " + GetVariables(r,"p0_M",STATE_LENGTH,variable)[i])
                res.append("6 " + GetVariables(r,"p1_M",STATE_LENGTH,variable)[i])
    elif (WEIGHT == 7):
        for r in range (R_D, R_D+R_M+1):
            for i in range (STATE_LENGTH):
                res.append("7 " + GetVariables(r,"p0_M",STATE_LENGTH,variable)[i])
                res.append("7 " + GetVariables(r,"p1_M",STATE_LENGTH,variable)[i])
    elif (WEIGHT == 8):
        for r in range (R_D, R_D+R_M+1):
            for i in range (STATE_LENGTH):
                res.append("8 " + GetVariables(r,"p0_M",STATE_LENGTH,variable)[i])
                res.append("8 " + GetVariables(r,"p1_M",STATE_LENGTH,variable)[i])
    elif (WEIGHT == 9):
        for r in range (R_D, R_D+R_M+1):
            for i in range (STATE_LENGTH):
                res.append("9 " + GetVariables(r,"p0_M",STATE_LENGTH,variable)[i])
                res.append("9 " + GetVariables(r,"p1_M",STATE_LENGTH,variable)[i])
    elif (WEIGHT == 10):
        for r in range (R_D, R_D+R_M+1):
            for i in range (STATE_LENGTH):
                res.append("10 " + GetVariables(r,"p0_M",STATE_LENGTH,variable)[i])
                res.append("10 " + GetVariables(r,"p1_M",STATE_LENGTH,variable)[i])
    elif (WEIGHT == 11):
        for r in range (R_D, R_D+R_M+1):
            for i in range (STATE_LENGTH):
                res.append("11 " + GetVariables(r,"p0_M",STATE_LENGTH,variable)[i])
                res.append("11 " + GetVariables(r,"p1_M",STATE_LENGTH,variable)[i])
    elif (WEIGHT == 12):
        for r in range (R_D, R_D+R_M+1):
            for i in range (STATE_LENGTH):
                res.append("12 " + GetVariables(r,"p0_M",STATE_LENGTH,variable)[i])
                res.append("12 " + GetVariables(r,"p1_M",STATE_LENGTH,variable)[i])
    elif (WEIGHT == 13):
        for r in range (R_D, R_D+R_M+1):
            for i in range (STATE_LENGTH):
                res.append("13 " + GetVariables(r,"p0_M",STATE_LENGTH,variable)[i])
                res.append("13 " + GetVariables(r,"p1_M",STATE_LENGTH,variable)[i])
    elif (WEIGHT == 14):
        for r in range (R_D, R_D+R_M+1):
            for i in range (STATE_LENGTH):
                res.append("14 " + GetVariables(r,"p0_M",STATE_LENGTH,variable)[i])
                res.append("14 " + GetVariables(r,"p1_M",STATE_LENGTH,variable)[i])
    elif (WEIGHT == 15):
        for r in range (R_D, R_D+R_M+1):
            for i in range (STATE_LENGTH):
                res.append("15 " + GetVariables(r,"p0_M",STATE_LENGTH,variable)[i])
                res.append("15 " + GetVariables(r,"p1_M",STATE_LENGTH,variable)[i])
    elif (WEIGHT == 16):
        for r in range (R_D, R_D+R_M+1):
            for i in range (STATE_LENGTH):
                res.append("16 " + GetVariables(r,"p0_M",STATE_LENGTH,variable)[i])
                res.append("16 " + GetVariables(r,"p1_M",STATE_LENGTH,variable)[i])
    elif (WEIGHT == 17):
        for r in range (R_D, R_D+R_M+1):
            for i in range (STATE_LENGTH):
                res.append("17 " + GetVariables(r,"p0_M",STATE_LENGTH,variable)[i])
                res.append("17 " + GetVariables(r,"p1_M",STATE_LENGTH,variable)[i])
    elif (WEIGHT == 18):
        for r in range (R_D, R_D+R_M+1):
            for i in range (STATE_LENGTH):
                res.append("18 " + GetVariables(r,"p0_M",STATE_LENGTH,variable)[i])
                res.append("18 " + GetVariables(r,"p1_M",STATE_LENGTH,variable)[i])
    elif (WEIGHT == 19):
        for r in range (R_D, R_D+R_M+1):
            for i in range (STATE_LENGTH):
                res.append("19 " + GetVariables(r,"p0_M",STATE_LENGTH,variable)[i])
                res.append("19 " + GetVariables(r,"p1_M",STATE_LENGTH,variable)[i])
    else:
        for r in range (R_D, R_D+R_M+1):
            for i in range (STATE_LENGTH):
                res.append("20 " + GetVariables(r,"p0_M",STATE_LENGTH,variable)[i])
                res.append("20 " + GetVariables(r,"p1_M",STATE_LENGTH,variable)[i])



    for r in range (R_D+R_M, R_D+R_M+R_L):
        for i in range (int(STATE_LENGTH/4)):
            res.append("4 " + GetVariables(r,"p0_L",int(STATE_LENGTH/4),variable)[i])
            res.append("2 " + GetVariables(r,"q0_L",int(STATE_LENGTH/4),variable)[i])
            res.append("4 " + GetVariables(r,"p1_L",int(STATE_LENGTH/4),variable)[i])
            res.append("2 " + GetVariables(r,"q1_L",int(STATE_LENGTH/4),variable)[i])

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
    # model.setParam('OutputFlag', 0)
    model.Params.PoolSearchMode = 2
    model.Params.PoolSolutions = 1
    model.optimize()
    # model.computeIIS()
    # model.write("LELBC_dl.ilp")
    model.write(solFileName)
    # if model.status == GRB.OPTIMAL:
    #     print('Optimal objective:', model.objVal)
    #     print(model.status)
    # return (model.objVal)
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
        Z = 0
        W = 0

        for j in range ((32*R_D+64*R_M+64+32*R_L)+1, (32*R_D+64*R_M+64+32*R_L)+1+32):
            if (abs(Solution[j]) < 0.1):
                X = X + (0 << (j-((32*R_D+64*R_M+64+32*R_L)+1)))
            else:
                X = X + (1 << (j-((32*R_D+64*R_M+64+32*R_L)+1)))

        for j in range ((32*R_D+64*R_M+64+32*R_L)+1+32, (32*R_D+64*R_M+64+32*R_L)+1+64):
            if (abs(Solution[j]) < 0.1):
                Y = Y + (0 << (j-((32*R_D+64*R_M+64+32*R_L)+1+32)))
            else:
                Y = Y + (1 << (j-((32*R_D+64*R_M+64+32*R_L)+1+32)))

    #     Solutions_0x.append([X,Y,Solution[32*R_D+64*R_M+64+32*R_L]])
    # for i in range (len(Solutions_0x)):
        f.write("[" + str(hex(INPUT_DIFFER[0])) + ", " + str(hex(INPUT_DIFFER[1])) + ", " + str(hex(X)) + ", " + str(hex(Y)) + ", " + str(Solution[32*R_D+64*R_M+64+32*R_L])+ "],\n")


if __name__ == '__main__':
    ANSWER = [[0x20, 0x1, 0xfeff2f0f, 0xfffffbff],
[0x40, 0x2, 0xfeee0e0f, 0xfffffaff],
[0x80, 0x4, 0xe7f2ff0f, 0xff7ffffd],
[0x100, 0x8, 0xe1e0fe0f, 0xff0fffff],
[0x200, 0x10, 0xefe3f0ff, 0xffffefff],
[0x400, 0x20, 0xe2e0f0ff, 0xffff0fff],
[0x800, 0x40, 0x7faff0fe, 0xfaffffaf],
[0x1000, 0x80, 0xe0fe0fe, 0xf0f7efff],
[0x2000, 0x100, 0xfe1f0fff, 0xfffeffff],
[0x4000, 0x200, 0x6e0f0ffe, 0xfff8ffff],
[0x8000, 0x400, 0xf0ff0fef, 0x2ffff4ff],
[0x10000, 0x800, 0xe0fe0fe1, 0x8ffff7ff],
[0x20000, 0x1000, 0xe5f0ffff, 0xffffffff],
[0x40000, 0x2000, 0xe0e0ffee, 0xff2fffff],
[0x80000, 0x4000, 0x6ff0fe7f, 0xffffcff6],
[0x100000, 0x8000, 0x4fe0ee0e, 0xffff7ff0],
[0x200000, 0x10000, 0x3f0feffe, 0xffffffff],
[0x400000, 0x20000, 0xe0ffe6e, 0xffffffff],
[0x800000, 0x40000, 0xff0feff6, 0xfffcffef],
[0x1000000, 0x80000, 0xfe0fe4e0, 0x7fffff0f],
[0x2000000, 0x100000, 0xf0ffffe1, 0xcfffffff],
[0x4000000, 0x200000, 0xf0ffeee0, 0xffffffff],
[0x8000000, 0x400000, 0xf0fe7f0f, 0xff9fffff],
[0x10000000, 0x800000, 0xe0fe0e0f, 0xff7ff0f0],
[0x20000000, 0x1000000, 0xffeffbf, 0xffffffff],
[0x40000000, 0x2000000, 0xffe6e0f, 0xffffffff],
[0x80000000, 0x4000000, 0xfe7f8ff, 0xf4ff6fff],
[0x1, 0x8000000, 0xfe0e0fe, 0xffff0f73],
[0x2, 0x10000000, 0xffffe8f0, 0xffffffef],
[0x4, 0x20000000, 0xffe6e0f0, 0xffffbf2f],
[0x8, 0x40000000, 0xfe7f2ff1, 0xbfffffff],
[0x10, 0x80000000, 0xee1e0fe0, 0x7ff0f7ff],
[0x1, 0x0, 0xffffebf6, 0xffffffaf],
[0x3, 0x0, 0xffefe1f4, 0xffffaf2f],
[0x5, 0x0, 0xffebf6f2, 0xffffefaf],
[0x9, 0x0, 0xfe0f80fc, 0xfff7ffaf],
[0x2, 0x0, 0xffffe3fc, 0xffffffdf],
[0x6, 0x0, 0xffeff2fc, 0xffffffff],
[0xa, 0x0, 0xfe0e80f0, 0xfff3ff0f],
[0x4, 0x0, 0xfffff1fe, 0xffffaf5f],
[0xc, 0x0, 0x406e0f0, 0xf5f7afff],
[0x8, 0x0, 0xfeefc2f5, 0xfff7ffaf],
[0x10, 0x0, 0xfffebf6f, 0xfffffeff],
[0x30, 0x0, 0xfeff2f4f, 0xfffef8ff],
[0x50, 0x0, 0xfebeafaf, 0xfffffbff],
[0x90, 0x0, 0xe0f80f0f, 0xff0ff3ff],
[0x20, 0x0, 0xfffebf8f, 0xffffffff],
[0x60, 0x0, 0xfefe0fdf, 0xfffff9ff],
[0xa0, 0x0, 0xa0e00f0c, 0xff0ffaff],
[0x40, 0x0, 0xffff8fef, 0xffffffff],
[0xc0, 0x0, 0x406e0f00, 0xa6af0ff],
[0x80, 0x0, 0xeffcef5f, 0xff7ff2ff],
[0x100, 0x0, 0xffe3f4ff, 0xffff9fff],
[0x300, 0x0, 0xefe1f4ff, 0xffbf2fff],
[0x500, 0x0, 0xfbe4f2ff, 0xffbfafff],
[0x900, 0x0, 0xf80f0fe, 0xf0ffafff],
[0x200, 0x0, 0xffe1f2ff, 0xffffcfff],
[0x600, 0x0, 0xeff1f4ff, 0xffffffff],
[0xa00, 0x0, 0xe80f0e2, 0xf2ff0fff],
[0x400, 0x0, 0xfff1feff, 0xffbf5fff],
[0xc00, 0x0, 0x6e0f020, 0xe72ffff4],
[0x800, 0x0, 0xef80f5fe, 0xf7ffafff],
[0x1000, 0x0, 0xfebf4fff, 0xfff8ffff],
[0x3000, 0x0, 0xfe3fcffe, 0xfbf8ffff],
[0x5000, 0x0, 0xbfaf3eff, 0xfffaffff],
[0x9000, 0x0, 0xf84fcfe1, 0x7ff2ffff],
[0x2000, 0x0, 0xfe7f0fff, 0xffffffff],
[0x6000, 0x0, 0xfe0fcffe, 0xfff8ffff],
[0xa000, 0x0, 0xe80f0ee0, 0x6ff1ffff],
[0x4000, 0x0, 0xffaf6ffe, 0xfaffffff],
[0xc000, 0x0, 0x6e0f0140, 0x7af4ff1f],
[0x8000, 0x0, 0xf8cf5fee, 0x7ffaffff],
[0x10000, 0x0, 0xe3f6ffff, 0xffffffff],
[0x30000, 0x0, 0xe1f4ffef, 0xaf2fffff],
[0x50000, 0x0, 0xf2f2efee, 0xffbfffff],
[0x90000, 0x0, 0x84f0fe0f, 0xff8ffff7],
[0x20000, 0x0, 0xf3f0ffff, 0xffcfffff],
[0x60000, 0x0, 0xe1f4ffef, 0xff7fffff],
[0xa0000, 0x0, 0x80f05e0f, 0xff4ffff7],
[0x40000, 0x0, 0xf2feffef, 0xafafffff],
[0xc0000, 0x0, 0xe0f0040e, 0xaf7f74b7],
[0x80000, 0x0, 0xe0f7feff, 0xff7ffff7],
[0x100000, 0x0, 0xbf6feffe, 0xfaffffff],
[0x300000, 0x0, 0x9fcffefe, 0xfefffffa],
[0x500000, 0x0, 0x6f6efe9e, 0xffffffff],
[0x900000, 0x0, 0x4f07e0f2, 0xffffff6f],
[0x200000, 0x0, 0xff8ffffe, 0xf4ffffff],
[0x600000, 0x0, 0xaf4ffeff, 0xffffffff],
[0xa00000, 0x0, 0xf2660fa, 0xf0ffff0f],
[0x400000, 0x0, 0x3f6fffff, 0xfafffffe],
[0xc00000, 0x0, 0xf0000fe, 0xf7ff5f7f],
[0x800000, 0x0, 0xf5feef6, 0xffffffff],
[0x1000000, 0x0, 0xf6ffffe3, 0xefffffff],
[0x3000000, 0x0, 0xf4ffefe1, 0xefffffef],
[0x5000000, 0x0, 0xfeffecf0, 0xffffffff],
[0x9000000, 0x0, 0xfafe0fa0, 0xaffff7ff],
[0x2000000, 0x0, 0xf2ffffeb, 0xafffffff],
[0x6000000, 0x0, 0xf4ffefe0, 0xffffffff],
[0xa000000, 0x0, 0xf04e0f80, 0x2ffff7ff],
[0x4000000, 0x0, 0xf6ffefe0, 0xdfffffaf],
[0xc000000, 0x0, 0xf00006e0, 0xfff1e7af],
[0x8000000, 0x0, 0xf7feef80, 0xffffffff],
[0x10000000, 0x0, 0x4ffffe3f, 0xfffffffa],
[0x30000000, 0x0, 0x4ffefe1f, 0xfffffbff],
[0x50000000, 0x0, 0x2ffffe6f, 0xffffffff],
[0x90000000, 0x0, 0xcfe0f84f, 0xffff0ffa],
[0x20000000, 0x0, 0x2ffffe7f, 0xffffffff],
[0x60000000, 0x0, 0x4feefe0f, 0xffffffff],
[0xa0000000, 0x0, 0xee0e80f, 0xffff0ff0],
[0x40000000, 0x0, 0x6ffefe2f, 0xfffffffb],
[0xc0000000, 0x0, 0x6e0f, 0xf74a6aff],
[0x80000000, 0x0, 0x7feefe1f, 0xffff7ffa]]
    cor_min = 64
    cor_index = []
    for ans in range (len(ANSWER)):
        for WEIGHT in range (1, 11):
            INPUT_DIFFER = [ANSWER[ans][0], ANSWER[ans][1]]
            OUTPUT_MASK = [ANSWER[ans][2], ANSWER[ans][3]]
            STATE_LENGTH = 32

            R_D = 2

            R_M = 4

            R_M_PL = 0
            R_M_L = R_M - R_M_PL

            R_M_PD = 0
            R_M_D = R_M - R_M_PD

            R_L = 3

            variable = set()
            lpFileName = "LELBC_dl.lp"
            solFileName = "LELBC_dl_%d_%d_%d.sol" % (R_D, R_M, R_L)
            lpFileName_result = "LELBC_dl_%d_%d_%d_%d.txt" % (R_D, R_M, R_L, WEIGHT)
            CreateModel(lpFileName, variable)
            SolveModel(lpFileName, solFileName, lpFileName_result)
