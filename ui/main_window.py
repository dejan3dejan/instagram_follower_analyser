from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QFileDialog, QTabWidget,
                             QListWidget, QMessageBox, QProgressBar, QSplitter,
                             QComboBox, QTextEdit, QGridLayout)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon
from controllers.analyzer_controller import AnalyzerController
from ui.visualization_widget import VisualizationWidget
from ui.history_widget import HistoryWidget
from ui.user_list_widget import UserListWidget
from ui.engagement_widget import EngagementWidget
import os


class MainWindow(QMainWindow):
    """Glavni prozor aplikacije za analizu Instagram pratilaca"""

    def __init__(self, controller: AnalyzerController):
        super().__init__()

        self.controller = controller
        self.init_ui()

    def init_ui(self):
        """Inicijalizacija korisničkog interfejsa"""
        self.setWindowTitle("Instagram Follower Analyzer")
        self.setMinimumSize(900, 700)

        # Postavljanje brutalističkog stila
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #ffffff;
                color: #000000;
            }
            QPushButton {
                background-color: #000000;
                color: #ffffff;
                border: none;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #333333;
            }
            QPushButton:pressed {
                background-color: #555555;
            }
            QTabWidget::pane {
                border: 2px solid #000000;
            }
            QTabBar::tab {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #000000;
                padding: 8px 16px;
            }
            QTabBar::tab:selected {
                background-color: #000000;
                color: #ffffff;
            }
            QLabel {
                font-weight: normal;
            }
            QListWidget {
                border: 1px solid #000000;
                padding: 4px;
            }
            QProgressBar {
                border: 1px solid #000000;
                background-color: #ffffff;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #000000;
            }
        """)

        # Glavni widget
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        # Gornji deo - kontrole
        control_layout = QHBoxLayout()

        # Dugme za učitavanje podataka
        self.load_button = QPushButton("UČITAJ INSTAGRAM PODATKE")
        self.load_button.setFixedHeight(40)
        self.load_button.clicked.connect(self.load_data)

        # Dugme za analizu
        self.analyze_button = QPushButton("ANALIZIRAJ")
        self.analyze_button.setFixedHeight(40)
        self.analyze_button.setEnabled(False)
        self.analyze_button.clicked.connect(self.analyze_data)

        # Dugme za izvoz
        self.export_button = QPushButton("IZVEZI REZULTATE")
        self.export_button.setFixedHeight(40)
        self.export_button.setEnabled(False)
        self.export_button.clicked.connect(self.export_results)

        # Status label
        self.status_label = QLabel("Status: Čekanje na podatke")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        # Dodaj kontrole u layout
        control_layout.addWidget(self.load_button)
        control_layout.addWidget(self.analyze_button)
        control_layout.addWidget(self.export_button)
        control_layout.addWidget(self.status_label)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(15)

        # Tab widget za različite prikaze
        self.tab_widget = QTabWidget()

        # 1. Kartica za osnovnu statistiku
        self.stats_widget = QWidget()
        stats_layout = QVBoxLayout(self.stats_widget)

        # Statistički grid
        self.stats_grid = QGridLayout()

        # Labele za statistiku
        self.total_followers_label = QLabel("Ukupno pratilaca: 0")
        self.total_following_label = QLabel("Ukupno profila koje pratite: 0")
        self.not_following_back_label = QLabel("Ne prate vas nazad: 0")
        self.you_not_following_back_label = QLabel("Ne pratite nazad: 0")
        self.mutual_followers_label = QLabel("Uzajamno praćenje: 0")

        # Postavi labele u grid
        self.stats_grid.addWidget(self.total_followers_label, 0, 0)
        self.stats_grid.addWidget(self.total_following_label, 0, 1)
        self.stats_grid.addWidget(self.not_following_back_label, 1, 0)
        self.stats_grid.addWidget(self.you_not_following_back_label, 1, 1)
        self.stats_grid.addWidget(self.mutual_followers_label, 2, 0)

        # Vizualizacioni widget
        self.viz_widget = VisualizationWidget()

        # Dodaj u layout statistike
        stats_layout.addLayout(self.stats_grid)
        stats_layout.addWidget(self.viz_widget)

        # 2. Kartica za liste korisnika
        self.user_list_widget = UserListWidget()

        # 3. Kartica za engagement analizu
        self.engagement_widget = EngagementWidget()

        # 4. Kartica za istoriju
        self.history_widget = HistoryWidget()

        # Dodaj kartice u tab widget
        self.tab_widget.addTab(self.stats_widget, "STATISTIKA")
        self.tab_widget.addTab(self.user_list_widget, "LISTE KORISNIKA")
        self.tab_widget.addTab(self.engagement_widget, "ENGAGEMENT")
        self.tab_widget.addTab(self.history_widget, "ISTORIJA")

        # Dodaj sve u glavni layout
        main_layout.addLayout(control_layout)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.tab_widget)

        # Postavi centralni widget
        self.setCentralWidget(central_widget)

    def load_data(self):
        """Učitavanje Instagram podataka"""
        data_path = QFileDialog.getExistingDirectory(self, "Izaberite folder sa Instagram podacima")

        if data_path:
            self.progress_bar.setValue(20)
            self.status_label.setText("Status: Učitavanje podataka...")

            # Postavi putanju do podataka
            self.controller.set_data_path(data_path)

            # Učitaj podatke
            success = self.controller.load_data()

            if success:
                self.progress_bar.setValue(40)
                self.status_label.setText("Status: Podaci uspešno učitani")
                self.analyze_button.setEnabled(True)
            else:
                self.progress_bar.setValue(0)
                self.status_label.setText("Status: Greška pri učitavanju podataka")
                QMessageBox.critical(self, "Greška",
                                     "Nije moguće učitati Instagram podatke. Proverite format i lokaciju datoteka.")

    def analyze_data(self):
        """Analiza podataka"""
        self.progress_bar.setValue(60)
        self.status_label.setText("Status: Analiza u toku...")

        # Izvrši analizu
        success = self.controller.analyze_relationships()

        if success:
            self.progress_bar.setValue(80)
            self.status_label.setText("Status: Analiza završena")
            self.export_button.setEnabled(True)

            # Ažuriraj statistiku
            self.update_statistics()

            # Ažuriraj vizualizaciju
            self.update_visualization()

            # Ažuriraj liste korisnika
            self.update_user_lists()

            # Ažuriraj engagement analizu
            self.update_engagement()

            # Ažuriraj istoriju
            self.update_history()

            self.progress_bar.setValue(100)
        else:
            self.progress_bar.setValue(40)
            self.status_label.setText("Status: Greška pri analizi")
            QMessageBox.critical(self, "Greška", "Analiza nije uspela. Pokušajte ponovo.")

    def export_results(self):
        """Izvoz rezultata"""
        export_folder = QFileDialog.getExistingDirectory(self, "Izaberite folder za izvoz rezultata")

        if export_folder:
            # Sačuvaj izveštaj
            report_path = os.path.join(export_folder, "instagram_follower_report.json")
            self.controller.save_report(report_path)

            # Sačuvaj liste korisnika
            self.controller.save_user_lists(export_folder)

            QMessageBox.information(self, "Uspeh", f"Rezultati su izvezeni u folder:\n{export_folder}")

    def update_statistics(self):
        """Ažuriranje statistike"""
        stats = self.controller.get_statistics()

        if stats:
            self.total_followers_label.setText(f"Ukupno pratilaca: {stats['total_followers']}")
            self.total_following_label.setText(f"Ukupno profila koje pratite: {stats['total_following']}")
            self.not_following_back_label.setText(f"Ne prate vas nazad: {stats['not_following_back_count']}")
            self.you_not_following_back_label.setText(f"Ne pratite nazad: {stats['you_not_following_back_count']}")
            self.mutual_followers_label.setText(f"Uzajamno praćenje: {stats['mutual_followers_count']}")

    def update_visualization(self):
        """Ažuriranje vizualizacije"""
        categories, values = self.controller.get_visualization_data()
        if categories and values:
            self.viz_widget.update_chart(categories, values)

    def update_user_lists(self):
        """Ažuriranje listi korisnika"""
        user_lists = self.controller.get_user_lists()
        if user_lists:
            self.user_list_widget.update_lists(
                user_lists["not_following_back"],
                user_lists["you_not_following_back"],
                user_lists["mutual_followers"]
            )

    def update_engagement(self):
        """Ažuriranje engagement analize"""
        engagement_data = self.controller.analyze_engagement()
        self.engagement_widget.update_data(engagement_data)

    def update_history(self):
        """Ažuriranje istorije"""
        history_data = self.controller.get_history_data()
        self.history_widget.update_history(history_data)