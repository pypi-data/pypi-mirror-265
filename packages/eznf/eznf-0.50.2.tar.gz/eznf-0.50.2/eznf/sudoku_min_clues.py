""" argparse is used to parse CLI arguments."""
import argparse
import modeler


argparser = argparse.ArgumentParser()
argparser.add_argument(
    "-b", "--bound", type=int, default=16, help="Minimum number of clues"
)

args = argparser.parse_args()
clue_bound = args.bound
BOARD_SIZE = 9


def encode_sudoku(clue_bd):
    """
    Encodes a Sudoku puzzle into a SAT problem.

    Parameters:
    - clue_bd (int): The maximum number of clues allowed in the Sudoku puzzle.

    Returns:
    - enc (Modeler): An instance of the Modeler class representing the encoded Sudoku problem.
    """

    enc = modeler.Modeler()

    # Add variables for each cell and number
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            enc.add_var(f"d_{i, j}")
            enc.add_var(f"c_{i, j}")
            for n in range(1, 10):
                enc.add_var(f"x_{i, j, n}")
                enc.add_var(f"y_{i, j, n}")
                enc.add_var(f"c_{i, j, n}")

    # Each cell gets exactly one number
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            enc.exactly_one([f"x_{i, j, n}" for n in range(1, 10)])
            enc.exactly_one([f"y_{i, j, n}" for n in range(1, 10)])

    # At most one clue per cell
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            enc.at_most_one([f"c_{i, j, n}" for n in range(1, 10)])

    # Semantics for the d_{i, j} variables
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            for n in range(1, 10):
                enc.constraint(f"(x_{i, j, n} & y_{i, j, n}) -> -d_{i, j}")
    
    # Semantics for the c_{i, j} variables
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            enc.add_clause([f"-c_{i, j}"] + [f"c_{i, j, n}" for n in range(1, 10)])
            

    # Non-unique solution
    enc.add_clause([f"d_{i, j}" for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)])
        
    #  At most `clue_bd` clues
    clue_vars = [
        f"c_{i, j}"
        for i in range(BOARD_SIZE)
        for j in range(BOARD_SIZE)
    ]
    enc.at_least_k(clue_vars, k=clue_bd)
    # enc.add_kconstraint(bound=clue_bd, variables=clue_vars)

    # Both the x-solution and y-solution are valid
    ## They respect the clues
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            for n in range(1, 10):
                enc.constraint(f"c_{i, j, n} -> x_{i, j, n}")
                enc.constraint(f"c_{i, j, n} -> y_{i, j, n}")
    ## They respect the exactly_one constraints
    for n in range(1, 10):
        # Rows
        for i in range(BOARD_SIZE):
            enc.exactly_one([f"x_{i, j, n}" for j in range(BOARD_SIZE)])
            enc.exactly_one([f"y_{i, j, n}" for j in range(BOARD_SIZE)])
        # Columns
        for j in range(BOARD_SIZE):
            enc.exactly_one([f"x_{i, j, n}" for i in range(BOARD_SIZE)])
            enc.exactly_one([f"y_{i, j, n}" for i in range(BOARD_SIZE)])
        # Sub-grids
        sgrid_size = int(BOARD_SIZE**0.5)
        assert sgrid_size == 3
        sub_grids = [[[] for _ in range(sgrid_size)] for _ in range(sgrid_size)]
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                sub_grids[i // sgrid_size][j // sgrid_size].append((i, j))
        for si in range(sgrid_size):
            for sj in range(sgrid_size):
                enc.exactly_one([f"x_{*cell, n}" for cell in sub_grids[si][sj]])
                enc.exactly_one([f"y_{*cell, n}" for cell in sub_grids[si][sj]])

    return enc


encoding = encode_sudoku(clue_bound)
encoding.serialize(f"sudoku-min-clues-{clue_bound}.cnf")


def print_sudoku(sudoku_mat):
    for row in sudoku_mat:
        print(" ".join(row))

def decode_sudoku(model):
    clues = [["-" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    x_sol = [["-" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    y_sol = [["-" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    diff = [["-" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    for i in range(9):
        for j in range(9):
            if model[f"d_{i, j}"]:
                diff[i][j] = "D"
            for n in range(1, 10):
                if model[f"c_{i, j, n}"]:
                    clues[i][j] = str(n)
                if model[f"x_{i, j, n}"]:
                    x_sol[i][j] = str(n)
                if model[f"y_{i, j, n}"]:
                    y_sol[i][j] = str(n)
                
    print("Clues:")
    print_sudoku(clues)
    print("\nX-Solution:")
    print_sudoku(x_sol)
    print("\nY-Solution:")
    print_sudoku(y_sol)
    print("\nDiff:")
    print_sudoku(diff)
    
    
# encoding.solve_and_decode(decode_sudoku, solver="kcadical")
