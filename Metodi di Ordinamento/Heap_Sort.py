#Utilizzo dell'Heap Sort

def heap_sort(a):
    n = len(a)
    for i in range (n // 2 -1, -1, -1):
        heapify(a,n,i)

    for i in range (n-1, 0, -1):
        a[i], a[0] = a[0], a[i]
        heapify(a, i, 0)

def heapify(a, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and a[left] > a[largest]:
        largest = left
    if right < n and a[right] > a[largest]:
        largest = right
    if largest != i:
        a[i], a[largest], = a[largest], a[i]
        heapify(a,n,largest)    


def main():
    a = [12,34,26,99,67,59,81,45,7]
    print(f"L'array iniziale è il seguente: {a} ")
    heap_sort(a)
    print(f"L'array ordinato: {a}")

main()