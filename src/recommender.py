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
    release_year: Optional[int] = None

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

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """
        Recommend top k songs for a user based on scoring logic.
        Scores are based on: genre match (+1.0), mood match (+1.0),
        energy similarity (0-2.0), and acousticness bonus (0-0.5).
        """
        # Score all songs
        scored_songs = []
        for song in self.songs:
            score = self._calculate_song_score(song, user)
            scored_songs.append((song, score))
        
        # Sort by score descending
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        
        # Return top k songs
        return [song for song, _ in scored_songs[:k]]
    
    def _calculate_song_score(self, song: Song, user: UserProfile) -> float:
        """
        Calculate a song's score based on user preferences.
        Weights:
        - Genre match: +1.0
        - Mood match: +1.0
        - Energy similarity: 0-2.0 (2.0 * (1.0 - abs_difference))
        - Acousticness bonus: 0-0.5 (if user likes acoustic)
        """
        score = 0.0
        
        # Genre match: +1.0
        if song.genre.lower() == user.favorite_genre.lower():
            score += 1.0
        
        # Mood match: +1.0
        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.0
        
        # Energy similarity: 0.0 - 2.0
        energy_diff = abs(song.energy - user.target_energy)
        energy_score = max(0.0, 1.0 - energy_diff)
        score += energy_score * 2
        
        # Acousticness bonus: 0.0 - 0.5
        if user.likes_acoustic:
            score += song.acousticness * 0.5
        
        return score

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """
        Provide a human-readable explanation of why a song was recommended.
        """
        score = self._calculate_song_score(song, user)
        reasons = []
        
        # Genre match
        if song.genre.lower() == user.favorite_genre.lower():
            reasons.append(f"Matches your favorite genre: {song.genre}")
        
        # Mood match
        if song.mood.lower() == user.favorite_mood.lower():
            reasons.append(f"Matches your favorite mood: {song.mood}")
        
        # Energy similarity
        energy_diff = abs(song.energy - user.target_energy)
        if energy_diff < 0.1:
            reasons.append(f"Perfect energy level (target: {user.target_energy}, song: {song.energy})")
        elif energy_diff < 0.3:
            reasons.append(f"Close energy match (target: {user.target_energy}, song: {song.energy})")
        
        # Acousticness
        if user.likes_acoustic and song.acousticness > 0.7:
            reasons.append(f"Highly acoustic ({song.acousticness:.1%})")
        
        explanation = f"'{song.title}' by {song.artist}\n"
        explanation += f"Overall Score: {score:.2f}\n"
        explanation += "Why recommended:\n"
        if reasons:
            explanation += "\n".join(f"  • {reason}" for reason in reasons)
        else:
            explanation += "  • Similar to songs in your taste profile"
        
        return explanation

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file and returns a list of dictionaries.
    Uses Python's csv.DictReader to parse the CSV file.
    
    Expected CSV columns: id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, acousticness
    
    Returns:
        List[Dict]: A list of song dictionaries with keys from the CSV header.
    """
    print(f"Loading songs from {csv_path}...")
    songs = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric strings to float for relevant fields
                song = {
                    'id': int(row['id']),
                    'title': row['title'],
                    'artist': row['artist'],
                    'genre': row['genre'],
                    'mood': row['mood'],
                    'energy': float(row['energy']),
                    'tempo_bpm': float(row['tempo_bpm']),
                    'valence': float(row['valence']),
                    'danceability': float(row['danceability']),
                    'acousticness': float(row['acousticness']),
                }
                songs.append(song)
        print(f"Successfully loaded {len(songs)} songs.")
    except FileNotFoundError:
        print(f"Error: File {csv_path} not found.")
        print(f"Make sure the file exists at: {csv_path}")
    except ValueError as e:
        print(f"Error: Failed to convert numeric values in CSV: {e}")
    except Exception as e:
        print(f"Error loading CSV: {e}")
    
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song and return both the score and list of reasons."""
    score = 0.0
    reasons = []
    
    # Normalize preference keys for flexibility
    favorite_genre = (user_prefs.get('favorite_genre') or user_prefs.get('genre', '')).lower()
    favorite_mood = (user_prefs.get('favorite_mood') or user_prefs.get('mood', '')).lower()
    target_energy = float(user_prefs.get('target_energy') or user_prefs.get('energy', 0.5))
    likes_acoustic = user_prefs.get('likes_acoustic', False)
    
    # Get song attributes
    song_genre = song.get('genre', '').lower()
    song_mood = song.get('mood', '').lower()
    song_energy = float(song.get('energy', 0.5))
    song_acousticness = float(song.get('acousticness', 0))
    
    # GENRE MATCH: +1.0 points
    if song_genre == favorite_genre and favorite_genre:
        score += 1.0
        reasons.append(f"genre match: {song.get('genre')} (+1.0)")
    
    # MOOD MATCH: +1.0 point
    if song_mood == favorite_mood and favorite_mood:
        score += 1.0
        reasons.append(f"mood match: {song.get('mood')} (+1.0)")
    
    # ENERGY SIMILARITY: 0-2.0 points
    energy_diff = abs(song_energy - target_energy)
    energy_score = max(0.0, 1.0 - energy_diff)
    score += energy_score * 2
    reasons.append(f"energy similarity: target {target_energy:.1f}, song {song_energy:.1f} (+{energy_score * 2:.2f})")
    
    # ACOUSTICNESS BONUS: 0-0.5 points (if user likes acoustic)
    if likes_acoustic:
        acoustic_bonus = song_acousticness * 0.5
        score += acoustic_bonus
        reasons.append(f"acousticness bonus: {song_acousticness:.1%} acoustic (+{acoustic_bonus:.2f})")
    
    return score, reasons

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    # TODO: Implement scoring logic using your Algorithm Recipe from Phase 2.
    # Expected return format: (score, reasons)
    return []

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top k scored song recommendations with explanations."""
    def to_recommendation(song: Dict) -> Tuple[Dict, float, str]:
        """Transform a song into a (song, score, explanation) tuple."""
        score, reasons = score_song(user_prefs, song)
        explanation = "\n".join(f"  • {reason}" for reason in reasons)
        return (song, score, explanation)
    
    # Map scoring function to all songs, sort by score, return top k
    return sorted(map(to_recommendation, songs), key=lambda x: x[1], reverse=True)[:k]
