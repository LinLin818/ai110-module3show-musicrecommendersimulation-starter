import sys
sys.path.insert(0, 'src')
from recommender import load_songs, recommend_songs

songs = load_songs('data/songs.csv')

profiles = [
    ('High-Energy Pop', {'genre': 'pop', 'mood': 'happy', 'energy': 0.9, 'likes_acoustic': False}),
    ('Chill Lofi', {'genre': 'lofi', 'mood': 'chill', 'energy': 0.4, 'likes_acoustic': True}),
    ('Deep Intense Rock', {'genre': 'rock', 'mood': 'intense', 'energy': 0.95, 'likes_acoustic': False}),
]

for name, prefs in profiles:
    print('\n' + '=' * 70)
    print(name.upper())
    print('=' * 70)
    recs = recommend_songs(prefs, songs, k=5)
    for i, (song, score, explanation) in enumerate(recs, 1):
        print(f"# {i}. {song['title']} by {song['artist']} - Score: {score:.2f}")
        print(explanation)
        print()
