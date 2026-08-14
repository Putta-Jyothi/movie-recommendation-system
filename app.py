import pickle
import requests
import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)


# Load recommendation data
with open("movie_list.pkl", "rb") as file:
    movies = pickle.load(file)

with open("similarity.pkl", "rb") as file:
    similarity = pickle.load(file)

# Load original movie data for dashboard
dashboard_data = pd.read_csv("tmdb_5000_movies.csv")

API_KEY = st.secrets["TMDB_API_KEY"]


def fetch_movie_details(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?append_to_response=credits"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "accept": "application/json"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )
    except requests.RequestException:
        return (
            None,
            "N/A",
            "N/A",
            "N/A",
            "N/A",
            "N/A",
            "No overview available."
        )

    if response.status_code != 200:
        st.error(f"TMDB API Error: {response.status_code}")
        return (
            None,
            "N/A",
            "N/A",
            "N/A",
            "N/A",
            "N/A",
            "No overview available."
        )

    data = response.json()

    # Poster
    poster = None

    if data.get("poster_path"):
        poster = (
            "https://image.tmdb.org/t/p/w500"
            + data["poster_path"]
        )

    # Rating
    rating = data.get("vote_average", "N/A")

    if rating != "N/A":
        rating = round(float(rating), 1)

    # Release year
    release_date = data.get("release_date", "")
    year = release_date[:4] if release_date else "N/A"

    # Genres
    genre_list = data.get("genres", [])

    genres = ", ".join(
        genre["name"]
        for genre in genre_list
        if genre.get("name")
    )

    if not genres:
        genres = "N/A"

    # Director
    director = "N/A"

    crew = data.get("credits", {}).get("crew", [])

    for person in crew:
        if person.get("job") == "Director":
            director = person.get("name", "N/A")
            break

    # Cast - Top 5
    cast_list = data.get("credits", {}).get("cast", [])

    cast_names = []

    for person in cast_list[:5]:
        if person.get("name"):
            cast_names.append(person["name"])

    cast = ", ".join(cast_names)

    if not cast:
        cast = "N/A"

    # Overview
    overview = data.get(
        "overview",
        "No overview available."
    )

    if not overview:
        overview = "No overview available."

    return (
        poster,
        rating,
        year,
        genres,
        director,
        cast,
        overview
    )


def recommend(movie):
    movie_rows = movies[movies["title"] == movie]

    if movie_rows.empty:
        return [], [], [], [], [], [], [], []

    movie_index = movie_rows.index[0]

    distances = similarity[movie_index]

    similar_movies = sorted(
        enumerate(distances),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    recommended_movies = []
    posters = []
    ratings = []
    years = []
    genres = []
    directors = []
    cast_list = []
    overviews = []

    for index, score in similar_movies:
        movie_id = movies.iloc[index]["movie_id"]
        movie_title = movies.iloc[index]["title"]

        details = fetch_movie_details(movie_id)

        poster, rating, year, genre, director, cast, overview = details

        recommended_movies.append(movie_title)
        posters.append(poster)
        ratings.append(rating)
        years.append(year)
        genres.append(genre)
        directors.append(director)
        cast_list.append(cast)
        overviews.append(overview)

    return (
        recommended_movies,
        posters,
        ratings,
        years,
        genres,
        directors,
        cast_list,
        overviews
    )


# Sidebar
st.sidebar.title("About")

st.sidebar.info(
    """
🎬 Movie Recommendation System

Features:
• Content-Based Filtering
• Machine Learning
• TMDB Posters
• Movie Ratings
• Release Year
• Top 5 Recommendations
• Watchlist
• Dashboard

Technologies:
• Python
• Streamlit
• Scikit-learn
• Plotly
• TMDB API
"""
)

st.sidebar.markdown("---")
st.sidebar.write("👨‍💻 Developed by Putta Jyothi")


st.title("🎬 Movie Recommendation System")
st.markdown("### Discover movies similar to your favorite ones! 🍿")


# Dashboard
st.markdown("---")
st.markdown("## 📊 Movie Dashboard")

dashboard_movies = dashboard_data.copy()

dashboard_movies["vote_average"] = pd.to_numeric(
    dashboard_movies["vote_average"],
    errors="coerce"
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🎬 Total Movies",
        len(dashboard_movies)
    )

with col2:
    average_rating = dashboard_movies["vote_average"].mean()

    st.metric(
        "⭐ Average Rating",
        f"{average_rating:.1f}"
    )

with col3:
    highest_rating = dashboard_movies["vote_average"].max()

    st.metric(
        "🏆 Highest Rating",
        f"{highest_rating:.1f}"
    )

with col4:
    st.metric(
        "🎯 Recommendation Type",
        "Top 5"
    )


st.markdown("### ⭐ Rating Distribution")

rating_data = dashboard_movies.dropna(
    subset=["vote_average"]
)

fig_rating = px.histogram(
    rating_data,
    x="vote_average",
    nbins=20,
    title="Movie Rating Distribution"
)

fig_rating.update_layout(
    xaxis_title="Rating",
    yaxis_title="Number of Movies"
)

st.plotly_chart(
    fig_rating,
    width="stretch"
)


st.markdown("### 📅 Movies by Release Year")

dashboard_movies["release_date"] = pd.to_datetime(
    dashboard_movies["release_date"],
    errors="coerce"
)

dashboard_movies["release_year"] = (
    dashboard_movies["release_date"].dt.year
)

year_data = (
    dashboard_movies["release_year"]
    .dropna()
    .value_counts()
    .sort_index()
    .reset_index()
)

year_data.columns = ["Year", "Movies"]

fig_year = px.line(
    year_data,
    x="Year",
    y="Movies",
    markers=True,
    title="Movies Released by Year"
)

st.plotly_chart(
    fig_year,
    width="stretch"
)


st.markdown("### 🎭 Movies by Genre")

genre_names = []

for genre_string in dashboard_movies["genres"].dropna():

    try:
        genre_list = eval(genre_string)

        for genre in genre_list:
            if isinstance(genre, dict):
                name = genre.get("name")

                if name:
                    genre_names.append(name)

    except (ValueError, SyntaxError, TypeError):
        continue


if genre_names:
    genre_data = (
        pd.Series(genre_names)
        .value_counts()
        .reset_index()
    )

    genre_data.columns = ["Genre", "Movies"]

    fig_genre = px.bar(
        genre_data.head(10),
        x="Genre",
        y="Movies",
        title="Top 10 Movie Genres"
    )

    st.plotly_chart(
        fig_genre,
        width="stretch"
    )


st.markdown("### 🏆 Top Rated Movies")

top_movies = (
    dashboard_movies[
        ["title", "vote_average"]
    ]
    .dropna()
    .sort_values(
        "vote_average",
        ascending=False
    )
    .head(10)
)

top_movies = top_movies.rename(
    columns={
        "title": "Movie",
        "vote_average": "Rating"
    }
)

st.dataframe(
    top_movies,
    width="stretch",
    hide_index=True
)


# Movie search
st.markdown("---")
st.markdown("### 🔎 Search for a Movie")

search_text = st.text_input(
    "Enter movie name",
    placeholder="Example: Spider-Man"
)

if search_text:
    filtered_movies = movies[
        movies["title"].str.contains(
            search_text,
            case=False,
            na=False
        )
    ]["title"].values

    if len(filtered_movies) == 0:
        st.warning("No movies found. Try another name.")
        filtered_movies = movies["title"].values
else:
    filtered_movies = movies["title"].values


selected_movie = st.selectbox(
    "🎬 Select a Movie",
    filtered_movies
)


if st.button(
    "🎯 Recommend Movies",
    width="stretch"
):

    with st.spinner("Finding similar movies..."):

        (
            recommended_movies,
            posters,
            ratings,
            years,
            genres,
            directors,
            cast_list,
            overviews
        ) = recommend(selected_movie)

    if recommended_movies:

        st.success("🎉 Recommendations Generated!")

        st.markdown("## 🎬 Recommended Movies")

        cols = st.columns(5)

        for i, movie_title in enumerate(recommended_movies):

            with cols[i]:

                if posters[i]:
                    st.image(
                        posters[i],
                        width="stretch"
                    )
                else:
                    st.write("🚫 Poster unavailable")

                st.markdown(
                    f"### {movie_title}"
                )

                st.write(
                    f"⭐ **Rating:** {ratings[i]}"
                )

                st.write(
                    f"📅 **Year:** {years[i]}"
                )

                with st.expander("🎬 Movie Details"):

                    st.write(
                        f"🎭 **Genre:** {genres[i]}"
                    )

                    st.write(
                        f"🎬 **Director:** {directors[i]}"
                    )

                    st.write("👥 **Cast:**")
                    st.write(cast_list[i])

                    st.write("📝 **Overview:**")
                    st.write(overviews[i])

    else:
        st.warning("Could not generate recommendations.")


# Watchlist
st.markdown("---")
st.markdown("## ❤️ My Watchlist")

if "watchlist" not in st.session_state:
    st.session_state.watchlist = []


if st.button(
    "❤️ Add Selected Movie to Watchlist",
    key="add_watchlist"
):

    if selected_movie not in st.session_state.watchlist:

        st.session_state.watchlist.append(
            selected_movie
        )

        st.success(
            f"✅ {selected_movie} added to your watchlist!"
        )

    else:

        st.info(
            "ℹ️ This movie is already in your watchlist."
        )


if st.session_state.watchlist:

    st.markdown("### 🎬 Saved Movies")

    for watch_movie in st.session_state.watchlist:

        movie_row = movies[
            movies["title"] == watch_movie
        ]

        if not movie_row.empty:

            movie_id = movie_row.iloc[0]["movie_id"]

            (
                poster,
                rating,
                year,
                genres,
                director,
                cast,
                overview
            ) = fetch_movie_details(movie_id)

            col1, col2 = st.columns([1, 3])

            with col1:

                if poster:
                    st.image(
                        poster,
                        width="stretch"
                    )

            with col2:

                st.markdown(
                    f"### ❤️ {watch_movie}"
                )

                st.write(
                    f"⭐ Rating: {rating}"
                )

                st.write(
                    f"📅 Year: {year}"
                )

                st.write(
                    f"🎭 Genre: {genres}"
                )

                st.write(
                    f"🎬 Director: {director}"
                )

                st.write(
                    f"👥 Cast: {cast}"
                )

                with st.expander("📝 Overview"):
                    st.write(overview)

else:

    st.info(
        "Your watchlist is empty. Select a movie and add it!"
    )



