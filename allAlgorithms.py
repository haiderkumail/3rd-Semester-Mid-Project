import collections
def bubble_sort(arr, attributeNr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j][attributeNr] > arr[j+1][attributeNr]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr



def selection_sort(arr, attributeNr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j][attributeNr] < arr[min_idx][attributeNr]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def insertion_sort(arr, attributeNr):
    for i in range(1, len(arr)):
        key = arr[i][attributeNr]
        j = i-1
        while j >= 0 and key < arr[j][attributeNr]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1][attributeNr] = key
    return arr


def merge_sort(arr, attributeNr):
    if len(arr) > 1:
        mid = len(arr)//2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L, attributeNr)
        merge_sort(R, attributeNr)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i][attributeNr] < R[j][attributeNr]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

    return arr


def quick_sort(arr, s, e, attributeNr):
    if e - s + 1 <= 1:
        return arr

    pivot = arr[e][attributeNr]
    left = s # pointer for left side

    # Partition: elements smaller than pivot on left side
    for i in range(s, e):
        if arr[i][attributeNr] < pivot:
            tmp = arr[left]
            arr[left] = arr[i]
            arr[i] = tmp
            left += 1

    # Move pivot in-between left & right sides
    # arr[e] = arr[left]
    # arr[left] = pivot
    arr[e], arr[left] = arr[left], arr[e]
    
    # Quick sort left side
    quick_sort(arr, s, left - 1, attributeNr)

    # Quick sort right side
    quick_sort(arr, left + 1, e, attributeNr)

    return arr




# Bucket Sort

def bucket_sort(arr, attributeNr):
    if len(arr) == 0:
        return arr

    # Find maximum and minimum values
    max_val = float("-inf")
    min_val = float("inf")
    bucket_range = 0

    vType = type(arr[0][attributeNr])

    if vType == int or vType == float:
        for i in arr:
            max_val = max(max_val, i[attributeNr])
            min_val = min(min_val, i[attributeNr])
        bucket_range = (max_val - min_val) / len(arr)


    # Create buckets
    num_buckets = len(arr)
    buckets = [[] for _ in range(num_buckets)]

    # Add elements to buckets
    for i in range(len(arr)):
        if vType == int or vType == float:
            index = int((arr[i][attributeNr] - min_val) / bucket_range) if arr[i][attributeNr] != max_val else num_buckets - 1
        else:
            if arr[i][attributeNr]:
                index = ord(arr[i][attributeNr][0]) % len(arr)
            else:
                index = 0
        buckets[index].append(arr[i])

    # Sort buckets and concatenate
    sorted_arr = []
    for bucket in buckets:
        temp = quick_sort(bucket, 0, len(bucket)-1, attributeNr)
        sorted_arr.extend(temp)

    return sorted_arr



# Radix Sort
def countingSortRadix(arr, exp, r, attributeNr):
    # print(arr)
    count = [0] * r

    for i in arr:
        idx = i[attributeNr] // exp
        count[idx % r] += 1

    for i in range(1, len(count)):
        count[i] += count[i-1]
    # print(count)

    res = [0] * len(arr)
    for i in range(len(arr) -1, -1, -1): 
        idx = arr[i][attributeNr] // exp
        idx = idx % r
        count[idx] -= 1
        temp = count[idx]
        res[temp] = arr[i]

    return res


def radix_sort(arr, attributeNr):
    r = 10
    max_val = float("-inf")
    for i in arr:
        max_val = max(max_val, i[attributeNr])
    exp = 1
    for i in range(len(str(max_val))):
        arr = countingSortRadix(arr, exp, r, attributeNr)
        exp *= r

    return arr


# count sort
def count_sort(arr, attributeNr):

    minVal = float("inf")
    maxval = float("-inf")
    for i in arr:
        minVal = min(minVal, i[attributeNr])
        maxval = max(maxval, i[attributeNr])


    mid = [0] * (maxval + 1 - minVal)

    for i in arr:
        mid[i[attributeNr] - minVal] += 1

    for i in range(1, len(mid)):
        mid[i] += mid[i-1]

    res = [0] * (len(arr))

    for i in arr:
        mid[i[attributeNr] - minVal] -= 1
        temp = mid[i[attributeNr] - minVal]
        res[temp] = i

    return res


# pigeonHole Sort
def pigeonhole_sort(arr, attributeNr):

    minVal = float("inf")
    maxval = float("-inf")
    for i in arr:
        minVal = min(minVal, i[attributeNr])
        maxval = max(maxval, i[attributeNr])

    mid = [[] for i in range(maxval + 1 - minVal)]

    for i in arr:
        mid[i[attributeNr] - minVal].append(i)

    res = []

    for i in mid:
        res.extend(i)
        
    return res


# Heap Sort

def heapify(arr, n, i, attributeNr):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and arr[i][attributeNr] < arr[l][attributeNr]:
        largest = l

    if r < n and arr[largest][attributeNr] < arr[r][attributeNr]:
        largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest, attributeNr)


def heap_sort(arr, attributeNr):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, attributeNr)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0, attributeNr)

    return arr




def oddEven_sort(arr, attributeNr):
    n = len(arr)
	# Initially array is unsorted
    isSorted = 0
    while isSorted == 0:
        isSorted = 1
        temp = 0
        for i in range(1, n-1, 2):
            if arr[i][attributeNr] > arr[i+1][attributeNr]:
                arr[i], arr[i+1] = arr[i+1], arr[i]
                isSorted = 0
                
        for i in range(0, n-1, 2):
            if arr[i][attributeNr] > arr[i+1][attributeNr]:
                arr[i], arr[i+1] = arr[i+1], arr[i]
                isSorted = 0
	
    return arr


	



