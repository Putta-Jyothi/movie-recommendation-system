import pandas as pd
import ast
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

# -------------------- Load Dataset --------------------
movies = pd.read_csv(r"C:\Users\Putta Jyothi\OneDrive\Desktop\Movie\archive\tmdb_5000_movies.csv")
credits = pd.read_csv(r"C:\Users\Putta Jyothi\OneDrive\Desktop\Movie\archive\tmdb_5000_credits.csv")

# -------------------- Merge --------------------
movies = movies.merge(credits, on='title')

# -------------------- Select Columns --------------------
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

# -------------------- Remove Missing Values --------------------
movies.dropna(inplace=True)

# -------------------- Functions --------------------

def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name'])
    return L

def convert3(text):
    L = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter < 3:
            L.append(i['name'])
            counter += 1
        else:
            break
    return L

def fetch_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L

# -------------------- Data Cleaning --------------------

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert3)
movies['crew'] = movies['crew'].apply(fetch_director)

movies['overview'] = movies['overview'].apply(lambda x: x.split())

movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])

# -------------------- Create Tags --------------------

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

new_df = movies[['movie_id','title','tags']]

new_df['tags'] = new_df['tags'].apply(lambda x:" ".join(x))
new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())

# -------------------- Stemming --------------------

def stem(text):
    y = []

    for i in text.split():
        y.append(ps.stem(i))

    return " ".join(y)

new_df['tags'] = new_df['tags'].apply(stem)

# -------------------- Vectorization --------------------

cv = CountVectorizer(max_features=5000, stop_words='english')

vectors = cv.fit_transform(new_df['tags']).toarray()

# -------------------- Similarity --------------------

similarity = cosine_similarity(vectors)

# -------------------- Recommendation Function --------------------

def recommend(movie):
    movie = movie.lower()

    found = False

    for i in range(len(new_df)):
        if new_df.iloc[i].title.lower() == movie:
            movie_index = i
            found = True
            break

    if not found:
        print("Movie not found!")
        return

    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)),
                         reverse=True,
                         key=lambda x:x[1])[1:6]

    print("\nTop 5 Recommended Movies:\n")

    for i in movies_list:
        print(new_df.iloc[i[0]].title)

# -------------------- Test --------------------

recommend("Avatar")

pickle.dump(new_df, open('movie_list.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

print("Files saved successfully!")