# Twitter Scraper App

This  app periodically fetches tweets from the Twitter user 'coindesk' using the Nitter API and saves them to a PostgreSQL database. It automatically saves images associated with the tweets to local storage. Additionally, it sends email notifications when a tweet contains a video. The app provides a GET API endpoint for accessing saved tweets with pagination support. Swagger documentation is also included, allowing users to test the GET API endpoints conveniently.

## Prerequisites

Before running the app, make sure you have the following installed:

- Python (version 3.x)
- Django
- PostgreSQL
- Nitter API wrapper (ntscraper)

## Setup

1. Clone the repository:

```bash
git clone https://github.com/rkipchumba/twitter-scraper.git
```

## Install dependencies
```bash
cd core
pip install -r requirements.txt
```

 Copy the .env.example file to .env and update the environment variables as needed, including database credentials and email settings.

 ## Migrate the database
 ```bash
 python manage.py migrate
 ```

 ## Running the App
 To scrape tweets from the "coindesk" Twitter user and save them to the database, run the following Django management command. This command will fetch tweets, save them to the database, save images to local storage, and send an email notification if there are tweets with videos.

 ```bash
 Replace the recipient email address in twitter_scraper.py

 python manage.py twitter_scraper 
 ```

### After scraping the tweets, you can start the Django app by running
```bash
python manage.py runserver
```

After scraping the tweets, you can access the Swagger documentation by default at http://localhost:8000/swagger/. This provides an interactive API documentation where you can explore and test the endpoints of the Django app





