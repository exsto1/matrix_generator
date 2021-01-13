from tqdm import tqdm

seq = open("all_files/representative_alignment.fasta").readlines()
seq = [i.rstrip() for i in seq if ">" in i]
matrix = open("all_files/test_matrix_new.csv").readlines()
matrix = [i.rstrip().split(",") for i in matrix]
output_file = open("all_files/new_alignment_reduced.fasta").readlines()
output_file = [i.rstrip() for i in output_file]
used = []
result_filename = "all_files/result.fasta"
result = open(result_filename, "w")

seq_len = len(output_file[1].rstrip())
matrix_len = len(matrix[0])


for i in tqdm(range(len(output_file))):
    if ">" in output_file[i]:
        state = False
        result.write(output_file[i] + "\n")
        id = output_file[i].split("_")[0].lstrip(">")
        for i1 in range(len(seq)):
            if id in seq[i1]:
                if seq[i1] not in used:
                    used.append(seq[i1])
                    # output_file[i+1] += "".join(matrix[i1]).replace("1", "X").replace("0", "-")
                    output_file[i + 1] += "".join(matrix[i1])
                    result.write(output_file[i+1] + "\n")
                    state = True
                    break
        if not state:
            result.write(output_file[i+1] + "-" * matrix_len + "\n")
result.close()


print("begin mrbayes;")
print(f"charset seq = 1-{seq_len};")
print(f"charset mat1 = {seq_len + 1}-.;")
print("partition favored = 2: seq, mat1;")
print("prset aamodelpr=fixed(vt);")
print("mcmc ngen=5000000;")
print("end;")
print("----")
print(f"Format datatype=mixed(Protein:1-{seq_len},Standard:{seq_len + 1}-{seq_len+matrix_len}) gap=- missing=?;")

