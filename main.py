import sys
from PyQt6.QtWidgets import QApplication
from pokedex_window import PokedexWindow

def main():
    app = QApplication(sys.argv)
    dark_stylesheet = """
        QWidget {
            background-color: #121212;
            color: #ffffff;
            font-family: Arial;
        }
        QLineEdit, QTextEdit, QPlainTextEdit {
            background-color: #1e1e1e;
            color: #ffffff;
            border: 1px solid #333;
        }
        QPushButton {
            background-color: #2c2c2c;
            border: 1px solid #555;
            padding: 5px;
            color: #fff;
        }
        QPushButton:hover {
            background-color: #3c3c3c;
        }
        QTabWidget::pane {
            border: 1px solid #444;
        }
        QTabBar::tab {
            background: #2c2c2c;
            padding: 6px;
            color: #fff;
        }
        QTabBar::tab:selected {
            background: #555;
        }
        QLabel {
            color: #ffffff;
        }
        QCheckBox {
            color: #ffffff;
        }
    """

    app.setStyleSheet(dark_stylesheet)

    window = PokedexWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
