def quicksort(a, inf, sup):
    i = inf
    j = sup
    pivot = a[(inf + sup) // 2]
    while i <= j:
        while a[i] < pivot:
            i+=1
        while a[j] > pivot:
            j-=1
        if i <= j:
            if i < j:
                temp = a[i]
                a[i] = a[j]
                a[j] = temp
            i += 1
            j -= 1
    if inf < j:
        quicksort(a, inf, j)
    if i < sup:
        quicksort(a, i, sup)    


def main():
    a = [12,34,26,99,67,59,81,45,7]
    n = len(a)
    quicksort (a, 0, n-1)
    print(a)
main()