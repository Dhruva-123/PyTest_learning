def binary_search_recursive(arr, target):
    return _binary_search(arr, target, 0, len(arr) - 1)


def _binary_search(arr, target, left, right):
    if left > right:
        return -1

    mid = (left + right) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return _binary_search(arr, target, mid + 1, right)
    else:
        return _binary_search(arr, target, left, mid - 1)
