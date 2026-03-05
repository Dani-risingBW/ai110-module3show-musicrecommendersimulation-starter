from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_tempo_bpm: Optional[float] = None

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Initialize recommender with a list of songs."""
        self.songs = songs

    def _tempo_range(self) -> float:
        """Calculate the tempo range (max - min) across all songs."""
        if not self.songs:
            return 1.0
        tempos = [song.tempo_bpm for song in self.songs]
        spread = max(tempos) - min(tempos)
        return spread if spread > 0 else 1.0

    @staticmethod
    def _energy_closeness(song_energy: float, target_energy: float) -> float:
        """Compute closeness score between song energy and target energy (1.0 = exact match)."""
        score = 1.0 - abs(song_energy - target_energy)
        return max(0.0, min(1.0, score))

    @staticmethod
    def _tempo_closeness(song_tempo: float, target_tempo: float, tempo_range: float) -> float:
        """Compute normalized closeness score between song tempo and target tempo."""
        score = 1.0 - (abs(song_tempo - target_tempo) / tempo_range)
        return max(0.0, min(1.0, score))

    def _score_song(self, user: UserProfile, song: Song) -> float:
        """Compute weighted score for a song based on user preferences."""
        weights = {
            "genre": 0.25,
            "mood": 0.25,
            "energy": 0.30,
            "tempo": 0.20,
        }

        components: List[Tuple[float, float]] = []

        genre_score = 1.0 if song.genre == user.favorite_genre else 0.0
        components.append((genre_score, weights["genre"]))

        mood_score = 1.0 if song.mood == user.favorite_mood else 0.0
        components.append((mood_score, weights["mood"]))

        energy_score = self._energy_closeness(song.energy, user.target_energy)
        components.append((energy_score, weights["energy"]))

        if user.target_tempo_bpm is not None:
            tempo_score = self._tempo_closeness(
                song.tempo_bpm,
                user.target_tempo_bpm,
                self._tempo_range(),
            )
            components.append((tempo_score, weights["tempo"]))

        weight_total = sum(weight for _, weight in components)
        if weight_total == 0:
            return 0.0
        weighted_sum = sum(score * weight for score, weight in components)
        return weighted_sum / weight_total

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return top k songs ranked by score for the given user profile."""
        ranked = sorted(
            self.songs,
            key=lambda song: self._score_song(user, song),
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Generate human-readable explanation for why a song was recommended."""
        reasons: List[str] = []

        if song.genre == user.favorite_genre:
            reasons.append("genre matches")
        if song.mood == user.favorite_mood:
            reasons.append("mood matches")

        energy_gap = abs(song.energy - user.target_energy)
        reasons.append(f"energy is close (Δ={energy_gap:.2f})")

        if user.target_tempo_bpm is not None:
            tempo_gap = abs(song.tempo_bpm - user.target_tempo_bpm)
            reasons.append(f"tempo is close (Δ={tempo_gap:.0f} bpm)")

        return ", ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []
    with open(csv_path, "r", encoding="utf-8") as file_handle:
        reader = csv.DictReader(file_handle)
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )
    return songs


def _tempo_range_dicts(songs: List[Dict]) -> float:
    """Calculate tempo range from a list of song dictionaries."""
    if not songs:
        return 1.0
    tempos = [song["tempo_bpm"] for song in songs]
    spread = max(tempos) - min(tempos)
    return spread if spread > 0 else 1.0


def _score_song_dict(user_prefs: Dict, song: Dict, tempo_range: float) -> float:
    """Compute weighted score for a song dictionary based on user preference dictionary."""
    weights = {
        "genre": 0.25,
        "mood": 0.25,
        "energy": 0.30,
        "tempo": 0.20,
    }

    components: List[Tuple[float, float]] = []

    if "genre" in user_prefs:
        genre_score = 1.0 if song["genre"] == user_prefs["genre"] else 0.0
        components.append((genre_score, weights["genre"]))

    if "mood" in user_prefs:
        mood_score = 1.0 if song["mood"] == user_prefs["mood"] else 0.0
        components.append((mood_score, weights["mood"]))

    if "energy" in user_prefs:
        energy_score = 1.0 - abs(song["energy"] - user_prefs["energy"])
        energy_score = max(0.0, min(1.0, energy_score))
        components.append((energy_score, weights["energy"]))

    if "tempo_bpm" in user_prefs:
        tempo_score = 1.0 - (abs(song["tempo_bpm"] - user_prefs["tempo_bpm"]) / tempo_range)
        tempo_score = max(0.0, min(1.0, tempo_score))
        components.append((tempo_score, weights["tempo"]))

    if not components:
        return 0.0

    total_weight = sum(weight for _, weight in components)
    return sum(score * weight for score, weight in components) / total_weight


def _build_explanation(user_prefs: Dict, song: Dict) -> str:
    """Build human-readable explanation string for a recommendation."""
    reasons: List[str] = []
    if user_prefs.get("genre") == song["genre"]:
        reasons.append("genre matches")
    if user_prefs.get("mood") == song["mood"]:
        reasons.append("mood matches")
    if "energy" in user_prefs:
        reasons.append(f"energy close (Δ={abs(song['energy'] - user_prefs['energy']):.2f})")
    if "tempo_bpm" in user_prefs:
        reasons.append(
            f"tempo close (Δ={abs(song['tempo_bpm'] - user_prefs['tempo_bpm']):.0f} bpm)"
        )
    return ", ".join(reasons) if reasons else "closest overall feature match"

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    tempo_range = _tempo_range_dicts(songs)
    scored: List[Tuple[Dict, float, str]] = []

    for song in songs:
        score = _score_song_dict(user_prefs, song, tempo_range)
        explanation = _build_explanation(user_prefs, song)
        scored.append((song, score, explanation))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
