"""
Command line runner for the Music Recommender Simulation.

Run from the project root:
    python -m src.main
"""

import os
from src.recommender import load_songs, recommend_songs

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")

# ---------------------------------------------------------------------------
# User Profiles (Phase 4 — Stress Testing)
# ---------------------------------------------------------------------------

PROFILES = {
    "High-Energy Pop Fan": {
        "genre":        "pop",
        "mood":         "happy",
        "energy":       0.85,
        "valence":      0.82,
        "acousticness": 0.15,
        "tempo_bpm":    125,
        "danceability": 0.85,
    },
    "Chill Lofi Studier": {
        "genre":        "lofi",
        "mood":         "focused",
        "energy":       0.38,
        "valence":      0.58,
        "acousticness": 0.80,
        "tempo_bpm":    78,
        "danceability": 0.55,
    },
    "Deep Intense Rock": {
        "genre":        "rock",
        "mood":         "intense",
        "energy":       0.92,
        "valence":      0.40,
        "acousticness": 0.08,
        "tempo_bpm":    155,
        "danceability": 0.65,
    },
}


def print_recommendations(profile_name: str, recs: list) -> None:
    """Print a formatted recommendation block for one user profile."""
    width = 60
    print("\n" + "=" * width)
    print(f"  Profile: {profile_name}")
    print("=" * width)
    for rank, (song, score, explanation) in enumerate(recs, start=1):
        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}  |  Score: {score:.4f}")
        for reason in explanation.split("; "):
            print(f"       • {reason}")
    print()


def main() -> None:
    songs = load_songs(DATA_PATH)
    print(f"Loaded songs: {len(songs)}")

    for profile_name, user_prefs in PROFILES.items():
        recs = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(profile_name, recs)


if __name__ == "__main__":
    main()
