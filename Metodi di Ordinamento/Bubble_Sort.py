#Ordinamento con Bubble sort

def main():
    a = [31,12,42,27,88,64,59,99,3]
    n = len(a)
    scambio = True

    while (scambio) :
        scambio = False
        for i in range(n -1):
            if a[i] > a[i + 1]:
             temp = a[i]
             a[i] = a[i + 1]
             a[i + 1] = temp
             scambio = True

    print(a)       
main()
