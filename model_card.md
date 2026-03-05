# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **NEXSONG 1.2**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

- It recommends songs from a list/csv file that could represent your library or a library of songs that you don't know. The user would have to enter specific things about themselves or I could implement something to read the users profile or current song choice to then recommned other music. Right now this is from classroom exploration. 
---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

- I went further into detail in the README file but essentially it uses genre, energy, mood, and tempo to score and rank music. It weighs each feature differently but it does matching to the categorical features while the numerical data uses a mathematical formula. 
---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

- The data set is a fixed file where I can add or remove data. It may not be the best to test since it is a small dataset. 
---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

- Every recommendation is traceable to clear factors
- It's modular; everything is separated cleanly and easy to improve incrementally
- it handles partial preferences: if a user omits tempo_bpm
- It handles messy categorical input well
- It's fast and lightweight
---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

- Valence, danceability, and acousticness are currently unused. The scoring can also introduce energy-gap bias, and the combined genre+mood exact-match weight (50%) can dominate results; this effect becomes stronger when `tempo_bpm` is missing. 

Because genre and mood are exact-match checks with large combined weight, users whose tastes do not fit those labels exactly can be pushed down in rankings even when other signals are close. The energy-gap formula also assumes each user has one ideal energy point, which can misrepresent people with broader or context-dependent taste (for example, liking both very calm and very high-energy songs). This can create a filter-bubble effect where similar songs keep repeating while less obvious but still relevant songs are rarely surfaced.
---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

Overall, I learned that the recommender behaved as expected. 
I evaluated the recommender with three baseline taste profiles (`focus`, `workout`, and `chill`) and an adversarial profile set in the test suite. The adversarial set included out-of-range numeric inputs, unknown genre/mood labels, case/whitespace variants (for example, `" Pop "` and `"HAPPY"`), missing tempo, genre-only preferences, contradictory preferences, and tie-making values. For simple comparisons, I checked whether rankings stayed sorted by score, whether all scores stayed in the valid range `[0,1]`, and whether exact or near-exact matches appeared at the top as expected. I also used lightweight automated tests (`pytest`) to confirm core behavior: recommendation ordering, non-empty explanations, case/whitespace normalization for categorical matching, and stable top-`k` outputs across adversarial inputs.


---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

- I could connect it to an actual dataset to test it. 
- I could make it automate for itself with testing and training using datasets. 
- I could build playlist using the recommended songs
- I can utilize the other features that I didn't use from the songs file
---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

- I learned that you can use mathematical formulas to score data and rank them. I learned that that's what spotify and apple use (i used a more simplified version). 
- I can see basic biases that can be discussed before making my recommender to avoid those.
- It makes me appreciate how they take in multiple features to determine the best songs to recommend you. Also all the suggested playlist come from weighing features differently. 