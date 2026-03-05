"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from importlib import import_module

try:
    from .recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs

try:
    tabulate = import_module("tabulate").tabulate
except ModuleNotFoundError:
    tabulate = None


def _print_recommendation_table(recommendations) -> None:
    headers = ["Rank", "Title", "Artist", "Score", "Reason"]
    rows = []
    for index, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        rows.append([
            index,
            song["title"],
            song["artist"],
            f"{score:.2f}",
            explanation,
        ])

    if tabulate is not None:
        print(tabulate(rows, headers=headers, tablefmt="github"))
        return

    all_rows = [headers] + rows
    widths = [max(len(str(row[col])) for row in all_rows) for col in range(len(headers))]

    def format_row(row_values):
        cells = [str(value).ljust(widths[idx]) for idx, value in enumerate(row_values)]
        return "| " + " | ".join(cells) + " |"

    divider = "+-" + "-+-".join("-" * width for width in widths) + "-+"

    print(divider)
    print(format_row(headers))
    print(divider)
    for row in rows:
        print(format_row(row))
    print(divider)


def main() -> None:
    songs = load_songs("data/songs.csv") 

    focus_profile = {"genre": "lofi", "mood": "focused", "energy": 0.4, "tempo_bpm": 80}
    workout_profile = {"genre": "hiphop", "mood": "intense", "energy": 0.9, "tempo_bpm": 140}
    chill_profile = {"genre": "acoustic", "mood": "chill", "energy": 0.3, "tempo_bpm": 70}

    # Pick one profile to run recommendations for
    user_profile_name = "focus"
    user_prefs = focus_profile

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nUser profile:")
    print(f"Name: {user_profile_name}")
    for key, value in user_prefs.items():
        print(f"- {key}: {value}")

    print("\nTop recommendations:\n")
    _print_recommendation_table(recommendations)


if __name__ == "__main__":
    main()
