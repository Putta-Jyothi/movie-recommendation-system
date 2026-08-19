# 🎬 Movie Recommendation System

A Machine Learning-based web application that recommends movies based on the movie selected by the user.

The system uses **Content-Based Filtering** to find similar movies and provides detailed movie information such as ratings, release year, genre, director, cast, overview, and posters.

---

## 🚀 Live Demo

[Open Movie Recommendation System](https://putta-jyothi-movie.streamlit.app/)

---

## 📸 Screenshots

### 🏠 Home Page

![Home Page](./home.png)

### 🎬 Movie Recommendations

![Movie Recommendations](./recommend.png)

### 📊 Dashboard

![Dashboard](./dashboard.png)

### ❤️ Watchlist

![Watchlist](./watchlist.png)

---

## 📌 Project Overview

The **Movie Recommendation System** is an interactive web application that helps users discover movies based on their interests.

Users can select a movie from the available movie collection, and the system recommends the **Top 5 similar movies** using Content-Based Filtering and Cosine Similarity.

The application also provides detailed movie information, an interactive dashboard, and a watchlist feature.

---

## ✨ Features

### 🎬 Movie Recommendations

- Content-Based Movie Recommendation
- Recommends Top 5 similar movies
- Uses Cosine Similarity
- Movie search and selection
- Displays recommended movie posters

### 🔎 Movie Search

- Search and select movies easily
- Select a movie from the available movie collection
- Get recommendations based on the selected movie

### ⭐ Movie Ratings

- Displays movie ratings
- Shows rating information for selected and recommended movies
- Rating distribution available in the dashboard

### 📅 Release Information

- Displays movie release year
- Shows movie release date
- Provides movies-by-year visualization

### 🎭 Genre Information

- Displays movie genres
- Allows users to explore genre information
- Provides genre-based statistics in the dashboard

### 🎬 Director Information

- Displays the director of the selected movie
- Director information is retrieved from movie data

### 👥 Cast Information

- Displays cast information
- Provides details about actors associated with the movie

### 📝 Movie Overview

- Displays a description of the selected movie
- Helps users understand the movie before watching

### 🖼️ Movie Posters

- Displays movie posters
- Posters are retrieved using the TMDB API

### ❤️ Watchlist

- Add movies to a personal watchlist
- View saved movies
- Display movie information in the watchlist
- Keep track of movies to watch later

### 📊 Interactive Dashboard

The dashboard provides useful movie statistics including:

- Total number of movies
- Average rating
- Highest-rated movies
- Rating distribution
- Movies by release year
- Movies by genre
- Top-rated movies

---

## 🧠 Machine Learning

The recommendation system uses **Content-Based Filtering**.

### How It Works

```text
User selects a movie
        ↓
Movie features are extracted
        ↓
Movie features are processed
        ↓
Movie features are converted into numerical representation
        ↓
Cosine Similarity is calculated
        ↓
Movies are ranked based on similarity
        ↓
Top 5 similar movies are displayed
```

### 🎯 Cosine Similarity

Cosine Similarity is used to calculate how similar two movies are based on their feature vectors.

Movies with higher similarity scores are considered more similar and are recommended to the user.

---

## 🌟 Project Highlights

- Built a content-based movie recommendation system using Machine Learning
- Implemented Cosine Similarity to recommend the Top 5 similar movies
- Integrated TMDB API for movie posters and movie details
- Developed an interactive Streamlit web application
- Added Watchlist functionality for saving movies
- Created an interactive dashboard for movie statistics and visualizations

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Programming language |
| Streamlit | Web application and user interface |
| Pandas | Data processing |
| NumPy | Numerical operations |
| Scikit-learn | Machine Learning and similarity calculation |
| Plotly | Interactive data visualization |
| TMDB API | Movie information and posters |
| Pickle | Saving and loading processed data |

---

## 📂 Dataset

The project uses the **TMDB 5000 Movie Dataset**.

### Dataset Files

- `tmdb_5000_movies.csv`
- `tmdb_5000_credits.csv`

The dataset contains information such as:

- Movie title
- Genres
- Cast
- Director
- Ratings
- Release date
- Overview
- Keywords

---

## 📊 Dashboard

The application provides an interactive dashboard for exploring movie statistics.

### Dashboard Features

- 📊 Total number of movies
- ⭐ Average rating
- 🏆 Highest-rated movies
- 📈 Rating distribution
- 📅 Movies by release year
- 🎭 Movies by genre
- 🏆 Top-rated movies

---

## ❤️ Watchlist

The Watchlist feature allows users to save movies they are interested in.

Saved movies can display information such as:

- 🎬 Movie title
- ⭐ Rating
- 📅 Release year
- 🎭 Genre
- 🎬 Director
- 👥 Cast
- 📝 Overview

This allows users to keep track of movies they want to watch later.

---

## 🎞️ Movie Details

For selected movies, the application displays:

- 🖼️ Movie poster
- 🎬 Movie title
- ⭐ Rating
- 📅 Release date
- 📅 Release year
- 🎭 Genre
- 🎬 Director
- 👥 Cast
- 📝 Overview

Movie posters and additional movie information are retrieved using the **TMDB API**.

---

## 🔐 API Key Security

The TMDB API key is stored securely using **Streamlit Secrets**.

The API key is not included directly in the source code or GitHub repository.

The `.streamlit/secrets.toml` file is excluded using `.gitignore`.

---

## 📁 Project Structure

```text
Movie-Recommendation-System/
│
├── app.py
├── main.py
├── movie_list.pkl
├── similarity.pkl
├── tmdb_5000_movies.csv
├── tmdb_5000_credits.csv
├── requirements.txt
├── README.md
│
├── home.png
├── recommend.png
├── dashboard.png
├── watchlist.png
│
└── .streamlit/
    └── secrets.toml
```

---

## ⚙️ How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/Putta-Jyothi/movie-recommendation-system.git
```

### 2. Open the Project Folder

```bash
cd movie-recommendation-system
```

### 3. Install Required Libraries

```bash
pip install -r requirements.txt
```

### 4. Configure TMDB API Key

Create the following file:

```text
.streamlit/secrets.toml
```

Add your TMDB API key:

```toml
TMDB_API_KEY = "your_api_key_here"
```

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your web browser.

---

## 🔗 Repository

[View Source Code on GitHub](https://github.com/Putta-Jyothi/movie-recommendation-system)

---

## 🎯 Project Objective

The objective of this project is to develop an interactive movie recommendation system that helps users discover movies based on their interests using Machine Learning techniques.

The project demonstrates the practical use of:

- Machine Learning
- Content-Based Filtering
- Cosine Similarity
- Data Processing
- Data Visualization
- API Integration
- Web Application Development

---

## 🔮 Future Enhancements

- 👤 User accounts and personalized profiles
- 🎯 Personalized recommendations
- 🎞️ Movie trailers
- 🔍 Advanced movie filtering
- 📚 Improved recommendation algorithms
- ❤️ Persistent user watchlists
- ⭐ User ratings and reviews
- 🤖 Hybrid recommendation system

---

## 👩‍💻 Developer

**Putta Jyothi**

B.Tech — CAI

---

## 📜 License

This project is developed for educational and portfolio purposes.
