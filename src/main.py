"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs
import json


def format_recommendations(recommendations: list) -> None:
    """
    Display recommendations in a clean, readable terminal format.
    
    Shows:
    - Rank with heart emoji
    - Song title and artist
    - Final score with visual indicator
    - Detailed scoring breakdown with reasons
    """
    print("\n" + "=" * 70)
    print("🎵 TOP MUSIC RECOMMENDATIONS 🎵".center(70))
    print("=" * 70 + "\n")
    
    for rank, (song, score, explanation) in enumerate(recommendations, 1):
        # Format: Rank + Song info
        print(f"#{rank} ❤️  {song['title']}")
        print(f"    Artist: {song['artist']}")
        
        # Format: Score with visual bar
        score_pct = min(int(score / 4.0 * 20), 20)  # Max score ~4.0, normalize to 20 chars
        score_bar = "█" * score_pct + "░" * (20 - score_pct)
        print(f"    Score: {score:.2f}/4.0  [{score_bar}]")
        
        # Format: Scoring reasons
        print(f"    Why recommended:")
        print(f"{explanation}")
        
        # Separator
        print()


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    # Example user preference profiles
    high_energy_pop = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.9,
        "likes_acoustic": False,
    }
    chill_lofi = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.4,
        "likes_acoustic": True,
    }
    deep_intense_rock = {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.95,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    # Format and display recommendations
    format_recommendations(recommendations)
    
    # Summary stats
    print("=" * 70)
    print(f"User Profile: Genre={user_prefs.get('genre', 'any')} | "
          f"Mood={user_prefs.get('mood', 'any')} | "
          f"Energy={user_prefs.get('energy', 'any')}")
    print(f"Total songs scanned: {len(songs)}")
    print(f"Recommendations returned: {len(recommendations)}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

