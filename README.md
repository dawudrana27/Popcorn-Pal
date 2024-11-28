HOW TO USE:
Use Scraper.py to collect the user reviews for users inside of UserReviews.csv:
1. Change the username in the inputted link to the desired user on line 17.
2. Run Scraper.py to collect that user's reviews.
3. Repeat until you have compiled a satisfactory dataset. (A small sample dataset has been included)
   
Then use Recommender.py to get recommendations:
1. Enter the username of the user you are seeking recommendations for on line 43.

The program will then print the top 5 recommendations for the user along with their expected ratings from the user.


Developed a movie recommendation program for movie nights with friends using Python and Surprise library to analyze a user’s ratings, compare them to other users’ ratings, and provide personalized suggestions.
Trained a collaborative filtering model using SVD algorithm to recommend top N movies for a user based on their rating history, ensuring an engaging user experience.
Designed a web scraping module using BeautifulSoup and Selenium to extract a dataset of over 100,000 user ratings from Letterboxd to create an original dataset.
Utilized pandas for data manipulation, CSV handling, and integrating user reviews into a structured format for further analysis.
