from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
from PyQt6.QtCore import Qt


class HistoryWidget(QWidget):
    """Widget za prikaz istorije promena"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Inicijalizacija UI-a"""
        layout = QVBoxLayout(self)

        # Naslov
        self.title_label = QLabel("Istorija promena")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Tabela za istoriju
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels([
            "Datum", "Ukupno pratilaca", "Ukupno praćenja",
            "Ne prate nazad", "Ne pratite nazad"
        ])

        # Dodavanje u glavni layout
        layout.addWidget(self.title_label)
        layout.addWidget(self.history_table)

    def update_history(self, history_data):
        """Ažuriranje istorije"""
        # Brisanje stare tabele
        self.history_table.setRowCount(0)

        # Ako nema podataka, izađi
        if not history_data:
            return

        # Ažuriranje tabele
        for row, entry in enumerate(history_data):
            self.history_table.insertRow(row)
            self.history_table.setItem(row, 0, QTableWidgetItem(entry["timestamp"]))
            self.history_table.setItem(row, 1, QTableWidgetItem(str(entry["total_followers"])))
            self.history_table.setItem(row, 2, QTableWidgetItem(str(entry["total_following"])))
            self.history_table.setItem(row, 3, QTableWidgetItem(str(entry["not_following_back_count"])))
            self.history_table.setItem(row, 4, QTableWidgetItem(str(entry["you_not_following_back_count"])))

        # Podešavanje tabele
        self.history_table.resizeColumnsToContents()