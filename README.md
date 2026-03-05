# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
  - My system uses `mood`, `energy`, and `tempo_bpm` to match songs to a user's preference.
- What information does your `UserProfile` store
  - My `UserProfile` stores preferred mood, target energy (0 to 1), and target tempo in BPM, which are used to score songs by closeness and mood match.
- How does your `Recommender` compute a score for each song
  - It computes a weighted score from mood match, energy closeness, and tempo closeness, then ranks songs from highest to lowest score.
  - Explained below
- How do you choose which songs to recommend
  - Explained below

You can include a simple diagram or bullet list if helpful.

---

## Example Taste Profiles

Use these as concrete user profiles your recommender can compare songs against.

- **Focus profile**
  - `mood = focused`
  - `energy = 0.40`
  - `tempo_bpm = 80`
  - Description: Calm, steady tracks for concentration.

- **Workout profile**
  - `mood = intense`
  - `energy = 0.90`
  - `tempo_bpm = 140`
  - Description: Fast, high-energy songs for training.

- **Chill profile**
  - `mood = chill`
  - `energy = 0.30`
  - `tempo_bpm = 70`
  - Description: Low-energy, slower songs for relaxing.

In Python dictionary form:

```python
focus_profile = {"mood": "focused", "energy": 0.40, "tempo_bpm": 80}
workout_profile = {"mood": "intense", "energy": 0.90, "tempo_bpm": 140}
chill_profile = {"mood": "chill", "energy": 0.30, "tempo_bpm": 70}
```

---

## Distance-to-Preference Score (Numerical Features)

Use this score when you want to reward songs that are **closer** to a user's target value (instead of just higher or lower).

For a numerical feature like `energy`:

$$
s_f(u, i) = 1 - \frac{|x_{i,f} - p_{u,f}|}{x_{f,\max} - x_{f,\min}}
$$

Where:

- $s_f(u, i)$ = similarity score for feature $f$ between user $u$ and song $i$
- $x_{i,f}$ = song value for feature $f$ (for example, song energy)
- $p_{u,f}$ = user preferred value for feature $f$
- $x_{f,\min}, x_{f,\max}$ = min and max values for feature $f$ in your dataset

Interpretation:

- Exact match ($x_{i,f} = p_{u,f}$) gives score $1.0$
- Larger distance from preference lowers the score toward $0.0$
- The score is symmetric: being above or below preference is penalized equally

Example with `energy` in range $[0,1]$:

- User preference: $p = 0.80$
- Song A: $x = 0.75 \Rightarrow s = 1 - |0.75 - 0.80| = 0.95$
- Song B: $x = 0.40 \Rightarrow s = 1 - |0.40 - 0.80| = 0.60$

So Song A is a better match on `energy` because it is closer to the user's preference.

---

## Scoring Recipe (Used in This Code)

My recommender computes a weighted score between 0 and 1 for each song, then sorts songs from highest to lowest score.

### Feature Weights

- Genre match: 0.25
- Mood match: 0.25
- Energy closeness: 0.30
- Tempo closeness: 0.20 (only used if the user provides `tempo_bpm`)

### Per-Feature Scores

- Genre score:

$$
	ext{genre\_score} =
\begin{cases}
1, & \text{if song.genre = user.genre} \\
0, & \text{otherwise}
\end{cases}
$$

- Mood score:

$$
	ext{mood\_score} =
\begin{cases}
1, & \text{if song.mood = user.mood} \\
0, & \text{otherwise}
\end{cases}
$$

- Energy closeness:

$$
	ext{energy\_score} = \max\left(0,\, 1 - |\text{song.energy} - \text{user.target\_energy}|\right)
$$

- Tempo closeness (if target tempo exists):

$$
	ext{tempo\_score} = \max\left(0,\, 1 - \frac{|\text{song.tempo} - \text{user.target\_tempo}|}{\text{tempo\_range}}\right)
$$

where:

$$
	ext{tempo\_range} = \max(\text{all song tempos}) - \min(\text{all song tempos})
$$

### Final Song Score

If all 4 features are present:

$$
	ext{score} = \frac{0.25\cdot\text{genre\_score} + 0.25\cdot\text{mood\_score} + 0.30\cdot\text{energy\_score} + 0.20\cdot\text{tempo\_score}}{1.00}
$$

If tempo is not provided, the recommender excludes tempo and re-normalizes by the sum of the used weights:

$$
	ext{score} = \frac{\sum (w_i \cdot s_i)}{\sum w_i\text{ used}}
$$

Then it recommends the top $k$ songs with the highest score.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

Expected bias note: this recommender is likely to favor songs from already common genres/moods in the CSV and songs near the chosen energy/tempo targets, which can under-recommend niche styles or tracks that are good fits in ways not captured by these features.

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

