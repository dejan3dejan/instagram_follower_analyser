from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QLabel, QComboBox)

class EngagementWidget(QWidget):
    """Widget za prikaz engagement analize"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Inicijalizacija UI-a"""
        layout = QVBoxLayout(self)

        # Kontrole za filter
        filter_layout = QHBoxLayout()
        self.filter_label = QLabel("Sortiraj po:")
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Korisničko ime", "Engagement score", "Poslednja interakcija"])
        filter_layout.addWidget(self.filter_label)
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addStretch()

        # Tabela za engagement podatke
        self.engagement_table = QTableWidget()
        self.engagement_table.setColumnCount(5)
        self.engagement_table.setHorizontalHeaderLabels(
            ["Korisničko ime", "Lajkovi", "Komentari", "Pregledi", "Engagement score"])

        # Dodavanje u glavni layout
        layout.addLayout(filter_layout)
        layout.addWidget(self.engagement_table)

    def update_data(self, engagement_data):
        """Ažuriranje engagement podataka"""
        self.engagement_table.setRowCount(0)

        # Ako nema podataka, izađi
        if not engagement_data:
            return

        # Dodavanje redova u tabelu
        for row, (username, data) in enumerate(engagement_data.items()):
            self.engagement_table.insertRow(row)
            self.engagement_table.setItem(row, 0, QTableWidgetItem(username))
            self.engagement_table.setItem(row, 1, QTableWidgetItem(str(data["likes"])))
            self.engagement_table.setItem(row, 2, QTableWidgetItem(str(data["comments"])))
            self.engagement_table.setItem(row, 3, QTableWidgetItem(str(data["views"])))
            self.engagement_table.setItem(row, 4, QTableWidgetItem(str(data["engagement_score"])))

        # Podešavanje tabele
        self.engagement_table.resizeColumnsToContents()