import modeler
DATA = {}

for N in range(11, 13):
    print("Processing N = ", N)
    DATA[N] = {}
    D = {"3-chunks": modeler.Modeler(),
         "3-chunks-o": modeler.Modeler(),
         "bin-tree": modeler.Modeler()}

    for k in D:
        print("processing k = ", k)
        Z = D[k]
        for i in range(N+1):
            for j in range(N):
                Z.add_var(f"x_{i, j}", description=f"Element {i} maps to {j}")

        # at least one per i
        for i in range(N+1):
            Z.add_clause([f"x_{i, j}" for j in range(N)])

        # at most one per j
        for j in range(N):
            Z.at_most_one([f"x_{i, j}" for i in range(N+1)], type=k)

        DATA[N][k] = {"vars": Z.n_vars(),
                      "clauses": Z.n_clauses()}

        proof, time = Z.solve_with_proof()
        DATA[N][k]["proof_length"] = len(proof)
        DATA[N][k]["time"] = time / 1e9

for N_key in DATA.keys():
    print(f"N = {N_key}")
    for d_k in DATA[N_key].keys():
        print(f"    Enc = {d_k}. Results = {DATA[N_key][d_k]}")
    print("-"*20)
