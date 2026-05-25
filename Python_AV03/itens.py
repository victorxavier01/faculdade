import sqlite3


def buscar_ou_criar_categoria(conexao: sqlite3.Connection, nome: str) -> int:
    nome_categoria = nome.strip().title() or "Geral"

    conexao.execute(
        "INSERT OR IGNORE INTO categorias (nome) VALUES (?)",
        (nome_categoria,),
    )
    categoria = conexao.execute(
        "SELECT id FROM categorias WHERE nome = ?",
        (nome_categoria,),
    ).fetchone()
    conexao.commit()

    return int(categoria["id"])


def cadastrar_item(
    conexao: sqlite3.Connection,
    nome: str,
    descricao: str,
    quantidade: int,
    preco: float,
    categoria_nome: str,
    usuario_id: int,
) -> int:
    categoria_id = buscar_ou_criar_categoria(conexao, categoria_nome)
    sql = """
        INSERT INTO itens (nome, descricao, quantidade, preco, categoria_id, usuario_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor = conexao.execute(
        sql,
        (nome.strip(), descricao.strip(), quantidade, preco, categoria_id, usuario_id),
    )
    conexao.commit()

    return int(cursor.lastrowid)


def buscar_itens(conexao: sqlite3.Connection, termo: str = "") -> list[sqlite3.Row]:
    sql = """
        SELECT
            i.id,
            i.nome,
            i.descricao,
            i.quantidade,
            i.preco,
            c.nome AS categoria,
            u.nome AS cadastrado_por
        FROM itens i
        JOIN categorias c ON c.id = i.categoria_id
        JOIN usuarios u ON u.id = i.usuario_id
        WHERE i.ativo = 1
          AND LOWER(i.nome) LIKE LOWER(?)
        ORDER BY i.nome
    """
    termo_like = f"%{termo.strip()}%"
    return list(conexao.execute(sql, (termo_like,)).fetchall())


def atualizar_item(
    conexao: sqlite3.Connection,
    item_id: int,
    nome: str | None = None,
    descricao: str | None = None,
    quantidade: int | None = None,
    preco: float | None = None,
    categoria_nome: str | None = None,
) -> bool:
    campos = []
    valores = []

    if nome:
        campos.append("nome = ?")
        valores.append(nome.strip())
    if descricao is not None:
        campos.append("descricao = ?")
        valores.append(descricao.strip())
    if quantidade is not None:
        campos.append("quantidade = ?")
        valores.append(quantidade)
    if preco is not None:
        campos.append("preco = ?")
        valores.append(preco)
    if categoria_nome:
        campos.append("categoria_id = ?")
        valores.append(buscar_ou_criar_categoria(conexao, categoria_nome))

    if not campos:
        return False

    campos.append("atualizado_em = CURRENT_TIMESTAMP")
    valores.append(item_id)

    sql = f"UPDATE itens SET {', '.join(campos)} WHERE id = ? AND ativo = 1"
    cursor = conexao.execute(sql, valores)
    conexao.commit()

    return cursor.rowcount > 0


def deletar_item(conexao: sqlite3.Connection, item_id: int) -> bool:
    sql = """
        UPDATE itens
        SET ativo = 0,
            atualizado_em = CURRENT_TIMESTAMP
        WHERE id = ? AND ativo = 1
    """
    cursor = conexao.execute(sql, (item_id,))
    conexao.commit()

    return cursor.rowcount > 0
