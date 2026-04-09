# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder 1.0 is a classroom simulation designed to suggest songs from a small catalog based on a user's stated musical preferences. It is intended for educational exploration of how content-based recommender systems work — not for use in a real product. It assumes the user can describe their taste in advance using attributes like preferred energy level, mood, and genre. It does not learn from behavior over time.

**Intended for:** Students learning about AI recommendation logic, content-based filtering, and algorithmic bias.
**Not intended for:** Real music discovery, deployment in any app, or drawing conclusions about real users' preferences.

---

## 3. How the Model Works

Imagine you tell a friend: "I want something high-energy, happy, and not too acoustic." VibeFinder does exactly what that friend would do — it goes through every song in its list and asks, "How closely does this song match what you described?"

For each song, it measures the gap between the song's properties and your stated preferences. A song with energy 0.82 scores nearly perfectly for a user who wants energy 0.85, because the gap is tiny. A song with energy 0.28 scores poorly. The same logic applies to mood match (happy vs. chill vs. intense), valence (how emotionally positive the song feels), acousticness (organic vs. electronic), tempo, and danceability.

Each dimension is given a weight that reflects how much it matters to overall vibe. Energy matters most (25%), followed by valence and mood (20% each), then acousticness (15%), tempo (10%), and danceability and genre (5% each). All the weighted scores are added together to give a final number between 0 and 1. The songs with the highest numbers are recommended.

The key design choice is that genre gets the *least* weight. This is intentional — a chill country ballad and a chill lo-fi track both match a "relaxed" user better than an intense rock song in the "right" genre.

---

## 4. Data

- **Catalog size:** 18 songs (10 original + 8 added)
- **Genres represented:** pop, lo-fi, rock, ambient, jazz, synthwave, indie pop, EDM, country, hip-hop, classical, metal, R&B, reggae, blues
- **Moods represented:** happy, chill, intense, relaxed, moody, focused, sad
- **Added songs cover:** electronic, acoustic, global, and heavy genres missing from the starter set
- **Limitations:** All songs are fictional. The catalog skews toward Western genres. There is no representation of K-pop, Latin, afrobeats, or classical non-Western music. Mood labels were assigned manually and reflect one person's interpretation — another person might label the same song differently.

---

## 5. Strengths

- **Clear matches feel right.** When a user's profile closely mirrors a song's attributes (e.g., "Chill Lofi Studier" gets Focus Flow at score 0.9856), the system produces results that feel intuitive.
- **Mood is a strong signal.** Because mood carries 20% weight, the system correctly separates an intense rock user from a chill ambient user even when their energy levels overlap.
- **Explanations are transparent.** Every recommendation includes a breakdown of why each feature contributed to the score, making the system auditable.
- **Works across genre boundaries.** A "happy" reggae song ranks highly for a "happy pop" user because the emotional match outweighs the genre mismatch — which is often correct in practice.

---

## 6. Limitations and Bias

- **Filter bubble risk.** Because the system only scores songs against a static profile, it will always return the same top songs for the same user. There is no diversity mechanism to surface surprising or "just outside your comfort zone" picks.
- **Small catalog amplifies bias.** With only 18 songs, any genre or mood with two or more entries has a structural advantage. If a user's top match is "happy," all three happy songs will appear in the top 5 regardless of other features.
- **Genre weight is almost invisible.** At 5% weight, genre has very little influence. This is intentional for vibe accuracy, but it means two songs with completely different sonic textures (jazz vs. metal) could score similarly if their numeric features align.
- **No context awareness.** The system does not know if the user is working out, sleeping, or commuting. Spotify adjusts recommendations by time of day and activity — this system treats all listening as equivalent.
- **Mood labels are subjective.** "Moody" was assigned to Night Drive Loop and Velvet Hours based on one person's interpretation. Another listener might call either of these "chill" or "romantic." Subjective labels are a real risk in any content-based system.
- **Acousticness can penalize valid matches.** A user who selects `acousticness: 0.80` (acoustic preference) will significantly downrank electronic songs even if those songs match perfectly on energy and mood.

---

## 7. Evaluation

Three distinct user profiles were tested:

**Profile 1 — High-Energy Pop Fan** (energy: 0.85, mood: happy, genre: pop)
Top result: Sunrise City (score 0.97). This felt correct — it is the only pop/happy song with high energy and high valence. The second result, Block Party Anthem (hip-hop/happy), was a pleasant surprise: it scored higher than Gym Hero because its valence and danceability were a better match, even without the genre bonus.

**Profile 2 — Chill Lofi Studier** (energy: 0.38, mood: focused, genre: lofi)
Top result: Focus Flow (score 0.99). Near-perfect match. The second and third results (Library Rain, Midnight Coding) are also lofi tracks but with "chill" mood rather than "focused" — they ranked below because they missed the mood bonus. Coffee Shop Jazz appeared at #4 despite being a different genre, because its energy and acousticness were close matches. This shows the system working as intended.

**Profile 3 — Deep Intense Rock** (energy: 0.92, mood: intense, genre: rock)
Top result: Storm Runner (score 0.98). Correct. Iron Cathedral (metal, intense) ranked #2 ahead of EDM and pop tracks because mood carries more weight than genre — intense metal is a better vibe match than a pop song that happens to be energetic.

**Experiment — Weight shift (energy doubled, genre halved):**
Doubling energy weight from 0.25 to 0.50 and halving genre from 0.05 to 0.025 caused Bass Drop Galaxy (EDM, 0.96 energy) to jump ahead of Storm Runner for the rock profile — because energy similarity now dominated. This confirmed that weight choices directly shape the character of the recommender, and that genre weight being too low makes the system genre-blind.

---

## 8. Future Work

1. **Add a diversity penalty.** After scoring all songs, demote songs by the same artist or genre if they already appear in the top 3 — this prevents the same cluster from dominating every recommendation.
2. **Add a "context" dimension.** Let the user specify activity (studying, working out, falling asleep) and map that to adjusted weights. Working out → boost energy weight. Studying → boost acousticness and reduce danceability weight.
3. **Replace manual mood labels with embeddings.** Use a small ML model trained on audio features to assign mood scores as continuous values rather than discrete strings — this eliminates the subjective labeling problem and enables finer-grained similarity.
4. **Support collaborative signals.** Even a simple "users who saved this song also saved these" layer would add genuine discovery beyond the user's stated preferences.
5. **Expand the catalog.** 18 songs is enough to learn the mechanics but too small to produce surprising results. A catalog of 500+ songs across more global genres would reveal real-world edge cases.

---

## 9. Personal Reflection

Building this system made me realize that a recommendation algorithm is really just a formalized version of "how similar is this to that?" — and the interesting part is *deciding what similar means*. Choosing that energy matters more than genre felt obvious once I thought about it (people listen to music for how it makes them feel, not what label it has), but without this project I probably would have assumed genre was the main factor.

The most surprising moment was when Block Party Anthem (hip-hop) ranked above Gym Hero (pop) for a "High-Energy Pop Fan" — not because the genre matched, but because the valence and danceability were a closer fit. That result was actually more musically correct than what a genre-first system would have produced. It showed me that even a simple algorithm, when the weights are thoughtfully designed, can surface genuinely good suggestions.

What this project also revealed is where human judgment still matters: someone had to decide what features to include, how to weight them, and how to label the moods. The math executes the logic, but the values embedded in the weights reflect a human perspective on what music is *for*. If I had weighted genre highest, the system would have recommended music based on taxonomy, not feeling — and that would have been technically functional but experientially wrong.
