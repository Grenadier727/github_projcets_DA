def main ():
    a = [41,26,10,88,67,91,15,7,32,55]
    n = len(a)
    for i in range (1,n):
        value = a[i]
        j = i - 1
        while j >= 0 and a[j] > value :
            a[j +1] = a[j]
            j = j - 1

            a[j + 1] = value

    print (a)

main()
