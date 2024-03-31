from typing import List, Tuple


def bubble_sort(arr: List[int]) -> Tuple[List[int], List[int]]:
    """
    _summary_

    Args:
        arr (List[int]): _description_

    Returns:
        Tuple[List[int], List[int]]: _description_
    """
    arr = arr.copy()
    n = len(arr)
    idx = list(range(n))  # Initialize indexes list
    for i in range(n):
        # Last i elements are already in place, so we don't need to check them
        for j in range(0, n - i - 1):
            # Traverse the array from 0 to n-i-1
            # Swap if the element found is greater than the next element
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  # Swap elements
                idx[j], idx[j + 1] = idx[j + 1], idx[j]  # Swap indexes
    return arr, idx
