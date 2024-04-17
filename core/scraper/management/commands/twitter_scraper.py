import os
import smtplib
import requests
from email.mime.text import MIMEText
from django.core.management.base import BaseCommand
from django.conf import settings
from scraper.models import Tweet
from ntscraper import Nitter
from datetime import datetime
from django.utils import timezone
import random
import time  

class Command(BaseCommand):
    help = 'Scrapes tweets from the Coindesk Twitter channel using Nitter and saves them to the database'

    def handle(self, *args, **kwargs):
        # List of Nitter instances
        nitter_instances = [
            'https://nitter.net',
            'https://nitter.pussthecat.org',
            'https://nitter.snopyta.org',
        ]

        # Initialize Nitter scraper
        scraper = Nitter()

        # Fetch tweets from the Coindesk Twitter channel using a random Nitter instance
        random.shuffle(nitter_instances)
        for instance in nitter_instances:
            try:
                tweets = scraper.get_tweets('coindesk', mode='user', number=5, instance=instance)
                break  # Break the loop if tweets are successfully fetched from an instance
            except Exception as e:
                print(f"Fetching tweets from {instance} failed: {e}")
                time.sleep(5)  # Introduce a delay before retrying with another instance

        for tweet in tweets['tweets']:
            text = tweet['text']
            link = tweet['link']
            date_str = tweet['date']
            date = datetime.strptime(date_str, '%b %d, %Y · %I:%M %p %Z')
            date_aware = timezone.make_aware(date, timezone.get_current_timezone())
            date_formatted = date_aware.strftime('%Y-%m-%d %H:%M:%S')
            likes = tweet['stats']['likes']
            comments = tweet['stats']['comments']

            # Save the tweet to the database
            saved_tweet = Tweet.objects.create(text=text, link=link, date=date_formatted, likes=likes, comments=comments)
        
            # Save images to local storage
            self.save_images(tweet, saved_tweet.id)

        self.stdout.write(self.style.SUCCESS('Tweets scraped successfully and saved to the database.'))

        # Send email notification if desired
        self.send_email_notification()

    def save_images(self, tweet_data, tweet_id):
        if 'media' in tweet_data:
            # Define the folder to save images
            image_folder = os.path.join(settings.BASE_DIR, 'media', 'tweet_images')
            os.makedirs(image_folder, exist_ok=True)
            
            for idx, media in enumerate(tweet_data['media']):
                if media['type'] == 'photo':
                    image_url = media['url']
                    # Generate a unique filename for the image
                    image_filename = f"tweet_{tweet_id}_image_{idx+1}.jpg"
                    image_path = os.path.join(image_folder, image_filename)
                    
                    # Download the image
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        # Save the image to the designated folder
                        with open(image_path, 'wb') as f:
                            f.write(response.content)
                    else:
                        print(f"Failed to download image: {image_url}")

    def send_email_notification(self):
        subject = 'Tweets Scraped Successfully'
        body = 'Tweets from the Coindesk Twitter channel have been scraped and saved to the database.\n\n'
        
        # Retrieve tweets with videos
        tweets_with_videos = Tweet.objects.filter(link__contains='video')
        if tweets_with_videos.exists():
            body += 'Tweets with videos:\n\n'
            for tweet in tweets_with_videos:
                body += f"- {tweet.text}: {tweet.link}\n"
        else:
            body += 'No tweets with videos found.'

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = 'kipchumbarodgers151@gmail.com'  # Replace with the recipient's email address

        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.EMAIL_HOST_USER, msg['To'], msg.as_string())
        server.quit()
