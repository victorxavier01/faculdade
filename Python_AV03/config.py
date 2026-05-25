from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DB_PADRAO = BASE_DIR / "av03_lab_ii.sqlite3"
SCHEMA_PATH = BASE_DIR / "schema.sql"
ITERACOES_HASH = 260_000
