# Profile Comparison Reflection

## Profile 1 vs Profile 2: High-Energy Pop Fan vs Chill Lofi Studier

**What changed:** The top results were completely different — Sunrise City (energetic, bright pop) dominated the first profile, while Focus Flow (quiet, focused lofi) dominated the second. No song appeared in both top-5 lists.

**Why it makes sense:** These two profiles sit at opposite ends of the energy spectrum (0.85 vs 0.38) and opposite ends of acousticness (electronic vs acoustic). Since energy carries the highest weight (25%), the algorithm correctly identifies that songs near the middle — like Coffee Shop Jazz (0.37 energy) — belong closer to the lofi profile even though they share no genre. The profiles are genuinely different people, and the system treated them that way.

**Interesting observation:** Reggae (Island Breeze) appeared in the High-Energy Pop profile at #4, and Jazz (Coffee Shop Stories) appeared in the Chill Lofi profile at #4. Neither matched the genre preference. This shows the system is mood-and-vibe driven, not genre-driven — which is the intended behavior.

---

## Profile 2 vs Profile 3: Chill Lofi Studier vs Deep Intense Rock

**What changed:** The rock profile returned Storm Runner, Iron Cathedral, and Bass Drop Galaxy — all high-intensity tracks with very low acousticness and tempo above 140 BPM. The lofi profile returned quiet, slow songs with high acousticness. The two profiles share zero overlap in their top 5.

**Why it makes sense:** Energy (0.38 vs 0.92) and acousticness (0.80 vs 0.08) are almost perfectly inverted between these two profiles. Any song that scores well for one scores poorly for the other. This is the algorithm working as designed — the weights on these two features together account for 40% of the total score, which is enough to completely separate these two listening contexts.

**Interesting observation:** Bass Drop Galaxy (EDM) ranked #3 for the rock user, despite being a different genre. Its energy (0.96), low acousticness (0.03), and intense mood all matched the rock profile closely. This is a case where the algorithm found a musically valid cross-genre recommendation — someone who wants intense, hard-driving music would likely enjoy bass-heavy EDM even if they primarily identify as a rock listener.

---

## Profile 1 vs Profile 3: High-Energy Pop Fan vs Deep Intense Rock

**What changed:** Both profiles have high energy, but the rock profile wants darker valence (0.40 vs 0.82) and much lower acousticness (0.08 vs 0.15). The pop profile wants happy, bright music; the rock profile wants intense, dark music.

**Why it makes sense:** Gym Hero (pop/intense) appeared in both lists — #5 for the pop fan, #4 for the rock user. This is the one song in the catalog that bridges both profiles: it has high energy but is pop-genre and has slightly higher valence than the ideal for a rock user. The system correctly placed it lower for both rather than #1 for either, because it is not a perfect match for either profile — it sits in between.

**Key takeaway:** Valence is doing important work here. Two users can both want high energy, but one wants it to feel euphoric and the other wants it to feel dark and aggressive. Without the valence feature, both profiles would receive nearly identical recommendations. This confirms that energy + valence together capture the two-axis emotional space that most people use when describing "what kind of music do I want right now."
