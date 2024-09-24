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

    resR = []
    for i in range (size):
        resR.append(GetVariables(R,"X",size,variable)[i])

    if (AAA == BBB):
        f.write(" + ".join(resR) + " = 1 " + "\n")
        f.write(GetVariables(R,"X",size,variable)[AAA] + " = 1\n")
        f.write(GetVariables(R,"X",size,variable)[BBB] + " = 1\n")
    else:
        f.write(" + ".join(resR) + " = 2 " + "\n")
        f.write(GetVariables(R,"X",size,variable)[AAA] + " = 1\n")
        f.write(GetVariables(R,"X",size,variable)[BBB] + " = 1\n")


    res = []
    for r in range (R):
        for i in range (16):
            res.append("3 " + GetVariables(r,"p0",16,variable)[i])
            res.append("2 " + GetVariables(r,"P1",16,variable)[i])
            res.append("1.415 " + GetVariables(r,"P2",16,variable)[i])
    f.write(" + ".join(res) + " <= 3 " + "\n")

def Constraint_Sbox(r, f, variable):
    M0 = [[1, 3, 2, 4, 4, 2, 2, 3, -8, -6, -10, 0], [-2, -1, -1, -1, -4, -1, 1, 0, 9, 6, 1, 0], [4, 3, 3, -2, 0, 4, 3, 2, 2, -9, -11, 0], [0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1], [-2, -4, 0, -2, 4, -1, -3, -3, 11, 9, 11, 0], [1, -1, -1, 3, -4, 0, -3, -4, 9, 10, 9, 0], [1, 1, -1, 3, 4, 1, 2, 2, -5, -2, -4, 0], [5, 1, 7, 5, -1, -1, -3, 3, -1, -3, 0, 0], [-3, 3, -3, -2, -1, -3, 1, -2, 12, 8, 1, 0], [0, 2, 1, 3, 2, 0, 1, 1, -4, -2, -4, 0], [-4, 1, -2, -3, -1, 2, -2, 1, 10, 6, 2, 0], [4, -4, -1, -1, 2, -4, -1, 2, 8, 6, 7, 0], [-1, -1, 0, -1, 0, 0, 1, 1, 0, 1, 0, -2], [1, -1, 0, -2, 1, 0, -2, -2, 5, 6, 5, 0], [-2, -2, 3, -2, -3, 3, 3, -1, 7, 3, -3, 0], [-1, -1, -1, 1, -1, 0, -1, 0, 4, 3, 3, 0], [-1, 1, 2, -1, -2, -2, -2, 1, 6, 6, 2, 0], [3, 1, -1, -1, 2, 3, 1, -1, 0, -1, 0, 0], [2, -2, -5, -1, -1, -5, -1, -1, 14, 11, 9, 0], [-1, 1, 2, 2, -1, 0, -1, -2, 2, 5, 2, 0], [-1, 0, 0, 0, 1, -1, 1, -1, 0, 0, 0, -2], [1, -1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0], [1, 1, 1, 0, -1, -1, 1, -1, 0, 0, 0, -2], [0, 1, -1, -1, 0, 1, -1, 1, 0, 0, 0, -2], [1, -1, 1, 0, -1, 1, -1, 0, 0, 0, 0, -2]]

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
            res.append(str(M0[t][8]) + " " + GetVariables(r,"p0",16,variable)[i])
            res.append(str(M0[t][9]) + " " + GetVariables(r,"P1",16,variable)[i])
            res.append(str(M0[t][10]) + " " + GetVariables(r,"P2",16,variable)[i])
            f.write(" + ".join(res) + " - " + str(M0[t][11]) + " c >= 0 " + "\n")

def Constraint_Permutation(r, f, variable):
    P = [0, 17, 34, 51, 48, 1, 18, 35, 32, 49, 2, 19, 16, 33, 50, 3, 4, 21, 38, 55, 52, 5, 22, 39, 36, 53, 6, 23, 20, 37, 54, 7, 8, 25, 42, 59, 56, 9, 26, 43, 40, 57, 10, 27, 24, 41, 58, 11, 12, 29, 46, 63, 60, 13, 30, 47, 44, 61, 14, 31, 28, 45, 62, 15]
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
            res.append("3 " + GetVariables(r,"p0",16,variable)[i])
            res.append("2 " + GetVariables(r,"P1",16,variable)[i])
            res.append("1.415 " + GetVariables(r,"P2",16,variable)[i])
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
    # model.write(solFileName)
    status = model.status
    if (status == 2):
        obj = model.objVal
    else:
        obj = 0
    return [status, obj]

if __name__ == "__main__":
    res1 = []
    ff = open("GIFT_D_1_3.txt","w")
    for AAA in range (64):
        for BBB in range (AAA, 64):
            R = 1
            size = 64
            variable = set()
            lpFileName = "gift64_d.lp"
            solFileName = "gift64_d_%d.sol" % R
            CreateModel(lpFileName, variable)
            temp = SolveModel(lpFileName, solFileName)
            if (temp[0] == 2):
                res1.append([AAA, BBB, int(temp[1])])
                ff.write("[" + str(AAA) + ", " + str(BBB) + ", " + str(int(temp[1])) + "],\n")

    print(res1)
