vogais = ['a', 'e', 'i', 'o', 'u']
letra = input("Digite uma letra: ")

if letra in vogais:
    print(f"A letra '{letra}' é uma vogal.")
else:
    print(f"A letra '{letra}' é uma consoante.")