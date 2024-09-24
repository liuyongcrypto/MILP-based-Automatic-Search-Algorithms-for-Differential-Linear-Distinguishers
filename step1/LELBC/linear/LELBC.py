from gurobipy import *

def GetVariables(round,varName,varSize,variable):
    res = []
    for i in range(varSize):
        res.append(varName + "_" + str(round) + "_" + str(i))
        variable.add(varName + "_" + str(round) + "_" + str(i))
    return res

def Constraint_initialize(R, f, variable):
    f.write("c" + " = 1 " + "\n")

    res = []
    for i in range (32):
        res.append(GetVariables(0,"X",32,variable)[i])
        res.append(GetVariables(0,"Y",32,variable)[i])
    f.write(" + ".join(res) + " >= 1 " + "\n")

def Constraint_MDD(r, f, variable):
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

    for i in range (8):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(r,"A",32,variable)[4*i+3])
            res.append(str(M0[t][1]) + " " + GetVariables(r,"A",32,variable)[4*i+2])
            res.append(str(M0[t][2]) + " " + GetVariables(r,"A",32,variable)[4*i+1])
            res.append(str(M0[t][3]) + " " + GetVariables(r,"A",32,variable)[4*i+0])
            res.append(str(M0[t][4]) + " " + GetVariables(r+1,"X",32,variable)[4*i+3])
            res.append(str(M0[t][5]) + " " + GetVariables(r+1,"X",32,variable)[4*i+2])
            res.append(str(M0[t][6]) + " " + GetVariables(r+1,"X",32,variable)[4*i+1])
            res.append(str(M0[t][7]) + " " + GetVariables(r+1,"X",32,variable)[4*i+0])
            res.append(str(M0[t][8]) + " " + GetVariables(r,"p0",8,variable)[i])
            res.append(str(M0[t][9]) + " " + GetVariables(r,"q0",8,variable)[i])
            f.write(" + ".join(res) + " - " + str(M0[t][10]) + " " + "c" + " >= 0 " + "\n")
    
    for i in range (8):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(r,"Y",32,variable)[4*i+3])
            res.append(str(M0[t][1]) + " " + GetVariables(r,"Y",32,variable)[4*i+2])
            res.append(str(M0[t][2]) + " " + GetVariables(r,"Y",32,variable)[4*i+1])
            res.append(str(M0[t][3]) + " " + GetVariables(r,"Y",32,variable)[4*i+0])
            res.append(str(M0[t][4]) + " " + GetVariables(r,"B",32,variable)[4*i+3])
            res.append(str(M0[t][5]) + " " + GetVariables(r,"B",32,variable)[4*i+2])
            res.append(str(M0[t][6]) + " " + GetVariables(r,"B",32,variable)[4*i+1])
            res.append(str(M0[t][7]) + " " + GetVariables(r,"B",32,variable)[4*i+0])
            res.append(str(M0[t][8]) + " " + GetVariables(r,"p1",8,variable)[i])
            res.append(str(M0[t][9]) + " " + GetVariables(r,"q1",8,variable)[i])
            f.write(" + ".join(res) + " - " + str(M0[t][10]) + " " + "c" + " >= 0 " + "\n")

def Constraint_THREE(r, f, variable):
    for i in range (32):
        f.write(GetVariables(r,"X",32,variable)[i] + " + " + GetVariables(r,"Y",32,variable)[(i+5)%32] + " - " + GetVariables(r,"A",32,variable)[i] + " >= 0 " + "\n")
        f.write(GetVariables(r,"X",32,variable)[i] + " - " + GetVariables(r,"Y",32,variable)[(i+5)%32] + " + " + GetVariables(r,"A",32,variable)[i] + " >= 0 " + "\n")
        f.write(" - " + GetVariables(r,"X",32,variable)[i] + " + " + GetVariables(r,"Y",32,variable)[(i+5)%32] + " + " + GetVariables(r,"A",32,variable)[i] + " >= 0 " + "\n")
        f.write(GetVariables(r,"X",32,variable)[i] + " + " + GetVariables(r,"Y",32,variable)[(i+5)%32] + " + " + GetVariables(r,"A",32,variable)[i] + " <= 2 " + "\n")

    for i in range (32):
        f.write(GetVariables(r,"B",32,variable)[i] + " + " + GetVariables(r+1,"X",32,variable)[(i+5)%32] + " - " + GetVariables(r+1,"Y",32,variable)[i] + " >= 0 " + "\n")
        f.write(GetVariables(r,"B",32,variable)[i] + " - " + GetVariables(r+1,"X",32,variable)[(i+5)%32] + " + " + GetVariables(r+1,"Y",32,variable)[i] + " >= 0 " + "\n")
        f.write(" - " + GetVariables(r,"B",32,variable)[i] + " + " + GetVariables(r+1,"X",32,variable)[(i+5)%32] + " + " + GetVariables(r+1,"Y",32,variable)[i] + " >= 0 " + "\n")
        f.write(GetVariables(r,"B",32,variable)[i] + " + " + GetVariables(r+1,"X",32,variable)[(i+5)%32] + " + " + GetVariables(r+1,"Y",32,variable)[i] + " <= 2 " + "\n")

def Constraint(f, variable):
    Constraint_initialize(R, f, variable)

    for r in range (R):
        Constraint_MDD(r, f, variable)
        Constraint_THREE(r, f, variable)   

def ObjectiveFunction(f, variable):
    res = []
    for r in range (R):
        for i in range (8):
            res.append("2 " + GetVariables(r,"p0",8,variable)[i])
            res.append(GetVariables(r,"q0",8,variable)[i])
            res.append("2 " + GetVariables(r,"p1",8,variable)[i])
            res.append(GetVariables(r,"q1",8,variable)[i])
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

def SolveModel(lpFileName, solFileName):
    model = read(lpFileName)
    # model.setParam('OutputFlag', 0)
    # model.Params.PoolSearchMode = 2
    # model.Params.PoolSolutions = 200000000
    model.optimize()
    model.write(solFileName)

if __name__ == '__main__':
    R = 3
    variable = set()
    lpFileName = "LELBC_l.lp"
    solFileName = "LELBC_l_%d.sol" % R
    CreateModel(lpFileName, variable)
    SolveModel(lpFileName, solFileName)
