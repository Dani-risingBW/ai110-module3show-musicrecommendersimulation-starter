
from src.recommender import Song, UserProfile, Recommender, recommend_songs


ADVERSARIAL_PROFILES = {
    "out_of_bounds_numeric": {"genre": "pop", "mood": "happy", "energy": 1.7, "tempo_bpm": 500},
    "negative_numeric": {"genre": "lofi", "mood": "chill", "energy": -0.6, "tempo_bpm": -20},
    "unknown_tags": {
        "genre": "drill-jazz-fusion",
        "mood": "transcendent",
        "energy": 0.5,
        "tempo_bpm": 100,
    },
    "case_whitespace_attack": {"genre": " Pop ", "mood": "HAPPY", "energy": 0.82, "tempo_bpm": 118},
    "tempo_omitted": {"genre": "pop", "mood": "happy", "energy": 0.82},
    "genre_only_bias_probe": {"genre": "ambient"},
    "contradictory_profile": {"genre": "ambient", "mood": "intense", "energy": 0.05, "tempo_bpm": 170},
    "tie_maker": {"genre": "lofi", "mood": "chill", "energy": 0.385, "tempo_bpm": 75},
}


def _adversarial_catalog():
    return [
        {
            "id": 1,
            "title": "Sunrise City",
            "artist": "Neon Echo",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.82,
            "tempo_bpm": 118.0,
            "valence": 0.84,
            "danceability": 0.79,
            "acousticness": 0.18,
        },
        {
            "id": 2,
            "title": "Focus Flow",
            "artist": "LoRoom",
            "genre": "lofi",
            "mood": "focused",
            "energy": 0.40,
            "tempo_bpm": 80.0,
            "valence": 0.59,
            "danceability": 0.60,
            "acousticness": 0.78,
        },
        {
            "id": 3,
            "title": "Library Rain",
            "artist": "Paper Lanterns",
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "tempo_bpm": 72.0,
            "valence": 0.60,
            "danceability": 0.58,
            "acousticness": 0.86,
        },
        {
            "id": 4,
            "title": "Temple of Silence",
            "artist": "Lotus Array",
            "genre": "ambient",
            "mood": "chill",
            "energy": 0.18,
            "tempo_bpm": 58.0,
            "valence": 0.63,
            "danceability": 0.27,
            "acousticness": 0.98,
        },
        {
            "id": 5,
            "title": "Bassline Mirage",
            "artist": "Subcurrent",
            "genre": "synthwave",
            "mood": "intense",
            "energy": 0.95,
            "tempo_bpm": 174.0,
            "valence": 0.72,
            "danceability": 0.89,
            "acousticness": 0.04,
        },
    ]

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_case_and_whitespace_in_prefs_still_match_genre_and_mood():
    songs = [
        {
            "id": 1,
            "title": "Case Match Track",
            "artist": "Tester",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "tempo_bpm": 120.0,
            "valence": 0.8,
            "danceability": 0.8,
            "acousticness": 0.2,
        },
        {
            "id": 2,
            "title": "Mismatch Track",
            "artist": "Tester",
            "genre": "rock",
            "mood": "intense",
            "energy": 0.8,
            "tempo_bpm": 120.0,
            "valence": 0.5,
            "danceability": 0.5,
            "acousticness": 0.2,
        },
    ]

    user_prefs = {"genre": " Pop ", "mood": "HAPPY", "energy": 0.8, "tempo_bpm": 120.0}
    recommendations = recommend_songs(user_prefs, songs, k=2)

    top_song, top_score, top_explanation = recommendations[0]
    assert top_song["title"] == "Case Match Track"
    assert top_score == 1.0
    assert "genre matches" in top_explanation
    assert "mood matches" in top_explanation


def test_adversarial_profiles_produce_ranked_results():
    songs = _adversarial_catalog()

    for profile_name, user_prefs in ADVERSARIAL_PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=3)

        assert len(recommendations) == 3, f"{profile_name} should return top-3 results"
        scores = [item[1] for item in recommendations]
        assert scores == sorted(scores, reverse=True), f"{profile_name} scores should be descending"
        assert all(0.0 <= score <= 1.0 for score in scores), f"{profile_name} scores must stay in [0, 1]"
