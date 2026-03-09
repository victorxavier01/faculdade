contador = 0

pergunta1 = input("Telefonou para a vítima? ").lower()
pergunta2 = input("Esteve no local do crime? ").lower()
pergunta3 = input("Mora perto da vítima? ").lower()
pergunta4 = input("Devia para a vítima? ").lower()
pergunta5 = input("Já trabalhou com a vítima? ").lower()

respostas = [pergunta1, pergunta2, pergunta3, pergunta4, pergunta5]

for resposta in respostas:
    if resposta == "sim":
        contador += 1

if contador == 5:
    print("Assassino")

elif contador >= 3 and contador <= 4:
    print("Cúmplice")

elif contador == 2:
    print("Suspeito")