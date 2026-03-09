nota1 = int(input("Insira a primeira nota: "))
nota2 = int(input("Insira a segunda nota: "))

media = (nota1 + nota2) / 2

if media == 10:
    print("Aprovado com distinção")
if media >= 7 and media < 10:
    print("Aprovado")
elif media < 7:
    print("Reprovado")