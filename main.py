import simulation
from vpython import *
import csv
import numpy as np


# i,j = simulation.run(leg_strength=2000, torque= vector(0,203,0), pull_in_time= 0.1)

leg_range = np.arange(1382, 2000, 10)
torque_range = np.arange(200, 250.1, 1)
pull_in_range = np.arange(0.14,.211, 0.01)

variables = [['leg_strength', 'torque', 'pull_in_time', 'jump time', 'rotations']]



for i in leg_range:
    for j in torque_range:
        for k in pull_in_range:
            time, result = simulation.run(i,vector(0,j,0),k)
            variables.append([i, j, k, time, result])


            print(i,j,k)

# for i in (2000,2001,2002):
#     for j in (200, 200.1, 200.2):
#         for k in (0.1,0.11,0.12):
#             time, result = simulation.run(i,vector(0,j,0),k)
#             variables.append([i, j, k, time, result])
#             print(i,j,k)



with open("Figure Skating Data.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(variables[0])
    writer.writerows(variables[1:])
