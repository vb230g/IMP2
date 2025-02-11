def read_cost_matrix():
    """Reads a cost matrix from a file with a specific format."""
    with open("imp2cost.txt", 'r') as f:
        lines = [line.strip().split(',') for line in f.readlines()]
    headers = lines[0][1:]  
    x = {char: i for i, char in enumerate(headers)}
    y = x.copy()  
    cost_matrix = []
    for row in lines[1:]:  
        cost_matrix.append([int(val) for val in row[1:]]) 

    return cost_matrix, x, y


def dp():
    cost_matrix, x, y = read_cost_matrix()

    with open("imp2output.txt", "w") as output_file:
        with open("imp2input.txt", "r") as file:
            for line in file:
                line = line.strip()
                subseq = line.split(",")
                seq1, seq2 = subseq
                m, n = len(seq1), len(seq2)
                dp_table = [[0] * (n + 1) for _ in range(m + 1)] 
                trace = [[None] * (n + 1) for _ in range(m + 1)]

                for i in range(1, m + 1):
                    dp_table[i][0] = dp_table[i - 1][0] + cost_matrix[x[seq1[i - 1]]][x['-']]  
                    trace[i][0] = (i - 1, 0)
                for j in range(1, n + 1):
                    dp_table[0][j] = dp_table[0][j - 1] + cost_matrix[x['-']][x[seq2[j - 1]]]  
                    trace[0][j] = (0, j - 1)

                for i in range(1, m + 1):
                    for j in range(1, n + 1):
                        match_mismatch = dp_table[i - 1][j - 1] + cost_matrix[x[seq1[i - 1]]][x[seq2[j - 1]]]
                        insertion = dp_table[i][j - 1] + cost_matrix[x['-']][x[seq2[j - 1]]]
                        deletion = dp_table[i - 1][j] + cost_matrix[x[seq1[i - 1]]][x['-']]
                        min_cost = min(match_mismatch, insertion, deletion)

                        dp_table[i][j] = min_cost

                       
                        if min_cost == match_mismatch:
                            trace[i][j] = (i - 1, j - 1)
                        elif min_cost == insertion:
                            trace[i][j] = (i, j - 1)
                        else:
                            trace[i][j] = (i - 1, j)

                align1, align2 = "", ""
                i, j = m, n
                while i > 0 or j > 0:
                    if trace[i][j] == (i - 1, j - 1):
                        align1 = seq1[i - 1] + align1
                        align2 = seq2[j - 1] + align2
                        i, j = i - 1, j - 1
                    elif trace[i][j] == (i, j - 1):
                        align1 = "-" + align1
                        align2 = seq2[j - 1] + align2
                        j -= 1
                    else:
                        align1 = seq1[i - 1] + align1
                        align2 = "-" + align2
                        i -= 1

               
                output_file.write(f"{align1},{align2}:{dp_table[m][n]}\n")

dp()



