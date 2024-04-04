from AquaNutriOpt import *

Example= EPA()
Example.Read_Data('Net_Data.csv','BMP_Tech.csv')

#Setting the cost budget
Example.Set_Cost_Budget(100000)

#Setting the target node
Example.Set_TargetLocation('1')

Example.Set_BoundedMeasures(['N'],[0])
Example.Set_Objective('P')

#Solving single objective model
Example.Solve_SO_Det_Model()


""" Single Objective Time Indexed Model """

Example.Read_Data('Net_Data.csv','BMP_Tech.csv', 5)


Example.Set_BoundedMeasures(['P'],[99999])

Example.Set_Objective('N')

Example.Solve_SOTI_Det_Model()

#Example.Set_Measure_Budget('N',99999)

"""FOR Multi Objective Time Indexed Model (Objectives will be to minimize P, N, Budget)"""

# Setting Budget List (Give Inputs of the budgets you wish to run experiments for)
Example.Set_Budget_List([100000, 500000, 1000000, 1500000, 2000000, 2500000, 3000000, 3500000, 4000000])
# Setting the target node
# Example.Set_TargetLocation('1')
Example.Solve_MOTI_Det_Model()