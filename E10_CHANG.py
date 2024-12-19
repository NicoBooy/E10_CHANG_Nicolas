import heapq

# Input Data
profits = [15, 20, 5, 25, 22, 17]
weights = [51, 60, 35, 60, 53, 10]

total_days = 100  # Set the limit here

# Define the Branch and Bound node
class Node:
    def __init__(self, level, profit, weight, bound, items):
        self.level = level  # Current project index
        self.profit = profit  # Total profit so far
        self.weight = weight  # Total days so far
        self.bound = bound  # Upper bound of the node
        self.items = items  # List of chosen projects

    def __lt__(self, other):
        return self.bound > other.bound  # Max heap based on bound

# Function to calculate upper bound
def calculate_bound(node, profits, weights, total_days):
    if node.weight >= total_days:
        return 0
    bound = node.profit
    j = node.level + 1
    total_weight = node.weight
    
    # Greedy filling of knapsack to compute bound
    while j < len(profits) and total_weight + weights[j] <= total_days:
        total_weight += weights[j]
        bound += profits[j]
        j += 1
    
    # If room left, add fraction of next project
    if j < len(profits):
        bound += (total_days - total_weight) * (profits[j] / weights[j])
    return bound

# Branch and Bound Knapsack Solver
def knapsack_branch_and_bound(profits, weights, total_days):
    n = len(profits)
    # Initial root node
    root = Node(level=-1, profit=0, weight=0, bound=0, items=[])
    root.bound = calculate_bound(root, profits, weights, total_days)
    max_profit = 0
    best_items = []

    # Priority Queue for Branch and Bound
    pq = []
    heapq.heappush(pq, root)

    while pq:
        current = heapq.heappop(pq)

        if current.bound > max_profit:  # Only explore promising nodes
            # Include the next project
            next_level = current.level + 1
            if next_level < n:
                # Create node including this project
                include = Node(level=next_level,
                               profit=current.profit + profits[next_level],
                               weight=current.weight + weights[next_level],
                               bound=0,
                               items=current.items + [next_level])
                if include.weight <= total_days and include.profit > max_profit:
                    max_profit = include.profit
                    best_items = include.items
                include.bound = calculate_bound(include, profits, weights, total_days)
                if include.bound > max_profit:
                    heapq.heappush(pq, include)

                # Create node excluding this project
                exclude = Node(level=next_level,
                               profit=current.profit,
                               weight=current.weight,
                               bound=0,
                               items=current.items)
                exclude.bound = calculate_bound(exclude, profits, weights, total_days)
                if exclude.bound > max_profit:
                    heapq.heappush(pq, exclude)

    return max_profit, best_items

# Solve the problem
max_profit, best_projects = knapsack_branch_and_bound(profits, weights, total_days)
print("Maximum Profit:", max_profit)
print("Selected Projects:", [i + 1 for i in best_projects])
