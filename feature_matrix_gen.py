from matplotlib import pyplot as plt
import numpy as np
min_gap_size = 2
sekwencje = open('representative_alignment.fasta').readlines()
sekwencje = [i for i in sekwencje if '>' not in i]

# Wersja precyzyjna z uwzględnianiem pojedynczych gapów.
sectors_positions = []
is_Gap = True
gap_counter = 1
for i in range(len(sekwencje)):
    for i1 in range(len(sekwencje[i])):
        if is_Gap:
            if sekwencje[i][i1] != "-":
                if gap_counter > 5:
                    sectors_positions.append(i1)
                    is_Gap = False
                    gap_counter = 1
                else:
                    # is_Gap = False
                    gap_counter = 1
            else:
                gap_counter += 1
        else:
            if sekwencje[i][i1] == "-":
                sectors_positions.append(i1)
                is_Gap = True

sectors_positions = list(dict.fromkeys(sectors_positions))
sectors_positions.sort()

matrix = []

temp_list = []
for i in range(len(sekwencje)):
    for i1 in sectors_positions:
        if sekwencje[i][i1] == "-":
            temp_list.append(0)
        else:
            temp_list.append(1)
    matrix.append(temp_list)
    temp_list = []

matrix_numpy = np.array(matrix)
# print(matrix_numpy)

np.savetxt('test_matrix.csv', matrix_numpy, fmt='%1i', delimiter=',')

a = plt.imshow(matrix)
plt.colorbar()
plt.savefig("new1")
plt.show()