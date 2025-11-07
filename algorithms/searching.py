"""Searching Algorithms"""

def linear_search(arr, target):
    """Linear Search - Searches sequentially through the array"""
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1


def binary_search(arr, target):
    """Binary Search - Searches sorted array by dividing in half"""
    arr_sorted = sorted(arr)
    left, right = 0, len(arr_sorted) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr_sorted[mid] == target:
            return mid
        elif arr_sorted[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1


def fibonacci_search(arr, target):
    """Fibonacci Search - Uses Fibonacci numbers to divide search space"""
    arr_sorted = sorted(arr)
    n = len(arr_sorted)
    
    # Initialize fibonacci numbers
    fib2 = 0  # (m-2)'th Fibonacci number
    fib1 = 1  # (m-1)'th Fibonacci number
    fib = fib2 + fib1  # m'th Fibonacci number
    
    while fib < n:
        fib2 = fib1
        fib1 = fib
        fib = fib2 + fib1
    
    offset = -1
    
    while fib > 1:
        i = min(offset + fib2, n - 1)
        
        if arr_sorted[i] < target:
            fib = fib1
            fib1 = fib2
            fib2 = fib - fib1
            offset = i
        elif arr_sorted[i] > target:
            fib = fib2
            fib1 = fib1 - fib2
            fib2 = fib - fib1
        else:
            return i
    
    if fib1 and offset + 1 < n and arr_sorted[offset + 1] == target:
        return offset + 1
    
    return -1
