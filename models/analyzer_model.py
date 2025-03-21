import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
from typing import Set, Dict, List, Optional, Any, Tuple


class InstagramFollowerAnalyzer:
    """Klasa za analizu Instagram pratilaca"""

    def __init__(self):
        """Inicijalizacija analizatora Instagram pratilaca"""
        self.data_path = None
        self.followers = None
        self.following = None
        self.not_following_back = None
        self.you_not_following_back = None
        self.mutual_followers = None
        self.followers_data_raw = None
        self.following_data_raw = None
        self.engagement_stats = {}
        self.history_data = []
        self.loaded_successfully = False

    def set_data_path(self, data_path: str) -> None:
        """Postavi putanju do foldera sa Instagram podacima"""
        self.data_path = data_path

    def load_data(self) -> bool:
        """Učitava podatke o pratiocima iz Instagram JSON datoteka"""
        if not self.data_path:
            return False

        try:
            # Učitavanje datoteka o pratiocima i onima koje pratite
            followers_path = os.path.join(self.data_path, 'followers_1.json')
            following_path = os.path.join(self.data_path, 'following.json')

            with open(followers_path, 'r', encoding='utf-8') as f:
                self.followers_data_raw = json.load(f)

            with open(following_path, 'r', encoding='utf-8') as f:
                self.following_data_raw = json.load(f)

            # Pretvaranje u DataFrame za lakše upravljanje
            if 'relationships_followers' in self.followers_data_raw:
                self.followers = pd.DataFrame(self.followers_data_raw['relationships_followers'])
            else:
                # Alternativno, ako je drugačija struktura
                self.followers = pd.DataFrame(self.followers_data_raw)

            if 'relationships_following' in self.following_data_raw:
                self.following = pd.DataFrame(self.following_data_raw['relationships_following'])
            else:
                # Alternativno, ako je drugačija struktura
                self.following = pd.DataFrame(self.following_data_raw)

            self.loaded_successfully = True
            return True

        except Exception as e:
            self.loaded_successfully = False
            return False

    def analyze_relationships(self) -> bool:
        """Analizira odnose između pratilaca"""
        if self.followers is None or self.following is None:
            return False

        try:
            # Dobijanje liste korisničkih imena
            follower_usernames = set()
            following_usernames = set()

            # Provjera svih mogućih struktura Instagram podataka
            follower_usernames = self._extract_usernames(self.followers)
            following_usernames = self._extract_usernames(self.following)

            # Uklanjanje None vrijednosti
            follower_usernames = {u for u in follower_usernames if u is not None}
            following_usernames = {u for u in following_usernames if u is not None}

            # Pronalaženje profila koji vas ne prate nazad
            self.not_following_back = following_usernames - follower_usernames

            # Pronalaženje profila koje vi ne pratite nazad
            self.you_not_following_back = follower_usernames - following_usernames

            # Pronalaženje uzajamnih pratilaca
            self.mutual_followers = follower_usernames.intersection(following_usernames)

            # Sačuvaj trenutnu analizu u istoriju
            self._add_to_history()

            return True

        except Exception as e:
            return False

    def _extract_usernames(self, data_frame: pd.DataFrame) -> Set[str]:
        """Pomoćna metoda za ekstrakciju korisničkih imena iz DataFrame-a"""
        usernames = set()

        if 'string_list_data' in data_frame.columns:
            usernames = set(data_frame['string_list_data'].apply(
                lambda x: x[0]['value'] if isinstance(x, list) and x and 'value' in x[0] else None
            ))
        elif 'username' in data_frame.columns:
            usernames = set(data_frame['username'])
        elif 'name' in data_frame.columns:
            usernames = set(data_frame['name'])
        elif 'value' in data_frame.columns:
            usernames = set(data_frame['value'])
        elif 'title' in data_frame.columns:
            usernames = set(data_frame['title'])
        else:
            # Pokušaj sa prvom kolonom ako ništa drugo ne uspije
            if len(data_frame.columns) > 0:
                first_col = data_frame.columns[0]
                usernames = set(data_frame[first_col])

        return usernames

    def _add_to_history(self) -> None:
        """Dodaje trenutnu analizu u istoriju"""
        if not all([isinstance(self.not_following_back, set),
                    isinstance(self.you_not_following_back, set),
                    isinstance(self.mutual_followers, set)]):
            return

        history_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_followers": len(self.followers) if self.followers is not None else 0,
            "total_following": len(self.following) if self.following is not None else 0,
            "not_following_back_count": len(self.not_following_back),
            "you_not_following_back_count": len(self.you_not_following_back),
            "mutual_followers_count": len(self.mutual_followers)
        }

        self.history_data.append(history_entry)

    def generate_report(self) -> Dict[str, Any]:
        """
        Generira izvještaj o odnosima pratilaca

        Returns:
            Dict: Rečnik sa podacima izveštaja
        """
        if not all([isinstance(self.not_following_back, set),
                    isinstance(self.you_not_following_back, set),
                    isinstance(self.mutual_followers, set)]):
            return {}

        # Kreiranje izvještaja
        report = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_followers": len(self.followers) if self.followers is not None else 0,
            "total_following": len(self.following) if self.following is not None else 0,
            "not_following_back": sorted(list(self.not_following_back)),
            "you_not_following_back": sorted(list(self.you_not_following_back)),
            "mutual_followers": sorted(list(self.mutual_followers)),
            "mutual_followers_count": len(self.mutual_followers)
        }

        return report

    def save_report(self, output_path: str) -> bool:
        """Čuva izveštaj u JSON formatu"""
        report = self.generate_report()
        if not report:
            return False

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False

    def generate_visualization_data(self) -> Tuple[List[str], List[int]]:
        """Priprema podatke za vizualizaciju"""
        if not all([isinstance(self.not_following_back, set),
                    isinstance(self.you_not_following_back, set),
                    isinstance(self.mutual_followers, set)]):
            return [], []

        # Priprema podataka za vizualizaciju
        categories = ['Uzajamni pratioci', 'Ne prate vas nazad', 'Ne pratite ih nazad']
        values = [len(self.mutual_followers), len(self.not_following_back), len(self.you_not_following_back)]

        return categories, values

    def save_user_lists(self, output_folder: str) -> bool:
        """
        Sprema liste korisnika u tekstualne datoteke

        Args:
            output_folder (str): Putanja za spremanje datoteka
        """
        if not all([isinstance(self.not_following_back, set),
                    isinstance(self.you_not_following_back, set),
                    isinstance(self.mutual_followers, set)]):
            return False

        # Osigurajte da folder postoji
        os.makedirs(output_folder, exist_ok=True)

        try:
            # Spremanje lista korisnika
            with open(os.path.join(output_folder, "ne_prate_nazad.txt"), 'w', encoding='utf-8') as f:
                f.write("\n".join(sorted(self.not_following_back)))

            with open(os.path.join(output_folder, "ne_pratite_nazad.txt"), 'w', encoding='utf-8') as f:
                f.write("\n".join(sorted(self.you_not_following_back)))

            with open(os.path.join(output_folder, "uzajamni_pratioci.txt"), 'w', encoding='utf-8') as f:
                f.write("\n".join(sorted(self.mutual_followers)))

            return True
        except Exception:
            return False

    def analyze_engagement(self) -> Dict[str, Any]:
        """
        Analizira engagement korisnika koji vas ne prate nazad
        (Nova funkcionalnost)
        """
        if not isinstance(self.not_following_back, set) or not self.followers_data_raw:
            return {}

        # Simulacija engagement analize - u stvarnoj aplikaciji ovo bi zahtevalo
        # dodatne podatke iz Instagram-a
        engagement_stats = {}
        for username in self.not_following_back:
            # Simulirano - u stvarnoj aplikaciji bi se pristupalo stvarnim podacima
            engagement_stats[username] = {
                "likes": 0,
                "comments": 0,
                "views": 0,
                "last_interaction": "Nepoznato",
                "engagement_score": 0
            }

        self.engagement_stats = engagement_stats
        return engagement_stats

    def get_history_data(self) -> List[Dict[str, Any]]:
        """Vraća istorijske podatke za praćenje promena u vremenu"""
        return self.history_data