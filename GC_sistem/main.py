import sys
from db import init_db
from cli import menu


def main():
    init_db()
    # se o usuário passar 'gui' como argumento, inicia interface gráfica
    if len(sys.argv) > 1 and sys.argv[1].lower() == 'gui':
        import gui
        gui.main()
    else:
        menu()


if __name__ == "__main__":
    main()
