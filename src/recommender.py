import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass

TEMPO_MIN = 60
TEMPO_MAX = 168

# Feature weights — must sum to 1.0
WEIGHTS = {
    "energy":       0.25,
    "valence":      0.20,
    "mood":         0.20,
    "acousticness": 0.15,
    "tempo_bpm":    0.10,
    "danceability": 0.05,
    "genre":        0.05,
}


@dataclass
class Song:
    """Represents a song and its audio and metadata attributes."""
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
    """Represents a user's music taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """Scores and ranks Song objects against a UserProfile using weighted proximity scoring."""

    def __init__(self, songs: List[Song]):
        """Initialize the recommender with a catalog of Song objects."""
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, str]:
        """Compute a weighted proximity score and explanation string for a single Song."""
        parts = []
        total = 0.0

        # Genre match (binary)
        if song.genre == user.favorite_genre:
            total += WEIGHTS["genre"]
            parts.append(f"genre match (+{WEIGHTS['genre']:.2f})")

        # Mood match (binary)
        if song.mood == user.favorite_mood:
            total += WEIGHTS["mood"]
            parts.append(f"mood match (+{WEIGHTS['mood']:.2f})")

        # Energy proximity: reward closeness, not raw magnitude
        ep = 1.0 - abs(song.energy - user.target_energy)
        total += ep * WEIGHTS["energy"]
        parts.append(f"energy proximity {ep:.2f} (+{ep * WEIGHTS['energy']:.2f})")

        # Acousticness preference (derived from likes_acoustic flag)
        target_ac = 0.80 if user.likes_acoustic else 0.20
        acp = 1.0 - abs(song.acousticness - target_ac)
        total += acp * WEIGHTS["acousticness"]
        parts.append(f"acousticness fit {acp:.2f} (+{acp * WEIGHTS['acousticness']:.2f})")

        # Tempo proximity (normalized to 0–1 range, target derived from energy level)
        target_bpm_raw = TEMPO_MIN + user.target_energy * (TEMPO_MAX - TEMPO_MIN)
        norm_song   = (song.tempo_bpm   - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)
        norm_target = (target_bpm_raw   - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)
        tp = 1.0 - abs(norm_song - norm_target)
        total += tp * WEIGHTS["tempo_bpm"]
        parts.append(f"tempo proximity {tp:.2f} (+{tp * WEIGHTS['tempo_bpm']:.2f})")

        # Valence fit: high-energy users tend to want positive valence
        vp = 1.0 - abs(song.valence - user.target_energy)
        total += vp * WEIGHTS["valence"]
        parts.append(f"valence fit {vp:.2f} (+{vp * WEIGHTS['valence']:.2f})")

        # Danceability fit: high-energy users tend to want high danceability
        dp = 1.0 - abs(song.danceability - user.target_energy)
        total += dp * WEIGHTS["danceability"]
        parts.append(f"danceability fit {dp:.2f} (+{dp * WEIGHTS['danceability']:.2f})")

        return round(total, 4), "; ".join(parts)

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Songs ranked by score for the given UserProfile."""
        scored = [(song, self._score(user, song)[0]) for song in self.songs]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a Song was recommended."""
        _, explanation = self._score(user, song)
        return explanation


# ---------------------------------------------------------------------------
# Functional API (used by src/main.py)
# ---------------------------------------------------------------------------

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dicts with typed numeric values."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    int(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song dict against user preferences using weighted proximity.

    Returns (score, reasons) where score is 0.0–1.0 and reasons is a list
    of strings explaining each scoring component.
    """
    reasons = []
    total = 0.0

    # Genre match (binary)
    if song["genre"] == user_prefs.get("genre", ""):
        total += WEIGHTS["genre"]
        reasons.append(f"genre match (+{WEIGHTS['genre']:.2f})")

    # Mood match (binary)
    if song["mood"] == user_prefs.get("mood", ""):
        total += WEIGHTS["mood"]
        reasons.append(f"mood match (+{WEIGHTS['mood']:.2f})")

    # Energy proximity: reward closeness to target, not raw magnitude
    target_energy = user_prefs.get("energy", 0.5)
    ep = 1.0 - abs(song["energy"] - target_energy)
    total += ep * WEIGHTS["energy"]
    reasons.append(f"energy proximity {ep:.2f} (+{ep * WEIGHTS['energy']:.2f})")

    # Valence proximity
    target_valence = user_prefs.get("valence", 0.5)
    vp = 1.0 - abs(song["valence"] - target_valence)
    total += vp * WEIGHTS["valence"]
    reasons.append(f"valence proximity {vp:.2f} (+{vp * WEIGHTS['valence']:.2f})")

    # Acousticness proximity
    target_ac = user_prefs.get("acousticness", 0.5)
    acp = 1.0 - abs(song["acousticness"] - target_ac)
    total += acp * WEIGHTS["acousticness"]
    reasons.append(f"acousticness proximity {acp:.2f} (+{acp * WEIGHTS['acousticness']:.2f})")

    # Tempo proximity (normalized to 0–1 before differencing)
    target_bpm  = user_prefs.get("tempo_bpm", 100)
    norm_song   = (song["tempo_bpm"] - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)
    norm_target = (target_bpm        - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)
    tp = 1.0 - abs(norm_song - norm_target)
    total += tp * WEIGHTS["tempo_bpm"]
    reasons.append(f"tempo proximity {tp:.2f} (+{tp * WEIGHTS['tempo_bpm']:.2f})")

    # Danceability proximity
    target_dance = user_prefs.get("danceability", 0.5)
    dp = 1.0 - abs(song["danceability"] - target_dance)
    total += dp * WEIGHTS["danceability"]
    reasons.append(f"danceability proximity {dp:.2f} (+{dp * WEIGHTS['danceability']:.2f})")

    return round(total, 4), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort descending by score, and return the top k results.

    Each result is a tuple of (song_dict, score, explanation_string).
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
