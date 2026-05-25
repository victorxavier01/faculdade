import base64
import binascii
import hashlib
import hmac
import os
import sqlite3

from config import ITERACOES_HASH


def gerar_hash_senha(senha: str) -> str:
    salt = os.urandom(16)
    senha_hash = hashlib.pbkdf2_hmac(
        "sha256",
        senha.encode("utf-8"),
        salt,
        ITERACOES_HASH,
    )
    salt_b64 = base64.b64encode(salt).decode("ascii")
    hash_b64 = base64.b64encode(senha_hash).decode("ascii")
    return f"pbkdf2_sha256${ITERACOES_HASH}${salt_b64}${hash_b64}"


def verificar_senha(senha: str, senha_hash_salva: str) -> bool:
    try:
        algoritmo, iteracoes, salt_b64, hash_b64 = senha_hash_salva.split("$")
        salt = base64.b64decode(salt_b64)
        hash_salvo = base64.b64decode(hash_b64)
    except (ValueError, binascii.Error):
        return False

    if algoritmo != "pbkdf2_sha256":
        return False

    hash_tentativa = hashlib.pbkdf2_hmac(
        "sha256",
        senha.encode("utf-8"),
        salt,
        int(iteracoes),
    )
    return hmac.compare_digest(hash_tentativa, hash_salvo)


def cadastrar_usuario(
    conexao: sqlite3.Connection,
    nome: str,
    email: str,
    senha: str,
) -> int:
    sql = """
        INSERT INTO usuarios (nome, email, senha_hash)
        VALUES (?, ?, ?)
    """
    cursor = conexao.execute(
        sql,
        (nome.strip(), email.strip().lower(), gerar_hash_senha(senha)),
    )
    conexao.commit()
    return int(cursor.lastrowid)


def login(conexao: sqlite3.Connection, email: str, senha: str) -> sqlite3.Row | None:
    sql = """
        SELECT id, nome, email, senha_hash
        FROM usuarios
        WHERE email = ?
    """
    usuario = conexao.execute(sql, (email.strip().lower(),)).fetchone()

    if usuario and verificar_senha(senha, usuario["senha_hash"]):
        return usuario

    return None
