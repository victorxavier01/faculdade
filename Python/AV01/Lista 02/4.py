n = 0
fibonacci = []

while n <= 500:
    if n <= 1:
        print(n)
        fibonacci.append(n)
        n += 1
        fibonacci.append(n)

    if n == 2:
        print(n)
    # print(n) < se o output precisa ser necessariamente menor que 500, então ele deverá vir antes da soma com a lista
    n += fibonacci[-2]
    print(n)
    fibonacci.append(n)

    
    
    