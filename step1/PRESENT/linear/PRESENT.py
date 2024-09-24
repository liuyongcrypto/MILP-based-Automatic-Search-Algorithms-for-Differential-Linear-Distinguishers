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
    for i in range (size):
        res.append(GetVariables(0,"X",size,variable)[i])
    f.write(" + ".join(res) + " >= 1 " + "\n")

def Constraint_Sbox(r, f, variable):
    M0 = [[-7, -2, -4, -2, 4, -5, -10, -3, 33, 21, 0], [0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1], [4, 4, 4, 3, 1, 3, 1, 3, -5, -9, 0], [-7, -2, 1, -3, -3, -4, 2, 0, 19, 12, 0], [1, -1, -1, 0, 0, 0, 0, 0, 1, 2, 0], [0, 0, 0, 0, -1, 1, -1, 0, 1, 2, 0], [5, 1, 1, 0, 3, 5, 3, 2, -4, -7, 0], [1, 2, 2, 6, 3, 2, 3, -1, -3, -6, 0], [1, 1, 1, 0, 0, 0, 0, 0, -1, 0, 0], [2, -3, -1, -1, -1, -4, 1, -3, 11, 9, 0], [0, 0, 0, 0, 1, 1, 1, 0, -1, 0, 0], [1, -1, -1, 3, -2, 2, -2, 3, 3, 2, 0], [-1, 2, -1, -6, -3, 4, -3, -5, 15, 13, 0], [-1, -1, 1, 0, 0, 1, 0, 0, 1, 2, 0], [1, 0, 0, 0, 1, -1, -1, 0, 1, 2, 0], [1, 0, 0, 0, -1, -1, 1, 0, 1, 2, 0], [-1, 1, -1, 0, 0, 1, 0, 0, 1, 2, 0], [0, -1, -1, 0, -1, 0, -1, 0, 3, 4, 0], [0, -1, -1, 0, 1, 0, 1, 0, 1, 2, 0], [-2, 2, -5, 1, -2, -3, -1, 2, 13, 8, 0], [0, 1, 1, 0, -1, 0, -1, 0, 1, 2, 0], [1, 2, 5, 3, 6, -1, 1, 5, -1, -7, 0], [-2, 1, 1, 0, 1, -2, 1, 0, 3, 2, 0], [-4, -5, -2, 3, 2, 4, -1, 1, 12, 7, 0], [1, -1, -1, -1, 0, -2, 0, -2, 6, 5, 0], [-1, -2, 1, 0, -1, -1, -1, 1, 6, 4, 0], [0, 1, 1, 0, 0, 1, -1, -1, 2, 1, 0]]

    for i in range (16):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(r,"X",size,variable)[4*i+3])
            res.append(str(M0[t][1]) + " " + GetVariables(r,"X",size,variable)[4*i+2])
            res.append(str(M0[t][2]) + " " + GetVariables(r,"X",size,variable)[4*i+1])
            res.append(str(M0[t][3]) + " " + GetVariables(r,"X",size,variable)[4*i+0])
            res.append(str(M0[t][4]) + " " + GetVariables(r,"Y",size,variable)[4*i+3])
            res.append(str(M0[t][5]) + " " + GetVariables(r,"Y",size,variable)[4*i+2])
            res.append(str(M0[t][6]) + " " + GetVariables(r,"Y",size,variable)[4*i+1])
            res.append(str(M0[t][7]) + " " + GetVariables(r,"Y",size,variable)[4*i+0])
            res.append(str(M0[t][8]) + " " + GetVariables(r,"p",16,variable)[i])
            res.append(str(M0[t][9]) + " " + GetVariables(r,"q",16,variable)[i])
            f.write(" + ".join(res) + " - " + str(M0[t][10]) + " c >= 0 " + "\n")

def Constraint_Permutation(r, f, variable):
    P = [0, 16, 32, 48, 1, 17, 33, 49, 2, 18, 34, 50, 3, 19, 35, 51, 4, 20, 36, 52, 5, 21, 37, 53, 6, 22, 38, 54, 7, 23, 39, 55, 8, 24, 40, 56, 9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59, 12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63]
    for i in range (size):
        f.write(GetVariables(r,"Y",size,variable)[i] + " - " + GetVariables(r+1,"X",size,variable)[P[i]] + " = 0 " + "\n")

def Constraint(f, variable):
    Constraint_initialize(R, f, variable)
    for r in range (R):
        Constraint_Sbox(r, f, variable)
        Constraint_Permutation(r, f, variable) 

def ObjectiveFunction(f, variable):
    res = []
    for r in range (R):
        for i in range (16):
            res.append("2 " + GetVariables(r,"p",16,variable)[i])
            res.append("1 " + GetVariables(r,"q",16,variable)[i])
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
    # model.Params.PoolSearchMode = 2
    # model.Params.PoolSolutions = 200000000
    model.optimize()
    model.write(solFileName)

if __name__ == "__main__":

    R = 5
    size = 64
    variable = set()
    lpFileName = "present_l.lp"
    solFileName = "present_l_%d.sol" % R
    CreateModel(lpFileName, variable)
    SolveModel(lpFileName, solFileName)
