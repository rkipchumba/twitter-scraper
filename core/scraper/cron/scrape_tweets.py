from django_cron import CronJobBase, Schedule
from scraper.scraper import scrape_tweets

class ScrapeTweetsCronJob(CronJobBase):
    RUN_EVERY_MINS = 60  # Run every hour

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'scraper.scrape_tweets_cron_job'    # a unique code

    def do(self):
        scrape_tweets()
