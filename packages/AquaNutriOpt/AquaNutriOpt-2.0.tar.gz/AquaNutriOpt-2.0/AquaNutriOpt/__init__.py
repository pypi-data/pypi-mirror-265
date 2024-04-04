import numpy as np
import pulp
import os
import sys
import time
BigM = 9999
class EPA:
    def __init__(self):
        print('**************************************************************')
        print('**************************************************************')
        print('**** EPA Package -- Version 02.0 *****************************')
        print('**************************************************************')
        print('**************************************************************')
        self.Um = {}
        self.C = np.Inf
        self.budgetList = []
        self.writefiles = True
        #self.Solver =
    # %%
    def Solve_SO_Det_Model(self, Budget=np.Inf):
        if Budget == np.Inf:
            pass
        else:
            self.C = Budget
        #self.Solver = Solver
        print('**************************************************************')
        print('**************************************************************')
        print('Building the model ... ***************************************')
        print('**************************************************************')
        print('**************************************************************')
        # Modeling
        MODEL = pulp.LpProblem("Deterministic Model", pulp.LpMinimize)
        # Variables

        Fijm = pulp.LpVariable.dicts('F', [(i, j, m) for m in self.MM for i in self.NN for j in self.NNp_i[i]],
                                     lowBound=0)
        for m in self.MM:
            for i in self.NN:
                for j in self.NNp_i[i]:
                    if i[-1] == 'a':
                        Fijm[(i, j, m)].lowBound = None

        Xit = pulp.LpVariable.dicts('X', {(i, t) for i in self.NN for t in self.TTi[i]}, lowBound=0, upBound=1,
                                    cat=pulp.LpInteger)
        Yijmt = pulp.LpVariable.dicts('Y',
                                      {(i, j, m, t) for j in self.NN for i in self.NNn_i[j] for m in self.MM for t in
                                       self.TTi[j]}, lowBound=0)

        # Objective
        MODEL += pulp.lpSum([Fijm[(i, self.L, self.ZZ[0])] for i in self.NNn_i[self.L]]), 'Obj'

        # Constraints
        ## Cons. 1
        for j in self.NN:
            if len(self.NNp_i[j]) > 1:
                continue
            for m in self.MM:
                if j != self.L:
                    for Time in range(self.TimePeriod):
                        MODEL += (pulp.lpSum([Fijm[(i, j, m)] for i in self.NNn_i[j]])
                                  - pulp.lpSum([Fijm[(j, i, m)] for i in self.NNp_i[j]])
                                  - pulp.lpSum([self.ALPHAtm[(t, m)] * Yijmt[(i, j, m, t)] for t in self.TTi[j] for i in
                                                self.NNn_i[j]])
                                  - pulp.lpSum(
                                    [self.PimTime[(j, m,Time)] * self.ALPHAtm[(t, m)] * Xit[(j, t)] for t in self.TTi[j]]) <= -
                                  self.PimTime[(j, m, Time)]), 'C1_{}_{}'.format(j, m)
        for j in self.NN:
            if len(self.NNp_i[j]) > 1:
                continue
            for i in self.NNn_i[j]:
                for m in self.MM:
                    for t in self.TTi[j]:
                        MODEL += Yijmt[(i, j, m, t)] <= Fijm[(i, j, m)], 'LC1_{}_{}_{}_{}'.format(i, j, m, t)
                        MODEL += Yijmt[(i, j, m, t)] <= BigM * Xit[(j, t)], 'LC2_{}_{}_{}_{}'.format(i, j, m, t)
                        MODEL += Yijmt[(i, j, m, t)] >= Fijm[(i, j, m)] - BigM * (
                                    1 - Xit[(j, t)]), 'LC3_{}_{}_{}_{}'.format(i, j, m, t)

        # Cons. 2
        for i in self.NN:
            MODEL += pulp.lpSum([Xit[(i, t)] for t in self.TTi[i]]) <= 1, 'C2_{}'.format(i)

        # Cons. 3
        for m in self.ZZp:
            MODEL += pulp.lpSum([Fijm[(i, self.L, m)] for i in self.NNn_i[self.L]]) <= self.Um[m], 'C3_{}'.format(m)

        # Cons. 4
        MODEL += pulp.lpSum([self.Cit[(i, t)] * Xit[(i, t)] for i in self.NN for t in self.TTi[i]]) <= self.C, 'C4'

        # Cons. 5
        for j in self.NNs:
            for k in self.NNp_i[j]:
                for m in self.MM:
                    MODEL += Fijm[(j, k, m)] == self.BETAij[(j, k)] * pulp.lpSum(
                        Fijm[(i, j, m)] for i in self.NNn_i[j]), 'C5_{}_{}_{}'.format(j, k, m)

        if self.C == np.Inf:
            print('**WARNING**: No budget is set for cost!!')

        print('**************************************************************')
        print('**************************************************************')
        print('Solving the model ... ****************************************')
        print('**************************************************************')
        print('**************************************************************')

        #solver = pulp.get_solver(self.Solver)
        Sol = MODEL.solve()

        print('**************************************************************')
        print('**************************************************************')
        print('Generating the results ... ***********************************')
        print('**************************************************************')
        print('**************************************************************')
        #if self.writefiles:
        file = open('Res_BMPs_SO_{}.txt'.format(self.C), 'w+')
        Counter = 0
        for i in self.NN:
            for t in self.TTi[i]:
                try:
                    if Xit[(i, t)].value() > .5:
                        file.write(i)
                        file.write(',')
                        file.write(t)
                        file.write('\n')
                except:
                    Counter = Counter + 1
        file.close()

        file = open('Res_Flow_SO_{}.txt'.format(self.C), 'w+')
        #
        for j in self.NN:
            for i in self.NNn_i[j]:
                try:
                    #            print('{} ==> {} : {}'.format(i, j, Fijm[(i,j,'P')].value() ) )
                    file.write('{}_{} {}\n'.format(i, j, str(Fijm[(i, j, 'P')].value())))
                except:
                    pass

        file.close()
        print('**************************************************************')
        print('**************************************************************')
        print('Solution is done. Find the results in the directory.**********')
        print('**************************************************************')
        print('**************************************************************')

    # %%
    def Solve_SOTI_Det_Model(self, Budget=np.Inf):
        self.TargetLoad = 0
        if isinstance(self.TimePeriod, int) != True:
            print("Please Enter integer values")
            return "Null"
        elif self.TimePeriod < 1:
            print("Please Enter the value of Time greater or equal to 1")
            return "Null"
        if Budget == np.Inf:
            pass
        else:
            self.C = Budget
        #self.Solver = Solver
        print('**************************************************************')
        print('**************************************************************')
        print('Building the model ... ***************************************')
        print('**************************************************************')
        print('**************************************************************')
        # %% Modeling
        MODEL = pulp.LpProblem("Deterministic Time Indexed Model", pulp.LpMinimize)
        # Variables

        FijmTime = pulp.LpVariable.dicts('F', [(i, j, m, Time) for m in self.MM for i in self.NN for j in self.NNp_i[i] for Time in
                                               range(self.TimePeriod)], lowBound=0)
        for m in self.MM:
            for i in self.NN:
                for j in self.NNp_i[i]:
                    for Time in range(self.TimePeriod):
                        if i[-1] == 'a':
                            FijmTime[(i, j, m, Time)].lowBound = None

        Xit = pulp.LpVariable.dicts('X', {(i, t) for i in self.NN for t in self.TTi[i]}, lowBound=0, upBound=1, cat=pulp.LpInteger)
        YijmtTime = pulp.LpVariable.dicts('Y', {(i, j, m, t, Time) for j in self.NN for i in self.NNn_i[j] for m in self.MM for t in self.TTi[j] for Time in range(self.TimePeriod)}, lowBound=0)

        # Objective
        MODEL += pulp.lpSum([FijmTime[(i, self.L, self.ZZ[0], Time)] for i in self.NNn_i[self.L] for Time in range(self.TimePeriod)]), 'Obj'

        # Constraints
        ## Cons. 1
        for j in self.NN:
            if len(self.NNp_i[j]) > 1:
                continue
            for m in self.MM:
                if j != self.L:
                    for Time in range(self.TimePeriod):
                        MODEL += (pulp.lpSum([FijmTime[(i, j, m, Time)] for i in self.NNn_i[j]])
                                  - pulp.lpSum([FijmTime[(j, i, m, Time)] for i in self.NNp_i[j]])
                                  - pulp.lpSum([self.ALPHAtm[(t, m)] * YijmtTime[(i, j, m, t, Time)] for t in self.TTi[j] for i in self.NNn_i[j]])
                                  - pulp.lpSum([self.PimTime[(j, m, Time)] * self.ALPHAtm[(t, m)] * Xit[(j, t)] for t in self.TTi[j]]) <= -self.PimTime[(j, m, Time)]), 'C1_{}_{}_{}'.format(j, m, Time)
        for j in self.NN:
            if len(self.NNp_i[j]) > 1:
                continue
            for i in self.NNn_i[j]:
                for m in self.MM:
                    for t in self.TTi[j]:
                        for Time in range(self.TimePeriod):
                            MODEL += YijmtTime[(i, j, m, t, Time)] <= FijmTime[
                                (i, j, m, Time)], 'LC1_{}_{}_{}_{}_{}'.format(i, j, m, t, Time)
                            MODEL += YijmtTime[(i, j, m, t, Time)] <= BigM * Xit[(j, t)], 'LC2_{}_{}_{}_{}_{}'.format(i,
                                                                                                                      j,
                                                                                                                      m,
                                                                                                                      t,
                                                                                                                      Time)
                            MODEL += YijmtTime[(i, j, m, t, Time)] >= FijmTime[(i, j, m, Time)] - BigM * (
                                        1 - Xit[(j, t)]), 'LC3_{}_{}_{}_{}_{}'.format(i, j, m, t, Time)

        # Cons. 2
        for i in self.NN:
            MODEL += pulp.lpSum([Xit[(i, t)] for t in self.TTi[i]]) <= 1, 'C2_{}'.format(i)

        # Cons. 3
        for m in self.ZZp:
            for Time in range(self.TimePeriod):
                MODEL += pulp.lpSum([FijmTime[(i, self.L, m, Time)] for i in self.NNn_i[self.L]]) <= self.Um[m], 'C3_{}_{}'.format(Time, m)

        # Cons. 4
        MODEL += pulp.lpSum([self.Cit[(i, t)] * Xit[(i, t)] for i in self.NN for t in self.TTi[i]]) <= self.C, 'C4'

        # Cons. 5
        for j in self.NNs:
            for k in self.NNp_i[j]:
                for m in self.MM:
                    for Time in range(self.TimePeriod):
                        MODEL += FijmTime[(j, k, m, Time)] == self.BETAij[(j, k)] * pulp.lpSum(
                            FijmTime[(i, j, m, Time)] for i in self.NNn_i[j]), 'C5_{}_{}_{}_{}'.format(j, k, m, Time)

        if self.C == np.Inf:
            print('**WARNING**: No budget is set !!')

        print('**************************************************************')
        print('**************************************************************')
        print('Solving the model ... ****************************************')
        print('**************************************************************')
        print('**************************************************************')

        #solver = pulp.get_solver(self.Solver)
        Sol = MODEL.solve()
        self.TargetLoad = MODEL.objective.value()
        print('**************************************************************')
        print('**************************************************************')
        print('Generating the results ... ***********************************')
        print('**************************************************************')
        print('**************************************************************')
        if self.writefiles:
            file = open('Res_BMPs_SOTI_{}.txt'.format(self.C), 'w+')
            Counter = 0
            for i in self.NN:
                for t in self.TTi[i]:
                    try:
                        if Xit[(i, t)].value() > .5:
                            file.write(i)
                            file.write(',')
                            file.write(t)
                            file.write('\n')
                    except:
                        Counter = Counter + 1
            file.close()

            file = open('Res_Flow_SOTI_{}.txt'.format(self.C), 'w+')
            #
            for j in self.NN:
                for i in self.NNn_i[j]:
                    try:
            #            print('{} ==> {} : {}'.format(i, j, Fijm[(i,j,'P')].value() ) )
                        file.write('{}_{} {}\n'.format(i,j, str(sum(FijmTime[(i,j,self.ZZ[0],Time)].value() for Time in range(self.TimePeriod))) ))
                    except:
                        pass

            file.close()
            print('**************************************************************')
            print('**************************************************************')
            print('Solution is done. Find the results in the directory.**********')
        print('**************************************************************')
        print('**************************************************************')

    def Solve_MOTI_Det_Model(self):
        self.TargetLoad = 0
        self.singleObjResults = []
        sys.setrecursionlimit(3000)
        if self.TimePeriod <= 4:
            BigM = 99999
        else:
            BigM = 99999
        epsilon = 0.0001
        self.writefiles = False

        # Setting the target node
        self.Set_TargetLocation('1')
        bounddata = open('singleObjResults.csv', 'w+')
        for item in self.MM:
            ZZ = [item]
            self.Set_Objective(item)
            self.Set_BoundedMeasures([itm for itm in self.MM if itm not in ZZ ], [99999])
            for values in self.budgetList:
                self.Solve_SOTI_Det_Model(values)
                #self.Set_Cost_Budget(1500000)
                self.singleObjResults.append(self.TargetLoad)

        bounddata.write('Budget, P, N\n')
        for i in range(len(self.budgetList)):
            bounddata.write(str(self.budgetList[i])+','+str(self.singleObjResults[i])+','+str(self.singleObjResults[i+len(self.budgetList)]))
            if self.budgetList[i] != self.budgetList[-1]:
                bounddata.write('\n')

        self.writefiles = True
        time.sleep(1)

        """Read the bound data (single objective results) for P and N w.r.t their budgets"""
        bounddata = open('singleObjResults.csv')
        bounddata.readline()  # reading the header (the name of the header is of no concern to the algorithm.
        PhosphorusBound = []
        NitrogenBound = []

        while True:
            bd = bounddata.readline()
            bd = bd.strip('\n')
            if bd == '':
                break
            bd = bd.split(',')
            PhosphorusBound.append((int(bd[0]), float(bd[1])))
            NitrogenBound.append((int(bd[0]), float(bd[2])))

        pulp.PULP_CBC_CMD().msg = 0
        pulp.LpSolverDefault.msg = 0

        allpoints = []
        bounds = []

        print('**************************************************************')
        print('**************************************************************')
        print('Building the model ... ***************************************')
        print('**************************************************************')
        print('**************************************************************')
        # %% Modeling
        MODEL = pulp.LpProblem("Deterministic Time Indexed Model", pulp.LpMinimize)
        # Variables

        FijmTime = pulp.LpVariable.dicts('F', [(i, j, m, Time) for m in self.MM for i in self.NN for j in self.NNp_i[i] for Time in
                                               range(self.TimePeriod)], lowBound=0)
        for m in self.MM:
            for i in self.NN:
                for j in self.NNp_i[i]:
                    for Time in range(self.TimePeriod):
                        if i[-1] == 'a':
                            FijmTime[(i, j, m, Time)].lowBound = None

        Xit = pulp.LpVariable.dicts('X', {(i, t) for i in self.NN for t in self.TTi[i]}, lowBound=0, upBound=1, cat=pulp.LpInteger)
        YijmtTime = pulp.LpVariable.dicts('Y', {(i, j, m, t, Time) for j in self.NN for i in self.NNn_i[j] for m in self.MM for t in self.TTi[j] for Time in range(self.TimePeriod)}, lowBound=0)

        # Constraints
        ## Cons. 1
        for j in self.NN:
            if len(self.NNp_i[j]) > 1:
                continue
            for m in self.MM:
                if j != self.L:
                    for Time in range(self.TimePeriod):
                        MODEL += (pulp.lpSum([FijmTime[(i, j, m, Time)] for i in self.NNn_i[j]])
                                  - pulp.lpSum([FijmTime[(j, i, m, Time)] for i in self.NNp_i[j]])
                                  - pulp.lpSum([self.ALPHAtm[(t, m)] * YijmtTime[(i, j, m, t, Time)] for t in self.TTi[j] for i in self.NNn_i[j]])
                                  - pulp.lpSum([self.PimTime[(j, m, Time)] * self.ALPHAtm[(t, m)] * Xit[(j, t)] for t in self.TTi[j]]) <= -self.PimTime[(j, m, Time)]), 'C1_{}_{}_{}'.format(j, m, Time)
        for j in self.NN:
            if len(self.NNp_i[j]) > 1:
                continue
            for i in self.NNn_i[j]:
                for m in self.MM:
                    for t in self.TTi[j]:
                        for Time in range(self.TimePeriod):
                            MODEL += YijmtTime[(i, j, m, t, Time)] <= FijmTime[
                                (i, j, m, Time)], 'LC1_{}_{}_{}_{}_{}'.format(i, j, m, t, Time)
                            MODEL += YijmtTime[(i, j, m, t, Time)] <= BigM * Xit[(j, t)], 'LC2_{}_{}_{}_{}_{}'.format(i,
                                                                                                                      j,
                                                                                                                      m,
                                                                                                                      t,
                                                                                                                      Time)
                            MODEL += YijmtTime[(i, j, m, t, Time)] >= FijmTime[(i, j, m, Time)] - BigM * (
                                        1 - Xit[(j, t)]), 'LC3_{}_{}_{}_{}_{}'.format(i, j, m, t, Time)

        # Cons. 2
        for i in self.NN:
            MODEL += pulp.lpSum([Xit[(i, t)] for t in self.TTi[i]]) <= 1, 'C2_{}'.format(i)

        # Cons. 5
        for j in self.NNs:
            for k in self.NNp_i[j]:
                for m in self.MM:
                    for Time in range(self.TimePeriod):
                        MODEL += FijmTime[(j, k, m, Time)] == self.BETAij[(j, k)] * pulp.lpSum(
                            FijmTime[(i, j, m, Time)] for i in self.NNn_i[j]), 'C5_{}_{}_{}_{}'.format(j, k, m, Time)

        print('**************************************************************')
        print('**************************************************************')
        print('Solving the model ... ****************************************')
        print('**************************************************************')
        print('**************************************************************')

        """ Run the multi-objective optimization automation loop"""
        file1 = open('allPointsWithBounds.csv', 'w+')
        for item in self.MM:
            ZZ = [item]  # Set of Objectives
            ZZp = [itm for itm in self.MM if itm not in ZZ]  # Set of bounded measures
            # Objective
            MODEL.setObjective(
                pulp.lpSum([FijmTime[(i, self.L, ZZ[0], Time)] for i in self.NNn_i[self.L] for Time in range(self.TimePeriod)]))
            if item == 'P':
                for nb in NitrogenBound:
                    self.Um[ZZp[0]] = nb[1]
                    budgetLB = nb[0]
                    # Cons. 3
                    for m in ZZp:
                        # MODEL += pulp.lpSum([FijmTime[(i, L, m, Time)] for i in self.NNn_i[L] for Time in range(self.TimePeriod)]) <= (self.Um[m]*(1+epsilon)+epsilon), 'C3'
                        MODEL += pulp.lpSum(
                            [FijmTime[(i, self.L, m, Time)] for i in self.NNn_i[self.L] for Time in range(self.TimePeriod)]) <= self.Um[m], 'C3'
                    file1.write("****************************************************\n")
                    file1.write('Nitrogen is bounded to ' + str(round(self.Um['N'],3)) + ' and P is minimized\n')
                    file1.write("****************************************************\n")
                    file1.write('Budget, PhosphporusLoading, NitrogenLoading\n')
                    for budget in NitrogenBound:
                        if budget[0] >= budgetLB:
                            C = budget[0]
                            # Sol = MODEL.solve(pulp.CPLEX_PY())
                            # Cons. 4
                            MODEL += pulp.lpSum([self.Cit[(i, t)] * Xit[(i, t)] for i in self.NN for t in self.TTi[i]]) <= C, 'C4'

                            Sol = MODEL.solve()
                            minimalLoadP = MODEL.objective.value()
                            del MODEL.constraints['C4']
                            ## print(MODEL.status)
                            nitrogenValue = sum(
                                FijmTime[(i, self.L, m, Time)].varValue for i in self.NNn_i[self.L] for Time in range(self.TimePeriod))

                            file1.write(str(C) + ',' + str(round(minimalLoadP,3)) + ',' + str(round(nitrogenValue,3)) + '\n')
                            # print('{} in Lake when {} bound is {} for budget {}  = {}'.format('P','N',self.Um['N'], C, MODEL.objective.value()))
                            # print("Nitrogen Value is", nitrogenValue)
                            allpoints.append((C, round(minimalLoadP, 3), round(nitrogenValue, 3)))
                            bounds.append('N_' + str(round(self.Um['N'],3)))
                            BMPfile = open('BMPs_' + str(C) + 'bound_N_' + str(round(self.Um['N'],3)) + '.txt', 'w+')
                            CounterP = 0
                            BMPfile.write('Node, BMPs\n')
                            for i in self.NN:
                                for t in self.TTi[i]:
                                    try:
                                        if Xit[(i, t)].value() > 0.5:
                                            # print(("{}={}".format(Xit[(i,t)] ,Xit[(i,t)].value())))
                                            ind = i.find('_')
                                            if ind > 0:
                                                BMPfile.write(i[0:ind])
                                            else:
                                                BMPfile.write(i)
                                            BMPfile.write(',')
                                            ind = t.find('_')
                                            BMPfile.write(t[3:ind])
                                            BMPfile.write('\n')
                                            # print('Location i = {}, Technology t = {} => {}'.format(i, t, Xit[(i, t)].value()))
                                    except:
                                        CounterP = CounterP + 1
                                        # print('Location i = {}, Technology t = {} => {}'.format(i, t, 0))
                            BMPfile.close()

                            Flowfile = open('Flow_P' + str(C) + 'bound_N_' + str(round(self.Um['N'],3)) + '.txt', 'w+')
                            for j in self.NN:
                                for i in self.NNn_i[j]:
                                    try:
                                        # print('{} ==> {} : {}'.format(i, j, FijmTime[(i,j,'P',Time)].value() ) )
                                        Flowfile.write('{}_{} {}\n'.format(i, j, str(sum(
                                            FijmTime[(i, j, 'P', Time)].value() for Time in range(self.TimePeriod)))))
                                    except:
                                        pass
                                        # print('{} ==> {} : {}'.format(i, j, 0))
                            Flowfile.close()
                    del MODEL.constraints['C3']

            elif item == 'N':
                for pb in PhosphorusBound:
                    self.Um[ZZp[0]] = pb[1]
                    budgetLB = pb[0]
                    # Cons. 3
                    for m in ZZp:
                        MODEL += pulp.lpSum(
                            [FijmTime[(i, self.L, m, Time)] for i in self.NNn_i[self.L] for Time in range(self.TimePeriod)]) <= self.Um[m], 'C3'
                    file1.write("******************************************************\n")
                    file1.write('Phosphorous is bounded to ' + str(round(self.Um['P'],3)) + ' and N is minimized\n')
                    file1.write("******************************************************\n")
                    file1.write('Budget, PhosphporusLoading, NitrogenLoading\n')
                    for budget in PhosphorusBound:
                        if budget[0] >= budgetLB:
                            C = budget[0]
                            # Sol = MODEL.solve(pulp.CPLEX_PY())
                            # Cons. 4
                            MODEL += pulp.lpSum([self.Cit[(i, t)] * Xit[(i, t)] for i in self.NN for t in self.TTi[i]]) <= C, 'C4'

                            Sol = MODEL.solve()
                            minimalLoadN = MODEL.objective.value()
                            del MODEL.constraints['C4']
                            ## print(MODEL.status)
                            phosphorousValue = sum(
                                FijmTime[(i, self.L, m, Time)].varValue for i in self.NNn_i[self.L] for Time in range(self.TimePeriod))
                            file1.write(str(C) + ',' + str(round(phosphorousValue,3)) + ',' + str(round(minimalLoadN,3)) + '\n')
                            allpoints.append((C, round(phosphorousValue, 3), round(minimalLoadN, 3)))
                            bounds.append('P_' + str(round(self.Um['P'],3)))
                            # print('{} in Lake when {} bound is {} for budget {}  = {}'.format('N','P',self.Um['P'], C, MODEL.objective.value()))
                            # print("Phosphorous Value is", phosphorousValue)

                            BMPfile = open('BMPs_' + str(C) + 'bound_P_' + str(round(self.Um['P'],3)) + '.txt', 'w+')
                            BMPfile.write('Node, BMPs\n')
                            CounterN = 0
                            for i in self.NN:
                                for t in self.TTi[i]:
                                    try:
                                        if Xit[(i, t)].value() > 0.5:
                                            ind = i.find('_')
                                            if ind > 0:
                                                BMPfile.write(i[0:ind])
                                            else:
                                                BMPfile.write(i)
                                            BMPfile.write(',')
                                            ind = t.find('_')
                                            BMPfile.write(t[3:ind])
                                            BMPfile.write('\n')
                                            # print('Location i = {}, Technology t = {} => {}'.format(i, t, Xit[(i, t)].value()))
                                    except:
                                        CounterN = CounterN + 1
                                        # print('Location i = {}, Technology t = {} => {}'.format(i, t, 0))
                            BMPfile.close()

                            Flowfile = open('Flow_N' + str(C) + 'bound_P_' + str(round(self.Um['P'],3)) + '.txt', 'w+')
                            for j in self.NN:
                                for i in self.NNn_i[j]:
                                    try:
                                        # print('{} ==> {} : {}'.format(i, j, FijmTime[(i,j,'N',Time)].value() ) )
                                        Flowfile.write('{}_{} {}\n'.format(i, j, str(sum(
                                            FijmTime[(i, j, 'N', Time)].value() for Time in range(self.TimePeriod)))))
                                    except:
                                        pass
                                        # print('{} ==> {} : {}'.format(i, j, 0))
                            Flowfile.close()
                    del MODEL.constraints['C3']
        file1.close()

    #def find_non_dominated(points, bounds):
        file2 = open('NonDominatedPoints.csv', 'w+')
        file2.write('Budget, PhosphorousLoad, NitrogenLoad, Bounds\n')

        # non_dominated = []
        for i in range(len(allpoints)):
            dominated = False
            for j in range(len(allpoints)):
                if i != j and all(allpoints[j][k] <= allpoints[i][k] for k in range(len(allpoints[i]))):
                    dominated = True
                    break
            if not dominated:
                file2.write(str(allpoints[i]) + ',' + str(bounds[i]) + '\n')
                # non_dominated.append(points[i])
        file2.close()
        # return non_dominated

        #non_dominated_points = find_non_dominated(allpoints, bounds)
    # %%
    def Read_Data(self, Network, BMP_Tech, TimePeriod=1):
        self.TimePeriod = TimePeriod
        if isinstance(self.TimePeriod, int) != True:
            print("Please Enter integer values")
            return "Null"
        elif self.TimePeriod < 1:
            print("Please Enter the value of Time greater or equal to 1")
            return "Null"

        # Network ---------------------------------------------------------------
        if not os.path.exists(Network):
            print('The network file does not exist. Make sure you have entered the right directory')
            return

        if Network[-3:].lower() != 'csv':
            print('The network file must be a .csv file. Suffix is not csv!!!')
            return

        NetFile = open(Network)

        l = NetFile.readline()
        l = l.split(',')
        self.MM = ['P','N']
        print('The list of imported measures is: ', end='')
        #for i in range(4, len(l) - 1):
            #self.MM.append(l[i])
            #print(l[i], ', ', end='')
        print(self.MM)

        self.NN = []
        self.NNs = []
        self.NNp_i = {}
        self.NNn_i = {}
        self.PimTime = {}
        self.BETAij = {}
        self.TTi = {}  # Set of all Technologies that can be implemented in location i
        while True:
            l = NetFile.readline()
            if l == '':
                break
            l = l.split(',')
            self.NN.append(l[0])
            if l[1] != '':
                self.NNn_i[l[0]] = l[1].split(' ')
            else:
                self.NNn_i[l[0]] = []
            if l[2] != '':
                self.NNp_i[l[0]] = l[2].split(' ')
            else:
                self.NNp_i[l[0]] = []

            if len(self.NNp_i[l[0]]) > 1:
                self.NNs.append(l[0])
                temp = l[3].split(' ')
                assert (len(temp) == len(self.NNp_i[l[0]]))
                for j in range(len(temp)):
                    self.BETAij[(l[0], self.NNp_i[l[0]][j])] = float(temp[j])
            for Time in range(self.TimePeriod):
                self.PimTime[(l[0], 'P', Time)] = float(l[4+Time])
                self.PimTime[(l[0], 'N', Time)] = float(l[4+self.TimePeriod+Time])

            if l[4 + 2 * self.TimePeriod] != '\n':
                l[4 + 2 * self.TimePeriod] = l[4 + 2 * self.TimePeriod].strip(' \n')
                l[4 + 2 * self.TimePeriod] = l[4 + 2 * self.TimePeriod].strip('\n')
                self.TTi[l[0]] = l[4 + 2 * self.TimePeriod].split(' ')
            else:
                self.TTi[l[0]] = []

        NetFile.close()

        # Cost and effectiveness ---------------------------------------------------
        if not os.path.exists(BMP_Tech):
            print('The BMP/Technology information file does not exist. Make sure you have entered the right directory')
            return

        if BMP_Tech[-3:].lower() != 'csv':
            print('The BMP_Tech file must be a .csv file. The suffix is not csv!!!')
            return

        TBFile = open(BMP_Tech)
        l = TBFile.readline()
        l = l.strip('\n')
        Header = l.split(',')
        CostInd = 0
        for i in range(1, len(Header)):
            if Header[i].lower() == 'cost':
                CostInd = i
                break
        if CostInd == 0:
            print("Header of file '{}' has no attribute Cost".format(BMP_Tech))
            print(Header)
            return

        self.ALPHAtm = {};
        self.Cit = {};
        self.ALPHA_HATtm = {};
        while True:
            l = TBFile.readline()
            if l == '':
                break
            temp = {}
            l = l.split(',')
            # effectiveness
            for i in range(1, len(l)):
                if i == CostInd:
                    for j in self.NN:
                        if l[0] in self.TTi[j]:
                            self.Cit[(j, l[0])] = float(l[i])
                else:
                    ind = Header[i].find('_')
                    temp[(Header[i][0:ind], Header[i][ind + 1:])] = float(l[i]) / 100
            for m in self.MM:
                self.ALPHAtm[(l[0], m)] = (temp[(m, 'UB')] + temp[(m, 'LB')]) / 2
                self.ALPHA_HATtm[(l[0], m)] = temp[(m, 'UB')] - self.ALPHAtm[(l[0], m)]

        print('--------------------------------------------------------------')
        print('The data was successfully imported ***************************')
        print('--------------------------------------------------------------')

    # %% Set the budgets
    def Set_Cost_Budget(self, C):
        if C < 0:
            print('WARNING: the budget of the cost is negative.')
        self.C = C
        print('--------------------------------------------------------------')
        print('The cost budget was successfully set to {} ****************'.format(C))
        print('--------------------------------------------------------------')

    def Set_Budget_List(self, budgetList):
        if len(budgetList) < 0:
            print("WARNING: no budgets provided.")
        validBudgetList = []
        for value in budgetList:
            if isinstance(value, int) or isinstance(value, float):
                validBudgetList.append(value)
            else:
                raise ValueError("Invalid value type in Budget List: {}".format(value))
        self.budgetList = validBudgetList



    # %% Set the upper limit of measures
    def Set_Measure_Budget(self, Measure, Value):
        if type(Measure) == list:
            if (len(Measure) != len(Value)):
                print("ERROR: The number of entered measures and values does not match!!!")
                return
            else:
                if np.any(np.array(Value) < 0):
                    print("ERROR: Budget values cannot be negative")
                    print(Value)
                    return
                i = 0
                for m in Measure:
                    if not m in self.MM:
                        print(self.MM)
                        return
                    self.Um[m] = Value[i]
                    i += 1
        else:
            if not Measure in self.MM:
                print("ERROR: Measure '{}' is not among the imported measures:".format(Measure))
                print(self.MM)
                return
            elif Value < 0:
                print("ERROR: Budget values cannot be negative")
                return
            else:
                self.Um[Measure] = Value

            # %% Set the target location

    def Set_TargetLocation(self, location):
        if not (location in self.NN):
            if (self.NN == []):
                print("No network has been imported yet. Please read the network data using 'Read_Data'")
                return
            else:
                print(
                    "The entered location '{}' does exit not in the imported network. Make sure you enter a string.".format(
                        location))
                return
        self.L = location

    # %% Set the single Objective
    def Set_Objective(self, Objective_Measure):
        if not (Objective_Measure in self.MM):
            if self.MM == []:
                print(
                    "The list of measure has been imported yet. Please read the network data using 'Read_Data' first.")
                return
            else:
                print(
                    "The entered measure '{}' does exit not in the list of measures. Make sure you enter a string.".format(
                        Objective_Measure))
                print(self.MM)
                return
        self.ZZ = [Objective_Measure]  # Set of Objectives

    # %% Set the limits of the bounded objectives
    def Set_BoundedMeasures(self, Measures, Bounds):
        if not (IsSubset(Measures, self.MM)):
            if self.MM == []:
                print(
                    "The list of measure has not been imported yet. Please read the network data using 'Read_Data' first.")
                return
            else:
                print(
                    "At least one of the entered measures '{}' does not exit in the list of measures. Make sure you enter a string.".format(
                        Measures))
                print(self.MM)
                return
        self.ZZp = Measures  # Set of bounded measures
        self.Um = {}
        for i in range(len(self.ZZp)):
            self.Um[self.ZZp[i]] = Bounds[i]

        # %% Set the solver
        def Set_Solver(solver):
            if not solver in pulp.listSolvers(onlyAvailable=True):
                print('ERROR: solver {} is not available on your system!'.format(solver))
                return
            self.Solver = solver
            print('Solver is properly set to {}'.format(solver))


# %%
def IsSubset(X, Y):
    return len(np.setdiff1d(X, Y)) == 0