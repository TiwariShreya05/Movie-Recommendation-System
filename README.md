# 🎬 Movie Recommendation System

A content-based ML system that suggests personalized movie recommendations by analyzing metadata — genre, cast, keywords, and overview.

---

## 📌 Project Overview

With the explosion of digital content, finding relevant movies is overwhelming. This system solves that by computing similarity scores between movies and recommending the most relevant ones based on a user's input.

---

## 🧠 How It Works

| Step | Process |
|------|---------|
| 1 | Load and clean movie dataset (titles, genres, cast, overview, keywords) |
| 2 | Combine relevant attributes into a unified feature representation |
| 3 | Vectorize text data using TF-IDF / Count Vectorizer |
| 4 | Compute cosine similarity scores between movies |
| 5 | Return top N most similar movies for a given input |

**Example**
```
Input:  Avatar
Output: Interstellar, Gravity, Star Wars... (based on content similarity)
```

---

## ⚙️ Tech Stack

- **Python** — core language
- **Pandas / NumPy** — data manipulation
- **Scikit-learn** — vectorization and cosine similarity
- **Jupyter Notebook** — development environment

---

## 🚀 Getting Started

**1. Clone the repository**
```bash
git clone https://github.com/TiwariShreya05/movie-recommendation-system.git
cd movie-recommendation-system
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the notebook**

Open `Jupyter Notebook` and run all cells, or execute the application script directly.

---

## 🔮 Future Improvements

- Collaborative filtering integration
- Hybrid recommendation system (content + collaborative)
- Web app deployment via Flask or Streamlit
- Real-time user ratings and feedback

---

## 📬 Contact

- 💼 LinkedIn: [linkedin.com/in/shreya-tiwari-520b692b3](https://www.linkedin.com/in/shreya-tiwari-520b692b3/)
- 📧 Email: shreyatiwari0801@gmail.com
- 🐙 GitHub: [github.com/TiwariShreya05](https://github.com/TiwariShreya05)
