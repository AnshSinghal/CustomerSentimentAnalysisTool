import nltk
from nltk.corpus import movie_reviews
import pandas as pd

# Download the dataset
nltk.download('movie_reviews')

# Load the reviews and their sentiment labels
reviews = []
for fileid in movie_reviews.fileids():
    category = movie_reviews.categories(fileid)[0]  # 'pos' or 'neg'
    text = movie_reviews.raw(fileid)
    reviews.append((text, category))

# Convert to a DataFrame
imdb_df = pd.DataFrame(reviews, columns=["review", "sentiment"])
print(imdb_df.head())
