import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy

# Step 1: Load the CSV data into a pandas DataFrame
data_path = 'UserReviews.csv'  # Update with your CSV file path
df = pd.read_csv(data_path)

# Convert DataFrame into a format that Surprise can use
# Surprise expects user_id, item_id (movie), and rating columns.
reader = Reader(rating_scale=(0.5, 5))

# Load the data into Surprise's Dataset object
data = Dataset.load_from_df(df[['User', 'Title', 'User-Rating']], reader)

# Train-test split
trainset, testset = train_test_split(data, test_size=0.25)

# Use the SVD algorithm to train the model
algo = SVD()
algo.fit(trainset)

# Make predictions for the testset and evaluate the model
predictions = algo.test(testset)
accuracy.rmse(predictions)

# Recommend top N movies for a specific user
def recommend_movies(algo, user, df, n=5):
    # Get all unique movies from the dataset
    all_movies = df['Title'].unique()

    # Get the list of all unique movies that the user has NOT rated
    rated_movies = df[df['User'] == user]['Title'].unique()
    unrated_movies = [movie for movie in all_movies if movie not in rated_movies]
    movie_predictions = [(movie, algo.predict(user, movie).est) for movie in unrated_movies]

    # Sort predictions by estimated rating in descending order and return the top N (Currently 5)
    movie_predictions.sort(key=lambda x: x[1], reverse=True)
    return movie_predictions[:n]

# Use the function to recommend movies to a specific user
user = 'Aazam21'  # Enter any username from the dataset
recommended_movies = recommend_movies(algo, user, df, n=5)

# Print recommendations
print(f"\nTop 5 movie recommendations for {user}:")
count = 1
for movie, predicted_rating in recommended_movies:
    print(str(count)+":")
    print(f"{movie}:  predicted rating {predicted_rating:.2f}")
    count = count+1