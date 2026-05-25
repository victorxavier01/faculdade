import sqlite3
from pathlib import Path

from config import DB_PADRAO, SCHEMA_PATH


def conectar(caminho_banco: Path = DB_PADRAO) -> sqlite3.Connection:
    conexao = sqlite3.connect(caminho_banco)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_tabelas(conexao: sqlite3.Connection) -> None:
    conexao.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    conexao.commit()
