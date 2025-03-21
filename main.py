import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from controllers.analyzer_controller import AnalyzerController
from models.analyzer_model import InstagramFollowerAnalyzer


def main():
    """Glavna funkcija za pokretanje aplikacije"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Inicijalizacija modela, kontrolera i pogleda
    model = InstagramFollowerAnalyzer()
    controller = AnalyzerController(model)
    window = MainWindow(controller)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()