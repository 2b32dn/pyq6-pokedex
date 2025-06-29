import sys
from PyQt6.QtWidgets import QApplication
from pokedex_window import PokedexWindow

def main():
    app = QApplication(sys.argv)
    window = PokedexWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
