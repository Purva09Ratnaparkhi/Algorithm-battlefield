"""Subset Generation Algorithms"""

from itertools import combinations


def subset_bitmasking(arr):
    """Subset Generation using Bitmasking"""
    n = len(arr)
    subsets = []
    
    for i in range(1 << n):  # 2^n combinations
        subset = []
        for j in range(n):
            if i & (1 << j):  # Check if j-th bit is set
                subset.append(arr[j])
        subsets.append(subset)
    
    return subsets


def subset_backtracking(arr, index=0, current=None, result=None):
    """Subset Generation using Backtracking"""
    if current is None:
        current = []
    if result is None:
        result = []
    
    result.append(current[:])
    
    for i in range(index, len(arr)):
        current.append(arr[i])
        subset_backtracking(arr, i + 1, current, result)
        current.pop()
    
    return result


def subset_recursive(arr):
    """Subset Generation using Recursion"""
    if len(arr) == 0:
        return [[]]
    
    first = arr[0]
    rest = arr[1:]
    rest_subsets = subset_recursive(rest)
    
    result = rest_subsets[:]
    for subset in rest_subsets:
        result.append([first] + subset)
    
    return result


def subset_iterative(arr):
    """Subset Generation using Iteration"""
    subsets = [[]]
    
    for elem in arr:
        subsets += [subset + [elem] for subset in subsets]
    
    return subsets


def subset_builtin(arr):
    """Subset Generation using Python Built-in Functions"""
    subsets = [[]]
    
    for i in range(1, len(arr) + 1):
        for combo in combinations(arr, i):
            subsets.append(list(combo))
    
    return subsets
