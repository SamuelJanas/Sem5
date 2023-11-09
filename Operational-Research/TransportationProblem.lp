\* Transportation_Problem *\
Minimize
Sum_of_Transporting_Costs: 5 Route_0_0 + 8 Route_0_1 + 3 Route_0_2
 + 4 Route_0_3 + 9 Route_0_4 + 7 Route_1_0 + 5 Route_1_1 + 9 Route_1_2
 + 10 Route_1_3 + 999 Route_1_4 + 2 Route_2_0 + 9 Route_2_1 + 8 Route_2_2
 + 9 Route_2_4 + 5 Route_3_0 + 5 Route_3_1 + 3 Route_3_2 + 5 Route_3_3
 + 8 Route_3_4 + 999 Route_4_0 + 5 Route_4_1 + 2 Route_4_2 + 9 Route_4_3
Subject To
Demand_0: Route_0_0 + Route_1_0 + Route_2_0 + Route_3_0 + Route_4_0 >= 0
Demand_1: Route_0_1 + Route_1_1 + Route_2_1 + Route_3_1 + Route_4_1 >= 0
Demand_2: Route_0_2 + Route_1_2 + Route_2_2 + Route_3_2 + Route_4_2 >= 0
Demand_3: Route_0_3 + Route_1_3 + Route_2_3 + Route_3_3 + Route_4_3 >= 0
Demand_4: Route_0_4 + Route_1_4 + Route_2_4 + Route_3_4 + Route_4_4 >= 0
Supply_0: Route_0_0 + Route_0_1 + Route_0_2 + Route_0_3 + Route_0_4 <= 0
Supply_1: Route_1_0 + Route_1_1 + Route_1_2 + Route_1_3 + Route_1_4 <= 0
Supply_2: Route_2_0 + Route_2_1 + Route_2_2 + Route_2_3 + Route_2_4 <= 0
Supply_3: Route_3_0 + Route_3_1 + Route_3_2 + Route_3_3 + Route_3_4 <= 0
Supply_4: Route_4_0 + Route_4_1 + Route_4_2 + Route_4_3 + Route_4_4 <= 0
Bounds
 0 <= Route_0_0
 0 <= Route_0_1
 0 <= Route_0_2
 0 <= Route_0_3
 0 <= Route_0_4
 0 <= Route_1_0
 0 <= Route_1_1
 0 <= Route_1_2
 0 <= Route_1_3
 0 <= Route_1_4
 0 <= Route_2_0
 0 <= Route_2_1
 0 <= Route_2_2
 0 <= Route_2_3
 0 <= Route_2_4
 0 <= Route_3_0
 0 <= Route_3_1
 0 <= Route_3_2
 0 <= Route_3_3
 0 <= Route_3_4
 0 <= Route_4_0
 0 <= Route_4_1
 0 <= Route_4_2
 0 <= Route_4_3
 0 <= Route_4_4
Generals
Route_0_0
Route_0_1
Route_0_2
Route_0_3
Route_0_4
Route_1_0
Route_1_1
Route_1_2
Route_1_3
Route_1_4
Route_2_0
Route_2_1
Route_2_2
Route_2_3
Route_2_4
Route_3_0
Route_3_1
Route_3_2
Route_3_3
Route_3_4
Route_4_0
Route_4_1
Route_4_2
Route_4_3
Route_4_4
End
