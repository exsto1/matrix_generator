from tqdm import tqdm
from matplotlib import pyplot as plt
import numpy as np
sequences = open('all_files/representative_alignment.fasta').readlines()
sequences = [i for i in sequences if '>' not in i]

"""
                                                                                                                                  @                                                                                           
---------------------|--------------------------|AAAAAAAAAAAAAAA-AAAAAAAA-AAAA-AAAA-AAAAA|-------------|-|AAAAAAA-AAAAAA|-------|A|---------------------

AAAAAAAAAAAAAAAAAAAAA|--------------------------|AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA|-AAAAAAAAAAAA|-|--------------|--------AAA


0010010
1011000

"""


min_gap_size = 2
start = []
end = []


for i in tqdm(range(len(sequences))):
    gaps = 0
    isGap = True
    for i1 in range(len(sequences[i])):
        if sequences[i][i1] == "-":
            gaps += 1
            if gaps >= min_gap_size:
                if isGap is False:
                    end.append(i1 - min_gap_size)
                    isGap = True
        else:
            if isGap is True:
                start.append(i1)
                isGap = False
            gaps = 0
    if isGap is False:
        end.append(len(sequences[i]) - 1)
    else:
        if gaps < min_gap_size:
            end.append(len(sequences[i]) - 1)



"""

-----TTTTTTTTTTTT--------
----------------AAA------
-------AAAAAAAAAAAAA-----
-------AAAAAAAAAA--------
-------AAAAAAA-----------


-----TTTTTTTTTTTT--------
-----AAAAAAAAAAAAAAAA----
-----AAAAAAAAAAAA--------
-----AAAAAAA-------------

-----TTTTTTTTTTTT--------
---AAAAAAAAAAAAAAAA------
---AAAAAAAAAAAAAA--------
---AAAAAAA---------------
---A---------------------


----AAAA---AAAAA----AAAAA---
----BBBBBBBBBBBBBBBBBBBBB---
----------CCCCCCCCCCCCCCC---
"""

template = [[start[0], end[0]]]

for i in tqdm(range(1, len(start))):
    state = False
    for i1 in range(len(template)):
        t_start = template[i1][0]
        t_end = template[i1][1]
        # if start[i] > t_end:
        #     pass
        if t_start < start[i] <= t_end:
            template[i1] = [t_start, start[i] - 1]
            if end[i] > t_end:
                template.append([start[i], t_end])
                template.append([t_end+1, end[i]])
                state = True
            elif end[i] == t_end:
                template.append([start[i], t_end])
                state = True
            elif end[i] < t_end:
                template.append([start[i], end[i]])
                template.append([end[i] + 1, t_end])
                state = True
            break
        elif t_start == start[i]:
            if end[i] > t_end:
                template.append([t_end+1, end[i]])
                state = True
            elif end[i] < t_end:
                template[i1] = [t_start, end[i]]
                template.append([end[i] + 1, t_end])
                state = True
            elif end[i] == t_end:
                state = True
            break
        elif start[i] < t_start:
            if end[i] > t_end:
                template.append([start[i], t_start - 1])
                template.append([t_end+1, end[i]])
                state = True
            elif end[i] == t_end:
                template[i1] = [start[i], t_start - 1]
                state = True
            elif t_start < end[i] < t_end:
                template[i1] = [start[i], t_start - 1]
                template.append([t_start, end[i]])
                template.append([end[i] + 1, t_end])
                state = True
            break
    if not state:
        template.append([start[i], end[i]])
    template.sort(key=lambda i: i[0])
    # print(template)

template_unique = []
for i in template:
    if i not in template_unique:
        template_unique.append(i)
template_unique.sort(key=lambda i: 1000 * i[0] + i[1])
template_unique = [i for i in template_unique if i[1] - i[0] > min_gap_size]

final_template = []

current_position = 0

for i in tqdm(range(len(template_unique))):
    if template_unique[i][0] > current_position:
        state = True
        i1=0
        while state is True:
            i1 += 1
            if template_unique[i+i1][0] != template_unique[i][0]:
                state = False
        final_template.append([current_position, template_unique[i + i1 - 1][1]])
        current_position = template_unique[i+i1-1][1] + 1
        # final_template.append([current_position, template_unique[i][1]])
        # current_position = template_unique[i][1] + 1

print(final_template)
matrix = []


for i in tqdm(range(len(sequences))):
    temp = []
    for i1 in range(len(final_template)):
        gaps_counter = 0
        for i2 in sequences[i][final_template[i1][0]: final_template[i1][1]+1]:
            if i2 == "-":
                gaps_counter += 1
        if gaps_counter/(final_template[i1][1]-final_template[i1][0]) > 0.5:
            temp.append(0)
        else:
            temp.append(1)
    matrix.append(temp)



sum_list = []
for i1 in range(len(final_template)):
    sum_value = sum([1 for i in range(len(matrix)) if matrix[i][i1] == 1])
    sum_list.append(round(sum_value/len(matrix), 2))

matrix = [[matrix[i][i1] for i1 in range(len(matrix[i])) if 0.03 < sum_list[i1] < 0.8] for i in range(len(matrix))]

matrix_numpy = np.array(matrix)

np.savetxt('test_matrix_new.csv', matrix_numpy, fmt='%1i', delimiter=',')

a = plt.imshow(matrix)
plt.colorbar()
plt.savefig("new2")
plt.show()
