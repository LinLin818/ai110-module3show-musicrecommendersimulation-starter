# 🎧 Model Card: Music Recommender Simulation

Major streaming platforms such as Youtube, Netflix and Spotify use sophisticated recommendatoin system to predict users' preferences.

Collaborative Filtering:
- Analyzing users' behaviors to find patterns
- Predict based on similar users's actions

Content Based Filtering:
- recommends contents users have enjoyed before
- Uses Matadata(genres, artists, themes) and user profiles to match content

Hybrid Approaches:
- Combines collaborative and content-based methods for better accuracy

Machine Learning Models:
- Matrix Factorization: Decomposes users' interaction
- Deep Learning: 
    - Neural Networks for complex patterns 

-Reinforcement Learning:
    - Optimizes recommendations in real time based on user feedback

Data Sources:
    - Explicit feedback(ratings, likes)
    - Implicit signals
    - External data


## Identify the main data types involved in these systems, such as likes, skips, playlists, tempo, or mood.

User interaction data:
-Likes/Dislikes :
-Skips/Plays
-Playlists
-Searches/Shares

Content Metadata:
-Tempo
-Mood/Emotion
-Genre/Style
-Artist/Album/Track info

Audio Features
- Acoustic Properties
- Embeddings

Contextual Data
-Temporal
-Situational

User Profiles
-Demographicwes
-Behavioral History


## Data Overview:
Total songs: 10 (small dataset; in practice, you'd need thousands for robust recommendations).
Categorical features: genre (7 unique: pop, lofi, rock, ambient, jazz, synthwave, indie pop), mood (6 unique: happy, chill, intense, relaxed, moody, focused).
Numerical features: energy (0.28–0.93), tempo_bpm (60–152), valence (0.48–0.84), danceability (0.41–0.88), acousticness (0.05–0.92).
Other: id, title, artist (identifiers, not features for similarity)



## 1. Model Name  

VibeFinder 1.0  

---

## 2. Intended Use  

This recommender suggests music based on user preferences. It generates song recommendations from a small catalog. It assumes users know their favorite genre, mood, and energy level. This is for classroom exploration, not real users yet.  

---

## 3. How the Model Works  

It scores songs by matching user preferences. It checks genre, mood, energy, and acousticness. Matches add points: genre +1, mood +1, energy similarity up to 2, acoustic bonus +0.5. I doubled energy weight and halved genre in experiments.

---

## 4. Data  

The model uses 18 songs from a CSV file. Genres include pop, lofi, rock, ambient, jazz, synthwave, indie pop. Moods are happy, chill, intense, relaxed, moody, focused. I did not add or remove data. Some musical tastes like classical or experimental are missing.  

---

## 5. Strengths  

The system works well for users with moderate preferences. It captures genre and mood matches correctly. Recommendations often matched my intuition for pop and lofi fans.  

---

## 6. Limitations and Bias 

One significant weakness discovered during experiments is the energy gap bias, where users with extreme energy preferences (e.g., very low or very high energy) are underserved by the linear penalty in the energy similarity calculation. This creates a filter bubble, as the system heavily favors songs within a moderate energy range (0.5-0.7), ignoring users who seek ultra-relaxing or hyper-intense music. For instance, a user targeting energy 0.9 might only receive low-scoring recommendations, limiting their exposure to diverse songs and reinforcing existing tastes rather than encouraging discovery. This bias stems from the dataset's clustering and the scoring logic's strict gap penalty, potentially marginalizing niche preferences in real-world applications.  

---

## 7. Evaluation  

I tested the recommender with three distinct user profiles: high_energy_pop (genre=pop, mood=happy, energy=0.9, likes_acoustic=False), chill_lofi (genre=lofi, mood=chill, energy=0.4, likes_acoustic=True), and deep_intense_rock (genre=rock, mood=intense, energy=0.95, likes_acoustic=False). What surprised me was how sensitive the rankings were to the weight shift experiment—doubling energy importance and halving genre led to significant reordering, like Rooftop Lights jumping in the high-energy profile despite no genre match, highlighting potential biases for extreme preferences.

Comparing high_energy_pop vs. chill_lofi: The high-energy profile favored upbeat, non-acoustic songs like Sunrise City and Gym Hero, while the chill profile shifted to relaxed, acoustic tracks like Forest Whispers and Midnight Jazz, making sense as it prioritizes low energy and acoustic bonuses over high-intensity matches.

Comparing high_energy_pop vs. deep_intense_rock: Both profiles emphasize high energy (0.9 and 0.95), but the rock profile leaned toward intense, non-acoustic rock songs like Thunder Road, whereas the pop profile included more genre-matched pop tracks; this difference validates that mood (intense vs. happy) and genre filters create distinct outputs even with similar energy levels.

Comparing chill_lofi vs. deep_intense_rock: The chill profile recommended mellow, acoustic lofi like Ocean Waves, while the rock profile pushed high-energy, intense rock; this contrast demonstrates the system's ability to handle opposing energy spectra, with acoustic preferences further differentiating the chill results.

---

## 8. Future Work  

Add more features like tempo or danceability. Explain recommendations better with reasons. Improve diversity by avoiding repeats. Handle complex tastes with user history.  

---

## 9. Personal Reflection  

My biggest learning moment was discovering how small changes in scoring weights can create big biases, like the energy gap ignoring extreme preferences. AI tools helped by generating code and explaining concepts quickly, but I double-checked them when outputs didn't match my intuition, like verifying math in scoring. I was surprised that simple matching algorithms still feel like real recommendations because they capture obvious patterns. Next, I'd try adding user feedback loops to adjust weights dynamically.  
