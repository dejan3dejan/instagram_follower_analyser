from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QSplitter
from PyQt6.QtCore import Qt


class UserListWidget(QWidget):
    """Widget za prikaz listi korisnika"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Inicijalizacija UI-a"""
        layout = QVBoxLayout(self)

        # Splitter za horizontalno deljenje
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Lista korisnika koji ne prate nazad
        not_following_widget = QWidget()
        not_following_layout = QVBoxLayout(not_following_widget)
        self.not_following_label = QLabel("Ne prate vas nazad:")
        self.not_following_list = QListWidget()
        not_following_layout.addWidget(self.not_following_label)
        not_following_layout.addWidget(self.not_following_list)

        # Lista korisnika koje ne pratite nazad
        you_not_following_widget = QWidget()
        you_not_following_layout = QVBoxLayout(you_not_following_widget)
        self.you_not_following_label = QLabel("Ne pratite nazad:")
        self.you_not_following_list = QListWidget()
        you_not_following_layout.addWidget(self.you_not_following_label)
        you_not_following_layout.addWidget(self.you_not_following_list)

        # Lista uzajamnih pratilaca
        mutual_widget = QWidget()
        mutual_layout = QVBoxLayout(mutual_widget)
        self.mutual_label = QLabel("Uzajamni pratioci:")
        self.mutual_list = QListWidget()
        mutual_layout.addWidget(self.mutual_label)
        mutual_layout.addWidget(self.mutual_list)

        # Dodavanje widgeta u splitter
        splitter.addWidget(not_following_widget)
        splitter.addWidget(you_not_following_widget)
        splitter.addWidget(mutual_widget)

        # Dodavanje splittera u glavni layout
        layout.addWidget(splitter)

    def update_lists(self, not_following_back, you_not_following_back, mutual_followers):
        """Ažuriranje lista korisnika"""
        # Brisanje starih podataka
        self.not_following_list.clear()
        self.you_not_following_list.clear()
        self.mutual_list.clear()

        # Dodavanje novih podataka
        self.not_following_list.addItems(not_following_back)
        self.you_not_following_list.addItems(you_not_following_back)
        self.mutual_list.addItems(mutual_followers)

        # Ažuriranje labela
        self.not_following_label.setText(f"Ne prate vas nazad: {len(not_following_back)}")
        self.you_not_following_label.setText(f"Ne pratite nazad: {len(you_not_following_back)}")
        self.mutual_label.setText(f"Uzajamni pratioci: {len(mutual_followers)}")