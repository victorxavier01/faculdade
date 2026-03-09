numeros = [5,102,531,999,314,3,1,23,500000,3218391,2]
numeros_permitidos = []

for numero in numeros:
    if numero > 1000:
        print(f"Apenas números menores que 1000 são permitidos. O número {numero} será excluído")

    else:
        numeros_permitidos.append(numero)

menor_numero = min(numeros_permitidos)
maior_numero = max(numeros_permitidos)

print(f"O menor número é: {menor_numero}")
print(f"O menor número é: {maior_numero}")
print(f"A soma é: {menor_numero + maior_numero}")