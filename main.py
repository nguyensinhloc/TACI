# TACI problem: given a 3x3 matrix of numbers, find the minimum number of swaps to sort the matrix in ascending order
# AKT: Algorithm for Knowledgeable Tree Search, a heuristic search algorithm that uses domain knowledge to guide the search

# Define a function to check if a matrix is sorted
def is_sorted(matrix):
    # A matrix is sorted if each row and column is sorted in ascending order
    for i in range(3):
        for j in range(2):
            if matrix[i][j] > matrix[i][j + 1] or matrix[j][i] > matrix[j + 1][i]:
                return False
    return True


# Define a function to swap two elements in a matrix
def swap(matrix, i1, j1, i2, j2):
    # Swap the elements at (i1, j1) and (i2, j2) in the matrix
    temp = matrix[i1][j1]
    matrix[i1][j1] = matrix[i2][j2]
    matrix[i2][j2] = temp


# Define a function to generate the successors of a state
def successors(state):
    # A successor is a state obtained by swapping any two adjacent elements in the matrix
    # Return a list of tuples (successor, action), where action is a string describing the swap
    succ = []
    for i in range(3):
        for j in range(2):
            # Swap horizontally
            new_state = [row[:] for row in state]  # Make a copy of the state
            swap(new_state, i, j, i, j + 1)
            action = f"Swap ({i}, {j}) and ({i}, {j + 1})"
            succ.append((new_state, action))
            # Swap vertically
            new_state = [row[:] for row in state]  # Make a copy of the state
            swap(new_state, j, i, j + 1, i)
            action = f"Swap ({j}, {i}) and ({j + 1}, {i})"
            succ.append((new_state, action))
    return succ


# Define a heuristic function to estimate the cost to reach the goal from a state
def heuristic(state):
    # The heuristic is the number of inversions in the matrix, i.e. the number of pairs of elements that are out of order
    inv = 0
    for i in range(3):
        for j in range(3):
            for k in range(i, 3):
                for l in range(j if k == i else 0, 3):
                    if state[i][j] > state[k][l]:
                        inv += 1
    return inv


# Define a function to print a matrix
def print_matrix(matrix):
    for row in matrix:
        print(row)

# Ask the user to enter a 3x3 matrix
print("Please enter a 3x3 matrix of numbers:")
matrix = []
for i in range(3):
    row = input(f"Enter row {i + 1} (separate numbers by spaces): ").split()
    row = [int(x) for x in row]
    matrix.append(row)

# Print the initial state
print("The initial state is:")
print_matrix(matrix)

# Apply AKT to find the solution
# Initialize the frontier as a priority queue of tuples (cost, state, path)
# where cost is the total estimated cost (g + h), state is the current state,
# and path is the list of actions taken so far
import heapq

frontier = []
heapq.heappush(frontier, (heuristic(matrix), matrix, []))
# Initialize the explored set as an empty set
explored = set()
# Loop until the frontier is empty or the goal is found
while frontier:
    # Pop the state with the lowest cost from the frontier
    cost, state, path = heapq.heappop(frontier)
    # Check if the state is the goal
    if is_sorted(state):
        # Print the solution and exit the loop
        print("The solution is:")
        for action in path:
            print(action)
        print("The final state is:")
        print_matrix(state)
        break
    # Add the state to the explored set
    explored.add(tuple(map(tuple, state)))  # Convert the state to a hashable tuple of tuples
    # Generate the successors of the state
    for succ, action in successors(state):
        # Check if the successor is already explored or in the frontier
        if tuple(map(tuple, succ)) not in explored and not any(s[1] == succ for s in frontier):
            # Calculate the cost of the successor
            g = len(path) + 1  # The cost so far is the length of the path plus one
            h = heuristic(succ)  # The estimated cost to the goal is the heuristic value
            f = g + h  # The total cost is the sum of g and h
            # Add the successor to the frontier with the updated cost and path
            heapq.heappush(frontier, (f, succ, path + [action]))
# If the frontier is empty and the goal is not found, print a message
else:
    print("No solution found.")
