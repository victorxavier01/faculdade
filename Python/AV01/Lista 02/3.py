soma = True
while soma:
    numero1 = int(input("Digite o primeiro número: "))
    numero2 = int(input("Digite o segundo número: "))

    print(numero1 + numero2)

    resposta = input("Deseja realizar outra soma? ").lower()

    if resposta == "nao":
        soma = False