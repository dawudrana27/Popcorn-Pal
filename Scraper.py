import requests
import csv, os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class Scrapper():
    
    def __init__(self):
        # Set up Selenium WebDriver (assuming you're using Chrome)
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)

        # Open the Letterboxd films page
        self.driver.get("https://letterboxd.com/hyperhaseeb/films/by/entry-rating/")
        time.sleep(5)

        # Get the page source after JavaScript has executed
        page_source = self.driver.page_source

        # Pass the page source to BeautifulSoup for parsing
        soup = BeautifulSoup(page_source, "html.parser")

        # Extract the number of pages
        self.page_links = soup.find_all('li', class_='paginate-page')
        if self.page_links:
            last_page_number = self.page_links[-1].a.text  # Access the last <li> and then the <a> tag

            self.page_count = list(range(2, (int(last_page_number)+1)))

        profile_section = soup.find("section", class_="profile-header")
        self.userid = profile_section.get("data-person")
        self.objects = soup.findAll("li", class_="poster-container")

        # Initialize empty lists for titles and ratings
        self.movies = []

        # Loop through each movie and extract the title and rating
        for movie in self.objects:
            # Extract the title
            title = movie.find("span", class_="frame-title")
            
            # Extract the rating from the 'data-average-rating' attribute
            stars = movie.find("span", class_=["rating -micro -darker rated-10", "rating -micro -darker rated-9", "rating -micro -darker rated-8", "rating -micro -darker rated-7", "rating -micro -darker rated-6", "rating -micro -darker rated-5",
            "rating -micro -darker rated-4", "rating -micro -darker rated-3", "rating -micro -darker rated-2", "rating -micro -darker rated-1", "rating -micro -darker rated-0"])
            if stars:
                user_rating = len(stars.text)
                if '½' in stars.text:
                    user_rating = user_rating - 0.5

            if title and stars:
                title = title.text
                self.movies.append({'User': self.userid, 'Title': title, 'User-Rating': user_rating})

        # Repeat for all pages if there are multiple
        if self.page_links:
            for page in self.page_count:
                self.driver.get("https://letterboxd.com/"+self.userid+"/films/by/entry-rating/page/"+str(page)+"/")
                time.sleep(5)

                page_source = self.driver.page_source
                soup = BeautifulSoup(page_source, "html.parser")

                # Find all <li> elements that contain the movie data
                self.new_objects = soup.findAll("li", class_="poster-container")

                # Loop through each movie and extract the title and rating
                for movie in self.new_objects:
                    # Extract the title
                    title = movie.find("span", class_="frame-title")
                    
                    # Extract the rating from the 'data-average-rating' attribute
                    stars = movie.find("span", class_=["rating -micro -darker rated-10", "rating -micro -darker rated-9", "rating -micro -darker rated-8", "rating -micro -darker rated-7", "rating -micro -darker rated-6", "rating -micro -darker rated-5",
                    "rating -micro -darker rated-4", "rating -micro -darker rated-3", "rating -micro -darker rated-2", "rating -micro -darker rated-1", "rating -micro -darker rated-0"])
                    if stars: 
                        user_rating = len(stars.text)
                        if '½' in stars.text:
                            user_rating = user_rating - 0.5
                            
                    if title and stars:
                        title = title.text
                        self.movies.append({'User': self.userid, 'Title': title, 'User-Rating': user_rating})

        print("Movie count:", len(self.movies))
        # Close the browser
        self.driver.quit()

    def save_to_csv(self, filename='UserReviews.csv'):

        file_exists = os.path.isfile(filename)
        with open(filename, 'a+', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['User', 'Title', 'User-Rating'])

            if not file_exists:
                writer.writeheader()
            for movie in self.movies:
                writer.writerow(movie)

    # Now titles_list and ratings_list contain all titles and ratings as lists

if __name__ == "__main__":
    scrapper = Scrapper()
    scrapper.save_to_csv()

