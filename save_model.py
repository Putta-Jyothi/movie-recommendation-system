import pickle

# Save the movie data
pickle.dump(new_df, open('movie_list.pkl', 'wb'))

# Save the similarity matrix
pickle.dump(similarity, open('similarity.pkl', 'wb'))

print("Files saved successfully!")