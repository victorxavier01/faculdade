import argparse
from pathlib import Path

from config import DB_PADRAO
from menus import executar_app


def main() -> None:
    parser = argparse.ArgumentParser(description="Prova banco de Dados/Python")
    parser.add_argument(
        "--db",
        type=Path,
        default=DB_PADRAO,
        help="Caminho do banco SQLite3",
    )
    args = parser.parse_args()

    executar_app(args.db)


if __name__ == "__main__":
    main()
