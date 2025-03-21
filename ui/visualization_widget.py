from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class VisualizationWidget(QWidget):
    """Widget za vizualizaciju podataka"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Inicijalizacija UI-a"""
        layout = QVBoxLayout(self)

        self.title_label = QLabel("Analiza Instagram pratilaca")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.data_label = QLabel("Podaci za analizu: (ovde prikazivati brojke ili druge podatke)")
        layout.addWidget(self.title_label)
        layout.addWidget(self.data_label)

    def update_chart(self, categories, values):
        """Ažuriranje podataka u labeli ili tabeli"""
        data_text = f"Kategorije: {', '.join(categories)}\nVrednosti: {', '.join(map(str, values))}"
        self.data_label.setText(data_text)