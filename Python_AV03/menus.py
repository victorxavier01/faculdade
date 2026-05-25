from contextlib import closing
import getpass
import sqlite3
from pathlib import Path

from auth import cadastrar_usuario, login
from config import DB_PADRAO
from database import conectar, criar_tabelas
from itens import atualizar_item, buscar_itens, cadastrar_item, deletar_item


def ler_inteiro(mensagem: str, minimo: int = 0) -> int:
    while True:
        try:
            valor = int(input(mensagem).strip())
            if valor >= minimo:
                return valor
        except ValueError:
            pass

        print(f"Digite um numero inteiro maior ou igual a {minimo}.")


def ler_float(mensagem: str, minimo: float = 0.0) -> float:
    while True:
        try:
            valor = float(input(mensagem).replace(",", ".").strip())
            if valor >= minimo:
                return valor
        except ValueError:
            pass

        print(f"Digite um numero maior ou igual a {minimo}.")


def ler_inteiro_opcional(mensagem: str, minimo: int = 0) -> int | None:
    texto = input(mensagem).strip()
    if not texto:
        return None

    try:
        valor = int(texto)
        if valor >= minimo:
            return valor
    except ValueError:
        pass

    print("Valor ignorado por ser invalido.")
    return None


def ler_float_opcional(mensagem: str, minimo: float = 0.0) -> float | None:
    texto = input(mensagem).replace(",", ".").strip()
    if not texto:
        return None

    try:
        valor = float(texto)
        if valor >= minimo:
            return valor
    except ValueError:
        pass

    print("Valor ignorado por ser invalido.")
    return None


def mostrar_itens(itens: list[sqlite3.Row]) -> None:
    if not itens:
        print("Nenhum item encontrado.")
        return

    print("\nID | Nome | Categoria | Qtd | Preco | Cadastrado por")
    print("-" * 72)

    for item in itens:
        print(
            f"{item['id']} | {item['nome']} | {item['categoria']} | "
            f"{item['quantidade']} | R$ {item['preco']:.2f} | {item['cadastrado_por']}"
        )

        if item["descricao"]:
            print(f"   Descricao: {item['descricao']}")


def menu_cadastrar_usuario(conexao: sqlite3.Connection) -> None:
    print("\nCadastro de usuario")
    nome = input("Nome: ")
    email = input("Email: ")
    senha = getpass.getpass("Senha: ")

    try:
        cadastrar_usuario(conexao, nome, email, senha)
        print("Usuario cadastrado com sucesso.")
    except sqlite3.IntegrityError:
        print("Ja existe usuario com esse email.")


def menu_login(conexao: sqlite3.Connection) -> sqlite3.Row | None:
    print("\nLogin")
    email = input("Email: ")
    senha = getpass.getpass("Senha: ")
    usuario = login(conexao, email, senha)

    if usuario:
        print(f"Bem-vindo(a), {usuario['nome']}!")
        return usuario

    print("Email ou senha invalidos.")
    return None


def menu_cadastrar_item(conexao: sqlite3.Connection, usuario_id: int) -> None:
    print("\nCadastrar item")
    nome = input("Nome: ")
    descricao = input("Descricao: ")
    quantidade = ler_inteiro("Quantidade: ")
    preco = ler_float("Preco: ")
    categoria = input("Categoria: ")

    item_id = cadastrar_item(
        conexao,
        nome,
        descricao,
        quantidade,
        preco,
        categoria,
        usuario_id,
    )
    print(f"Item cadastrado com ID {item_id}.")


def menu_atualizar_item(conexao: sqlite3.Connection) -> None:
    print("\nAlterar item")
    item_id = ler_inteiro("ID do item: ", minimo=1)
    print("Deixe em branco para manter o valor atual.")

    nome = input("Novo nome: ").strip() or None
    descricao = input("Nova descricao: ").strip() or None
    quantidade = ler_inteiro_opcional("Nova quantidade: ")
    preco = ler_float_opcional("Novo preco: ")
    categoria = input("Nova categoria: ").strip() or None

    alterou = atualizar_item(
        conexao,
        item_id,
        nome,
        descricao,
        quantidade,
        preco,
        categoria,
    )

    if alterou:
        print("Item atualizado com sucesso.")
    else:
        print("Item nao encontrado ou nenhum campo informado.")


def menu_deletar_item(conexao: sqlite3.Connection) -> None:
    print("\nRemover item")
    item_id = ler_inteiro("ID do item: ", minimo=1)
    confirmacao = input("Confirmar remocao? (s/N): ").strip().lower()

    if confirmacao == "s" and deletar_item(conexao, item_id):
        print("Item removido com sucesso.")
    else:
        print("Remocao cancelada ou item nao encontrado.")


def menu_buscar_item(conexao: sqlite3.Connection) -> None:
    termo = input("\nNome ou parte do nome: ")
    mostrar_itens(buscar_itens(conexao, termo))


def menu_interno(conexao: sqlite3.Connection, usuario: sqlite3.Row) -> None:
    while True:
        print("\nPARTE INTERNA")
        print("1. Cadastrar item")
        print("2. Alterar item")
        print("3. Remover item")
        print("4. Buscar item por nome")
        print("5. Exibir itens")
        print("0. Sair da conta")

        opcao = input("Opcao: ").strip()

        if opcao == "1":
            menu_cadastrar_item(conexao, int(usuario["id"]))
        elif opcao == "2":
            menu_atualizar_item(conexao)
        elif opcao == "3":
            menu_deletar_item(conexao)
        elif opcao == "4":
            menu_buscar_item(conexao)
        elif opcao == "5":
            mostrar_itens(buscar_itens(conexao))
        elif opcao == "0":
            break
        else:
            print("Opcao invalida.")


def executar_app(caminho_banco: Path = DB_PADRAO) -> None:
    with closing(conectar(caminho_banco)) as conexao:
        criar_tabelas(conexao)

        while True:
            print("\nMENU INICIAL")
            print("1. Cadastrar Usuario")
            print("2. Realizar Login")
            print("0. Sair")

            opcao = input("Opcao: ").strip()

            if opcao == "1":
                menu_cadastrar_usuario(conexao)
            elif opcao == "2":
                usuario = menu_login(conexao)
                if usuario:
                    menu_interno(conexao, usuario)
            elif opcao == "0":
                print("Ate logo!")
                break
            else:
                print("Opcao invalida.")
