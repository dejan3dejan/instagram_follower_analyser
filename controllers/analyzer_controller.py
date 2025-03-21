from models.analyzer_model import InstagramFollowerAnalyzer
from typing import Dict, List, Tuple, Any
import os


class AnalyzerController:
    """Kontroler za upravljanje logikom Instagram analizatora"""

    def __init__(self, model: InstagramFollowerAnalyzer):
        """Inicijalizacija kontrolera"""
        self.model = model

    def set_data_path(self, path: str) -> None:
        """Postavi putanju do podataka"""
        self.model.set_data_path(path)

    def load_data(self) -> bool:
        """Učitaj podatke sa Instagram-a"""
        return self.model.load_data()

    def analyze_relationships(self) -> bool:
        """Analiziraj odnose između pratilaca"""
        return self.model.analyze_relationships()

    def get_report(self) -> Dict[str, Any]:
        """Dobavi izveštaj o odnosima"""
        return self.model.generate_report()

    def save_report(self, path: str) -> bool:
        """Sačuvaj izveštaj na zadatoj putanji"""
        return self.model.save_report(path)

    def get_visualization_data(self) -> Tuple[List[str], List[int]]:
        """Dobavi podatke za vizualizaciju"""
        return self.model.generate_visualization_data()

    def save_user_lists(self, output_folder: str) -> bool:
        """Sačuvaj liste korisnika u tekstualnim datotekama"""
        return self.model.save_user_lists(output_folder)

    def analyze_engagement(self) -> Dict[str, Any]:
        """Analiziraj engagement korisnika"""
        return self.model.analyze_engagement()

    def get_history_data(self) -> List[Dict[str, Any]]:
        """Dobavi istorijske podatke"""
        return self.model.get_history_data()

    def get_statistics(self) -> Dict[str, int]:
        """Dobavi osnovne statistike"""
        report = self.model.generate_report()
        if not report:
            return {}

        return {
            "total_followers": report.get("total_followers", 0),
            "total_following": report.get("total_following", 0),
            "not_following_back_count": len(report.get("not_following_back", [])),
            "you_not_following_back_count": len(report.get("you_not_following_back", [])),
            "mutual_followers_count": report.get("mutual_followers_count", 0)
        }

    def get_user_lists(self) -> Dict[str, List[str]]:
        """Dobavi liste korisnika"""
        report = self.model.generate_report()
        if not report:
            return {}

        return {
            "not_following_back": report.get("not_following_back", []),
            "you_not_following_back": report.get("you_not_following_back", []),
            "mutual_followers": report.get("mutual_followers", [])
        }