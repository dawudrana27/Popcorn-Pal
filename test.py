import requests
import csv, os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class Scrapper():
    
    # Set up Selenium WebDriver (assuming you're using Chrome)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Open the Letterboxd films page
    driver.get("https://letterboxd.com/jaragon23/films/by/entry-rating/page/13/")
    time.sleep(3)


     # Get the page source after JavaScript has executed
    page_source = driver.page_source

    # Pass the page source to BeautifulSoup for parsing
    soup = BeautifulSoup(page_source, "html.parser")

    page_links = soup.find_all('li', class_='paginate-page')

        # Extract the number from the last link (4)
    if page_links:
        last_page_number = page_links[-1].a.text  # Access the last <li> and then the <a> tag

        page_count = list(range(2, (int(last_page_number)+1)))
    else:
        print(' cooked ')

    profile_section = soup.find("section", class_="profile-header")
    userid = profile_section.get("data-person")
    objects = soup.findAll("li", class_="poster-container")

    # Initialize empty lists for titles and ratings
    movies = []

    # Loop through each movie and extract the title and rating
    for movie in objects:
        # Extract the title
        title = movie.find("span", class_="frame-title")
        
        # Extract the rating from the 'data-average-rating' attribute
        stars = movie.find("span", class_=["rating -micro -darker rated-10", "rating -micro -darker rated-9", "rating -micro -darker rated-8", "rating -micro -darker rated-7", "rating -micro -darker rated-6", "rating -micro -darker rated-5",
        "rating -micro -darker rated-4", "rating -micro -darker rated-3", "rating -micro -darker rated-2", "rating -micro -darker rated-1", "rating -micro -darker rated-0"])
        user_rating = len(stars.text)
        if '½' in stars.text:
            user_rating = user_rating - 0.5

        if title and stars:
            title = title.text
            movies.append({'User': userid, 'Title': title, 'User-Rating': user_rating})

# Sample data to append (replace this with your actual extracted movies list)

    filename = 'UserReviews.csv'
    file_exists = os.path.isfile(filename)

    print(f"File exists: {file_exists}")  # Debugging line

    file_exists = os.path.isfile(filename)
    with open(filename, 'a+', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['User', 'Title', 'User-Rating'])

        if not file_exists:
            writer.writeheader()
        for movie in movies:
            writer.writerow(movie)
