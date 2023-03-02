from Making_Prediction_Class import Making_Prediction
import os


li = [["A",[[0.0,1.0]]],["B",[[0.0,0.9]]],["C",[[0.0,0.4]]]]
li2 = [["A",[[0.0,1.0]]],["A",[[0.0,0.9]]],["A",[[0.0,0.4]]]]
li3 = [["A",[[0.0,1.0]]],["B",[[0.0,1.0]]],["C",[[0.0,1.0]]]]
li4 = [["A",[[0.0,1.0]]],["A",[[0.0,1.0]]],["A",[[0.0,1.0]]]]

list_all = [li,li2,li3,li4]

for lists in list_all:
    print("------------------------------------------------------------------\n\n")
    print("Using List: ",lists,"\n")
    mp = Making_Prediction()
    mp.create_confidence_stack(lists)
    print(mp.final_prediction())
