"""Knapsack Problem Algorithms"""


def knapsack_dp(weights, values, capacity):
    """0/1 Knapsack using Dynamic Programming"""
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(
                    values[i - 1] + dp[i - 1][w - weights[i - 1]],
                    dp[i - 1][w]
                )
            else:
                dp[i][w] = dp[i - 1][w]
    
    return dp[n][capacity]


def knapsack_backtracking(weights, values, capacity, index=0, current_weight=0, current_value=0):
    """0/1 Knapsack using Backtracking"""
    if index == len(weights):
        return current_value
    
    # Exclude current item
    exclude = knapsack_backtracking(weights, values, capacity, index + 1, current_weight, current_value)
    
    # Include current item if it fits
    include = 0
    if current_weight + weights[index] <= capacity:
        include = knapsack_backtracking(
            weights, values, capacity, index + 1,
            current_weight + weights[index],
            current_value + values[index]
        )
    
    return max(include, exclude)


def knapsack_branch_bound(weights, values, capacity):
    """0/1 Knapsack using Branch and Bound"""
    n = len(weights)
    items = [(values[i] / weights[i], weights[i], values[i], i) for i in range(n)]
    items.sort(reverse=True)
    
    def bound(index, current_weight, current_value):
        if current_weight >= capacity:
            return current_value
        
        upper = current_value
        remaining = capacity - current_weight
        
        for i in range(index, n):
            if items[i][1] <= remaining:
                remaining -= items[i][1]
                upper += items[i][2]
            else:
                upper += (items[i][2] / items[i][1]) * remaining
                break
        
        return upper
    
    def solve(index, current_weight, current_value, best):
        if current_weight > capacity or index >= n:
            return best
        
        if bound(index, current_weight, current_value) <= best:
            return best
        
        include = solve(
            index + 1,
            current_weight + items[index][1],
            current_value + items[index][2],
            max(best, current_value)
        )
        
        exclude = solve(index + 1, current_weight, current_value, include)
        
        return max(include, exclude)
    
    return solve(0, 0, 0, 0)
