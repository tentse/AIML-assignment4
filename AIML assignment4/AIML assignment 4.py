import heapq

# Define the goal state
goal_state = (1, 2, 3, 8, 0, 4, 7, 6, 5)  # 0 represents the blank tile

# Define the heuristic function (Manhattan distance)
def heuristic(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            tile = state[i*3 + j]
            if tile != 0:
                goal_row = (tile - 1) // 3
                goal_col = (tile - 1) % 3
                distance += abs(goal_row - i) + abs(goal_col - j)
    return distance

# Define a function to get possible moves
def get_moves(state):
    moves = []
    blank_index = state.index(0)
    row, col = divmod(blank_index, 3)

    deltas = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up

    for dr, dc in deltas:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_index = new_row * 3 + new_col
            new_state = list(state)
            new_state[blank_index], new_state[new_index] = new_state[new_index], new_state[blank_index]
            moves.append(tuple(new_state))
    return moves

# Define the A* search algorithm
def astar(start_state):
    open_set = [(heuristic(start_state), 0, start_state)]
    heapq.heapify(open_set)
    came_from = {}
    g_score = {start_state: 0}

    while open_set:
        _, cost, current = heapq.heappop(open_set)
        if current == goal_state:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start_state)
            path.reverse()
            return path
        for neighbor in get_moves(current):
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                heapq.heappush(open_set, (tentative_g_score + heuristic(neighbor), tentative_g_score, neighbor))

# Example usage
initial_state = (2, 8, 3, 1, 6, 4, 7, 0, 5)  # Initial state example
solution_path = astar(initial_state)
if solution_path:
    print("Solution found in", len(solution_path) - 1, "moves:")
    for state in solution_path:
        print(state[:3])
        print(state[3:6])
        print(state[6:])
        print()
else:
    print("No solution found.")
